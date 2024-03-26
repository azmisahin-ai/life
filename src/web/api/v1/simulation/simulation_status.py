# src/web/api/v1/simulation_status.py

from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.package.logger import logger
from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationStatus(Resource):
    @app.route("/status", methods=["GET"])
    def get(self):
        try:
            simulation.status()
            if simulation.sampler:
                response = simulation.to_json()
            io.emit("simulation_status", response)
            return jsonify(response)
        except AttributeError as e:
            # Sadece 'AttributeError' hatasını loglayalım
            logger.error("An 'AttributeError' occurred: %s", e)
            # Hata yanıtı döndürelim
            return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
