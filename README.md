# MSDTask

A task involving kafka, redis, python, flask and websockets where a python application is made to communicate with a websocket api to retrieve bitcoin transactions and is used to process and send data to a kafka topic and redis server frm where it is retrieved whenever needed using api calls

## Introduction

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Prerequisites

Kafka Cluster Setup
Redis Server Setup
Code Setup

```
Give examples
```

## Installing

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
git clone
```


## Running tests



## Deployment



## Authors

* **Sandeep Rajan**


## Acknowledgments

* 
* 
* 

