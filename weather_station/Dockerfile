FROM alpine:latest

RUN apk add --update python3 py3-pip
# Set up a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip3 install paho-mqtt

# Simulation of sensor data
COPY sensor_script.py /sensor_script.py

# When the container starts, run Python script
CMD ["python3", "/sensor_script.py"]
