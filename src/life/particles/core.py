# src/life/particles/core.py

import logging
import os
import threading
import time
import colorlog

DATA_FOLDER = ""


class Core(threading.Thread):
    """
    Life sınıfı, parçacıkların yaşam döngüsünü yönetir.
    """

    def __init__(self, name: str, lifetime_seconds: float, lifecycle: float) -> None:
        """
        Life Oluşturulur.

        :param name: Parçacığın adı.
        :param lifetime_seconds: Parçacığın yaşam süresi saniye cinsinden.
        :param lifecycle: Parçacığın saniyedeki yaşam döngüsü.
        """
        super().__init__()

        if name is None:
            raise ValueError("Name cannot be None.")
        if lifetime_seconds <= 0:
            raise ValueError("Lifetime seconds must be a positive value.")
        if lifecycle <= 0:
            raise ValueError("Lifecycle must be a positive value.")
        self.lifetime_seconds = lifetime_seconds
        self.name = name
        # created information
        self.life_created_time = time.time()  # Just information
        self.life_start_time = None  # Henüz başlamadı
        # cycle information
        self.elapsed_lifespan = 0
        self.lifecycle = lifecycle
        # events
        self.event_function = None
        # self.event_trigger = threading.Event()
        self._paused = False
        self._stop_event = threading.Event()
        self._resumed = False
        # Log ayarlarını yapılandırma
        self.logger = logging.getLogger(name)
        self._configure_logging()
        # Created durumunu tetikle
        self.trigger_event(self)

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

    def to_json(self):
        """
        Nesneyi JSON formatına dönüştürür.

        :return: JSON formatında nesne.
        """
        return {
            "name": self.name,
            "lifetime_seconds": self.lifetime_seconds,
            # created information
            "life_created_time": self.life_created_time,
            "life_start_time": self.life_start_time,
            # cycle information
            "elapsed_lifespan": self.elapsed_lifespan,
            "lifecycle": self.lifecycle,
            # status information
            "life_status": self.status(),
        }

    def trigger_event(self, event_function):
        """
        Bir olay işlevini tetiklemek için kullanılır.

        :param event_function: Tetiklenen olayın işlevi.
        """
        self.event_function = event_function
        return self

    def run(self):
        """
        Parçacığın yaşam döngüsünü işler.
        """
        self.life_start_time = time.time()
        while (
            time.time() - self.life_start_time < self.lifetime_seconds
            and not self._stop_event.is_set()
        ):
            if not self._paused:
                self.elapsed_lifespan = time.time() - self.life_start_time
                if self.event_function:
                    self.event_function(self)
                time.sleep(self.lifecycle)

    def pause(self):
        """
        Örneği duraklatır ve durumu günceller.
        """
        self._paused = True
        if self.event_function:
            self.event_function(self)  # Durumu güncelle

    def resume(self):
        """
        Duraklatılan örneği devam ettirir ve durumu günceller.
        """
        self._paused = False
        if self.event_function:
            self.event_function(self)  # Durumu güncelle
        self._resumed = True  # Resumed bayrağını ayarla

    def stop(self):
        """
        Örneği durdurur ve durumu günceller.
        """
        self._stop_event.set()
        if self.event_function:
            self.event_function(self)  # Durumu güncelle

    def start(self):
        super().start()
        return self

    def status(self):
        """
        Örneğin mevcut durumunu döndürür.
        """
        state = "Unknown"
        if not hasattr(self, "created_printed"):
            state = "Created"
            self.created_printed = True  # Created durumu yazıldı
        else:
            if self._stop_event.is_set():
                state = "Stopped"
            elif self._paused:
                state = "Paused"
            elif self._resumed:
                self._resumed = False
                state = "Resumed"
            else:
                state = "Running"

        message = f"\
            {state}\
            {self.lifetime_seconds}\
            {self.lifecycle}\
            {self.elapsed_lifespan}\
            {self.life_created_time}\
            {self.life_start_time}"

        if state == "Created":
            self.logger.info(message)
        elif state == "Running":
            self.logger.info(message)
        elif state == "Paused" or state == "Resumed":
            self.logger.warning(message)
        elif state == "Stopped":
            self.logger.critical(message)
        else:
            self.logger.debug(message)
        return state


# Example Usage
if __name__ == "__main__":
    name = "Cycle"  # Parçacığın adı.
    lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 70  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 3  # oluşturulacak örnek sayısı

    instance_created_counter = 0

    def create_instance(name, lifetime_seconds, lifecycle):
        def instance_signal(instance):
            instance.status()

        global instance_created_counter
        instance_created_counter += 1
        instance_name = f"{name}_{instance_created_counter}"

        return (
            Core(
                name=instance_name,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
            .trigger_event(instance_signal)
            .start()
        )

    instances = []

    def main():
        # Örnek yönetimi
        for _ in range(number_of_instance):
            instance = create_instance(
                name=name,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
            instances.append(instance)

        # Tüm işlemleri burada kontrol edebilirsiniz
        time.sleep(2)  #
        # örnekleri duraklatma
        for instance in instances:
            if instance.name == f"{name}_1":
                instance.pause()

        time.sleep(2)  #
        # öernekleri devam ettirme
        for instance in instances:
            if instance.name == f"{name}_1":
                instance.resume()

        time.sleep(2)  #
        # Thread'leri durdurma
        for instance in instances:
            instance.stop()
            instance.join()

    main()
