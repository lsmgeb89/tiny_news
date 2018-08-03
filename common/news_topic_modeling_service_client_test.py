import news_topic_modeling_service_client as client

def test_basic():
    news_title = "Pentagon might propose ground troops for Syria"
    topic = client.classify(news_title)
    assert topic == "U.S."
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
