"""News monitor"""

import datetime
import hashlib
import logging
import os
import redis
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudamqp_client import CloudAMQPClient # pylint: disable=import-error, wrong-import-position
import news_api_client # pylint: disable=import-error, wrong-import-position

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3
SLEEP_TIME_IN_SECONDS = 10

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post',
    'ars-technica',
    'reuters'
]

SCRAPE_NEWS_TASK_QUEUE_URL = \
"amqp://vvfthevj:RDHPMvJF2ddNCRFIhztFPnG1g2-8SmFM@wombat.rmq.cloudamqp.com/vvfthevj"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tiny-news-scrape-news-task-queue"

def run():
    logging.info("[news_monitor] start running")
    redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
    cloudamqp_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

    while True:
        news_list = news_api_client.get_news_from_source(NEWS_SOURCES)
        logging.info("[news_monitor] get %d from news API", len(news_list))
        number_of_news = 0

        for news in news_list:
            news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

            if redis_client.get(news_digest) is None:
                number_of_news += 1
                news['digest'] = news_digest

                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

                redis_client.set(news_digest, "True")
                redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

                cloudamqp_client.send_message(news, "[news_monitor]")

        logging.info("[news_monitor] fetch %d news" % number_of_news)
        cloudamqp_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    logging.basicConfig(level=20)
    run()
