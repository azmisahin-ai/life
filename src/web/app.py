# src/web/app.py
import os
import ssl
from flask import Flask
from flask_cors import CORS

from .socket import initialize
from .api import blueprint as api_blueprint, api
from gevent.pywsgi import WSGIServer  # Import the WSGIServer from gevent
from geventwebsocket.handler import WebSocketHandler  # Yeni eklenen import

# Get environment variables
APP_ENV = os.environ.get("APP_ENV")
APP_NAME = os.environ.get("APP_NAME")
HOST_IP = os.environ.get("HOST_IP")
HTTP_PORT = os.environ.get("HTTP_PORT")
HTTPS_PORT = os.environ.get("HTTPS_PORT")
TCP_PORT = os.environ.get("TCP_PORT")
SOCKET_PORT = os.environ.get("SOCKET_PORT")

httpPortNumber = int(HTTP_PORT)
httpsPortNumber = int(HTTPS_PORT)
tcpPortNumber = int(TCP_PORT)
socketPortNumber = int(SOCKET_PORT)

# Install SSL/TLS certificate
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain("public-cert.pem", "private-key.pem")


def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Cross-Origin Resource Sharing
    CORS(app, origins="*")

    # This can help the application run in an optimized manner.
    app.config["ENV"] = APP_ENV

    # Register the API Blueprint with a URL prefix
    app.register_blueprint(api_blueprint, url_prefix="/api")

    # Ability to access endpoints via socket.
    io = initialize(app, api)

    # Listen for HTTP connections
    http_server = WSGIServer(
        (HOST_IP, httpPortNumber),
        # Flask Application
        app,
        # SSL/TLS certificate
        keyfile="private-key.pem",
        certfile="public-cert.pem",
        # Pass the SSL context here
        ssl_context=context,
        # Specify gevent worker class
        worker_class="gevent",
        # Improve logging with x-forwarded-for
        access_log_format="%({x-forwarded-for}i)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s",
        # It allows Gunicorn to process standard HTTP requests while also allowing WebSocket connections.
        handler_class=WebSocketHandler,
    )

    # Listen for WebSocket connections
    ws_server = WSGIServer(
        (HOST_IP, socketPortNumber),  # A different port number for WebSocket
        # Flask Application
        app,
        # SSL/TLS certificate
        keyfile="private-key.pem",
        certfile="public-cert.pem",
        # Pass the SSL context here
        ssl_context=context,
        # It allows Gunicorn to process standard HTTP requests while also allowing WebSocket connections.
        handler_class=WebSocketHandler,
    )

    # Get API paths from the request object
    paths = [
        rule.rule
        for rule in app.url_map.iter_rules()
        if rule.endpoint.startswith("api.")
    ]

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

    return app, io, http_server, ws_server


# Listen for HTTP and WebSocket connections on the same port
app, io, http_server, ws_server = create_app()

# Build Flask app to migrate to Gunicorn
if __name__ == "__main__":
    print("http", httpPortNumber)
    print("socket", socketPortNumber)
    http_server.start()
    ws_server.start()
    io.init_app(app)
    io.run(app, host=HOST_IP, port=httpPortNumber)
