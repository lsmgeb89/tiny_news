"""Test CloudAMQP client"""

from cloudamqp_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://hhmlgqql:0wJDR4KJY0Pafg2NkdGwEHLG63oJQxD5@wombat.rmq.cloudamqp.com/hhmlgqql"
TEST_QUEUE_NAME = "tiny-news-test"

def test_basic():
    """Test CloudAMQP client basically"""
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sent_msg = {"title": "test news"}
    client.send_message(sent_msg, "[cloudamqp tester]")
    received_msg = client.get_message("[cloudamqp tester]")

    assert sent_msg == received_msg
    print("test_basic passed!")

if __name__ == "__main__":
    test_basic()
