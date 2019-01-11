#!/usr/bin/python
"""This class consumes data from mentioned Kafka Topic(s)"""

from kafka import KafkaConsumer
from kafka import TopicPartition
import log
import json

class MyKafkaConsumer100(object):

    logger = log.getLogger('kafkaconsumer100')

    """Instantiating Kafka consumer for given brokers."""
    def __init__(self, kafka_brokers, kafka_topic_name):
        self.logger.info("The kafka broker address:"+kafka_brokers)
        try:
            self.consumer = KafkaConsumer(bootstrap_servers=kafka_brokers)
        except:
            self.logger.error("Kafka server address is wrong or server is not running")
        try:
            self.partition = TopicPartition(kafka_topic_name, 0)
        except:
            self.logger.error("Check if the topic exists and the partition number is correct")
        self.consumer.assign([self.partition])
    """
    Consuming the last 100 input message from the Kafka topic through kafka consumer when called.
    message value and key are raw bytes -- decode if necessary!
    e.g., for unicode: `message.value.decode('utf-8')`
    """
    def consume_100_messages(self):
        self.consumer.seek_to_beginning()
        start = self.consumer.position(self.partition) - 1
        list = []
        self.consumer.seek_to_end()
        end = self.consumer.position(self.partition) - 1
        if start == end:
            self.logger.info("No message in topic")
            self.consumer.close()
        else:
            if end > 100:
                start = end - 100
            else:
                self.consumer.seek_to_beginning()
                start = self.consumer.position(self.partition) - 1
            self.consumer.seek(self.partition, start)
            for message in self.consumer:
                if message.offset >= end:
                    break
                list.append(json.loads(message.value))
            #print (message.offset, message.topic, message.key.decode('utf-8'))
        self.consumer.close()
        return list


