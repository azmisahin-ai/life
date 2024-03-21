# src/web/controller/particle_life_cycle_simulation.py

import time

from src.life.particles.vector import Vector
from src.life.particles.particle import Particle
from src.web.controller.life_cycle_simulation import LifeCycleSimulation


class ParticleLifeCycleSimulation(LifeCycleSimulation):
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
        super().__init__(
            number_of_instance=number_of_instance, lifetime_seconds=lifetime_seconds
        )

    def force_function(self, t):
        return Vector(t**0.1, t**0.1, t**0.1)

    def create_instance(self):
        name = f"particle-{self.number_of_instance_created}"
        charge = -1.6e-19
        mass = 9.1e-31
        spin = 1 / 2
        lifetime_seconds = self.lifetime_seconds
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
            lifetime_seconds,
            energy,
            position,
            velocity,
            momentum,
            wave_function,
        )

        # Parçacık örneği oluşturulduktan sonra number_of_instance_created özelliğini artır
        self.number_of_instance_created += 1


if __name__ == "__main__":

    def particle_item_event(data):
        print("particle_item_event", data)

    def particle_event(data):
        print("particle-event", data)

    time_step = 1  # default simulation time step
    number_of_instance = 2  # default simulation instance
    lifetime_seconds = 5  # second

    instance = ParticleLifeCycleSimulation(
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
    )
    instance.trigger(particle_event)

    while instance.run_simulation():
        instance.last_item.trigger_event(particle_item_event)
        time.sleep(time_step)
