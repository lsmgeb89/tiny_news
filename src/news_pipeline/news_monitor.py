"""News monitor"""

import os
import sys
import datetime
import hashlib
import redis

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import news_api_client # pylint: disable=import-error, wrong-import-position
from cloudamqp_client import CloudAMQPClient # pylint: disable=import-error, wrong-import-position

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
    'the-washington-post'
]

SCRAPE_NEWS_TASK_QUEUE_URL = \
"amqp://vvfthevj:RDHPMvJF2ddNCRFIhztFPnG1g2-8SmFM@wombat.rmq.cloudamqp.com/vvfthevj"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tiny-news-scrape-news-task-queue"

REDIS_CLIENT = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
CLOUDAMQP_CLIENT = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    NEWS_LIST = news_api_client.get_news_from_source(NEWS_SOURCES)

    NUMBER_OF_NEWS = 0

    for news in NEWS_LIST:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

        if REDIS_CLIENT.get(news_digest) is None:
            NUMBER_OF_NEWS += 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            REDIS_CLIENT.set(news_digest, "True")
            REDIS_CLIENT.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            CLOUDAMQP_CLIENT.send_message(news)

    print("Fetched %d news." % NUMBER_OF_NEWS)
    CLOUDAMQP_CLIENT.sleep(SLEEP_TIME_IN_SECONDS)
