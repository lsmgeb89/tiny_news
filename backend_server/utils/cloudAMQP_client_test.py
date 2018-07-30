from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://hhmlgqql:0wJDR4KJY0Pafg2NkdGwEHLG63oJQxD5@wombat.rmq.cloudamqp.com/hhmlgqql"
TEST_QUEUE_NAME = "tiny-news-test"

def test_basic():
  client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

  sentMsg = {"tiny-news":"test"}
  client.sendMessage(sentMsg)
  receivedMsg = client.getMessage()

  assert sentMsg == receivedMsg
  print("test_basic passed!")

if __name__ == "__main__":
  test_basic()
