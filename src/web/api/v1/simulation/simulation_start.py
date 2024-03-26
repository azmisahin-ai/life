# src/web/api/v1/simulation_start.py

from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.simulation import simulation


app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationStart(Resource):
    @app.route("/start", methods=["POST"])
    def post(self):
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

        return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
