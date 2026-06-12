# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.13-slim

# Strictly for installing acspsuedo
RUN apt-get update && apt-get install -y git

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# Copy local code to the container image.
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip install git+https://github.com/ramindersinghdubb/acspsuedo.git

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:server

# [END cloudrun_helloworld_dockerfile_python]