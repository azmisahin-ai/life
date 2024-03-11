# src/web/socket/__init__.py

import os
import logging
from flask_socketio import SocketIO
import requests

HOST_IP = os.environ.get("HOST_IP")
HTTP_PORT = os.environ.get("HTTP_PORT")
httpPortNumber = int(HTTP_PORT)
PROTOCOL = "HTTP"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize(app, paths):
    """
    Initialize and configure Flask SocketIO.

    Parameters:
    - app: Flask application instance
    - paths: List of paths to check

    Returns:
    - SocketIO instance
    """
    # # First create an SSL/TLS certificate
    # context = SSL.Context(SSL.SSLv23_METHOD)
    # context.use_privatekey_file("private-key.pem")
    # context.use_certificate_file("public-cert.pem")

    io = SocketIO(
        app,
        # This allows all origins, but in a real production environment it is safer to opt for a more specific value.
        # For example, to only allow a specific origin:
        # cors_allowed_origins="https://example.com"
        cors_allowed_origins="*",
        logger=True,
        engineio_logger=True,
        # If your server uses secure connection (HTTPS), you need to use wss (WebSocket Secure) protocol.
        # ssl_context="adhoc",
        # ssl_context=context,
    )

    @io.on("message")
    def handle_ws_message(endpoint):
        """
        Handle WebSocket 'message' event.

        Parameters:
        - endpoint: WebSocket endpoint

        Emits:
        - 'message' event with the response
        """
        logger.debug("WebSocket message received: %s", endpoint)
        response = checkEndpoint(endpoint)
        io.emit("message", response)

    @io.on("get")
    def handle_ws_get(endpoint):
        """
        Handle WebSocket 'get' event.

        Parameters:
        - endpoint: WebSocket endpoint

        Emits:
        - Emits the response to the specified endpoint
        """
        logger.debug("WebSocket GET request received: %s", endpoint)
        response = getApi(endpoint)
        logger.debug("WebSocket GET response: %s", response)
        io.emit(endpoint, response)

    def checkEndpoint(endpoint):
        for path in paths:
            if endpoint in path:
                return endpoint
        return None

    def getUrl(endpoint):
        try:
            api_url = f"{PROTOCOL}://{HOST_IP}:{httpPortNumber}{endpoint}"
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return f"Error: {e}"

    def getApi(endpoint):
        if checkEndpoint(endpoint):
            return getUrl(endpoint)

        return None

    return io
