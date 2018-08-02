"""Service operations"""

import json
import os
import pickle
import redis
import sys

from bson.json_util import dumps

NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 200
USER_NEWS_TIME_OUT_IN_SECONDS = 60

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

LOG_CLICKS_TASK_QUEUE_URL = "amqp://ajftnpdj:6y0g9zX3VFRwBE6_yUeCQ-y2Nx4-LGIk@wombat.rmq.cloudamqp.com/ajftnpdj"
LOG_CLICKS_TASK_QUEUE_NAME = "tiny-news-log-clicks-task-queue"

cloudamqp_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

# import utils packages
sys.path.append(os.path.join(os.path.dirname(__file__), '../common/'))

import mongodb_client # pylint: disable=import-error, wrong-import-position

NEWS_TABLE_NAME = "news"

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

def get_one_news():
    """Get one news"""
    news = mongodb_client.get_db()[NEWS_TABLE_NAME].find_one()
    # bson to string, string to json
    return json.loads(dumps(news))

def get_news_summaries_for_user(user_id, page_num):
    """Get news summaries"""
    page_num = int(page_num)
    # [begin_index, end_index)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    if redis_client.get(user_id) is not None:
        # use pickle to convert json to string
        total_news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = total_news_digests[begin_index:end_index]

        # get full article from digests
        database = mongodb_client.get_db()
        sliced_news = list(database[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        # first time to request, redis is empty
        database = mongodb_client.get_db()
        # get recent news sorted by data
        total_news = list(database[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        # extract digests
        total_news_digests = [x['digest'] for x in total_news]
        # use pickle convert string to json
        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        sliced_news = total_news[begin_index:end_index]

    return json.loads(dumps(sliced_news))

def log_news_click_for_user(user_id, news_id):
    # send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudamqp_client.sendmessage(message)
