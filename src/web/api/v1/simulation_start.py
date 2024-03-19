# src/web/api/v1/simulation_start.py

from flask import Flask, request
from flask_restx import Api, Resource

from ...controller.simulation import Simulation

app = Flask(__name__)
api = Api(app)

simulation = Simulation()


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

        response = simulation.start(number_of_particles, time_step).to_json()

        return response


if __name__ == "__main__":
    app.run(debug=True)
