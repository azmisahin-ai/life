# src/web/api/v1/simulation_pause.py

from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationPause(Resource):
    @app.route("/pause", methods=["GET"])
    def get():
        paused = simulation.pause()
        return jsonify(paused.to_json())


if __name__ == "__main__":
    app.run(debug=True)
