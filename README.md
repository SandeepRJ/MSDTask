# MSDTask

A task involving kafka, redis, python, flask and websockets where a python application is made to communicate with a websocket api to retrieve bitcoin transactions and is used to process and send data to a kafka topic and redis server frm where it is retrieved whenever needed using api calls

## Overview
![alt text](https://github.com/SandeepRJ/MSDTask/blob/master/MSDTaskOverview.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Prerequisites
Knowledge on Kafka, Redis, Websocket, Flask
Kafka Cluster Setup
Redis Server Setup
Code Flowchart
Code Setup

## Knowledge on Kafka, Redis, Websocket, Flask
#### Useful links
```
kafka 
https://kafka.apache.org/documentation/
https://pypi.org/project/kafka-python/

redis 
https://redis.io/documentation/
https://pypi.org/project/redis/

websocket-client
https://www.tutorialspoint.com/websockets/websockets_api.htm
https://pypi.org/project/websocket-client/

Flask
http://flask.pocoo.org/docs/1.0/

```
## Installation and Setup

#### Kafka Installation
```
cd ~
wget https://www-eu.apache.org/dist/kafka/2.1.0/kafka_2.11-2.1.0.tgz
tar -xzf kafka_2.11-2.1.0.tgz
rm kafka_2.11-2.1.0.tgz
echo "KAFKA_HOME='/home/ec2-user/kafka_2.11-2.1.0'" >> ~/.bashrc
echo "export PATH=$PATH:$KAFKA_HOME/bin" >> ~/.bashrc
```

#### Kafka Setup
You need to first start a ZooKeeper server as kafka needs zookeeper server to run. We have to change a few of the configurations of kafka and then you can start the kafka server
```
zookeeper-server-start.sh -daemon ~/kafka_2.11-2.1.0/config/zookeeper.properties [To run zookeper in background]
In the file ~/kafka_2.11-2.1.0/config/server.properties 
Change this property : log.retention.hours
For this task I have set it to 3
log.retention.hours=3
kafka-server-start.sh -daemon ~/kafka_2.11-2.1.0/config/server.properties [To run kafka in background]
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic bitcointopic
```

#### Redis Installation 
```
sudo yum -y update
sudo yum -y install gcc make
cd ~
wget http://download.redis.io/releases/redis-5.0.3.tar.gz
tar xzf redis-5.0.3.tar.gz
rm redis-5.0.3.tar.gz
cd redis-5.0.3
sudo make distclean
sudo make
echo "REDIS_HOME='/home/ec2-user/redis-5.0.3'" >> ~/.bashrc
echo "export PATH=$PATH:$REDIS_HOME/bin" >> ~/.bashrc
```

#### Redis Setup
```
redis-server --daemonize yes
```

#### Code Flowchart

#### Code Setup
```
Clone the repo
git clone https://github.com/SandeepRJ/MSDTask.git
cd MSDTask
pip install websocket-client
pip install kafka-python
sudo pip install redis
sudo pip install jsonify
sudo pip install flask_cors
sudo pip install flask
sudo pip install ConfigParser
sudo pip install logging
nohup python main.py & [To run in background]
```

## Running tests
Now to run tests for the apis without hosting them
```
Inside the servertest.py file uncomment the functions that you want to run test on and run the python script after that
python servertest.py
```

## Deployment
The server.py script has the code to host the required apis 
/show_transactions/
To display latest 100 transactions

/high_value_addr
Display the bitcoin addresses which has the most aggregate value in transactions in the last 3 hours.

/transactions_count_per_minute/{min_value}
To display number of transactions per minute for the last hour
The min_value should be between 0 and 60 where 0 indicates 60 mins from current time in GMT and 59 indicating 1 min from current time in GMT

```
Inside the servertest.py file uncomment the functions that you want to run test on and run the python script after that
nohup python server.py & [To run in background]
```
## Future Improvements 
#### Infrastructure Setup Improvements

The current setup has a single node kafka broker and redis running on the same instance. On making the setup into a multi node cluster  we can get high availabilty, integrity and fault tolerant application. We can further reduce the memory requirement of the current setup by having redis run separately on a different instance.

#### Code Improvements

The current code structure has two consumer classes which are called when the api is hit. This leads to the data to be fetched from the topic after the api is hit which leads to slower response time. Instead of this, consumer classes should be made to write data continously to files where data of the last 3 hours from the topic is only stored. Now making the api read the files will reduce the response time and will make it produce results instantly.


## Authors

* **Sandeep Rajan**

