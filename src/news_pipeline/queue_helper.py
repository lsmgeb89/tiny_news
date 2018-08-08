"""Queue helper"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudamqp_client import CloudAMQPClient # pylint: disable=import-error, wrong-import-position

SCRAPE_NEWS_TASK_QUEUE_URL = \
"amqp://vvfthevj:RDHPMvJF2ddNCRFIhztFPnG1g2-8SmFM@wombat.rmq.cloudamqp.com/vvfthevj"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tiny-news-scrape-news-task-queue"

DEDUPE_NEWS_TASK_QUEUE_URL = \
"amqp://fhptegqw:WdCACLVa7HsRuR-i_lbUQNznHjz83uK9@wombat.rmq.cloudamqp.com/fhptegqw"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tiny-news-dedupe-news-task-queue"

LOG_CLICKS_TASK_QUEUE_URL = \
"amqp://ajftnpdj:6y0g9zX3VFRwBE6_yUeCQ-y2Nx4-LGIk@wombat.rmq.cloudamqp.com/ajftnpdj"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-log-clicks-task-queue"

def clear_queue(queue_url, queue_name):
    """Clear a specific queue"""
    queue_client = CloudAMQPClient(queue_url, queue_name)
    print("[news_pipeline][queue_helper] cleaning %s" % queue_name)
    num_of_messages = 0

    while True:
        if queue_client is not None:
            msg = queue_client.get_message("[queue_helper]")
            if msg is None:
                print("Cleared %d messages." % num_of_messages)
                return
            num_of_messages += 1

if __name__ == "__main__":
    clear_queue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
    clear_queue(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
    clear_queue(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)
