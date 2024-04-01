# src/web/controller/simulation.py


from src.package.logger import Logger, logger
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.core_simulation import CoreSimulation
from src.web.controller.particle_simulation import ParticleSimulation

from src.life.particles.core import Core
from src.life.particles.particle import Particle


class Simulation:
    """
    Simülasyon işlemlerini yöneten sınıf.
    """

    def __init__(self, name: str) -> None:
        """
        Particle simulasyonunu oluştur.
        """
        self.name = name
        # state
        self.simulation_status = SimulationStatus.Stopped
        self.sampler = None
        # Log ayarlarını yapılandırma
        self.logger = Logger(
            name=f"/simulation/{name}", log_to_file=True, log_to_console=True
        ).get_logger()

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
                name=f"{self.name}.core",
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
        elif simulation_type == SimulationType.Particles:
            return ParticleSimulation(
                name=f"{self.name}.particles",
                number_of_instance=number_of_instance,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
        else:
            return None

    def status(self):
        message = "{:.7s}\t{}".format(
            self.simulation_status.value, self.simulation_type
        )
        if self.simulation_status == SimulationStatus.Paused:
            self.logger.warning(message)
        elif self.simulation_status == SimulationStatus.Resumed:
            self.logger.info(message)
        elif self.simulation_status == SimulationStatus.Stopped:
            self.logger.warning(message)
        else:
            self.logger.info(message)

        return self.simulation_status

    def start(
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

        # state
        self.simulation_status = SimulationStatus.Running
        # trigger
        if self.simulation_event_function:
            self.simulation_event_function(self)
        # proccess
        self.sampler.trigger_event(self.sampler_event_function).trigger_event_instance(
            self.instance_event_function
        )
        self.sampler.start_simulation()

        return self

    def pause(self):
        # state
        self.simulation_status = SimulationStatus.Paused
        # trigger
        if self.simulation_event_function:
            self.simulation_event_function(self)
        # proccess
        self.sampler.pause_simulation()

        return self

    def resume(self):
        # state
        self.simulation_status = SimulationStatus.Resumed
        # trigger
        if self.simulation_event_function:
            self.simulation_event_function(self)
        # proccess
        self.sampler.resume_simulation()

        return self

    def stop(self):
        # state
        self.simulation_status = SimulationStatus.Stopped
        # trigger
        if self.simulation_event_function:
            self.simulation_event_function(self)
        # process
        if self.sampler:
            self.sampler.stop_simulation()
        return self

    def trigger_simulation(self, event_function):
        self.simulation_event_function = event_function
        return self

    def trigger_sampler(self, event_function):
        self.sampler_event_function = event_function
        return self

    def trigger_instance(self, event_function):
        self.instance_event_function = event_function
        return self


# create simulation
simulation = Simulation("life")


def simulation_status(simulation):
    try:
        if isinstance(simulation, Simulation):
            state = simulation.status()
            if state == SimulationStatus.Running:
                pass

            if state == SimulationStatus.Paused:
                pass

            if state == SimulationStatus.Resumed:
                pass

            if state == SimulationStatus.Stopped:
                pass
        else:
            raise RuntimeWarning("A new unknown simulation")
    except Exception as e:
        logger.exception("An error occurred: %s", e)


def simulation_sampler_status(sampler):
    try:
        if isinstance(sampler, ParticleSimulation):
            state = sampler.status()
            if state == "Running":
                pass

            if state == "Paused":
                pass

            if state == "Resumed":
                pass

            if state == "Stopped":
                pass
        elif isinstance(sampler, CoreSimulation):
            state = sampler.status()
            if state == "Running":
                pass

            if state == "Paused":
                pass

            if state == "Resumed":
                pass

            if state == "Stopped":
                pass
        else:
            raise RuntimeWarning("A new unknown sampler")
    except Exception as e:
        logger.exception("An error occurred: %s", e)


def simulation_instance_status(instance):
    try:
        if isinstance(instance, Particle):
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
        elif isinstance(instance, Core):
            state = instance.status()
            if state == "Running":
                pass

            if state == "Paused":
                pass

            if state == "Resumed":
                pass

            if state == "Stopped":
                pass
        else:
            raise RuntimeWarning("A new unknown instance")
    except Exception as e:
        logger.exception("An error occurred: %s", e)


# setup simulation
simulation.trigger_simulation(simulation_status).trigger_sampler(
    simulation_sampler_status
).trigger_instance(simulation_instance_status)

# Example usage
if __name__ == "__main__":
    lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 1  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 3  # oluşturulacak örnek sayısı
    simulation_type = SimulationType.Particles  # Simulaston türü

    # start simulation
    simulation.start(
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
        lifecycle=lifecycle,
        simulation_type=simulation_type,
    )
    simulation.pause()
    simulation.resume()
    simulation.stop()
