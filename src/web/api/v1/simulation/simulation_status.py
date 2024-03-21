# src/web/api/v1/simulation_status.py

from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationStatus(Resource):
    @app.route("/status", methods=["GET"])
    def get():
        status = simulation.status()
        return jsonify(status.to_json())


if __name__ == "__main__":
    app.run(debug=True)
