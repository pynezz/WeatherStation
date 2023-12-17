# Backend Dockerfile for FastAPI

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Leveraging Dockers caching by copying the requirements first,
# then, install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container, as defined in docker-compose.yml
EXPOSE 5000

# Define the command to run your app using CMD which defines your runtime
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
