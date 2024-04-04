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
        max_replicas: int = 2,
        max_generation: int = 2,
    ) -> None:
        """
        Life Oluşturulur.

        :param name: Parçacığın adı.
        :param lifetime_seconds: Parçacığın yaşam süresi saniye cinsinden.
        :param lifecycle: Parçacığın saniyedeki yaşam döngüsü.
        :param parent_uid: Üst çekirdek kimliği (varsayılan olarak 0).
        :param max_replicas: Maksimum kopya sayısı
        :param max_generation: Maksimum jenerasyon sayısı

        """
        super().__init__()
        Core.core_count += 1
        self.uid = str(uuid.uuid4())  # Benzersiz kimlik
        self.id = Core.core_count  # Otomatik artan benzersiz kimlik
        self.parent_id = parent_id if parent_id else 0  # Üst çekirdek kimliği
        self.max_replicas = max_replicas  # Maksimum kopya sayısı
        self.number_of_copies = 0
        self.max_generation = max_generation  # Maksimum jenerasyon sayısı
        self.generation = (
            Core.generation_map[parent_id] + 1 if parent_id else 1
        )  # Generation değeri
        Core.generation_map[self.id] = self.generation  # Generation değerini eşleştir
        self.match_count = 0  # eşleşme toplamı
        #
        self.replicas = []  # kopyaları tutulacağı alan
        self.codes = (
            bytearray()
        )  # Bytearray'i saklamak için boş bir bytearray oluşturulur
        self.fitness = 0.0  # Yaşam süresi ve evrim hızı
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

        self.formula = None  # Kullanıcı tarafından girilecek formül

    def apply_formula(self, formula: str) -> float:
        """
        Kullanıcının girdiği formülü güvenli bir şekilde değerlendirir ve yaşam süresini günceller.
        """
        # Güvenli bir şekilde formülü değerlendirme
        try:
            # Kullanıcı tarafından girilen formülü belirli bir kapsamda değerlendirir
            evaluated_formula = eval(formula, {"self": self})
        except Exception as e:
            print("Hata:", e)
            return

        # Hesaplanan formülü yaşam süresine uygula
        self.lifetime_seconds = evaluated_formula
        return evaluated_formula

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
            "parent_id": self.parent_id,
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
            "number_of_copies": self.number_of_copies,
            "generation": self.generation,
            "match_count": self.match_count,
            "fitness": self.fitness,
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

    def test(self):
        """
        Oluşturulan kodların belirli bir formata uyup uymadığını kontrol eder.
        Başarılı bir test durumunda kodun byte değeri kadar yaşam süresini artırır.
        """
        if not self.codes:
            return  # Eğer kod yoksa işlem yapma

        # Başlangıçta başarılı test sayısını ve kod uzunluğunu sıfıra ayarlayın
        successful_tests = 0
        code_length = len(self.codes)

        # Kodun formata uygunluğunu
        for byte in self.codes:
            if 0xB8 <= byte <= 0xBF:
                # MOV: 0xB8 ile 0xBF arasındaki opcode'lar
                successful_tests += 1
            elif 0xE9 <= byte <= 0xEB:
                # JMP: 0xE9 ile 0xEB arasındaki opcode'lar
                successful_tests += 1
            elif 0x00 <= byte <= 0x03:
                # ADD: 0x00 ile 0x03 arasındaki opcode'lar
                successful_tests += 1
            elif 0x28 <= byte <= 0x2F:
                # SUB: 0x28 ile 0x2F arasındaki opcode'lar
                successful_tests += 1
            elif 0x90 <= byte <= 0x97:
                # NOP: 0x90 ile 0x97 arasındaki opcode'lar
                successful_tests += 1
            elif 0xC3 <= byte <= 0xC5:
                # RET: 0xC3 ile 0xC5 arasındaki opcode'lar
                successful_tests += 1
            elif 0xE8 <= byte <= 0xEB:
                # CALL: 0xE8 ile 0xEB arasındaki opcode'lar
                successful_tests += 1
            elif 0xC7 <= byte <= 0xCF:
                # CMP: 0xC7 ile 0xCF arasındaki opcode'lar
                successful_tests += 1
            elif 0xD0 <= byte <= 0xD7:
                # ROL: 0xD0 ile 0xD7 arasındaki opcode'lar
                successful_tests += 1
            elif 0xD8 <= byte <= 0xDF:
                # RCX: 0xD8 ile 0xDF arasındaki opcode'lar
                successful_tests += 1
            elif 0x50 <= byte <= 0x57:
                # PUSH: 0x50 ile 0x57 arasındaki opcode'lar
                successful_tests += 1
            elif 0x58 <= byte <= 0x5F:
                # POP: 0x58 ile 0x5F arasındaki opcode'lar
                successful_tests += 1
            elif 0x83 <= byte <= 0x87:
                # ADD: 0x83 ile 0x87 arasındaki opcode'lar
                successful_tests += 1
            elif 0x81 <= byte <= 0x82:
                # CMP: 0x81 ile 0x82 arasındaki opcode'lar
                successful_tests += 1
            elif 0x8B <= byte <= 0x8F:
                # MOV: 0x8B ile 0x8F arasındaki opcode'lar
                successful_tests += 1
            elif 0xE0 <= byte <= 0xE3:
                # LOOP: 0xE0 ile 0xE3 arasındaki opcode'lar
                successful_tests += 1
            elif 0xE4 <= byte <= 0xE7:
                # IN: 0xE4 ile 0xE7 arasındaki opcode'lar
                successful_tests += 1
            elif 0xEE <= byte <= 0xEF:
                # OUT: 0xEE ile 0xEF arasındaki opcode'lar
                successful_tests += 1
            elif 0x74 <= byte <= 0x75:
                # JZ/JNZ: 0x74 ile 0x75 arasındaki opcode'lar
                successful_tests += 1
            elif 0x72 <= byte <= 0x73:
                # JC/JNC: 0x72 ile 0x73 arasındaki opcode'lar
                successful_tests += 1
            elif 0x7E <= byte <= 0x7F:
                # JLE/JG: 0x7E ile 0x7F arasındaki opcode'lar
                successful_tests += 1

        # Başarılı testlerin oranını hesapla
        success_ratio = successful_tests / code_length

        # Yaşam süresini tek seferde artırma veya azaltma
        if success_ratio >= 0.5:
            increase_amount = sum(byte / 1000 for byte in self.codes)
            self.increase_lifespan(
                seconds=increase_amount
            )  # Başarılı test durumunda yaşam süresini artır
            message = "{:.7s}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                "test-✅",
                self.elapsed_lifespan,
                self.lifetime_seconds,
                self.parent_id,
                self.generation,
                self.id,
                success_ratio,
            )
        else:
            decrease_amount = sum(byte / 1000 for byte in self.codes)
            self.decrease_lifespan(
                seconds=decrease_amount
            )  # Başarısız test durumunda yaşam süresini azalt
            message = "{:.7s}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                "test-✖️",
                self.elapsed_lifespan,
                self.lifetime_seconds,
                self.parent_id,
                self.generation,
                self.id,
                success_ratio,
            )

        self.logger.warning(message)

    # Fitness fonksiyonu: Yaşam süresi ve evrim hızı
    def calculate_fitness(self):
        if self.lifetime_seconds == float("inf"):
            self.mutation_rate = len(self.codes) / self.elapsed_lifespan

            # Genel fitness değeri: Evrim hızı
            self.fitness = self.mutation_rate

        else:
            self.lifetime_fitness = self.lifetime_seconds / self.elapsed_lifespan
            self.mutation_rate = len(self.codes) / self.elapsed_lifespan

            # Genel fitness değeri: Yaşam süresi ve evrim hızının bir kombinasyonu
            self.fitness = (self.lifetime_fitness + self.mutation_rate) / 2

        return self.fitness

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
                # Kendini Kodlarını test
                self.test()
                # Yaşam süresi ve evrim hızı
                self.calculate_fitness()
                # Durum bilgisini güncelle
                self.update_state()
                # Bilgilerini sinyal olarak gönderir
                if self.event_function:
                    self.event_function(self)
                # Yeni  kopyalar oluştur
                # self.replicate()

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

        return state

    def update_state(self):
        state = self.status()
        message = "{:.7s}\t{}\t{}\t{}\t{}\t{}\t{}".format(
            state,
            self.elapsed_lifespan,
            self.lifetime_seconds,
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
        Eşlenme işlemi gerçekleştiğinde çağrılır ve yeni nesneyi oluşturulmasını sağlar.
        """

        if (
            self.generation >= self.max_generation
            or self.number_of_copies >= self.max_replicas
            or self.lifetime_seconds < 0
        ):
            # Maksimum jenerasyon sayısına ulaşıldıysa veya max_replicas değeri 0 ise, eşleme yapmayı durdur
            return None

        # Yeni bir nesneyi oluştur
        new_item = Core(
            name=self.name,
            lifetime_seconds=self.lifetime_seconds,
            lifecycle=self.lifecycle,
            parent_id=self.id,  # Yeni çekirdeğin üst çekirdek kimliği, mevcut çekirdeğin kimliği olacak
            max_generation=self.max_generation,
            max_replicas=self.max_replicas,
        ).trigger_event(self.event_function)
        # Yeni nesnenin kodlarını kopyala
        new_item.codes = self.codes[:]
        # Yeni programcığın nesnesini başlat
        new_item.start()
        # Nesne oluşturma bilgisini güncelle
        self.logger.info(f"Replicated [{new_item.id}]")
        # kopya sayısına göre  zamanı (milisaniye ) belirle
        seconds = self.number_of_copies / 1000
        # Eşlenme işlemi gerçekleştirdikten sonra zamanı azalt
        self.decrease_lifespan(seconds=seconds)

        self.number_of_copies += 1

        # kopyaları sakla
        self.replicas.append(new_item)

        # replicasyon sinyali
        if self.event_function:
            self.event_function(self)

        return self

    def decrease_lifespan(self, seconds):
        """
        Yaşam süresini azalt
        """
        self.lifetime_seconds -= seconds

    def increase_lifespan(self, seconds):
        """
        Yaşam süresini arttır
        """

        self.lifetime_seconds += seconds


# Example Usage
if __name__ == "__main__":
    name = "core"  # Parçacığın adı.
    lifetime_seconds = 1  # float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 60  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 2  # oluşturulacak örnek sayısı
    #
    number_of_instance_created = 0  # oluşturulan örnek sayısı
    instances = []  # örnek havuzu
    #
    number_of_replicas = 2  # oluşturulacak kopya sayısı
    number_of_generation = 2  # jenerasyon derinliği
    #
    user_formula = "5.5 * self.generation"

    def simulation_instance_status(instance):
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

    def create_instance(name, lifetime_seconds, lifecycle):
        global number_of_instance_created
        number_of_instance_created += 1

        return Core(
            name=name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            #
            parent_id=0,
            max_replicas=number_of_replicas,
            max_generation=number_of_generation,
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

        # Formülü Core sınıfına uygula
        instance.apply_formula(user_formula)
        # Parçacığın yaşam süresini yazdır
        print("Updated Lifetime Seconds:", instance.lifetime_seconds)

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
