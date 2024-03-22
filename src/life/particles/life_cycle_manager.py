# src/life/particles/life_cycle_manager.py
import threading
import time
import json


class LifeCycleManager:
    """
    LifeCycleManager sınıfı, parçacıkların yaşam döngüsünü yönetir.
    """

    def __init__(self, name, lifetime_seconds):
        """
        Yöneticiyi başlatır.

        :param name: Parçacığın adı.
        :param lifetime_seconds: Parçacığın yaşam süresi saniye cinsinden.
        """
        self.life_start_time = time.time()
        self.elapsed_lifespan = 0
        self.lifecycle_rate_per_minute = 70
        self.lifecycle = 60.0 / self.lifecycle_rate_per_minute
        self.lifetime_seconds = lifetime_seconds
        self.name = name
        self.event_function = None
        self.event_trigger = threading.Event()
        threading.Thread(target=self._lifetime).start()

    def trigger_event(self, event_function):
        """
        Bir olay işlevini tetiklemek için kullanılır.

        :param event_function: Tetiklenen olayın işlevi.
        """
        self.event_function = event_function

    def _lifetime(self):
        """
        Parçacığın yaşam döngüsünü işler.
        """
        current_time = self.life_start_time
        while time.time() - current_time < self.lifetime_seconds:
            self.elapsed_lifespan = time.time() - self.life_start_time
            if self.event_function:
                self.event_function(self)
            time.sleep(self.lifecycle)

    def to_json(self):
        """
        Nesneyi JSON formatına dönüştürür.

        :return: JSON formatında nesne.
        """
        return json.dumps(
            {
                "name": self.name,
                "life_start_time": self.life_start_time,
                "elapsed_lifespan": self.elapsed_lifespan,
                "lifecycle_rate_per_minute": self.lifecycle_rate_per_minute,
                "lifecycle": self.lifecycle,
                "lifetime_seconds": self.lifetime_seconds,
            }
        )


if __name__ == "__main__":
    #
    simulation_time_step = 1  # default simulation time step
    # simulation_type = SimulationType.LifeCycle
    number_of_instance = 2  # default simulation instance
    lifetime_seconds = 2  # second or float("inf")

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"  # Renkleri sıfırlamak için kullanılır

    def simulation_event_item(data):
        print(f"{GREEN}simulation_event_item{RESET}", data)

    def simulation_event(data):
        print(f"{YELLOW}simulation_event_inst{RESET}", data)

    # Test kodu
    instance = LifeCycleManager(name="Particle", lifetime_seconds=lifetime_seconds)
    instance.trigger_event(simulation_event_item)
