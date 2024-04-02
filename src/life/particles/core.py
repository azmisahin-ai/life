# src/life/particles/core.py
import random
import threading
import time
import uuid

from src.package import Logger


class Core(threading.Thread):
    """
    Life sınıfı, parçacıkların yaşam döngüsünü yönetir.
    """

    core_count = 0  # Toplam çekirdek sayısı
    generation_map = {}  # Çekirdek ID'sini generation değeriyle eşleştiren sözlük

    def __init__(
        self,
        name: str,
        lifetime_seconds: float,
        lifecycle: float,
        parent_id: int = 0,
        max_generation: int = 3,
        max_replicas: int = 4,
    ) -> None:
        """
        Life Oluşturulur.

        :param name: Parçacığın adı.
        :param lifetime_seconds: Parçacığın yaşam süresi saniye cinsinden.
        :param lifecycle: Parçacığın saniyedeki yaşam döngüsü.
        :param parent_uid: Üst çekirdek kimliği (varsayılan olarak 0).
        :param max_generation: Maksimum jenerasyon sayısı
        :param max_replicas: Maksimum kopya sayısı
        """
        super().__init__()
        Core.core_count += 1
        self.uid = str(uuid.uuid4())  # Benzersiz kimlik
        self.id = Core.core_count  # Otomatik artan benzersiz kimlik
        self.parent_id = parent_id if parent_id else 0  # Üst çekirdek kimliği
        self.max_generation = max_generation  # Maksimum jenerasyon sayısı
        self.max_replicas = max_replicas  # Maksimum kopya sayısı

        self.generation = (
            Core.generation_map[parent_id] + 1 if parent_id else 1
        )  # Generation değeri
        Core.generation_map[self.id] = self.generation  # Generation değerini eşleştir

        #
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
        # yeni version
        self.version = f"v_{self.parent_id}_{self.generation}_{self.id}"
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
            name=f"/{self.name}/{self.version}", log_to_file=True, log_to_console=True
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
            "id": self.id,
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
            # süre sonunda  otomatik durdurmayı tetikler
            time.time() - self.life_start_time < self.lifetime_seconds
            and not self._stop_event.is_set()
        ):
            # eğer paused konumunda ise işlem devam ettirilmez
            if not self._paused:
                # zaman yönetimi için duraklatma önce yapılmalı.
                time.sleep(self.lifecycle)
                # geçen süreyi hesaplar
                self.elapsed_lifespan = time.time() - self.life_start_time
                # Çekirdeğin evrimsel kodlarını işletir
                self.evolve()
                # dış fonksiyonlara sinyal gönderir
                if self.event_function:
                    self.event_function(self)
                # yeni programcıkları oluştur
                self.replicate()

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

        message = "{:.7s}\t{}\t{}\t{}\t{}\t{}".format(
            state,
            self.elapsed_lifespan,
            self.parent_id,
            self.generation,
            self.id,
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

    def replicate(self):
        """
        Eşlenme işlemi gerçekleştiğinde çağrılır ve yeni programcıkların oluşturulmasını sağlar.
        """
        if self.generation >= self.max_generation or self.max_replicas <= 0:
            # Maksimum jenerasyon sayısına ulaşıldıysa veya max_replicas değeri 0 ise, eşleme yapmayı durdur
            return
        # Yeni bir programcık oluştur
        new_core = Core(
            name=self.name,
            lifetime_seconds=self.lifetime_seconds,
            lifecycle=self.lifecycle,
            parent_id=self.id,  # Yeni çekirdeğin üst çekirdek kimliği, mevcut çekirdeğin kimliği olacak
            max_generation=self.max_generation,
            max_replicas=self.max_replicas,
        ).trigger_event(self.event_function)
        # Yeni programcık kodlarını kopyala
        new_core.codes = self.codes[:]
        # Yeni programcığın nesnesini başlat
        new_core.start()
        # Nesne oluşturma bilgisini güncelle
        self.logger.info(f"Replicated [{new_core.id}]")


# Example Usage
if __name__ == "__main__":
    name = "core"  # Parçacığın adı.
    lifetime_seconds = 5  # float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 60  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 1  # oluşturulacak örnek sayısı
    number_of_replicas = 3  # oluşturulacak kopya sayısı
    number_of_generation = 2  # jenerasyon derinliği
    number_of_instance_created = 0  # oluşturulan örnek sayısı
    instances = []  # örnek havuzu
    fitness_values = {}  # Fitness değerlerini
    new_cores = []  # Her iterasyonda oluşturulan yeni core için boş bir liste oluşturulur

    def simulation_instance_status(instance):
        state = instance.status()
        if state == "Created":
            pass

        if state == "Running":
            fitness_values[instance] = instance.calculate_fitness()

        if state == "Paused":
            pass

        if state == "Resumed":
            pass

        if state == "Stopped":
            pass

    def create_instance(name, lifetime_seconds, lifecycle):
        global number_of_instance_created
        number_of_instance_created += 1

        return Core(
            name=name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            # başlangıç değeri
            parent_id=0,
            max_generation=number_of_generation,
            max_replicas=number_of_replicas,
        ).trigger_event(simulation_instance_status)

    # Örnek yönetimi oluşturma ve çalıştırma
    for _ in range(number_of_instance):
        # örnek oluştur
        instance = create_instance(
            name=name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
        )
        # örneği çalıştır.
        instance.start()
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
