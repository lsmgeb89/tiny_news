import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

NEWS_TABLE_NAME = "news"

if __name__ == '__main__':
    database = mongodb_client.get_db()
    cursor = database[NEWS_TABLE_NAME].find({})
    count = 0
    for news in cursor:
        count += 1
        print(count)
        if 'class' not in news:
            print('Populating classes...')
            title = news['title']
            topic = news_topic_modeling_service_client.classify(title)
            news['class'] = topic
            database[NEWS_TABLE_NAME].replace_one({'digest': news['digest']}, news, upsert=True)
