# src/web/api/v1/simulation_start.py

from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from flask_socketio import SocketIO

from src.life.particles.life_cycle_manager import LifeCycleManager
from src.life.particles.particle import Particle
from src.web.controller.simulation import simulation
from src.web.controller.simulation_type import SimulationType
from src.web.controller.life_cycle_simulation import LifeCycleSimulation
from src.web.controller.particle_life_cycle_simulation import (
    ParticleLifeCycleSimulation,
)

app = Flask(__name__)
api = Api(app)
io = SocketIO(app)


class SimulationStart(Resource):
    @app.route("/start", methods=["POST"])
    def post(self):
        data = request.json
        simulation_time_step = data.get("simulation_time_step", 1)
        simulation_type_str = data.get(
            "simulation_type", "LifeCycle"
        )  # Öntanımlı değer olarak dize kullanılabilir
        simulation_type = SimulationType(simulation_type_str)  # Dizeyi Enum'a dönüştür

        number_of_instance = data.get("number_of_instance", 2)
        lifetime_seconds = data.get("lifetime_seconds", 5)

        started = simulation.start(
            simulation_time_step=simulation_time_step,
            simulation_type=simulation_type,
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
        )

        # RED = "\033[91m"
        # GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        # CYAN = "\033[96m"
        RESET = "\033[0m"  # Renkleri sıfırlamak için kullanılır

        # Event status
        def simulation_event_item(inst):
            # print(f"{GREEN}simulation_event_item{RESET}", inst)
            if issubclass(type(inst), LifeCycleManager):
                print(f"{BLUE}simulation_event_event{RESET}", inst.name)
            elif isinstance(inst, Particle):
                print(f"{BLUE}simulation_event_event{RESET}", inst.name)

        # Simulation status
        def simulation_event(inst):
            print(f"{YELLOW}simulation_event_inst{RESET}", inst)
            if issubclass(type(inst), LifeCycleSimulation):
                inst.last_item.trigger_event(simulation_event_item)
            elif isinstance(inst, ParticleLifeCycleSimulation):
                inst.last_item.trigger_event(simulation_event_item)

        if started.instance:
            started.instance.trigger(simulation_event)

        return jsonify(started.to_json())


if __name__ == "__main__":
    app.run(debug=True)
