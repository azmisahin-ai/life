# web/controller/simulation.py

from .simulation_result import SimulationResult, Particle, Vector


def createParticle():
    return Particle(
        name="Particle",
        charge=-1.602176634e-19,
        mass=9.10938356e-31,
        spin=0.5,
        lifetime=-1,
        energy=0,
        position=Vector(x=0, y=0, z=0),
        velocity=Vector(x=0, y=0, z=0),
        momentum=Vector(x=0, y=0, z=0),
    )


class Simulation:
    def __init__(self) -> None:
        self.simulationResult = SimulationResult(
            status="starting", number_of_particles=0, time_step=0, particle=None
        )

    def start(self, number_of_particles, time_step):
        # Simülasyon başlatma işlemleri
        self.simulationResult.number_of_particles = number_of_particles
        self.simulationResult.time_step = time_step
        self.simulationResult.status = "started"
        self.simulationResult.particle = createParticle()

        return self.simulationResult

    def stop(self):
        # Simülasyon durdurma işlemleri
        self.simulationResult.status = "stopped"

        return self.simulationResult

    def pause(self):
        # Simülasyon duraklatma işlemler
        self.simulationResult.status = "paused"

        return self.simulationResult

    def continues(self):
        # Simülasyonun devam etme işlemleri
        self.simulationResult.status = "continues"

        return self.simulationResult

    def status(self):
        # Simülasyon durumunu döndür
        return self.continues()  # Şu an simülasyon devam ediyor kabul edelim


# Single instance
simulation = Simulation()
