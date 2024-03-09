# src/web/socket/__init__.py
from flask_socketio import SocketIO
from OpenSSL import SSL


def initialize(app, api):

    # First create an SSL/TLS certificate
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file("private-key.pem")
    context.use_certificate_file("public-cert.pem")

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
        ssl_context=context,
    )

    @io.on("message")
    def handle_ws_message(message):
        response = getApi(message)
        io.emit("message", response)

    def getApi(message):
        return f"Invalid API route: {message}"

    return io
