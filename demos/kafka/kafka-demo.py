import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

# LocalStack configurations
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'demo-topic'

def create_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        api_version=(2, 5, 0)  # Specify a compatible API version
    )

def create_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        api_version=(2, 5, 0)  # Specify a compatible API version
    )

def create_topic(producer, topic_name):
    # Kafka topics can be created by producing messages to them
    producer.send(topic_name, b'Initializing topic')
    producer.flush()
    print(f"Topic '{topic_name}' created")

def produce_messages(producer):
    for i in range(10):
        message = f"Message {i}"
        future = producer.send(TOPIC_NAME, message.encode('utf-8'))
        try:
            record_metadata = future.get(timeout=10)
            print(f"Sent {message} to {record_metadata.topic} partition {record_metadata.partition}")
        except KafkaError as e:
            print(f"Failed to send message: {e}")

def consume_messages(consumer):
    print(f"Consuming messages from topic '{TOPIC_NAME}'")
    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")

if __name__ == "__main__":
    producer = create_producer()
    consumer = create_consumer()
    
    create_topic(producer, TOPIC_NAME)
    time.sleep(1)  # Give some time for the topic to be fully created
    produce_messages(producer)
    time.sleep(1)  # Give some time for messages to be fully produced
    consume_messages(consumer)
