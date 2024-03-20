# src/web/api/v1/simulation_pause.py

from flask import Flask
from flask_restx import Api, Resource
from flask_socketio import SocketIO
from ...controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationPause(Resource):
    def get(self):
        """
        Pause the simulation.

        This endpoint is used to pause the simulation process.
        It returns a JSON response indicating the status of the simulation being paused.

        Returns:
            dict: A JSON object with the status of the paused simulation.
        """

        s = simulation.pause()

        response = s.to_json()

        return response


if __name__ == "__main__":
    app.run(debug=True)
