# Simulated IoT weather station application

A containerized docker environment for simulating a weather station in an IoT private network.

Docker containers:
    - weather_station
      - Contains the weather station (Python script). Outputs data to the MQTT broker.
    - mqtt_broker: The MQTT broker that collects data
      - Broker: Eclipse Mosquitto
    - backend
      - Database: SQLite
      - Framework: FastAPI
      - ORM: SQLAlchemy
      - Web server: Uvicorn
      - MQTT Client: paho-mqtt
    - frontend
      - Astro
      - Tailwind


**Data**: This folder contains the database for persistent storage between builds.
**Web**: This folder contains the actual web application, developed on the host machine.

```txt
WeatherStation/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── database.py
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
├── conf/
│    └── mosquitto/
│         └── mosquitto.conf
├── data/
├── frontend/
│    ├── .dockerignore
│    ├── Dockerfile
│    ├── tailwind.config.js
│    └── src/
├── weather_station
│   ├── Dockerfile
│   └── sensor_script.py
└── web/
```

## Weather station

Contains a script that simulates data collected from sensors

```json
/ # mosquitto_sub -h localhost -t "weather/data"
{"temperature": 2.637812310472853, "humidity": 4.519741820736398, "time": {"month": 12, "day": 16, "hour": 18, "minute": 54}, "season": "winter"}
{"temperature": 0.2653693406758393, "humidity": 19.61492780056725, "time": {"month": 12, "day": 16, "hour": 18, "minute": 55}, "season": "winter"}
{"temperature": -18.181499560747937, "humidity": 13.496124001713529, "time": {"month": 12, "day": 16, "hour": 18, "minute": 56}, "season": "winter"}
{"temperature": -16.054882751181047, "humidity": 11.585297278875466, "time": {"month": 12, "day": 16, "hour": 18, "minute": 57}, "season": "winter"}
{"temperature": -28.51523178457232, "humidity": 5.291888904052804, "time": {"month": 12, "day": 16, "hour": 18, "minute": 58}, "season": "winter"}
```

sensor_script.py
