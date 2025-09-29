import orjson
from kafka import KafkaConsumer
from utils.utils_config import KAFKA_BROKER, KAFKA_TOPIC
from utils.utils_logger import get_logger
from utils.utils_state import update_volume

LOG = get_logger("consumer_volume")

def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: orjson.loads(v)
    )

    LOG.info(f"Consumer started → broker={KAFKA_BROKER}, topic={KAFKA_TOPIC}")

    for message in consumer:
        data = message.value
        group = data["muscle_group"]
        reps = data["reps"]
        weight = data["weight"]
        totals = update_volume(group, reps, weight)
        LOG.info(f"Updated totals: {dict(totals)}")

if __name__ == "__main__":
    main()
