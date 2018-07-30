"""Service operations"""

import json
import os
import sys

from bson.json_util import dumps

# import utils packages
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import mongodb_client # pylint: disable=import-error, wrong-import-position

NEWS_TABLE_NAME = "news"

def get_one_news():
    """Get one news"""
    news = mongodb_client.get_db()[NEWS_TABLE_NAME].find_one()
    # bson to string, string to json
    return json.loads(dumps(news))
