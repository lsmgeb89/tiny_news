import jsonrpclib

CLASSIFIER_SERVICE_HOST = 'localhost'
CLASSIFIER_SERVICE_PORT = '6060'
CLASSIFIER_SERVICE_URL = 'http://' + CLASSIFIER_SERVICE_HOST + ':' + CLASSIFIER_SERVICE_PORT

client = jsonrpclib.ServerProxy(CLASSIFIER_SERVICE_URL)

def classify(text):
    topic = client.classify(text)
    print("Topic: %s" % str(topic))
    return topic
