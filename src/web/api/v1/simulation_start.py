# src/web/api/v1/simulation_start.py

from flask import Flask, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


class SimulationStart(Resource):
    def post(self):
        """
        Starts the simulation.

        This endpoint is used to start the simulation process.

        Parameters:
        - number_Of_particles (int): Number of particles for the simulation.
        - time_step (float): Time step for the simulation.

        Body:
        {
            "number_Of_particles": int,
            "time_step": float
        }

        Returns:
            dict: A JSON object with the status of the started simulation,
                  number of particles, and time step used.
        """
        data = request.json
        number_of_particles = data.get("number_of_particles")
        time_step = data.get("time_step")

        response = {
            "status": "started",
            "number_of_particles": number_of_particles,
            "time_step": time_step,
        }

        return response


if __name__ == "__main__":
    app.run(debug=True)
