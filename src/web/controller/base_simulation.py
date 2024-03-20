import threading
import time
from flask import Flask
from flask_socketio import SocketIO

from src.life.particles.base import Base
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType

app = Flask(__name__)
io = SocketIO(app)


class BaseSimulation:
    def __init__(self, number_of_instance, lifetime):
        self.status = SimulationStatus.stopped
        self.is_running = False
        self.is_paused = False
        self.type = SimulationType.Base  # default simualation type
        self.lifetime = lifetime
        self.number_of_instance = number_of_instance
        self.number_of_instance_created = 0
        self.last_item = None

        self.event_function = None  # Event işlevi
        self.event_trigger = threading.Event()  # Olay tetikleyici oluştur

    def trigger(self, event_function):
        self.event_function = event_function  # Event işlevini ata

    def to_json(self):
        return {
            "lifetime": self.lifetime,
            "number_of_instance": self.number_of_instance,
            "number_of_instance_created": self.number_of_instance_created,
        }

    def create(self):
        name = f"base-{self.number_of_instance_created}"
        self.last_item = Base(name, lifetime=self.lifetime)

    def simulate(self):
        condition = self.number_of_instance > self.number_of_instance_created
        if condition:
            self.number_of_instance_created += 1
            self.create()
            if self.event_function:
                self.event_function(self.to_json())  # Event işlevini çağır

        return condition


if __name__ == "__main__":

    def lastItemEvent(data):
        # print("event-simulation-base", data)
        pass

    def simulationEvent(data):
        print("event-simulation", data)

    time_step = 0.01  # default simulation time step
    number_of_instance = 1  # default simulation instance
    life_time = 2  # second

    instance = BaseSimulation(lifetime=life_time, number_of_instance=number_of_instance)
    instance.trigger(simulationEvent)

    while instance.simulate():
        instance.last_item.trigger(lastItemEvent)
        time.sleep(time_step)
