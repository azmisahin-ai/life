# src/web/controller/life_cycle_simulation.py

import threading
import time
from src.life.particles.life_cycle_manager import LifeCycleManager


class LifeCycleSimulation:
    """
    Parçacıkların yaşam döngüsü simülasyonunu yöneten sınıf.

    Args:
        number_of_instance (int): Oluşturulacak parçacık örneklerinin sayısı.
        lifetime_seconds (float): Parçacık örneklerinin yaşam süresi saniye cinsinden.

    Attributes:
        number_of_instance (int): Oluşturulacak parçacık örneklerinin sayısı.
        lifetime_seconds (float): Parçacık örneklerinin yaşam süresi saniye cinsinden.
        number_of_instance_created (int): Şu ana kadar oluşturulan parçacık örneklerinin sayısı.
        last_item (LifeCycleManager): Son oluşturulan parçacık örneği.
        event_function (function): Olay işlevi.
        event_trigger (threading.Event): Olay tetikleyici.
    """

    def __init__(self, number_of_instance, lifetime_seconds):
        self.number_of_instance = number_of_instance
        self.lifetime_seconds = lifetime_seconds
        self.number_of_instance_created = 0
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

    def create_instance(self):
        name = f"item-{self.number_of_instance_created}"
        self.last_item = LifeCycleManager(name, lifetime_seconds=self.lifetime_seconds)
        self.number_of_instance_created += 1

    def run_simulation(self):
        try:
            condition = self.number_of_instance > self.number_of_instance_created
            if condition:
                self.create_instance()
                if self.event_function:
                    self.event_function(self.to_json())  # Event işlevini çağır
            return condition
        except Exception as e:
            print(f"LifeCycleSimulation Error: {e}")


if __name__ == "__main__":

    def life_cycle_item_event(data):
        print("life_cycle_item_event", data)

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

    while instance.run_simulation():
        instance.last_item.trigger_event(life_cycle_item_event)
        time.sleep(time_step)
