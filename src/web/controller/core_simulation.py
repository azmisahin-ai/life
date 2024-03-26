# src/web/controller/core_simulation.py


import threading
import time

from src.package.logger import Logger
from src.life.particles.core import Core


class CoreSimulation:
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
        self._stop_event = threading.Event()
        self._paused = False
        self._resumed = False
        self._exit_flag = False
        # Log ayarlarını yapılandırma
        self.logger = Logger(
            name=name, log_to_file=False, log_to_console=True
        ).get_logger()

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

        return Core(
            name=instance_name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
        ).trigger_event(self.instance_signal)

    def run_simulation(self):
        try:
            condition = self.number_of_instance > self.number_of_instance_created
            if condition:
                instance = self.create_instance(
                    name=self.name,
                    lifetime_seconds=self.lifetime_seconds,
                    lifecycle=self.lifecycle,
                )
                self.instances.append(instance)
                instance.start()
                if self.event_function:
                    self.event_function(self)  # Event işlevini çağır
            return condition
        except TypeError as e:
            self.logger.error(f"Core Simulation Error Type : {e}")
        except Exception as e:
            self.logger.error(f"Core Simulation Error      : {e}")

    def _run_simulation_loop(self):
        """
        Simülasyon döngüsünü çalıştırır.
        """
        while not self._paused and not self._exit_flag and self.run_simulation():
            pass

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

    def pause_simulation(self):
        """
        Simülasyonu duraklatır.
        """
        self._paused = True
        self.status()
        for instance in self.instances:
            instance.pause()

    def resume_simulation(self):
        """
        Duraklatılan simülasyonu devam ettirir.
        """
        self._paused = False
        self._resumed = True
        self.status()
        for instance in self.instances:
            instance.resume()

    def stop_simulation(self):
        """
        Simülasyonu durdurur.
        """
        self._paused = False
        self._stop_event.set()  # _stop_event'i ayarlayın
        self.status()
        for instance in self.instances:
            instance.stop()

        self._exit_flag = True  # Uygulamayı sonlandırmak için bayrağı ayarla

    def start_simulation(self):
        """
        Simülasyonu başlatır.
        """
        self._paused = False
        self.status()
        self._run_simulation_loop()

    def status(self):
        """
        Örneğin mevcut durumunu döndürür.
        """
        if self._paused:
            state = "Paused"
        elif self._stop_event.is_set():
            state = "Stopped"
        elif self._resumed:
            self._resumed = False
            state = "Resumed"
        else:
            state = "Running"

        message = "{}\t{}\t{}\t{}".format(  # noqa: F524
            state,
            self.name,
            self.number_of_instance_created,
            self.number_of_instance,
        )
        if state == "Paused":
            self.logger.warning(message)
        elif state == "Resumed":
            self.logger.info(message)
        elif state == "Stopped":
            self.logger.warning(message)
        else:
            self.logger.info(message)

        return state


# Example Usage
if __name__ == "__main__":
    name = "Cycle"  # Parçacığın adı.
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
