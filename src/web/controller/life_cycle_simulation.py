import threading
import time
from flask import Flask
from flask_socketio import SocketIO


from src.life.particles.life_cycle_manager import LifeCycleManager


app = Flask(__name__)
io = SocketIO(app)


class LifeCycleSimulation:
    def __init__(self, number_of_instance, lifetime_seconds):
        self.number_of_instance = number_of_instance
        self.lifetime_seconds = lifetime_seconds

        #
        self.number_of_instance_created = 0

        #
        self.last_item = None

        self.event_function = None  # Event işlevi
        self.event_trigger = threading.Event()  # Olay tetikleyici oluştur

    def trigger(self, event_function):
        self.event_function = event_function  # Event işlevini ata

    def to_json(self):
        return {
            "number_of_instance": self.number_of_instance,
            "number_of_instance_created": self.number_of_instance_created,
        }

    def create(self):
        name = f"item-{self.number_of_instance_created}"
        self.last_item = LifeCycleManager(name, lifetime_seconds=self.lifetime_seconds)

    def simulate(self):
        condition = self.number_of_instance > self.number_of_instance_created
        if condition:
            self.number_of_instance_created += 1
            self.create()
            if self.event_function:
                self.event_function(self.to_json())  # Event işlevini çağır

        return condition


if __name__ == "__main__":

    def life_cycle_item_event(data):
        print("life_sycle_item_event", data)
        pass

    def life_cycle_event(data):
        print("life-cycle-event", data)

    time_step = 1  # default simulation time step
    number_of_instance = 2  # default simulation instance
    lifetime_seconds = 5  # second

    instance = LifeCycleSimulation(
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
    )
    instance.trigger(life_cycle_event)

    while instance.simulate():
        instance.last_item.trigger_event(life_cycle_item_event)
        time.sleep(time_step)
