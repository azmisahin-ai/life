import threading
import time


class Base:
    def __init__(self, name, lifetime):
        self.life_start_time = time.time()
        self.elapsed_lifespan = 0
        self.lifecycle_rate_per_minute = 70
        self.lifecycle = 60.0 / self.lifecycle_rate_per_minute
        self.lifetime_seconds = lifetime  # float("inf")  # lifetime
        self.name = name
        self.event_function = None  # Event işlevi
        self.event_trigger = threading.Event()  # Olay tetikleyici oluştur
        threading.Thread(target=self._lifetime).start()

    def trigger(self, event_function):
        self.event_function = event_function  # Event işlevini ata

    def _lifetime(self):
        current_time = self.life_start_time
        while time.time() - current_time < self.lifetime_seconds:
            self.elapsed_lifespan = time.time() - self.life_start_time
            if self.event_function:
                self.event_function(self.to_json())  # Event işlevini çağır
            time.sleep(self.lifecycle)

    def to_json(self):
        return {
            "name": self.name,
            "life_start_time": self.life_start_time,
            "elapsed_lifespan": self.elapsed_lifespan,
            "lifecycle_rate_per_minute": self.lifecycle_rate_per_minute,
            "lifecycle": self.lifecycle,
            "lifetime_seconds": self.lifetime_seconds,
        }


if __name__ == "__main__":

    def eventFunction(data):
        print("event-base", data)

    instance = Base(name="Particle", lifetime=10)
    instance.trigger(eventFunction)
