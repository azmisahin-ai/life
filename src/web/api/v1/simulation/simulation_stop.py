# src/web/api/v1/simulation_stop.py

from flask import Flask
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationStop(Resource):
    def get(self):
        """
        Stop the simulation.

        This endpoint is used to stop the simulation process.

        Returns:
            dict: A JSON object with the status of the stopped simulation.
        """

        s = simulation.stop()

        response = s.to_json()

        return response


if __name__ == "__main__":
    app.run(debug=True)
