# src/web/controller/core_simulation.py

import threading
from src.package import Logger
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
        #
        max_replicas: int = 2,
        max_generation: int = 2,
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
        self.max_replicas = max_replicas
        self.max_generation = max_generation
        #
        self.number_of_instance_created = 0
        self.instances = []  # örnek havuzu
        self.fitness_values = {}  # Fitness değerlerini
        # events
        self.event_function = None
        self.event_function_instance = None
        self._stop_event = threading.Event()
        self._paused = False
        self._resumed = False
        self._exit_flag = False
        # self.perform_crossover_start = False  # perform_crossover_start özelliği eklendi
        # Log ayarlarını yapılandırma
        self.logger = Logger(
            name=f"/sampler/{name}", log_to_file=True, log_to_console=True
        ).get_logger()

    def to_json(self) -> dict:
        lifetime_seconds = (
            "infinity"
            if self.lifetime_seconds == float("inf")
            else self.lifetime_seconds
        )
        return {
            "name": self.name,
            "number_of_instance": self.number_of_instance,
            "lifetime_seconds": lifetime_seconds,
            "lifecycle": self.lifecycle,
            "number_of_instance_created": self.number_of_instance_created,
        }

    def instance_status(self, instance):
        state = instance.status()
        if state == "Created":
            self.instances.append(instance)

        if state == "Running":
            self.fitness_values[instance.id] = instance.fitness

        if state == "Paused":
            pass

        if state == "Resumed":
            pass

        if state == "Stopped":
            # Çaprazlama işlemi daha önce yapılmadıysa ve tüm çekirdekler oluşturulduysa
            if self.number_of_instance_created == self.number_of_instance:
                self.perform_crossover()

        if self.event_function_instance:
            self.event_function_instance(instance)  # Event işlevini çağır

    def create_instance(
        self,
        name: str,
        lifetime_seconds: float,
        lifecycle: float,
        #
        parent_id: int,
        max_replicas: int,
        max_generation: int,
    ) -> Core:
        """
        Yeni bir çekirdek örneği oluşturur ve döndürür.

        :param name: Çekirdek örneği adı.
        :param lifetime_seconds: Örnek yaşam süresi (saniye cinsinden).
        :param lifecycle: Örnek yaşam döngüsü (saniyedeki adım sayısı).
        :param parent_id: örneklenen üst id ( default 0).
        :return: Oluşturulan çekirdek örneği.
        """
        instance = Core(
            name=name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            #
            parent_id=parent_id,
            max_replicas=max_replicas,
            max_generation=max_generation,
        )
        return instance

    def run_simulation(self):
        try:
            condition = self.number_of_instance > self.number_of_instance_created

            # Oluşturulmaya devam edilecek mi?
            if condition:
                instance = self.create_instance(
                    name=self.name,  # name değişkenini self.name olarak güncelliyorum
                    lifetime_seconds=self.lifetime_seconds,
                    lifecycle=self.lifecycle,
                    #
                    parent_id=0,
                    max_replicas=self.max_replicas,
                    max_generation=self.max_generation,
                )
                # olay dinleyici tetiği yapılandır
                instance.trigger_event(self.instance_status)
                # nesneyi havuza ekle
                self.instances.append(instance)
                # nesneyi başlat
                instance.start()
                # oluşturuldu bilgisini arttır
                self.number_of_instance_created += 1

                if self.event_function:
                    self.event_function(self)  # Event işlevini çağır

            return condition

        except TypeError as e:
            self.logger.error(f"Sampler Simulation Error Type : {e}")
        except Exception as e:
            self.logger.error(f"Sampler Simulation Error      : {e}")

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
        if self.event_function:
            self.event_function(self)  # Event işlevini çağır
        self.status()
        for instance in self.instances:
            instance.pause()

    def resume_simulation(self):
        """
        Duraklatılan simülasyonu devam ettirir.
        """
        self._paused = False
        self._resumed = True
        if self.event_function:
            self.event_function(self)  # Event işlevini çağır
        self.status()
        for instance in self.instances:
            instance.resume()

    def stop_simulation(self):
        """
        Simülasyonu durdurur.
        """
        self._paused = False
        self._stop_event.set()  # _stop_event'i ayarlayın
        if self.event_function:
            self.event_function(self)  # Event işlevini çağır
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

        message = "{:.7s}\t{}/{}".format(
            state,
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

    def perform_crossover(self):
        # Uyumlu core çiftlerini seçin
        compatible_cores = [
            core for core in self.instances if core.id in self.fitness_values.keys()
        ]

        compatible_cores.sort(
            key=lambda x: self.fitness_values[x.id], reverse=True
        )  # Fitness değerlerine göre sırala

        # Çift sayısını hesapla
        number_of_pairs = len(compatible_cores) // 2

        # Eşleştirilmiş çekirdek kimliklerini izleyin
        paired_core_ids = []

        # Çiftlerden yeni core'lar oluşturun
        for i in range(number_of_pairs):
            # türler
            female = compatible_cores[i * 2]
            male = compatible_cores[i * 2 + 1]

            # Çekirdeklerden herhangi birinin zaten eşleştirilmiş olup olmadığını kontrol edin
            if female.id in paired_core_ids or male.id in paired_core_ids:
                # Çekirdeklerden herhangi biri daha önce eşleştirilmişse eşleştirmeyi atlayın
                continue

            # Eşleştirilmiş çekirdek kimliklerini listeye ekleyin
            paired_core_ids.extend([female.id, male.id])

            # eşlenme sayaçlarını arttır
            female.match_count += 1
            male.match_count += 1

            # cinsiyet tanımlaması yapılabilir?
            # female.sex="f"
            # male.sex="m"

            # Eşlenmiş nesneden yeni nesne oluşturulmasını sağlar
            # new_core = female.replicate()
            _ = female.replicate()
            # replicate sırasında otomatik tetiklenir ve başlatılır.

            # logger
            message = "{:.7s}\t{}/{}\t{}\t{}\t{}".format(
                "crossover",
                self.number_of_instance_created,
                self.number_of_instance,
                female.id,
                male.id,
                female.match_count,
            )
            self.logger.info(message)

            # Yeni core'ları instances listesine ekleyin
            # mevcut listele eklemek hataya düşürüyor
            # self.instances.append(new_core)


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

    def simulation_sampler_status(sampler):
        state = sampler.status()
        if state == "Running":
            pass

        if state == "Paused":
            pass

        if state == "Resumed":
            pass

        if state == "Stopped":
            pass

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

    sampler = (
        CoreSimulation(
            name=name,
            number_of_instance=number_of_instance,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            #
            max_replicas=number_of_replicas,
            max_generation=number_of_generation,
        )
        .trigger_event(simulation_sampler_status)
        .trigger_event_instance(simulation_instance_status)
    )

    # # örnekleyiciyi başlat
    sampler.start_simulation()

    # # örnekleyiciyi duraklat
    # sampler.pause_simulation()

    # # örnekleyiciyi devam ettir
    # sampler.resume_simulation()

    # # örnekleyiciyi durdur
    # sampler.stop_simulation()
