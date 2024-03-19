# web/controller/simulation.py

from .simulation_result import SimulationResult, Particle, Vector


class Simulation:
    def __init__(self) -> None:
        pass

    def start(self, number_of_particles, time_step):
        # Simülasyon başlatma işlemleri
        return SimulationResult(
            status="started",
            number_of_particles=number_of_particles,
            time_step=time_step,
            particle=None,  # Başlangıçta parçacık bilgisi yok
        )

    def stop(self):
        # Simülasyon durdurma işlemleri
        return SimulationResult(
            status="stopped",
            number_of_particles=1,
            time_step=0.1,
            particle=None,  # Simülasyon durduğunda parçacık bilgisi yok
        )

    def pause(self):
        # Simülasyon duraklatma işlemleri
        return SimulationResult(
            status="paused",
            number_of_particles=1,
            time_step=0.1,
            particle=None,  # Simülasyon durakladığında parçacık bilgisi yok
        )

    def continues(self):
        # Simülasyonun devam etme işlemleri
        return SimulationResult(
            status="continues",
            number_of_particles=1,
            time_step=0.1,
            particle=Particle(
                name="Particle",
                charge=-1.602176634e-19,
                mass=9.10938356e-31,
                spin=0.5,
                lifetime=-1,
                energy=0,
                position=Vector(x=0, y=0, z=0),
                velocity=Vector(x=0, y=0, z=0),
                momentum=Vector(x=0, y=0, z=0),
            ),
        )

    def status(self):
        # Simülasyon durumunu döndür
        return self.continues()  # Şu an simülasyon devam ediyor kabul edelim
