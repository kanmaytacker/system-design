#!/bin/bash

# Generate CLUSTER_ID using the kafka-storage.sh script
CLUSTER_ID=$(/opt/bitnami/kafka/bin/kafka-storage.sh random-uuid)
echo "Generated CLUSTER_ID: $CLUSTER_ID"

# Format the storage with the generated CLUSTER_ID
/opt/bitnami/kafka/bin/kafka-storage.sh format --config /opt/bitnami/kafka/config/kraft/server.properties --cluster-id $CLUSTER_ID

# Start Kafka in KRaft mode
/opt/bitnami/scripts/kafka/run.sh
