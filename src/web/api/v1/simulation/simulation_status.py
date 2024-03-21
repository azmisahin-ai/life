# src/web/api/v1/simulation_status.py

from flask import Flask
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationStatus(Resource):
    def get(self):
        """
        Get the status of the simulation.

        This endpoint is used to retrieve the current status of the simulation process.

        Returns:
            dict: A JSON object with the status of the simulation and information about a particle.
                  - status (str): The status of the simulation.
                  - particle (dict): Information about
                  a particle including its name, charge, mass, spin, lifetime, energy, position, velocity, and momentum.
        """

        s = simulation.status()

        response = s.to_json()

        return response


if __name__ == "__main__":
    app.run(debug=True)
