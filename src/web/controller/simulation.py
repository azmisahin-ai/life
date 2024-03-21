# src/web/controller/simulation.py


import time
from threading import Thread

from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.life_cycle_simulation import LifeCycleSimulation
from src.web.controller.particle_life_cycle_simulation import (
    ParticleLifeCycleSimulation,
)


class Simulation:
    """
    Simülasyon işlemlerini yöneten sınıf.

    Attributes:
        simulation_status (SimulationStatus): Simülasyonun durumu.
        simulation_type (SimulationType): Simülasyonun türü.
        simulation_time_step (float): Simülasyon adım süresi.
        is_running (bool): Simülasyonun çalışıp çalışmadığını belirten bayrak.
        is_paused (bool): Simülasyonun duraklatılıp duraklatılmadığını belirten bayrak.
        instance (LifeCycleSimulation or ParticleLifeCycleSimulation): Simülasyon örneği.

    Methods:
        to_json(): Simülasyon durumunu JSON formatında döndürür.
        switch_simulation(simulation_type, number_of_instance, lifetime_seconds):
            Belirtilen türe göre uygun simülasyon örneğini döndürür.
        _simulation_loop(): Simülasyon döngüsünü başlatır ve çalıştırır.
        start(simulation_time_step, simulation_type, number_of_instance, lifetime_seconds):
            Simülasyonu başlatır.
        stop(): Simülasyonu durdurur.
        pause(): Simülasyonu duraklatır.
        continues(): Duraklatılan simülasyonu devam ettirir.
        status(): Simülasyon durumunu döndürür.
    """

    def __init__(self):
        self.simulation_status = SimulationStatus.stopped
        self.simulation_type = SimulationType.LifeCycle  # default life cycle type
        self.simulation_time_step = 1  # default life cycle time step
        self.is_running = False
        self.is_paused = False
        self.instance = None

    def to_json(self):
        """
        Simülasyon durumunu JSON formatında döndürür.

        Returns:
            str: JSON formatındaki simülasyon durumu.
        """
        simulation_data = {
            "simulation_status": self.simulation_status.value,
            "simulation_type": self.simulation_type.value,  # Enum'u string olarak dönüştürün
            "simulation_time_step": self.simulation_time_step,
        }
        return simulation_data

    def switch_simulation(self, simulation_type, number_of_instance, lifetime_seconds):
        """
        Belirtilen türe göre uygun simülasyon örneğini döndürür.

        Args:
            simulation_type (SimulationType): Simülasyon türü.
            number_of_instance (int): Oluşturulacak simülasyon örneklerinin sayısı.
            lifetime_seconds (float): Simülasyon örneklerinin yaşam süresi saniye cinsinden.

        Returns:
            LifeCycleSimulation or ParticleLifeCycleSimulation: Uygun simülasyon örneği.
        """
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
        """
        Simülasyon döngüsünü başlatır ve çalıştırır.
        """
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
        """
        Simülasyonu başlatır.

        Args:
            simulation_time_step (float): Simülasyon adım süresi.
            simulation_type (SimulationType): Simülasyon türü.
            number_of_instance (int): Oluşturulacak simülasyon örneklerinin sayısı.
            lifetime_seconds (float): Simülasyon örneklerinin yaşam süresi saniye cinsinden.

        Returns:
            Simulation: Oluşturulan simülasyon örneği.
        """
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
        """
        Simülasyonu durdurur.

        Returns:
            Simulation: Güncellenmiş simülasyon örneği.
        """
        self.is_running = False
        self.is_paused = False
        self.simulation_status = SimulationStatus.stopped
        return self

    def pause(self):
        """
        Simülasyonu duraklatır.

        Returns:
            Simulation: Güncellenmiş simülasyon örneği.
        """
        self.is_paused = True
        self.simulation_status = SimulationStatus.paused
        return self

    def continues(self):
        """
        Duraklatılan simülasyonu devam ettirir.

        Returns:
            Simulation: Güncellenmiş simülasyon örneği.
        """
        self.is_paused = False
        self.simulation_status = SimulationStatus.continues
        return self

    def status(self):
        """
        Simülasyon durumunu döndürür.

        Returns:
            SimulationStatus: Simülasyon durumu.
        """
        return self


simulation = Simulation()

if __name__ == "__main__":
    #
    simulation_time_step = 1  # default simulation time step
    simulation_type = SimulationType.LifeCycle
    number_of_instance = 2  # default simulation instance
    lifetime_seconds = 2  # second or float("inf")

    started = simulation.start(
        simulation_time_step=simulation_time_step,
        simulation_type=simulation_type,
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
    )

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"  # Renkleri sıfırlamak için kullanılır

    def simulation_event_item(data):
        print(f"{GREEN}simulation_event_item{RESET}", data)

    def simulation_event(data):
        print(f"{YELLOW}simulation_event{RESET}", data)

    if started.instance:
        started.instance.trigger(simulation_event)
        started.instance.last_item.trigger_event(simulation_event_item)
