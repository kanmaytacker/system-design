from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import KafkaError, KafkaTimeoutError, TopicAlreadyExistsError
import json
import time
import logging

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'demo-topic'
NUM_PARTITIONS = 3
REPLICATION_FACTOR = 1

logging.basicConfig(level=logging.INFO)

# Custom serializer for JSON
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Custom deserializer for JSON
def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

# Create Kafka topics
def create_topic(topic_name, num_partitions, replication_factor):
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
    topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    try:
        admin_client.create_topics([topic])
        logging.info(f"Topic '{topic_name}' created successfully.")
    except TopicAlreadyExistsError:
        logging.info(f"Topic '{topic_name}' already exists.")
    except KafkaError as e:
        logging.error(f"Failed to create topic '{topic_name}': {e}")

# Create Kafka producer
def create_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=json_serializer,
        retries=5,  # Retry up to 5 times
        acks='all'
    )

# Create Kafka consumer
def create_consumer(group_id):
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=False,  # Manual commit
        group_id=group_id,
        value_deserializer=json_deserializer
    )

# Produce messages to Kafka
def produce_messages(producer, messages):
    try:
        for message in messages:
            future = producer.send(TOPIC_NAME, message)
            record_metadata = future.get(timeout=10)
            logging.info(f"Sent {message} to {record_metadata.topic} partition {record_metadata.partition}")
    except KafkaTimeoutError as e:
        logging.error(f"Timeout error: {e}")
    except KafkaError as e:
        logging.error(f"Failed to send messages: {e}")

# Consume messages from Kafka
def consume_messages(consumer, group_id):
    logging.info(f"Consuming messages from topic '{TOPIC_NAME}' with group_id '{group_id}'")
    for message in consumer:
        logging.info(f"Received message: {message.value}")
        # Manually commit the offset
        consumer.commit()

if __name__ == "__main__":
    # Create the Kafka topic
    create_topic(TOPIC_NAME, NUM_PARTITIONS, REPLICATION_FACTOR)
    
    # Create producer and consumer
    producer = create_producer()
    consumer1 = create_consumer(group_id='group1')
    consumer2 = create_consumer(group_id='group2')
    
    # Produce messages
    messages = [{"message_number": i, "content": f"Message {i}"} for i in range(10)]
    produce_messages(producer, messages)
    time.sleep(1)  # Give some time for messages to be fully produced

    # Consume messages with two different consumers
    consume_messages(consumer1, 'group1')
    consume_messages(consumer2, 'group2')
