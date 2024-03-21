# simulation.py
import time
from threading import Thread

from flask import Flask
from flask_socketio import SocketIO


from src.web.controller.particle_life_cycle_simulation import ParticleSimulation

from web.controller.life_cycle_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.life_cycle_simulation import LifeCycleSimulation

app = Flask(__name__)
io = SocketIO(app)


class Simulation:
    def __init__(self):
        self.simulation_status = SimulationStatus.stopped
        self.is_running = False
        self.is_paused = False
        self.simulation_type = SimulationType.Base  # default simualation type

        self.time_step = 0.01  # default simulation time step
        self.number_of_instance = 1  # default simulation instance

    def to_json(self):
        return {
            "status": self.simulation_status.value,
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "simulation_type": self.simulation_type.value,  # Enum'u string olarak dönüştürün
            "simulation_time_step": self.time_step,
            "time_step": self.time_step,  # Bu satır kaldırılacak
            "number_of_particles": self.number_of_instance,  # Bu satır kaldırılacak
            "number_of_instance": self.number_of_instance,
        }

    def swich_simulation(self, simulation_type, number_of_instance, lifetime_seconds):
        if simulation_type == SimulationType.Base:
            return LifeCycleSimulation(
                number_of_instance=number_of_instance,
                lifetime=lifetime_seconds,
            )
        elif simulation_type == SimulationType.Particles:
            return ParticleSimulation(
                number_of_instance=number_of_instance,
                lifetime=lifetime_seconds,
            )
        else:
            return None

    def _simulation_loop(self):
        self.simulation_status = SimulationStatus.started
        while self.is_running:
            if not self.is_paused:
                # self.simulation_status = SimulationStatus.continues
                if isinstance(self.instance, LifeCycleSimulation):
                    self.instance.simulate()
                if isinstance(self.instance, ParticleSimulation):
                    self.instance.simulate()
            time.sleep(self.time_step)

    def start(
        self,
        number_of_instance,
        simulation_time_step,
        lifetime_seconds=5,
        simulation_type=SimulationType.Particles,
    ):
        self.is_running = True
        self.is_paused = False
        self.simulation_type = simulation_type
        self.time_step = simulation_time_step
        self.number_of_instance = number_of_instance

        self.instance = self.swich_simulation(
            simulation_type, number_of_instance, lifetime_seconds
        )

        # self.simulation_status = SimulationStatus.started # this will be set when the thread is started
        Thread(target=self._simulation_loop).start()

        return self

    def stop(self):
        self.is_running = False
        self.is_paused = False
        self.simulation_status = SimulationStatus.stopped
        return self

    def pause(self):
        self.is_paused = True
        self.simulation_status = SimulationStatus.paused
        return self

    def continues(self):
        self.is_paused = False
        self.simulation_status = SimulationStatus.continues
        return self

    def status(self):
        return self


simulation = Simulation()

if __name__ == "__main__":
    number_of_instance = 2  # default simulation instance
    time_step = 0.01  # default simulation time step
    life_time = 5  # second or float("inf")

    def simulationEvent(data):
        print("event-simulation", data)

    started = simulation.start(
        number_of_instance=number_of_instance,
        simulation_time_step=time_step,
        simulation_type=SimulationType.Particles,
        lifetime_seconds=life_time,
    )
    started.instance.trigger(simulationEvent)
