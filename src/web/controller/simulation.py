# src/web/controller/simulation.py


import time
from threading import Thread

from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.core_simulation import CoreSimulation
from src.web.controller.particle_simulation import ParticleSimulation


class Simulation:
    """
    Simülasyon işlemlerini yöneten sınıf.
    """

    def __init__(self) -> None:
        """
        Particle simulasyonunu oluştur.
        """
        # state
        self.simulation_status = SimulationStatus.stopped
        self.is_running = False
        self.is_paused = False
        self.sampler = None

    def to_json(self):
        """
        Simülasyon durumunu JSON formatında döndürür.

        Returns:
            str: JSON formatındaki simülasyon durumu.
        """
        simulation_data = {
            "simulation_type": self.simulation_type.value,
            "simulation_status": self.simulation_status.value,
        }
        return simulation_data

    def switch_simulation(
        self, number_of_instance, lifetime_seconds, lifecycle, simulation_type
    ):
        """
        Belirtilen türe göre uygun simülasyon örneğini döndürür.
        """
        if simulation_type == SimulationType.Core:
            return CoreSimulation(
                name="Simulation.Core",
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
        elif simulation_type == SimulationType.Particles:
            return ParticleSimulation(
                name="Simulation.Particles",
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
        else:
            return None

    def _run_simulation_loop(self):
        """
        Simülasyon döngüsünü başlatır ve çalıştırır.
        """
        self.simulation_status = SimulationStatus.started
        while self.is_running:
            if not self.is_paused and self.sampler:
                if isinstance(self.sampler, CoreSimulation):
                    if not self.sampler.start_simulation():
                        self.stop()
                if isinstance(self.sampler, ParticleSimulation):
                    if not self.sampler.start_simulation():
                        self.stop()
            time.sleep(self.lifecycle)
        self.simulation_status = SimulationStatus.stopped

    def setup(
        self,
        number_of_instance: int,
        lifetime_seconds: float,
        lifecycle: float,
        simulation_type: SimulationType,
    ):
        """
        Simülasyonu başlatır.

        :param number_of_instance: Oluşturulacak örnek sayısı
        :param lifetime_seconds: Örneklerin yaşam süresi saniye cinsinden.
        :param lifecycle: Örneklerin saniyedeki yaşam döngüsü.
        :param simulation_type: Simulasyonun türü
        """
        self.number_of_instance = number_of_instance
        self.lifetime_seconds = lifetime_seconds
        self.lifecycle = lifecycle
        self.simulation_type = simulation_type

        # Geçersiz girişleri kontrol et
        if not isinstance(simulation_type, SimulationType):
            raise ValueError("Invalid simulation type")
        if lifetime_seconds < 0:
            raise ValueError("Lifetime seconds cannot be negative")

        # swich simulation
        self.sampler = self.switch_simulation(
            number_of_instance=self.number_of_instance,
            lifetime_seconds=self.lifetime_seconds,
            lifecycle=self.lifecycle,
            simulation_type=self.simulation_type,
        )

        return self

    def start(self):
        # state
        self.is_running = True
        self.is_paused = False
        Thread(target=self._run_simulation_loop).start()
        self.simulation_status = SimulationStatus.started

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
    lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 70  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 3  # oluşturulacak örnek sayısı
    simulation_type = SimulationType.Particles  # Simulaston türü

    def simulation_signal(simulation):
        simulation.status()

    def instance_signal(instance):
        instance.status()

    simulation.setup(
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
        lifecycle=lifecycle,
        simulation_type=simulation_type,
    ).sampler.trigger_event(simulation_signal).trigger_event_instance(instance_signal)
    simulation.start()
