import boto3
import json
import subprocess

# Initialize SQS client with explicit endpoint URL
sqs_client = boto3.client('sqs', region_name='us-east-1', endpoint_url='http://localhost:4566')

# SQS Queue configuration
QUEUE_NAME = 'demo-queue'

def create_queue(queue_name):
    try:
        response = sqs_client.create_queue(QueueName=queue_name)
        print(f"Response from create_queue: {json.dumps(response, indent=2)}")
        queue_url = response.get('QueueUrl')
        if not queue_url:
            print(f"Failed to get QueueUrl from response. Trying AWS CLI. Full response: {json.dumps(response, indent=2)}")
            queue_url = create_queue_with_cli(queue_name)
        print(f"Queue '{queue_name}' created with URL: {queue_url}")
        return queue_url
    except KeyError:
        print(f"Failed to create queue '{queue_name}'. Response: {json.dumps(response, indent=2)}")
        raise

def create_queue_with_cli(queue_name):
    try:
        result = subprocess.run(
            ['aws', '--endpoint-url=http://localhost:4566', 'sqs', 'create-queue', '--queue-name', queue_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            print(f"Failed to create queue with AWS CLI. Error: {result.stderr.decode('utf-8')}")
            raise Exception("AWS CLI create-queue failed")
        response = json.loads(result.stdout)
        queue_url = response.get('QueueUrl')
        if not queue_url:
            raise KeyError("QueueUrl not found in the AWS CLI response")
        return queue_url
    except Exception as e:
        print(f"Failed to create queue with AWS CLI. Error: {e}")
        raise

def send_message(queue_url, message_body):
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to queue '{queue_url}' with message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send message to queue '{queue_url}'. Error: {e}")

def receive_messages(queue_url):
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=2
        )
        messages = response.get('Messages', [])
        for message in messages:
            print(f"Received message: {message['Body']}")
            delete_message(queue_url, message['ReceiptHandle'])
    except Exception as e:
        print(f"Failed to receive messages from queue '{queue_url}'. Error: {e}")

def delete_message(queue_url, receipt_handle):
    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print(f"Message deleted from queue '{queue_url}'")
    except Exception as e:
        print(f"Failed to delete message from queue '{queue_url}'. Error: {e}")

def set_queue_attributes(queue_url, attributes):
    try:
        sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes=attributes
        )
        print(f"Queue attributes set for '{queue_url}': {attributes}")
    except Exception as e:
        print(f"Failed to set attributes for queue '{queue_url}'. Error: {e}")

def list_queues():
    try:
        response = sqs_client.list_queues()
        queue_urls = response.get('QueueUrls', [])
        print("List of queues:")
        for queue_url in queue_urls:
            print(f"  {queue_url}")
    except Exception as e:
        print(f"Failed to list queues. Error: {e}")

if __name__ == "__main__":
    try:
        # SQS Operations
        queue_url = create_queue(QUEUE_NAME)
        
        # Set queue attributes (example: set visibility timeout to 60 seconds)
        attributes = {'VisibilityTimeout': '60'}
        set_queue_attributes(queue_url, attributes)

        # Send a message
        send_message(queue_url, "Hello, LocalStack!")

        # List all queues
        list_queues()

        # Receive messages
        receive_messages(queue_url)
        
    except Exception as e:
        print(f"An error occurred: {e}")
