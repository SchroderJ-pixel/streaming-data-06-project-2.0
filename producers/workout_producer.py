import time, uuid, random
import orjson
from datetime import datetime
from kafka import KafkaProducer
from utils.utils_config import KAFKA_BROKER, KAFKA_TOPIC
from utils.utils_logger import get_logger

LOG = get_logger("workout_producer")

EXERCISE_TO_GROUP = {
    "bench_press": "chest",
    "squat": "legs",
    "lat_pulldown": "back",
    "shoulder_press": "shoulders",
    "barbell_curl": "arms",
    "plank": "core",
}

EXERCISES = list(EXERCISE_TO_GROUP.keys())

def random_message(session_id: str):
    exercise = random.choice(EXERCISES)
    group = EXERCISE_TO_GROUP[exercise]
    reps = random.randint(5, 12)
    weight = random.choice([50, 75, 100, 125, 150])
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": session_id,
        "exercise": exercise,
        "muscle_group": group,
        "reps": reps,
        "weight": weight
    }

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: orjson.dumps(v)
    )

    session_id = str(uuid.uuid4())
    LOG.info(f"Producer started → broker={KAFKA_BROKER}, topic={KAFKA_TOPIC}")

    try:
        while True:
            msg = random_message(session_id)
            producer.send(KAFKA_TOPIC, msg)
            LOG.info(f"Sent: {msg}")
            time.sleep(2)  # send every 2s
    except KeyboardInterrupt:
        LOG.info("Stopping producer...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
