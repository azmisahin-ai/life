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
    def get():
        stopped = simulation.stop()
        return jsonify(stopped.to_json())


if __name__ == "__main__":
    app.run(debug=True)
