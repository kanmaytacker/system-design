# Kafka
## Setup

Run the following command to start LocalStack with Kafka:

```bash
docker-compose up -d
```

Connect to the Kafka client container:
```bash
docker exec -it kafka_kafka-client_1 /bin/bash
```

## Kafka Operations

You can create a Kafka topic directly using the `kafka-topics.sh` command:

```bash
kafka-topics.sh --create --topic demo-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

#### 4.2. **List Kafka Topics**

To see the available topics:

```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

#### 4.3. **Produce Messages to Kafka Topic**

You can send messages to the Kafka topic using the `kafka-console-producer.sh` command:

```bash
kafka-console-producer.sh --topic demo-topic --bootstrap-server localhost:9092
```

Once this is running, you can type messages that will be sent to the `demo-topic`.

For example, type:

```bash
Message 1
Message 2
```

#### 4.4. **Consume Messages from Kafka Topic**

To consume the messages from the `demo-topic`, open another terminal session and run the following command:

```bash
kafka-console-consumer.sh --topic demo-topic --from-beginning --bootstrap-server localhost:9092
```

This will output:

```
Message 1
Message 2
```

#### 4.5. **Delete a Kafka Topic**

You can delete a Kafka topic using the following command:

```bash
kafka-topics.sh --delete --topic demo-topic --bootstrap-server localhost:9092
```

---

### 5. Summary of Kafka CLI Operations

1. **Create a Topic**:
   ```bash
   kafka-topics.sh --create --topic demo-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

2. **Produce Messages**:
   ```bash
   kafka-console-producer.sh --topic demo-topic --bootstrap-server localhost:9092
   ```

3. **Consume Messages**:
   ```bash
   kafka-console-consumer.sh --topic demo-topic --from-beginning --bootstrap-server localhost:9092
   ```

4. **Delete a Topic**:
   ```bash
   kafka-topics.sh --delete --topic demo-topic --bootstrap-server localhost:9092
   ```

### Conclusion

Using these **CLI commands** inside the LocalStack container allows you to easily create, produce, consume, and manage Kafka topics without needing to write any code. By utilizing the `kafka-topics.sh`, `kafka-console-producer.sh`, and `kafka-console-consumer.sh` tools, you can fully interact with Kafka via the command line. 

Let me know if you need further assistance!