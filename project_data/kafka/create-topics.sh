#!/bin/bash
TOPICS=("location_topic" "user_data_avro_topic")

sleep 10

for TOPIC in "${TOPICS[@]}"; do
  kafka-topics --create --if-not-exists \
    --topic "$TOPIC" \
    --bootstrap-server kafka:9092 \
    --partitions 1 \
    --replication-factor 1
done
