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
    #
    simulation_time_step = 1  # default simulation time step
    # simulation_type = SimulationType.LifeCycle
    number_of_instance = 2  # default simulation instance
    lifetime_seconds = 2  # second or float("inf")

    instance = ParticleLifeCycleSimulation(
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

    while instance.run_simulation():
        if instance:
            instance.trigger(simulation_event)
            instance.last_item.trigger_event(simulation_event_item)

        time.sleep(simulation_time_step)
