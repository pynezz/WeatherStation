import asyncio
import json
from database import SessionLocal
from fastapi import FastAPI, HTTPException, WebSocket
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
import paho.mqtt.client as mqtt
import threading

from fastapi.middleware.cors import CORSMiddleware

async_engine = create_async_engine('sqlite+aiosqlite:///./weather_data.db')
async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

async def get_latest_data():
    async with async_session() as session:
        result = await session.execute(select(WeatherData).order_by(WeatherData.id.desc()).limit(1))
        latest_record = result.scalars().first()
        return json.dumps({
            "temperature": latest_record.temperature,
            "humidity": latest_record.humidity,
            "time": {
                "month": latest_record.month,
                "day": latest_record.day,
                "hour": latest_record.hour,
                "minute": latest_record.minute
            },
            "season": latest_record.season
        })

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await get_latest_data()  # Fetch the latest data from the database or MQTT
        await websocket.send_text(data)
        await asyncio.sleep(10)

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

# Added this now - haven't tested
# mqtt_client.connect_async(MQTT_BROKER, 9001, 60) # How about this? Shouldn't I try to tell Mosquitto that FastAPI wants ws-data?

# Start MQTT client in a separate thread
threading.Thread(target=mqtt_client.loop_forever, daemon=True).start()


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
