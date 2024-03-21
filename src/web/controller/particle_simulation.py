import time
from flask import Flask
from flask_socketio import SocketIO

from src.life.particles.vector import Vector
from src.life.particles.particle import Particle
from src.web.controller.life_cycle_simulation import LifeCycleSimulation


app = Flask(__name__)
io = SocketIO(app)


class ParticleSimulation(LifeCycleSimulation):
    def __init__(self, number_of_instance, lifetime_seconds):
        super().__init__(
            number_of_instance=number_of_instance, lifetime_seconds=lifetime_seconds
        )

    def force_function(self, t):
        return Vector(t**0.1, t**0.1, t**0.1)

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
