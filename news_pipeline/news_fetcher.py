"""News fetcher"""

import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper # pylint: disable=import-error, wrong-import-position
from cloudamqp_client import CloudAMQPClient # pylint: disable=import-error, wrong-import-position

DEDUPE_NEWS_TASK_QUEUE_URL = \
"amqp://fhptegqw:WdCACLVa7HsRuR-i_lbUQNznHjz83uK9@wombat.rmq.cloudamqp.com/fhptegqw"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tiny-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = \
"amqp://vvfthevj:RDHPMvJF2ddNCRFIhztFPnG1g2-8SmFM@wombat.rmq.cloudamqp.com/vvfthevj"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tiny-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    """Extract and send news"""
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    task = msg
    text = None

    if task['source'] == 'cnn':
        print('scraping CNN news')
        text = cnn_news_scraper.extract_news(task['url'])
    else:
        print('News source [%s] is not supported.' % task['source'])

    task['text'] = text
    dedupe_news_queue_client.send_message(task)

while True:
    if scrape_news_queue_client is not None:
        message = scrape_news_queue_client.get_message()
        if message is not None:
            # Parse and process the task
            try:
                handle_message(message)
            except Exception as error:
                print(error)
                pass

        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
