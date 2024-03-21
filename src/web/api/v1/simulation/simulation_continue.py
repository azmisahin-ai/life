# src/web/api/v1/simulation_continue.py

from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationContinue(Resource):
    @app.route("/continue", methods=["GET"])
    def get():
        continued = simulation.continues()
        return jsonify(continued.to_json())


if __name__ == "__main__":
    app.run(debug=True)
