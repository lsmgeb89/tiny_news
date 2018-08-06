"""Queue helper"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudamqp_client import CloudAMQPClient # pylint: disable=import-error, wrong-import-position

SCRAPE_NEWS_TASK_QUEUE_URL = \
"amqp://vvfthevj:RDHPMvJF2ddNCRFIhztFPnG1g2-8SmFM@wombat.rmq.cloudamqp.com/vvfthevj"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tiny-news-scrape-news-task-queue"

def clear_queue(queue_url, queue_name):
    """Clear a specific queue"""
    queue_client = CloudAMQPClient(queue_url, queue_name)

    num_of_messages = 0

    while True:
        if queue_client is not None:
            msg = queue_client.get_message()
            if msg is None:
                print("Cleared %d messages." % num_of_messages)
                return
            num_of_messages += 1

if __name__ == "__main__":
    clear_queue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
