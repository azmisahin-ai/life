# src/web/controller/simulation.py
import json
import time
from threading import Thread

from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.life_cycle_simulation import LifeCycleSimulation
from src.web.controller.particle_life_cycle_simulation import (
    ParticleLifeCycleSimulation,
)


class Simulation:
    def __init__(self):
        self.simulation_status = SimulationStatus.stopped
        self.simulation_type = SimulationType.LifeCycle  # default life cycle type
        self.simulation_time_step = 1  # default life cycle time step
        self.is_running = False
        self.is_paused = False
        self.instance = None

    def to_json(self):
        simulation_data = {
            "simulation_status": self.simulation_status.value,
            "simulation_type": self.simulation_type.value,  # Enum'u string olarak dönüştürün
            "simulation_time_step": self.simulation_time_step,
        }
        return json.dumps(simulation_data)

    def switch_simulation(self, simulation_type, number_of_instance, lifetime_seconds):
        if simulation_type == SimulationType.LifeCycle:
            return LifeCycleSimulation(
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
            )
        elif simulation_type == SimulationType.Particles:
            return ParticleLifeCycleSimulation(
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
            )
        else:
            return None

    def _simulation_loop(self):
        self.simulation_status = SimulationStatus.started
        while self.is_running:
            if not self.is_paused and self.instance:
                if isinstance(self.instance, LifeCycleSimulation):
                    if not self.instance.run_simulation():
                        self.stop()
                if isinstance(self.instance, ParticleLifeCycleSimulation):
                    if not self.instance.run_simulation():
                        self.stop()
            time.sleep(self.simulation_time_step)

    def start(
        self,
        simulation_time_step,
        simulation_type,
        number_of_instance,
        lifetime_seconds,
    ):
        self.is_running = True
        self.is_paused = False
        self.simulation_time_step = simulation_time_step
        self.simulation_type = simulation_type
        self.instance = self.switch_simulation(
            self.simulation_type, number_of_instance, lifetime_seconds
        )
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
    simulation_time_step = 1  # default simulation time step
    simulation_type = SimulationType.LifeCycle
    number_of_instance = 2  # default simulation instance
    lifetime_seconds = 5  # second or float("inf")

    started = simulation.start(
        simulation_time_step=simulation_time_step,
        simulation_type=simulation_type,
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
    )

    def simulation_event(data):
        print("simulation_event", data)

    if started.instance:
        started.instance.trigger(simulation_event)
