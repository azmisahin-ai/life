# src/web/api/v1/simulation_stop.py

from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


class SimulationStop(Resource):
    def get(self):
        """
        Stop the simulation.

        This endpoint is used to stop the simulation process.

        Returns:
            dict: A JSON object with the status of the stopped simulation.
        """
        return {"status": "stopped"}


if __name__ == "__main__":
    app.run(debug=True)
