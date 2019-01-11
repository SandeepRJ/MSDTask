#!/usr/bin/python
"""This class produces given input data into mentioned Kafka Topic(s)"""

from kafka import KafkaProducer
import websocket
import json
import log

class MyKafka(object):

    logger = log.getLogger('kafkaproducer')

    """Instantiating Kafka producer for given brokers."""
    def __init__(self, kafka_brokers):
        self.logger.info("Instantiating Kafka producer for given broker address:"+kafka_brokers)
        try:
            self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            bootstrap_servers=kafka_brokers
            )
        except Exception as e:
            self.logger.error("Error in Instantiating kafka producer")

    """Streaming the input message to the Kafka topic through kafka producer."""
    def send_transaction_data(self, json_data, kafka_topic_name):
        self.producer.send(kafka_topic_name, json_data)
        self.producer.flush()



