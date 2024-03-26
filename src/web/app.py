# src/web/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS


from .api import blueprint as api_blueprint
from .socket import initialize

from src.web.config import APP_ENV, APP_NAME, HOST_IP, httpPortNumber, DEBUG
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.simulation import simulation, Simulation
from src.life.particles.core import Core
from src.life.particles.particle import Particle
from src.web.controller.core_simulation import CoreSimulation
from src.web.controller.particle_simulation import ParticleSimulation
from src.package.logger import logger


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

    def simulation_status(simulation):
        try:
            if isinstance(simulation, Simulation):
                simulation.status()
                io.emit("simulation_status", simulation.to_json())

            else:
                raise RuntimeWarning("A new unknown simulation")
        except Exception as e:
            logger.exception("An error occurred: %s", e)

    def simulation_sampler_status(sampler):
        try:
            if isinstance(sampler, ParticleSimulation):
                sampler.status()
                io.emit("simulation_sampler_status", sampler.to_json())
            elif isinstance(sampler, CoreSimulation):
                sampler.status()
                io.emit("simulation_sampler_status", sampler.to_json())
            else:
                raise RuntimeWarning("A new unknown sampler")
        except Exception as e:
            logger.exception("An error occurred: %s", e)

    def simulation_instance_status(instance):
        try:
            if isinstance(instance, Particle):
                instance.status()
                io.emit("simulation_instance_status", instance.to_json())
            elif isinstance(instance, Core):
                instance.status()
                io.emit("simulation_instance_status", instance.to_json())
            else:
                raise RuntimeWarning("A new unknown instance")
        except Exception as e:
            logger.exception("An error occurred: %s", e)

    # setup simulation
    simulation.trigger_simulation(simulation_status).trigger_sampler(
        simulation_sampler_status
    ).trigger_instance(simulation_instance_status)

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("An error occurred: %s", e)
        return jsonify({"error": "Internal Server Error"}), 500

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
        io.emit("home", response)
        return response

    @app.route("/socket/v1/simulation/status", methods=["GET"])
    def get_status():
        try:
            simulation.status()
            if simulation.sampler:
                response = simulation.to_json()
            return jsonify(response)
        except AttributeError as e:
            # Sadece 'AttributeError' hatasını loglayalım
            logger.error("An 'AttributeError' occurred: %s", e)
            # Hata yanıtı döndürelim
            return jsonify({"error": "Internal Server Error"}), 500

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
        io.emit("simulation_status", response)

        return jsonify(response)

    @app.route("/socket/v1/simulation/pause", methods=["GET"])
    def get_pause():
        # proccess
        simulation.pause()

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_status", response)

        return jsonify(response)

    @app.route("/socket/v1/simulation/continue", methods=["GET"])
    def get_continue():
        # proccess
        simulation.continues()

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_status", response)

        return jsonify(response)

    @app.route("/socket/v1/simulation/stop", methods=["GET"])
    def get_stop():
        # proccess
        simulation.stop()

        if simulation.sampler:
            response = simulation.to_json()

        # send signal
        io.emit("simulation_status", response)

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
