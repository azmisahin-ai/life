# src/web/controller/core_simulation.py

import logging
import os

import colorlog
from src.life.particles.core import Core

DATA_FOLDER = ""


class CoreSimulation:
    """
    Parçacıkların yaşam döngüsü simülasyonunu yöneten sınıf.

    """

    def __init__(
        self, name: str, number_of_instance, lifetime_seconds: float, lifecycle: float
    ) -> None:
        """
        Çekirdek simulasyonunu oluştur.

        :param name: Simulasyon adı.
        :param number_of_instance: Oluşturulacak örnek sayısı
        :param lifetime_seconds: Örneklerin yaşam süresi saniye cinsinden.
        :param lifecycle: Örneklerin saniyedeki yaşam döngüsü.
        """
        self.name = name
        self.number_of_instance = number_of_instance
        self.lifetime_seconds = lifetime_seconds
        self.lifecycle = lifecycle
        #
        self.number_of_instance_created = 0
        self.instances = []
        # events
        self.event_function = None
        self.event_function_instance = None
        # Log ayarlarını yapılandırma
        self.logger = logging.getLogger(name)
        self._configure_logging()

    def _configure_logging(self):
        log_file_path = f"{DATA_FOLDER}logs/{self.name}.log"

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

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "number_of_instance": self.number_of_instance,
            "lifetime_seconds": self.lifetime_seconds,
            "lifecycle": self.lifecycle,
            "number_of_instance_created": self.number_of_instance_created,
        }

    def instance_signal(self, instance):
        if self.event_function_instance:
            self.event_function_instance(instance)  # Event işlevini çağır

    def create_instance(self, name, lifetime_seconds: float, lifecycle: float) -> Core:
        self.number_of_instance_created += 1
        instance_name = f"{name}_{self.number_of_instance_created}"

        return (
            Core(
                name=instance_name,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
            .trigger_event(self.instance_signal)
            .start()
        )

    def run_simulation(self):
        try:
            condition = self.number_of_instance > self.number_of_instance_created
            if condition:
                instance = self.create_instance(
                    name=self.name,
                    lifetime_seconds=lifetime_seconds,
                    lifecycle=self.lifecycle,
                )
                self.instances.append(instance)
                if self.event_function:
                    self.event_function(self)  # Event işlevini çağır
            return condition
        except Exception as e:
            print(f"CoreSimulation Error: {e}")

    def trigger_event(self, event_function):
        """
        Bir olay işlevini tetiklemek için kullanılır.
        Simulasyonun örneğini tetikler

        :param event_function: Tetiklenen olayın işlevi.
        """
        self.event_function = event_function
        return self

    def trigger_event_instance(self, event_function):
        """
        Bir olay işlevini tetiklemek için kullanılır.
        Oluşturulan örneğin olayını tetikler

        :param event_function: Tetiklenen olayın işlevi.
        """
        self.event_function_instance = event_function
        return self

    def status(self):
        """
        Örneğin mevcut durumunu döndürür.
        """
        state = "?"

        message = f"\
            {state}\
            {self.lifetime_seconds}\
            {self.lifecycle}\
            {self.number_of_instance}\
            {self.number_of_instance_created}\
            "

        self.logger.info(message)

        return state


if __name__ == "__main__":
    name = "Cycle"  # Parçacığın adı.
    lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 70  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 3  # oluşturulacak örnek sayısı

    def simulation_signal(simulation):
        simulation.status()
        pass

    def instance_signal(instance):
        instance.status()
        pass

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

    while simulation.run_simulation():
        pass
