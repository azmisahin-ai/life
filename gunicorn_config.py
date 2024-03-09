# gunicorn_config.py

import os

# Get environment variables
APP_ENV = os.environ.get("APP_ENV")
APP_NAME = os.environ.get("APP_NAME")
HOST_IP = os.environ.get("HOST_IP")
HTTP_PORT = os.environ.get("HTTP_PORT")
HTTPS_PORT = os.environ.get("HTTPS_PORT")
TCP_PORT = os.environ.get("TCP_PORT")
SOCKET_PORT = os.environ.get("SOCKET_PORT")

# set
bind = f"{HOST_IP}:{HTTP_PORT}"  # port for HTTP server
workers = 2  # Number of Gunicorn workers
worker_class = (
    # WebSocket worker class
    "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
)
certfile = "public-cert.pem"
keyfile = "private-key.pem"
