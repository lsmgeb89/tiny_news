"""CloudAMQP client"""

import json
import logging
import pika

class CloudAMQPClient:
    """CloudAMQP client"""
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.parms = pika.URLParameters(cloud_amqp_url)
        self.parms.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.parms)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, message, sender=''):
        """Send a json message"""
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        logging.info("%s push news to %s, title = %s", sender, self.queue_name, message['title'])

    def get_message(self, receiver=''):
        """Get a message"""
        method_frame, _, body = self.channel.basic_get(self.queue_name)

        if method_frame:
            # send ack to queue
            self.channel.basic_ack(method_frame.delivery_tag)

            # convert bytes to string
            news = json.loads(body.decode('utf-8'))
            logging.info("%s pop news from %s, title = %s", receiver, self.queue_name, news['title'])
            return news
        else:
            logging.info("%s %s is empty", receiver, self.queue_name)

        return None

    # BlockingConnection.sleep is a safer way to sleep than calling time.sleep().
    # This will respond to server's heartbeat.
    def sleep(self, seconds):
        """Sleep with heartbeat"""
        self.connection.sleep(seconds)
