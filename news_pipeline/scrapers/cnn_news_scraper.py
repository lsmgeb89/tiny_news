"""CNN news scraper"""

import os
import random
import requests
from lxml import html

GET_CNN_NEWS_XPATH = \
"""//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"""

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []
with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1]) # get rid of double quote

random.shuffle(USER_AGENTS)

def get_headers():
    """Get headers"""
    headers = {
        "Connection": "close",
        "User-Agent": random.choice(USER_AGENTS)
    }
    return headers

def extract_news(news_url):
    """Extract news"""
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=get_headers())
    news = {}

    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        # list to string
        news = ''.join(news)
    except Exception:
        return {}

    return news
