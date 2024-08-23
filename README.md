# scraper-kafka-pipeline
The scraper is the producer and mongoDD and sqlite are consumers.

## kafka setup: 
- Start Zookeper Container and expose PORT 2181.
  ```docker run -p 2181:2181 zookeeper```
- Start Kafka Container, expose PORT 9092 and setup ENV variables.
```
docker run -p 9092:9092 \
-e KAFKA_ZOOKEEPER_CONNECT=<PRIVATE_IP>:2181 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://<PRIVATE_IP>:9092 \
-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
confluentinc/cp-kafka
```
##  Run:
- setup virtual env
- setup mongo uri in ```.env```
- Install requirements.txt
- open 3 terminals and run ```scraper.py```,```db-consumer.py``` and ```db2-consumer.py```

