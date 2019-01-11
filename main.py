#!/usr/bin/python
"""The main class to orchestrate the functions for the kafka-redis-flask"""

import log
import ConfigParser
from producer.kafkaproducer import MyKafka
import datetime
import websocket
import redis

class Main(object):
    logger = log.getLogger('main')

    def __init__(self):
        config_parser = ConfigParser.RawConfigParser()
        try:
            conf_file_path = 'config'
            config_parser.read(conf_file_path)
        except IOError as e:
            self.logger.error("Specified configuration file is not found in the given path because: "+e.errno+":"+e.message)
        self.kafka_brokers = config_parser.get('KafkaSection', 'kafka.broker0.address')
        self.kafka_topic_name = config_parser.get('KafkaSection', 'kafka.topic.name')
        self.logger.info("Initializing Kafka Producer to the broker address: "+self.kafka_brokers)
        self.logger.info("Kafka topic name: " + self.kafka_topic_name)
        self.logger.info("Creating an object of websocket Class")
        self.websocketurl= config_parser.get('WebSocketSection','websocket.url')
        self.number_of_transactions = 0
        self.start_time = datetime.datetime.now()
        self.ws = websocket.WebSocketApp(self.websocketurl, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close, on_open = self.on_open)
        self.mykafka = MyKafka(self.kafka_brokers)
        self.r = redis.Redis(host='localhost', port=6379, db=0)
 
    def on_open(self):
        self.ws.send('{"op":"unconfirmed_sub"}')

    def on_message(self, message):
        self.number_of_transactions = self.number_of_transactions+1
        if ((datetime.datetime.now() - self.start_time).total_seconds())>60:
            start_time_string = self.start_time.strftime("%H:%M")
            if (self.r.set(start_time_string, self.number_of_transactions,ex=3660)):
                self.logger.info("The number of transactions per minute has been added to redis")
            else:
                self.logger.error("Error in adding to redis")
            self.number_of_transactions = 0
            self.start_time = datetime.datetime.now()
            self.logger.info("The total number of number of transactions is: "+str(number_of_transactions))

    def on_close(self):
        self.logger.info("Socket closed") 

    def on_error(self, error):
        self.logger.error("The connection to the websocket api has been disconnected due to following error " + str(error))
    
    def run(self):
        self.logger.info("Starting to run and connect to the websocket")
        self.ws.run_forever()

if __name__ == "__main__":
    main = Main()
    main.run()


