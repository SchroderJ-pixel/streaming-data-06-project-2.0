# --- project root on sys.path + six shim (Windows fix) ---
import sys, six
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.modules['kafka.vendor.six'] = six
sys.modules['kafka.vendor.six.moves'] = six.moves
# ----------------------------------------------------------

import threading
from collections import defaultdict
from datetime import datetime
import orjson
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter, AutoDateLocator
from kafka import KafkaConsumer
from utils.utils_config import KAFKA_BROKER, KAFKA_TOPIC
from utils.utils_logger import get_logger

LOG = get_logger("consumer_line_chart")

# shared state
volume_totals = defaultdict(int)           # cumulative per group
history_times = []                         # timestamps of updates
history_by_group = defaultdict(list)       # group -> list of cumulative values at its own timestamps
_lock = threading.Lock()

def consume_loop():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: orjson.loads(v),
        auto_offset_reset="latest",   # start from new messages
        enable_auto_commit=True,
        group_id="chart_line_group",
    )
    LOG.info(f"Chart consumer connected → broker={KAFKA_BROKER}, topic={KAFKA_TOPIC}")
    for msg in consumer:
        data = msg.value
        group = data["muscle_group"]
        reps = int(data["reps"])
        weight = int(data["weight"])
        ts = datetime.utcnow()

        with _lock:
            volume_totals[group] += reps * weight
            # record time and this group's cumulative value
            history_times.append(ts)
            history_by_group[group].append((ts, volume_totals[group]))

def start_consumer_thread():
    t = threading.Thread(target=consume_loop, daemon=True)
    t.start()
    return t

# ---- plotting ----
fig, ax = plt.subplots()
ax.set_title("Live Training Volume (Cumulative) by Muscle Group")
ax.set_xlabel("Time (UTC)")
ax.set_ylabel("Volume (reps × weight)")
locator = AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(DateFormatter("%H:%M:%S"))

def animate(_frame):
    ax.clear()
    ax.set_title("Live Training Volume (Cumulative) by Muscle Group")
    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Volume (reps × weight)")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M:%S"))

    with _lock:
        # plot each group's line with its own timestamps
        for group, series in history_by_group.items():
            if not series:
                continue
            times, values = zip(*series)
            ax.plot(times, values, label=group, linewidth=2)

    ax.legend(loc="upper left")
    ax.grid(True)

def main():
    start_consumer_thread()
    ani = FuncAnimation(fig, animate, interval=1500)  # update ~1.5s
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        LOG.info("Stopping chart...")

