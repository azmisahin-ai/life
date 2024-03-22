# src/web/app.py
import logging
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from src.life.particles.life_cycle_manager import LifeCycleManager
from src.life.particles.particle import Particle
from src.web.controller.simulation import simulation
from src.web.controller.life_cycle_simulation import LifeCycleSimulation
from src.web.controller.particle_life_cycle_simulation import (
    ParticleLifeCycleSimulation,
)
from src.web.controller.simulation_type import SimulationType

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

    io = initialize(app, paths)  # Call initialize and assign the SocketIO instance

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

    @app.route("/socket/v1/simulation/start", methods=["POST"])
    def post_start():
        data = request.json
        simulation_time_step = data.get("simulation_time_step", 1)
        simulation_type_str = data.get(
            "simulation_type", "LifeCycle"
        )  # Öntanımlı değer olarak dize kullanılabilir
        simulation_type = SimulationType(simulation_type_str)  # Dizeyi Enum'a dönüştür

        number_of_instance = data.get("number_of_instance", 2)
        lifetime_seconds = data.get("lifetime_seconds", 5)

        started = simulation.start(
            simulation_time_step=simulation_time_step,
            simulation_type=simulation_type,
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
        )

        # RED = "\033[91m"
        # GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        # CYAN = "\033[96m"
        RESET = "\033[0m"  # Renkleri sıfırlamak için kullanılır

        # Event status
        def simulation_event_item(inst):
            io.emit("/simulation/status/item", inst.to_json())
            # print(f"{GREEN}/simulation-status-item{RESET}", inst)
            if issubclass(type(inst), LifeCycleManager):
                print(f"{BLUE}/simulation/status/item{RESET}", inst.name)
            elif isinstance(inst, Particle):
                print(f"{BLUE}/simulation/status/item{RESET}", inst.name)

        # Simulation status
        def simulation_event(inst):
            io.emit("/simulation/status/instance", inst.to_json())
            print(f"{YELLOW}/simulation/status/instance{RESET}", inst)
            if issubclass(type(inst), LifeCycleSimulation):
                inst.last_item.trigger_event(simulation_event_item)
            elif isinstance(inst, ParticleLifeCycleSimulation):
                inst.last_item.trigger_event(simulation_event_item)

        if started.instance:
            started.instance.trigger(simulation_event)
            io.emit("/simulation/status", started.to_json())

        return jsonify(started.to_json())

    @app.route("/socket/v1/simulation/stop", methods=["GET"])
    def get_stop():
        stopped = simulation.stop()
        io.emit("/simulation/status", stopped.to_json())
        return jsonify(stopped.to_json())

    @app.route("/socket/v1/simulation/pause", methods=["GET"])
    def get_pause():
        paused = simulation.pause()
        io.emit("/simulation/status", paused.to_json())
        return jsonify(paused.to_json())

    @app.route("/socket/v1/simulation/continue", methods=["GET"])
    def get_continue():
        continued = simulation.continues()
        io.emit("/simulation/status", continued.to_json())
        return jsonify(continued.to_json())

    @app.route("/socket/v1/simulation/status", methods=["GET"])
    def get_status():
        status = simulation.status()
        io.emit("/simulation/status", status.to_json())
        return jsonify(status.to_json())

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
