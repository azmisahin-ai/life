# src/life/particles/life_cycle_manager.py
import asyncio
import threading
import time


class Life(threading.Thread):
    """
    Life sınıfı, parçacıkların yaşam döngüsünü yönetir.
    """

    def __init__(self, name, lifetime_seconds, lifecycle_rate_per_minute=70):
        super().__init__()
        """
        Life Oluşturulur.

        :param name: Parçacığın adı.
        :param lifetime_seconds: Parçacığın yaşam süresi saniye cinsinden.
        """
        if name is None:
            raise ValueError("Name cannot be None.")
        if lifetime_seconds <= 0:
            raise ValueError("Lifetime seconds must be a positive value.")
        self.lifetime_seconds = lifetime_seconds
        self.name = name
        # created information
        self.life_created_time = time.time()  # Just information
        self.life_start_time = None  # Henüz başlamadı
        # cycle information
        self.elapsed_lifespan = 0
        self.lifecycle_rate_per_minute = lifecycle_rate_per_minute
        self.lifecycle = 60.0 / self.lifecycle_rate_per_minute
        # events
        self.event_function = None
        self.event_trigger = threading.Event()
        self._paused = False
        self._stop_event = threading.Event()
        # Created durumunu tetikle
        self.trigger_event(self)

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
            "lifecycle_rate_per_minute": self.lifecycle_rate_per_minute,
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
        self.event_function(self)  # Durumu güncelle

    def resume(self):
        """
        Duraklatılan örneği devam ettirir ve durumu günceller.
        """
        self._paused = False
        self.event_function(self)  # Durumu güncelle

    def stop(self):
        """
        Örneği durdurur ve durumu günceller.
        """
        self._stop_event.set()
        self.event_function(self)  # Durumu güncelle

    def status(self):
        """
        Örneğin mevcut durumunu döndürür.
        """
        if not self._stop_event.is_set():
            if self._paused:
                return "Paused"
            else:
                return "Running"
        else:
            return "Stopped"


# Example Usage
if __name__ == "__main__":
    simulation_time_step = 1
    number_of_instance = 2
    lifetime_seconds = float("inf")
    instance_prefix = "Particle"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    SOFT = "\033[98m"
    RESET = "\033[0m"

    def instance_signal(data):
        if not hasattr(data, "created_printed"):
            print(
                f"{WHITE}instance_signal{RESET} ",
                f"{PURPLE}Created{RESET}",
                f"{CYAN}{data.name}{RESET}",
                f"{SOFT}{data.elapsed_lifespan}{RESET}",
            )
            data.created_printed = True  # Created durumu yazıldı
        else:
            status = data.status()
            if status == "Running":
                status_color = GREEN
            elif status == "Paused":
                status_color = YELLOW
            elif status == "Stopped":
                status_color = RED
            else:
                status_color = PURPLE  # Created durumu
                status = "Created"
            print(
                f"{WHITE}instance_signal{RESET} ",
                f"{status_color}{status}{RESET}",
                f"{CYAN}{data.name}{RESET}",
                f"{SOFT}{data.elapsed_lifespan}{RESET}",
            )

    instance_created_counter = 0

    async def create_instance(name, lifetime_seconds):
        global instance_created_counter
        instance_created_counter += 1
        instance = Life(
            name=f"{name}_{instance_created_counter}", lifetime_seconds=lifetime_seconds
        )
        instance.trigger_event(instance_signal)
        instance.start()
        return instance

    async def main():
        # Örnek yönetimi
        instances = await asyncio.gather(
            *[
                create_instance(instance_prefix, lifetime_seconds=2)
                for _ in range(number_of_instance)
            ]
        )
        # Tüm işlemleri burada kontrol edebilirsiniz
        await asyncio.sleep(2)  #
        # örnekleri duraklatma
        for instance in instances:
            if instance.name == f"{instance_prefix}_1":
                instance.pause()

        await asyncio.sleep(5)  #
        # öernekleri devam ettirme
        for instance in instances:
            if instance.name == f"{instance_prefix}_1":
                instance.resume()

        await asyncio.sleep(10)  #
        # Thread'leri durdurma
        for instance in instances:
            instance.stop()
            instance.join()

    asyncio.run(main())
