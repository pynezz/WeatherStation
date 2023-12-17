# #! /usr/bin/python3

# import threading
# from fastapi import FastAPI, BackgroundTasks
# import paho.mqtt.client as mqtt
# from database import SessionLocal, engine
# from models import WeatherDataModel, WeatherData, Base
# import json
# import asyncio

# from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session

# from . import crud, models, schemas
# from .database import SessionLocal, engine


# # Database initialization
# # In your main.py, replace the incorrect line with the following:
# models.Base.metadata.create_all(bind=engine)

# # Dependency


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # WeatherDataModel.Base.metadata.create_all(bind=engine)

# # MQTT settings
# MQTT_BROKER = 'mqtt_broker'
# MQTT_PORT = 1883
# MQTT_TOPIC = 'weather/data'

# # Start the MQTT subscription as a background task
# # @app.on_event("startup")
# # async def startup_event():
# #     print("+ Service started")
# #     BackgroundTasks().add_task(mqtt_subscribe)

# app = FastAPI()

# @app.post("/", response_model=schemas.)

# @app.on_event("startup")
# async def startup_event():
#     print("+ Startup event")
#     asyncio.create_task(mqtt_subscribe())


# # REST API to fetch weather data
# @app.get("/weather")
# async def get_weather_data():
#     print("+ GET request to /weather received")
#     db = SessionLocal()
#     try:
#         return db.query(WeatherDataModel).all()
#     finally:
#         db.close()


# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print(f"Connected to MQTT broker! {client}:{userdata}:{flags}:{rc}")
#     else:
#         print("Failed to connect, return code %d\n", rc)

# # MQTT on_message callback
# def on_message(client, userdata, message):
#     print(f"Received message: {message.payload.decode()}")
#     db = SessionLocal()
#     try:
#         data = json.loads(message.payload.decode())
#         weather_data = WeatherDataModel(
#             temperature=data['temperature'],
#             humidity=data['humidity'],
#             season=data['season'],
#             # Add other fields as necessary
#         )
#         db.add(weather_data)
#         db.commit()
#         print("Data committed to the database")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         db.close()

# async def mqtt_subscribe():
#     print("Starting MQTT subscription...")
#     try:
#         client = mqtt.Client()
#         client.on_connect = on_connect
#         client.on_disconnect = on_disconnect
#         client.on_message = on_message
#         client.connect(MQTT_BROKER, MQTT_PORT, 60)

#         # Run the loop in a separate thread
#         thread = threading.Thread(target=client.loop_forever)
#         thread.start()
#         print("MQTT loop fucking started!!")
#     except Exception as e:
#         print(f"Error in MQTT subscription fuckface: {e}")


# def on_disconnect(client, userdata, rc):
#     print("Disconnected from MQTT Broker")

import json
from database import SessionLocal
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import paho.mqtt.client as mqtt
import threading

from fastapi.middleware.cors import CORSMiddleware



Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)
    month = Column(Integer)
    day = Column(Integer)
    hour = Column(Integer)
    minute = Column(Integer)
    season = Column(String)

# Create an engine that stores data in the local directory's weather.db file.
# engine = create_engine('sqlite:///data/weather_data.db')
engine = create_engine('sqlite:///./weather_data.db')

# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# MQTT setup
MQTT_BROKER = "mqtt_broker"
MQTT_TOPIC = "weather/data"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)


# MQTT client's on_message function
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    # Parse time data
    time_data = data.get("time", {})
    month = time_data.get("month")
    day = time_data.get("day")
    hour = time_data.get("hour")
    minute = time_data.get("minute")

    # Create a new WeatherData object
    weather_entry = WeatherData(
        temperature=data.get("temperature"),
        humidity=data.get("humidity"),
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        season=data.get("season")
    )

    # Database session to add and commit new entry
    session = SessionLocal()
    session.add(weather_entry)
    session.commit()
    session.close()

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)

# Start MQTT client in a separate thread
threading.Thread(target=mqtt_client.loop_forever, daemon=True).start()

# FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    # In production, specify your frontend's domain instead of '*'
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/weather")
async def read_weather():
    session = SessionLocal()
    try:
        weather_records = session.query(WeatherData).all()
        return {
            "data": [
                {
                    "temperature": record.temperature,
                    "humidity": record.humidity,
                    "time": {
                        "month": record.month,
                        "day": record.day,
                        "hour": record.hour,
                        "minute": record.minute
                    },
                    "season": record.season
                }
                for record in weather_records
            ]
        }
    finally:
        session.close()
