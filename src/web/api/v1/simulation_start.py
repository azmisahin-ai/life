# src/web/api/v1/simulation_start.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_socketio import SocketIO


from src.web.controller.life_cycle_type import LifeCycleType
from src.web.controller.simulation import simulation

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


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
        #
        number_of_particles = data.get("number_of_particles")
        time_step = data.get("time_step")

        s = simulation.start(
            life_cycle_time_step=time_step,
            life_cycle_type=LifeCycleType.Particles,
            number_of_instance=number_of_particles,
            lifetime_seconds=5,  # second or float("inf")
        )

        def simulation_event(data):
            print("simulation_event", data)
            io.emit("/api/v1/simulation_status", data)

        s.instance.trigger(simulation_event)

        response = s.to_json()

        return response


if __name__ == "__main__":
    app.run(debug=True)
