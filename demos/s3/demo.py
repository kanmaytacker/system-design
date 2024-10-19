from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from localstack_client.session import Session

# Initialize a session using LocalStack
session = Session()

# Initialize S3 client
s3_client = session.client('s3', region_name='us-east-1')

# S3 Bucket and Object configuration
BUCKET_NAME = 'demo-bucket'
OBJECT_NAME = 'demo.txt'
OBJECT_CONTENT = 'Hello, LocalStack!'
FOLDER_NAME = 'demo-folder/'
MULTIPART_OBJECT_NAME = 'large-object.txt'
MULTIPART_CONTENT = 'A' * 10 * 1024 * 1024  # 10MB of 'A'


def create_s3_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket '{bucket_name}' already exists and is owned by you")


def upload_object_to_s3(bucket_name, object_name, content):
    value = s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=content)
    print(f"Object '{object_name}' uploaded to bucket '{bucket_name}'")


def read_object_from_s3(bucket_name, object_name):
    response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    content = response['Body'].read().decode('utf-8')
    print(f"Read from S3: {content}")


def create_folder(bucket_name, folder_name):
    s3_client.put_object(Bucket=bucket_name, Key=folder_name)
    print(f"Folder '{folder_name}' created in bucket '{bucket_name}'")


def list_objects(bucket_name, prefix=''):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    objects = response.get('Contents', [])
    print(f"Objects in bucket '{bucket_name}' with prefix '{prefix}':")
    for obj in objects:
        print(f"  {obj['Key']}")


def delete_object(bucket_name, object_name):
    s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    print(f"Object '{object_name}' deleted from bucket '{bucket_name}'")


def set_bucket_policy(bucket_name, policy):
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
    print(f"Policy set for bucket '{bucket_name}'")


def multipart_upload(bucket_name, object_name, content):
    # Initiate the multipart upload
    multipart_upload = s3_client.create_multipart_upload(Bucket=bucket_name, Key=object_name)
    upload_id = multipart_upload['UploadId']

    # Split the content into parts and upload each part
    part_size = 5 * 1024 * 1024  # 5MB per part
    parts = []
    for i in range(0, len(content), part_size):
        part_number = len(parts) + 1
        part_content = content[i:i + part_size]
        part_response = s3_client.upload_part(
            Bucket=bucket_name,
            Key=object_name,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=part_content
        )
        parts.append({
            'ETag': part_response['ETag'],
            'PartNumber': part_number
        })

    # Complete the multipart upload
    s3_client.complete_multipart_upload(
        Bucket=bucket_name,
        Key=object_name,
        MultipartUpload={'Parts': parts},
        UploadId=upload_id
    )
    print(f"Multipart upload for '{object_name}' completed")


if __name__ == "__main__":
    try:
        # S3 Operations
        create_s3_bucket(BUCKET_NAME)
        upload_object_to_s3(BUCKET_NAME, OBJECT_NAME, OBJECT_CONTENT)
        read_object_from_s3(BUCKET_NAME, OBJECT_NAME)

        # Folder operations
        create_folder(BUCKET_NAME, FOLDER_NAME)
        upload_object_to_s3(BUCKET_NAME, FOLDER_NAME + OBJECT_NAME, OBJECT_CONTENT)
        list_objects(BUCKET_NAME, FOLDER_NAME)

        # Policy setting (example policy)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"  # ARN is an identifier for resources in AWS
                }
            ]
        }
        set_bucket_policy(BUCKET_NAME, str(policy))

        # Multipart upload
        multipart_upload(BUCKET_NAME, MULTIPART_OBJECT_NAME, MULTIPART_CONTENT)

        # Listing and deleting objects
        list_objects(BUCKET_NAME)
        delete_object(BUCKET_NAME, OBJECT_NAME)
        delete_object(BUCKET_NAME, FOLDER_NAME + OBJECT_NAME)
        list_objects(BUCKET_NAME)
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
