import time
from flask import Flask
from flask_socketio import SocketIO

from src.life.particles.vector import Vector
from src.life.particles.particle import Particle
from src.web.controller.base_simulation import BaseSimulation


app = Flask(__name__)
io = SocketIO(app)


class ParticleSimulation(BaseSimulation):
    def __init__(self, lifetime, number_of_instance):
        super().__init__(lifetime, number_of_instance)

    def force_function(self, t):
        return Vector(t**0.1, t**0.1, t**0.1)

    def to_json(self):
        data = super().to_json()

        data.update(
            {
                "status": self.status.value,
                "number_of_particles": self.number_of_instance,
                "time_step": "0",
                "number_of_instance_created": self.number_of_instance_created,
                "lifetime": self.lifetime,
            }
        )
        data.update({"particle": self.last_item.to_json()})
        return data

    def create(self):
        name = f"electron-{self.number_of_instance_created}"
        charge = -1.6e-19
        mass = 9.1e-31
        spin = 1 / 2
        lifetime = self.lifetime
        energy = 0
        position = Vector(0, 0, 0)
        velocity = Vector(0, 0, 0)
        momentum = Vector(0, 0, 0)
        wave_function = self.force_function(0.1)

        self.last_item = Particle(
            name,
            charge,
            mass,
            spin,
            lifetime,
            energy,
            position,
            velocity,
            momentum,
            wave_function,
        )


if __name__ == "__main__":

    def lastItemEvent(data):
        # print("event-simulation-particle", data)
        pass

    def simulationEvent(data):
        print("event-simulation", data)
        pass

    time_step = 0.01  # default simulation time step
    number_of_instance = 1  # default simulation instance
    life_time = 5  # second or float("inf")

    instance = ParticleSimulation(
        lifetime=life_time, number_of_instance=number_of_instance
    )
    instance.trigger(simulationEvent)

    while instance.simulate():
        instance.last_item.trigger(lastItemEvent)
        time.sleep(time_step)
