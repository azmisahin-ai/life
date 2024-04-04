# src/web/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS


from src.web.api import blueprint as api_blueprint
from src.web.socket import initialize

from src.web.config import APP_ENV, APP_NAME, HOST_IP, httpPortNumber, DEBUG
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.simulation import simulation, io_event

from src.package.logger import logger

queue = None  # tekil güncelleme işlemleri.
queues = None  # toplu güncelleme işlemleri.


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

    def io_simulation_status(simulation):
        # send simulation_status signal
        args = simulation.to_json()
        io.emit("simulation_status", args)

    def io_simulation_sampler_status(sampler):
        # send simulation_sampler_status signal
        args = sampler.to_json()
        io.emit("simulation_sampler_status", args)

    def io_simulation_instance_status(instance):
        # send simulation_instance_status signal
        args = instance.to_json()
        io.emit("simulation_instance_status", args)

        state = instance.status()
        # update process
        global queue
        global queues

        if queue is not None:
            # Tekil güncelleme
            if (
                state == "Running"
                and queue.get("id") is not None
                and instance.id == queue["id"]
            ):
                try:
                    # örneğe formulu uygula
                    user_formula = queues["formula"]
                    instance.apply_formula(user_formula)
                except Exception as e:
                    print("Formul uygulanamadı:", e)
                    return
                queue = None  # İşlem tamamlandığında queue'yu temizle

        if queues is not None:  # ?
            # Çoğul güncelleme
            if state == "Running" and queues.get("formula") is not None:
                try:
                    user_formula = queues["formula"]
                    # örneğe formulu uygula
                    instance.apply_formula(user_formula)
                    # Tüm kopyalara formülü uygula
                    for replica in instance.replicas:
                        replica.apply_formula(user_formula)
                except Exception as e:
                    print("Formul uygulanamadı:", e)
                    return

                queues = None  # İşlem tamamlandığında queues'yu temizle

    # Simulation Event Handler
    io_event(
        io_simulation_status,
        io_simulation_sampler_status,
        io_simulation_instance_status,
    )

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

    @app.route("/socket/v1/simulation/update/all", methods=["POST"])
    def post_update_all():
        global queues
        # get request
        queues = request.json
        # request
        formula = queues.get("formula")

        # Check
        if formula is None:
            return jsonify({"error": "formula "}), 400

        # proccess

        # default response
        response = queues

        return jsonify(response)

    @app.route("/socket/v1/simulation/update", methods=["POST"])
    def post_update():
        global queue
        # get request
        queue = request.json
        # request
        id = queue.get("id")
        codes = queue.get("codes")

        # Check
        if codes is None:
            return jsonify({"error": "codes "}), 400
        if id is None:
            return jsonify({"error": "id "}), 400

        # proccess

        # default response
        response = queue

        return jsonify(response)

    @app.route("/socket/v1/simulation/start", methods=["POST"])
    def post_start():
        # get request
        data = request.json
        # request
        number_of_instance = data.get("number_of_instance", 2)
        lifetime_seconds = data.get("lifetime_seconds", 1)
        lifecycle = data.get("lifecycle", 60 / 60)
        simulation_type_string = data.get("simulation_type", "Core")
        simulation_type = SimulationType(simulation_type_string)
        #
        number_of_replicas = data.get("number_of_replicas", 2)
        number_of_generation = data.get("number_of_generation", 2)
        max_match_limit = data.get("max_match_limit", 2)

        # Check if lifetime_seconds is None and assign float('inf') instead
        if lifetime_seconds is None:
            lifetime_seconds = float("inf")
        # Check if lifetime_seconds is provided
        if lifetime_seconds < 0:
            return jsonify({"error": "Lifetime seconds cannot be negative"}), 400
        # proccess
        simulation.start(
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            simulation_type=simulation_type,
            #
            max_replicas=number_of_replicas,
            max_generation=number_of_generation,
            max_match_limit=max_match_limit,
        )

        # default response
        response = {
            "simulation_type": simulation_type.value,
            "simulation_status": SimulationStatus.Stopped.value,
        }

        if simulation.sampler:
            response = simulation.to_json()

        return jsonify(response)

    @app.route("/socket/v1/simulation/pause", methods=["GET"])
    def get_pause():
        # proccess
        simulation.pause()

        if simulation.sampler:
            response = simulation.to_json()

        return jsonify(response)

    @app.route("/socket/v1/simulation/continue", methods=["GET"])
    def get_continue():
        # proccess
        simulation.resume()

        if simulation.sampler:
            response = simulation.to_json()

        return jsonify(response)

    @app.route("/socket/v1/simulation/stop", methods=["GET"])
    def get_stop():
        # proccess
        simulation.stop()

        if simulation.sampler:
            response = simulation.to_json()

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
