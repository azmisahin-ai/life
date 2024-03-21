# src/web/controller/simulation.py
import json
import time
from threading import Thread

from src.web.controller.life_cycle_status import LifeCycleStatus
from src.web.controller.life_cycle_type import LifeCycleType
from src.web.controller.life_cycle_simulation import LifeCycleSimulation
from src.web.controller.particle_life_cycle_simulation import (
    ParticleLifeCycleSimulation,
)


class Simulation:
    def __init__(self):
        self.life_cycle_status = LifeCycleStatus.stopped
        self.life_cycle_type = LifeCycleType.LifeCycle  # default life cycle type
        self.life_cycle_time_step = 1  # ? default life cycle time step
        #
        self.is_running = False
        self.is_paused = False

    def to_json(self):
        instance_json = json.loads(self.instance.to_json())
        simulation_data = {
            "life_cycle_status": self.life_cycle_status.value,
            "life_cycle_type": self.life_cycle_type.value,  # Enum'u string olarak dönüştürün
            "life_cycle_time_step": self.time_step,
        }
        instance_json.update(simulation_data)  # Düzeltildi
        return json.dumps(instance_json)

    def swich_simulation(self, life_cycle_type, number_of_instance, lifetime_seconds):
        if life_cycle_type == LifeCycleType.LifeCycle:
            return LifeCycleSimulation(
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
            )
        elif life_cycle_type == LifeCycleType.Particles:
            return ParticleLifeCycleSimulation(
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
            )
        else:
            return None

    def _simulation_loop(self):
        self.life_cycle_status = LifeCycleStatus.started
        while self.is_running:
            if not self.is_paused:
                # self.life_cycle_status = LifeCycleStatus.continues
                if isinstance(self.instance, LifeCycleSimulation):
                    self.instance.run_simulation()
                if isinstance(self.instance, ParticleLifeCycleSimulation):
                    self.instance.run_simulation()
            time.sleep(self.life_cycle_time_step)

    def start(
        self,
        life_cycle_time_step,
        life_cycle_type,
        number_of_instance,
        lifetime_seconds,
    ):
        self.is_running = True
        self.is_paused = False
        #
        self.life_cycle_time_step = life_cycle_time_step
        self.life_cycle_type = life_cycle_type  # also transfer instance
        # self.number_of_instance = number_of_instance  # transfer instance
        # self.lifetime_seconds = lifetime_seconds  # transfer instance

        self.instance = self.swich_simulation(
            self.life_cycle_type, number_of_instance, lifetime_seconds
        )

        # self.life_cycle_type = LifeCycleStatus.started # this will be set when the thread is started
        Thread(target=self._simulation_loop).start()

        return self

    def stop(self):
        self.is_running = False
        self.is_paused = False
        self.simulation_status = LifeCycleStatus.stopped
        return self

    def pause(self):
        self.is_paused = True
        self.simulation_status = LifeCycleStatus.paused
        return self

    def continues(self):
        self.is_paused = False
        self.simulation_status = LifeCycleStatus.continues
        return self

    def status(self):
        return self


simulation = Simulation()

if __name__ == "__main__":
    life_cycle_time_step = 1  # default life cycle time step 0.1
    life_cycle_type = LifeCycleType.LifeCycle
    number_of_instance = 2  # default simulation instance
    lifetime_seconds = 5  # second or float("inf")

    started = simulation.start(
        life_cycle_time_step=life_cycle_time_step,
        life_cycle_type=life_cycle_type,
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
    )

    def life_cycle_event(data):
        print("life_cycle_event", data)

    started.instance.trigger(life_cycle_event)

    # def life_cycle_item_event(data):
    #     print("life_cycle_item_event", data)

    # started.instance.last_item.trigger_event(life_cycle_item_event)
