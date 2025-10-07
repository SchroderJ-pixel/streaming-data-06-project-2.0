# streaming-data-07-project
Streaming Data: Mod 7 Project

**Course:** Streaming Data – Module 7  
**Date:** October 7, 2025  
**Author:** Justin Schroder  
**GitHub:** [SchroderJ-pixel](https://github.com/SchroderJ-pixel) 

---

# 🏋️‍♂️ Live Workout Tracker (Kafka)

## What It Does
This project simulates a live data streaming pipeline using **Apache Kafka**.  
- The **producer** streams workout set data as JSON (reps × weight) by exercise/muscle group.  
- The **consumer** computes total **training volume (tonnage)** in real time, maintains per-group totals.
- A **chart consumer** provides a **live bar chart** of cumulative volume by muscle group.

---

## ⚙️ Quick Start

If you just want to get it running fast:
```bash
git clone https://github.com/SchroderJ-pixel/streaming-data-07-project
cd streaming-data-07-project

python -m venv .venv
.\venv\Scripts\activate  # Windows 
# or
# source .venv/bin/activate    # WSL/macOS

pip install -r requirements.txt

# In WSL:
cd ~/kafka_2.13-3.7.0
bin/zookeeper-server-start.sh config/zookeeper.properties

# In a new WSL terminal:
cd ~/kafka_2.13-3.7.0
bin/kafka-server-start.sh config/server.properties

# Create Kafka topic (run once)
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic workout_volume --partitions 1 --replication-factor 1

# (Optional) check topics
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```
---

Make sure Zookeeper and Kafka are already running before starting these scripts.

## Run the app

### 1) Start producer
#### First ensure venv is activated
```bash 
.\venv\Scripts\activate
python -m producers.producer_workout
```

### 2) Start consumer (logging version)
#### First ensure venv is activated
```bash 
.\venv\Scripts\activate
python -m consumers.consumer_volume
```

### 3) Start chart consumer
#### First ensure venv is activated
```bash 
.\venv\Scripts\activate
python -m consumers.consumer_chart
```

## Message Schema (example)
```json
{
  "ts": "2025-09-29T12:34:56.789012+00:00",
  "session_id": "a1b2c3d4",
  "exercise": "bench_press",
  "group": "chest",
  "reps": 10,
  "weight": 135
}
```

---

## Live Chart Example

**Live Line Chart (Kafka JSON streaming)**  
Cumulative training volume per muscle group over time.

![Kafka JSON Line](images/6.2.4.png)

