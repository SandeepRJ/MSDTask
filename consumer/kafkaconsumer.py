#!/usr/bin/python
"""This class consumes data from mentioned Kafka Topic(s)"""

from kafka import KafkaConsumer
from kafka import TopicPartition
import log
import json

class MyKafkaConsumer(object):

    logger = log.getLogger('kafkaconsumer')

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
    Consuming the input message from the Kafka topic through kafka consumer. Kafka is configured to retain the logs for only 3hours. Consumption from start till end will lead to consumption of transactions in the last 3 hours
    message value and key are raw bytes -- decode if necessary!
    e.g., for unicode: `message.value.decode('utf-8')`
    """
    def consume_messages(self):
        self.consumer.seek_to_end()
        end = self.consumer.position(self.partition) - 1
        self.consumer.seek_to_beginning()
        start = self.consumer.position(self.partition) - 1
        list = []
        if start == end:
            self.logger.info("No message in topic")
            self.consumer.close()
        
        else:
            for message in self.consumer:
                if message.offset >= end:
                    break
                list.append(json.loads(message.value))
        #print (message.offset, message.topic, message.key.decode('utf-8'))
	return list

