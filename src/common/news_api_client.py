"""News API client"""

from json import loads
import requests

NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = '22f3dd5c753a4d80a3902196b966efd2'

ARTICLES_API = 'articles'

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]
SORT_BY_TOP = 'top'

def _build_url(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
    return end_point + api_name

def get_news_from_source(sources=DEFAULT_SOURCES, sort_by=SORT_BY_TOP):
    """Gets news from source"""

    articles = []

    for source in sources:
        payload = {'apikey': NEWS_API_KEY,
                   'source': source,
                   'sortBy': sort_by}

        response = requests.get(_build_url(), params=payload)
        res_json = loads(response.content.decode('utf-8'))

        # extract news from response
        if (res_json is not None and
                res_json['status'] == 'ok' and
                res_json['source'] is not None):

            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = res_json['source']
            articles.extend(res_json['articles'])

    return articles
