# src/web/api/v1/simulation_start.py

from flask import Flask, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


class SimulationStart(Resource):
    def post(self):
        """
        Starts the simulation.

        Parameters:
        - number_Of_particles (int): Number of particles for the simulation.
        - time_step (float): Time step for the simulation.

        Body:
        {
            "number_Of_particles": int,
            "time_step": float
        }
        """
        data = request.json
        numberOfParticles = data.get("number_Of_particles")
        timeStep = data.get("time_step")

        response = {
            "status": "started",
            "number_Of_particles": numberOfParticles,
            "time_step": timeStep,
        }

        return response


if __name__ == "__main__":
    app.run(debug=True)
