"""News fetcher"""

import logging
import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudamqp_client import CloudAMQPClient # pylint: disable=import-error, wrong-import-position

DEDUPE_NEWS_TASK_QUEUE_URL = \
"amqp://fhptegqw:WdCACLVa7HsRuR-i_lbUQNznHjz83uK9@wombat.rmq.cloudamqp.com/fhptegqw"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tiny-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = \
"amqp://vvfthevj:RDHPMvJF2ddNCRFIhztFPnG1g2-8SmFM@wombat.rmq.cloudamqp.com/vvfthevj"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tiny-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    """Extract and send news"""

    if msg is not isinstance(msg, dict):
        logging.error("[news_fetcher] news is not dict")
        return

    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    dedupe_queue_client.send_message(task, "[news_fetcher]")

def run():
    scrape_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

    while True:
        if scrape_queue_client is not None:
            message = scrape_queue_client.get_message("[news_fetcher]")
            if message is not None:
                try:
                    handle_message(message)
                except Exception as error:
                    print(error)
                    pass
            scrape_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    logging.basicConfig(level=20)
    run()
