#!/usr/bin/python

import flask
import log
import ConfigParser
import json
from flask import Flask, render_template, flash, redirect, url_for, session, app, request, logging, Response , jsonify
from flask_cors import CORS, cross_origin
import sys
from consumer.kafkaconsumer import MyKafkaConsumer
from consumer.kafkaconsumer100 import MyKafkaConsumer100
import redis
import datetime
import jsonify

logger = log.getLogger('server')
r = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
config_parser = ConfigParser.RawConfigParser()

try:
    conf_file_path = 'config'
    config_parser.read(conf_file_path)
except IOError as e:
    logger.error("Specified configuration file is not found in the given path because: "+e.errno+":"+e.message)

kafka_brokers = config_parser.get('KafkaSection', 'kafka.broker0.address')
kafka_topic_name = config_parser.get('KafkaSection', 'kafka.topic.name')

def update_dict(temp_dict,key,value):
    if key in temp_dict:
        temp_dict[key] = temp_dict[key] + value
    else:
        temp_dict[key]=value

@app.route('/health', methods=['GET'])
def getHealth():
    return "I am Working"

@app.route('/show_transactions' , methods=['GET'])
def show_transactions():
    api_call_time = datetime.datetime.now()
    api_call_time = api_call_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("show_transactions API request made at " + api_call_time)
    mykafka100 = MyKafkaConsumer100(kafka_brokers, kafka_topic_name)
    transaction_list_100 = mykafka100.consume_100_messages()
    if len(transaction_list_100) == 0:
        return "Kafka Topic is empty"
    a = []
    for i in transaction_list_100:
        a.append(json.loads(i))
    logger.info("Number of transactions from the time of api call: "+str(len(transaction_list_100)))
    transaction_list_100 = a
    return flask.jsonify(transaction_list_100)

@app.route('/high_value_addr' , methods=['GET'])
def high_value_addr():
    api_call_time = datetime.datetime.now()
    api_call_time = api_call_time.strftime("%Y-%m-%d %H:%M:%S")
    tuplelist = []
    logger.info("high_value_addr API request made at " + api_call_time)
    mykafka = MyKafkaConsumer(kafka_brokers, kafka_topic_name)
    transaction_list = mykafka.consume_messages()
    if len(transaction_list) == 0:
        return "Kafka Topic is empty"
    my_dict = {}
    for i in transaction_list:
        i = json.loads(i)
        for j in i['x']['out']:
           key = j['addr']
           value = j['value']
           update_dict(my_dict, key, value)
    for key, value in sorted(my_dict.iteritems(), key=lambda (k,v): (v,k),reverse = True):
        a = (key,value)
        tuplelist.append(a)
    return flask.jsonify(tuplelist)

@app.route('/transactions_count_per_minute/<min_value>' , methods=['GET'])
def transactions_count_per_minute(min_value):
   api_call_time = datetime.datetime.now()
   api_call_time = api_call_time.strftime("%Y-%m-%d %H:%M:%S")
   logger.info("transactions_count_per_minute API request made at " + api_call_time)
   if int(min_value) < 0 and int(min_value) >= 60:
       logger.error("Error: min_value should be between 0 and 60")
       return "Error: min_value should be between 0 and 60"
   else:
       time = (60 - int(min_value))*60
       print time
       a = (datetime.datetime.now() - datetime.datetime.fromtimestamp(time)).total_seconds()
       b = datetime.datetime.fromtimestamp(a)
       c = b.strftime("%H:%M")
       r = redis.Redis(host='localhost', port=6379, db=0)
       d = r.get(c)
       print "%s: %s" % (c, d)
   tup = (c,d)
   return flask.jsonify(tup)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
