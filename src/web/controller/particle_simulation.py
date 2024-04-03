# src/web/controller/particle_simulation.py

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
        #
        max_replicas: int = 2,
        max_generation: int = 2,
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
            #
            max_replicas=max_replicas,
            max_generation=max_generation,
        )

    def force_function(self, t):
        return Vector(t**0.1, t**0.1, t**0.1)

    def create_instance(
        self,
        name,
        lifetime_seconds: float,
        lifecycle: float,
        #
        parent_id: int,
        max_replicas: int,
        max_generation: int,
    ) -> Particle:
        """
        Yeni bir çekirdek örneği oluşturur ve döndürür.

        :param name: Çekirdek örneği adı.
        :param lifetime_seconds: Örnek yaşam süresi (saniye cinsinden).
        :param lifecycle: Örnek yaşam döngüsü (saniyedeki adım sayısı).
        :param parent_id: örneklenen üst id ( default 0).
        :return: Oluşturulan çekirdek örneği.
        """
        instance = Particle(
            name=name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            #
            parent_id=parent_id,
            max_replicas=max_replicas,
            max_generation=max_generation,
            #
            charge=-1.6e-19,
            mass=9.1e-31,
            spin=1 / 2,
            energy=0,
            position=Vector(0, 0, 0),
            velocity=Vector(0, 0, 0),
            momentum=Vector(0, 0, 0),
            wave_function=self.force_function(0.1),
        )
        return instance


# Example Usage
if __name__ == "__main__":
    name = "particle"  # Parçacığın adı.
    lifetime_seconds = 1  # float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 60  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 2  # oluşturulacak örnek sayısı
    #
    number_of_instance_created = 0  # oluşturulan örnek sayısı
    instances = []  # örnek havuzu
    #
    number_of_replicas = 2  # oluşturulacak kopya sayısı
    number_of_generation = 2  # jenerasyon derinliği

    def simulation_sampler_status(sampler):
        state = sampler.status()
        if state == "Running":
            pass

        if state == "Paused":
            pass

        if state == "Resumed":
            pass

        if state == "Stopped":
            pass

    def simulation_instance_status(instance):
        state = instance.status()
        if state == "Created":
            pass

        if state == "Running":
            pass

        if state == "Paused":
            pass

        if state == "Resumed":
            pass

        if state == "Stopped":
            pass

    sampler = (
        CoreSimulation(
            name=name,
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            #
            max_replicas=number_of_replicas,
            max_generation=number_of_generation,
        )
        .trigger_event(simulation_sampler_status)
        .trigger_event_instance(simulation_instance_status)
    )

    # örnekleyiciyi başlat
    sampler.start_simulation()

    # # örnekleyiciyi duraklat
    # sampler.pause_simulation()

    # # örnekleyiciyi devam ettir
    # sampler.resume_simulation()

    # # örnekleyiciyi durdur
    # sampler.stop_simulation()
