# from websockets.server import serve
# from websockets.sync.client import connect
# import asyncio
import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

# MQTT settings
BROKER = 'mqtt_broker'  # MQTT broker address
PORT = 1883
TOPIC = 'weather/data'

# WS_PORT = 9001


# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)

def publish_sensor_data(client):
    while True:
        time_now = datetime.now()
        month = time_now.month
        day = time_now.day
        hour = time_now.hour
        minute = time_now.minute

        temp, hum, season = get_temp_and_hum(month)

        data = {
            'temperature': temp,
            'humidity': hum,
            'time': {
                'month': month,
                'day': day,
                'hour': hour,
                'minute': minute
            },
            'season': season    # This data may better be suited to calculate in the front-end
        }                       # But I ain't got time for that
        payload = json.dumps(data)
        client.publish(TOPIC, payload)

        # print("Sending Websockets")
        # ws_send(payload)

        time.sleep(10)  # Publish 10 seconds

def get_temp_and_hum(month) -> (int, int, str):
    temp = 0
    hum = 0
    season = ""

    if month == 12 or (month < 3 and month > 0):
        # ❄️ It's winter
        temp = random.uniform(-30, 10)
        hum = random.uniform(1, 20)
        season = "winter"

    elif 3 <= month <= 5:
        # 🌷 It's spring
        temp = random.uniform(10, 25)
        hum = random.uniform(20, 60)
        season = "spring"

    elif 6 <= month <= 8:
        # ☀️ It's summer
        temp = random.uniform(20, 35)
        hum = random.uniform(40, 80)
        season = "summer"

    elif 9 <= month <= 11:
        # 🍂 It's fall
        temp = random.uniform(10, 20)
        hum = random.uniform(30, 60)
        season = "fall"

    return temp, hum, season


# def ws_send(data):
#     with connect("ws://localhost:8765") as websocket:
#         websocket.send(data)
#         message = websocket.recv()
#         print(f"Received: {message}")

def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    publish_sensor_data(client)


#     async with serve(echo, BROKER, 9001):
#         await asyncio.Future()  # run forever


if __name__ == '__main__':
    main()
    # asyncio.run(main())
