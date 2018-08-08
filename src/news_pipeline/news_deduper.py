"""News deduper"""

import datetime
import logging
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client # pylint: disable=import-error, wrong-import-position
import news_topic_modeling_service_client # pylint: disable=import-error, wrong-import-position
from cloudamqp_client import CloudAMQPClient # pylint: disable=import-error, wrong-import-position

NEWS_TABLE_NAME = "news"
SLEEP_TIME_IN_SECONDS = 3
SAME_NEWS_SIMILARITY_THRESHOLD = 0.9
DEDUPE_NEWS_TASK_QUEUE_URL = \
"amqp://fhptegqw:WdCACLVa7HsRuR-i_lbUQNznHjz83uK9@wombat.rmq.cloudamqp.com/fhptegqw"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tiny-news-dedupe-news-task-queue"

def handle_message(msg):
    """Save deduplicated news into MongoDB"""
    if msg is not isinstance(msg, dict):
        logging.error("[news_deduper] news is not dict")
        return

    task = msg
    text = task['text']
    if text is None:
        logging.error("[news_deduper] text attribute is none")
        return

    # get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year,
                                               published_at.month,
                                               published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    database = mongodb_client.get_db()
    same_day_news_list = list(database[NEWS_TABLE_NAME].find({
        'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}
    }))

    # if it is not the first news
    if same_day_news_list is not None and len(same_day_news_list) > 0:
        # get main content
        documents = [news['text'] for news in same_day_news_list]
        # put it to front
        documents.insert(0, text)

        # calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        rows, _ = pairwise_sim.shape

        # scan first column except first element
        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                logging.info("[news_deduper] ignore deduplicated news")
                return

    # insert back to mongodb
    task['publishedAt'] = parser.parse(task['publishedAt'])

    # classify news
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic

    logging.info("[news_deduper] save news into MongoDB, title = %s", title)
    database[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

def run():
    cloudamqp_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

    while True:
        if cloudamqp_client is not None:
            message = cloudamqp_client.get_message()

            if message is not None:
                try:
                    handle_message(message)
                except Exception as error:
                    print(error)
                    pass

            cloudamqp_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    logging.basicConfig(level=20)
    run()
