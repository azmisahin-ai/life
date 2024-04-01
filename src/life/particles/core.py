# src/life/particles/core.py
import random
import threading
import time

from src.package import Logger


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
        self.generation = 1
        self.codes = (
            bytearray()
        )  # Bytearray'i saklamak için boş bir bytearray oluşturulur

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
        self.logger = Logger(
            name=f"/core/{name}", log_to_file=True, log_to_console=True
        ).get_logger()
        # Created durumunu tetikle
        self.trigger_event(self)

    def to_json(self):
        """
        Nesneyi JSON formatına dönüştürür.

        :return: JSON formatında nesne.
        """
        lifetime_seconds = (
            "infinity"
            if self.lifetime_seconds == float("inf")
            else self.lifetime_seconds
        )
        return {
            "name": self.name,
            "lifetime_seconds": lifetime_seconds,
            # created information
            "life_created_time": self.life_created_time,
            "life_start_time": self.life_start_time,
            # cycle information
            "elapsed_lifespan": self.elapsed_lifespan,
            "lifecycle": self.lifecycle,
            # status information
            "life_status": self.status(),
            "codes": list(self.codes),
            "generation": self.generation,
        }

    def trigger_event(self, event_function):
        """
        Bir olay işlevini tetiklemek için kullanılır.

        :param event_function: Tetiklenen olayın işlevi.
        """
        self.event_function = event_function
        return self

    def evolve(self):
        """
        Her seferinde 1 byte'lık rasgele bir ASCII karakter ekler.
        """
        self.code = bytes([random.randint(0, 255)])  # Rasgele bir byte oluştur
        # sys.maxsize
        self.codes.extend(self.code)  # Oluşturulan byte'ı self.code bytearray'ına ekler

    # Fitness fonksiyonu: Yaşam süresi ve evrim hızı
    def calculate_fitness(self):
        if self.lifetime_seconds == float("inf"):
            self.mutation_rate = len(self.codes) / self.elapsed_lifespan

            # Genel fitness değeri: Evrim hızı
            self.general_fitness = self.mutation_rate

        else:
            self.lifetime_fitness = self.lifetime_seconds / self.elapsed_lifespan
            self.mutation_rate = len(self.codes) / self.elapsed_lifespan

            # Genel fitness değeri: Yaşam süresi ve evrim hızının bir kombinasyonu
            self.general_fitness = (self.lifetime_fitness + self.mutation_rate) / 2

        return self.general_fitness

    def measure(self):
        """
        Belirli bir özelliğini ölçer ve sonucu döndürür.

        """
        # Çekirdek kodu
        return list(self.codes)

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
                # Zamana bağlı evrim
                self.evolve()
                if self.event_function:
                    self.event_function(self)
                time.sleep(self.lifecycle)
        # Yaşam döngüsü sona erdi
        self._stop_event.set()  # stopped
        if self.event_function:
            self.event_function(self)

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

        message = "{:.7s}\t{}\t{}".format(
            state,
            self.elapsed_lifespan,
            "".join(format(byte, "02x") for byte in self.codes),
        )
        if state == "Created":
            self.logger.info(message)
        elif state == "Running":
            self.logger.info(message)
        elif state == "Paused" or state == "Resumed":
            self.logger.warning(message)
        elif state == "Stopped":
            self.logger.warning(message)
        else:
            self.logger.debug(message)
        return state


# Example Usage
if __name__ == "__main__":
    name = "core"  # Parçacığın adı.
    lifetime_seconds = 1  # float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 100  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 20  # oluşturulacak örnek sayısı

    number_of_instance_created = 0  # oluşturulan örnek sayısı

    instances = []  # örnek havuzu

    fitness_values = {}  # Fitness değerlerini

    new_cores = []  # Her iterasyonda oluşturulan yeni core için boş bir liste oluşturulur

    def simulation_instance_status(instance):
        state = instance.status()
        if state == "Running":
            fitness_values[instance] = instance.calculate_fitness()

        if state == "Stopped":
            # Fitness değerlerine göre parçacıkları sıralama
            sorted_instances = sorted(
                instances, key=lambda x: fitness_values.get(x, 0), reverse=True
            )
            # En iyi olanları seç
            for index, instance in enumerate(sorted_instances[:3]):
                best_fitness = fitness_values.get(
                    instance,
                    0,  # "Fitness değeri bulunamadı"
                )
                # general_fitness = instance.general_fitness
                # mutation_rate = instance.mutation_rate
                # yeiden başlatılıyor

                if instance.status() == "Stopped":
                    print(f"{instance.name} [{instance.generation}]", best_fitness)
                    instance._stop_event = threading.Event()
                    instance.lifetime_seconds += 1
                    instance.generation += 1
                    instance.run()

    def create_instance(name, lifetime_seconds, lifecycle):
        global number_of_instance_created
        number_of_instance_created += 1
        instance_name = f"{name}_{number_of_instance_created}"

        return (
            Core(
                name=instance_name,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
            )
            .trigger_event(simulation_instance_status)
            .start()
        )

    # Örnek yönetimi
    for _ in range(number_of_instance):
        instance = create_instance(
            name=name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
        )
        instances.append(instance)

    # # örnekleri duraklatma
    # for instance in instances:
    #     if instance.name == f"{name}_1":
    #         instance.pause()

    # # öernekleri devam ettirme
    # for instance in instances:
    #     if instance.name == f"{name}_1":
    #         instance.resume()

    # # Thread'leri durdurma
    # for instance in instances:
    #     instance.stop()
    #     instance.join()
