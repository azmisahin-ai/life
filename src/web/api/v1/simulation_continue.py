# src/web/api/v1/simulation_continue.py

from flask import Flask
from flask_restx import Api, Resource

from ...controller.simulation import Simulation

app = Flask(__name__)
api = Api(app)

simulation = Simulation()


class SimulationContinue(Resource):
    def get(self):
        """
        Continue the simulation.

        This endpoint is used to continue the simulation process.
        It returns a JSON response indicating the status of the simulation.

        Returns:
            dict: A JSON object with the status of the simulation.
        """

        response = simulation.continues().to_json()

        return response


if __name__ == "__main__":
    app.run(debug=True)
