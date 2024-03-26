# Get environment variables
import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

APP_ENV = os.environ.get("APP_ENV")
APP_NAME = os.environ.get("APP_NAME")
HOST_IP = os.environ.get("HOST_IP")
HTTP_PORT = os.environ.get("HTTP_PORT")
HTTPS_PORT = os.environ.get("HTTPS_PORT")
TCP_PORT = os.environ.get("TCP_PORT")
SOCKET_PORT = os.environ.get("SOCKET_PORT")
DEBUG = os.environ.get("SWICH_TRACKING_DEBUG")

httpPortNumber = int(HTTP_PORT)
httpsPortNumber = int(HTTPS_PORT)
tcpPortNumber = int(TCP_PORT)
socketPortNumber = int(SOCKET_PORT)
