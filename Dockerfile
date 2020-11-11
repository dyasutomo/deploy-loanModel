# Use latest Python runtime as base image
FROM python:3.6.5-slim

# Set the working directory to /app and copy current dir
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip --no-cache-dir install flask numpy pandas lightgbm


RUN apt-get update \
 && apt-get -y --no-install-recommends install \
    libgomp1 \
 && apt-get clean \


# Setting port number
EXPOSE 8000

# Executing code
CMD [python, api.py]
