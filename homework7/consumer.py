import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kafka import KafkaConsumer
from models import ride_deserializer

# Connect to Kafka / Redpanda
server = "localhost:9092"  # since we're running Python in Codespaces host

consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=[server],
    auto_offset_reset='earliest',  # read from the beginning
    enable_auto_commit=True,
    value_deserializer=ride_deserializer,
    consumer_timeout_ms=2000  # stop after 2s of inactivity
)

count = 0

for message in consumer:
    ride = message.value
    trip_distance_current = ride.trip_distance
    if trip_distance_current > 5.0:
        count += 1

print(f"Number of trips with trip_distance > 5 km: {count}")
consumer.close()
