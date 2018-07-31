"""Test news API client"""

import news_api_client as client

def test_basic():
    """Test news API client basically"""
    news = client.get_news_from_source()
    print(news)
    assert news

    news = client.get_news_from_source(sources=['the-new-york-times'], sort_by='top')
    print(news)
    assert news

    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
