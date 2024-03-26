# src/web/controller/simulation.py

import logging
import os
import time

import colorlog
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType
from src.web.controller.core_simulation import CoreSimulation
from src.web.controller.particle_simulation import ParticleSimulation

DATA_FOLDER = ""


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
        self.sampler = None

        # Log ayarlarını yapılandırma
        self.logger = logging.getLogger("Simulation.__Life__")
        self._configure_logging()

    def _configure_logging(self):
        log_file_path = f"{DATA_FOLDER}logs/Simulation.log"

        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(
            logging.INFO
        )  # Konsola sadece INFO ve üstü seviyelerde mesaj gönderelim

        formatter = colorlog.ColoredFormatter(
            "%(asctime)s\t%(log_color)s%(name)s\t%(levelname)s\t%(reset)s%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
        file_formatter = logging.Formatter(
            "%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s"
        )

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)

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

    def status(self):
        message = "{}\t{}\t{}\t{}".format(  # noqa: F524
            self.simulation_status.value,
            "Simulation",
            self.simulation_type,
            self.number_of_instance,
        )
        if self.simulation_status == SimulationStatus.paused:
            self.logger.warning(message)
        elif self.simulation_status == SimulationStatus.continues:
            self.logger.info(message)
        elif self.simulation_status == SimulationStatus.stopped:
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
        self.simulation_status = SimulationStatus.started
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
        self.simulation_status = SimulationStatus.paused
        # trigger
        if self.simulation_event_function:
            self.simulation_event_function(self)
        # proccess
        self.sampler.pause_simulation()

        return self

    def continues(self):
        # state
        self.simulation_status = SimulationStatus.continues
        # trigger
        if self.simulation_event_function:
            self.simulation_event_function(self)
        # proccess
        self.sampler.resume_simulation()

        return self

    def stop(self):
        # state
        self.simulation_status = SimulationStatus.stopped
        # trigger
        if self.simulation_event_function:
            self.simulation_event_function(self)
        # proccess
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


simulation = Simulation()


def simulation_signal(simulation):
    simulation.status()


def sampler_signal(sampler):
    sampler.status()


def instance_signal(instance):
    instance.status()


simulation.trigger_simulation(simulation_signal).trigger_sampler(
    sampler_signal
).trigger_instance(instance_signal)

if __name__ == "__main__":
    lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 60  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 3  # oluşturulacak örnek sayısı
    simulation_type = SimulationType.Particles  # Simulaston türü

    simulation.start(
        number_of_instance=number_of_instance,
        lifetime_seconds=lifetime_seconds,
        lifecycle=lifecycle,
        simulation_type=simulation_type,
    )

    time.sleep(2)
    simulation.pause()

    time.sleep(2)
    simulation.continues()

    time.sleep(2)
    simulation.stop()
