# src/web/controller/particle_simulation.py

import time

from src.life.particles.vector import Vector
from src.life.particles.particle import Particle
from src.web.controller.core_simulation import CoreSimulation


class ParticleSimulation(CoreSimulation):
    """
    Parçacıkların yaşam döngüsü simülasyonunu yöneten sınıf.
    """

    def __init__(
        self,
        name: str,
        number_of_instance: int,
        lifetime_seconds: float,
        lifecycle: float,
    ) -> None:
        """
        Particle simulasyonunu oluştur.

        :param name: Simulasyon adı.
        :param number_of_instance: Oluşturulacak örnek sayısı
        :param lifetime_seconds: Örneklerin yaşam süresi saniye cinsinden.
        :param lifecycle: Örneklerin saniyedeki yaşam döngüsü.
        """
        super().__init__(
            name=name,
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
        )

    def force_function(self, t):
        return Vector(t**0.1, t**0.1, t**0.1)

    def create_instance(
        self, name, lifetime_seconds: float, lifecycle: float
    ) -> Particle:
        self.number_of_instance_created += 1
        instance_name = f"{name}_{self.number_of_instance_created}"

        return Particle(
            name=instance_name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            #
            charge=-1.6e-19,
            mass=9.1e-31,
            spin=1 / 2,
            energy=0,
            position=Vector(0, 0, 0),
            velocity=Vector(0, 0, 0),
            momentum=Vector(0, 0, 0),
            wave_function=self.force_function(0.1),
        ).trigger_event(self.instance_signal)


# Example Usage
if __name__ == "__main__":
    name = "Particle"  # Parçacığın adı.
    lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 70  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 3  # oluşturulacak örnek sayısı

    def simulation_signal(simulation):
        simulation.status()

    def instance_signal(instance):
        instance.status()

    simulation = (
        CoreSimulation(
            name=name,
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
        )
        .trigger_event(simulation_signal)
        .trigger_event_instance(instance_signal)
    )

    # Simülasyonu başlat
    simulation.start_simulation()

    # Simülasyonu duraklat
    time.sleep(2)
    simulation.pause_simulation()

    # Simülasyonu devam ettir
    time.sleep(2)
    simulation.resume_simulation()

    # Simülasyonu durdur
    time.sleep(2)
    simulation.stop_simulation()
