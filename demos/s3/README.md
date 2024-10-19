# S3
## Setup

Start LocalStack using the following command:

```bash
docker-compose up -d
```

Connect to the LocalStack container:

```bash
docker exec -it s3_localstack_1 /bin/bash
```

Run `aws configure` to configure the AWS CLI:

```bash
aws configure
```
```shell
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: ap-south-1
Default output format [None]: json
```

## Operations

You can create an S3 bucket by running the following command:
```bash
aws s3api create-bucket --bucket demo-bucket --endpoint-url=http://localhost:4566
```

Create a simple text file:

```bash
echo "Hello, LocalStack!" > demo.txt
```

Upload the file to the S3 bucket:

```bash
aws s3 cp demo.txt s3://demo-bucket/demo.txt --endpoint-url=http://localhost:4566
```

Download the object to read its content:

```bash
aws s3 cp s3://demo-bucket/demo.txt demo-read.txt --endpoint-url=http://localhost:4566
cat demo-read.txt
```

To list all the objects:

```bash
aws s3api list-objects --bucket demo-bucket --endpoint-url=http://localhost:4566
```

Generate a pre-signed URL for the object:

```bash
aws s3 presign s3://demo-bucket/demo.txt --endpoint-url=http://localhost:4566
```

> If you'd like to see how you can integrate Zookeeper programmatically, check out the script [here](./demo.py).