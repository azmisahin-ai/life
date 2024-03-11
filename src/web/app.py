# src/web/app.py
import logging
import os
from flask import Flask
from flask_cors import CORS

from .api import blueprint as api_blueprint
from .socket import initialize

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Get environment variables
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Cross-Origin Resource Sharing
    CORS(app, origins="*")

    # This can help the application run in an optimized manner.
    app.config["ENV"] = APP_ENV

    # Register the API Blueprint with a URL prefix
    app.register_blueprint(api_blueprint, url_prefix="/api")

    # Get API paths from the request object
    paths = [
        rule.rule
        for rule in app.url_map.iter_rules()
        if rule.endpoint.startswith("api.")
    ]

    _ = initialize(app, paths)  # Call initialize and assign the SocketIO instance

    @app.route("/")
    def home():
        """API Gateway Home

        Returns:
            dict: JSON response containing welcome message, application name, and environment.
        """
        return {
            "message": "Welcome to the API Gateway!",
            "application": APP_NAME,
            "environment": APP_ENV,
            "paths": paths,
        }

    logger.debug(
        "Application Start: %s",
        {
            "APP_ENV": APP_ENV,
            "HOST_IP": HOST_IP,
            "httpPortNumber": httpPortNumber,
        },
    )

    return app


# Listen for HTTP and WebSocket connections on the same port
app = create_app()

if __name__ == "__main__":
    # Use app instance for Flask functionalities
    app.run(debug=DEBUG, host=HOST_IP, port=httpPortNumber)
