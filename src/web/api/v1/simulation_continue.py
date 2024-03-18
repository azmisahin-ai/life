# src/web/api/v1/simulation_continue.py

from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


class SimulationContinue(Resource):
    def get(self):
        """
        Continue the simulation.

        This endpoint is used to continue the simulation process.
        It returns a JSON response indicating the status of the simulation.

        Returns:
            dict: A JSON object with the status of the simulation.
        """
        return {"status": "continues"}


if __name__ == "__main__":
    app.run(debug=True)