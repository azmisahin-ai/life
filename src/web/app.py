# src/web/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS


from .api import blueprint as api_blueprint
from .socket import initialize

from src.web.config import APP_ENV, APP_NAME, HOST_IP, httpPortNumber, DEBUG
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.simulation import simulation
from src.package import Logger

# Log ayarlarını yapılandırma
logger = Logger(name="application", log_to_file=True, log_to_console=True).get_logger()


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

    io = initialize(app, paths)  # Call initialize and assign the SocketIO instance

    @app.route("/")
    def home():
        """API Gateway Home

        Returns:
            dict: JSON response containing welcome message, application name, and environment.
        """
        response = {
            "message": "Welcome to the API Gateway!",
            "application": APP_NAME,
            "environment": APP_ENV,
            "paths": paths,
        }
        io.emit("api_signal", response)
        return

    @app.route("/socket/v1/simulation/status", methods=["GET"])
    def get_status():
        # proccess
        simulation.status()

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_signal", response)

        return jsonify(response)

    @app.route("/socket/v1/simulation/start", methods=["POST"])
    def post_start():
        # get request
        data = request.json
        # request
        number_of_instance = data.get("number_of_instance", 1)
        lifetime_seconds = data.get("lifetime_seconds", float("inf"))
        lifecycle = data.get("lifecycle", 60 / 1)
        simulation_type_string = data.get("simulation_type", "Core")
        simulation_type = SimulationType(simulation_type_string)

        # proccess
        simulation.start(
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            simulation_type=simulation_type,
        )

        # default response
        response = {
            "simulation_type": simulation_type.value,
            "simulation_status": SimulationStatus.stopped.value,
        }

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_signal", response)

        return jsonify(response)

    @app.route("/socket/v1/simulation/pause", methods=["GET"])
    def get_pause():
        # proccess
        simulation.pause()

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_signal", response)

        return jsonify(response)

    @app.route("/socket/v1/simulation/continue", methods=["GET"])
    def get_continue():
        # proccess
        simulation.continues()

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_signal", response)

        return jsonify(response)

    @app.route("/socket/v1/simulation/stop", methods=["GET"])
    def get_stop():
        # proccess
        simulation.stop()

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_signal", response)

        return jsonify(response)

    message = "{}\t{}\t{}\t{}".format(  # noqa: F524
        "started",
        APP_ENV,
        HOST_IP,
        httpPortNumber,
    )
    logger.info(message)

    return app


# Listen for HTTP and WebSocket connections on the same port
app = create_app()

if __name__ == "__main__":
    # Use app instance for Flask functionalities
    app.run(debug=DEBUG, host=HOST_IP, port=httpPortNumber)
