# src/web/api/v1/simulation_stop.py

from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationStop(Resource):
    @app.route("/stop", methods=["GET"])
    def get(self):
        # proccess
        simulation.stop()

        if simulation.sampler:
            response = simulation.to_json()

        return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
