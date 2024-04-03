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
        self.instances = []  # örnek havuzu
        self.fitness_values = {}  # Fitness değerlerini
        # events
        self.event_function = None
        self.event_function_instance = None
        self._stop_event = threading.Event()
        self._paused = False
        self._resumed = False
        self._exit_flag = False
        self.perform_crossover_start = False  # perform_crossover_start özelliği eklendi
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
            if (
                not self.perform_crossover_start
                and self.number_of_instance_created == self.number_of_instance
            ):
                self.perform_crossover_start = True
                self.perform_crossover()

        if self.event_function_instance:
            self.event_function_instance(instance)  # Event işlevini çağır

    def create_instance(
        self,
        name,
        lifetime_seconds,
        lifecycle,
        parent_id: int = 0,
        parent_id_2: int = None,
    ):
        """
        Yeni bir çekirdek örneği oluşturur ve döndürür.

        :param name: Çekirdek örneği adı.
        :param lifetime_seconds: Örnek yaşam süresi (saniye cinsinden).
        :param lifecycle: Örnek yaşam döngüsü (saniyedeki adım sayısı).
        :param parent_id: örneklenen üst id ( default 0).
        :param parent_id_2: crossover id ( default None).
        :return: Oluşturulan çekirdek örneği.
        """
        instance = Core(
            name=name,
            lifetime_seconds=lifetime_seconds,
            lifecycle=lifecycle,
            parent_id=parent_id,
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
                    parent_id=0,
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

        # print("compatible_cores", len(compatible_cores))

        compatible_cores.sort(
            key=lambda x: self.fitness_values[x.id], reverse=True
        )  # Fitness değerlerine göre sırala

        # Çift sayısını hesapla
        number_of_pairs = len(compatible_cores) // 2

        # print("number_of_pairs", number_of_pairs)

        # Çiftlerden yeni core'lar oluşturun
        for i in range(number_of_pairs):
            parent1 = compatible_cores[i * 2]
            parent2 = compatible_cores[i * 2 + 1]

            message = "{:.7s}\t{}/{}\t{}\t{}".format(
                "crossover",
                self.number_of_instance_created,
                self.number_of_instance,
                parent1.id,
                parent2.id,
            )
            self.logger.info(message)

            # Yeni core oluştur ve ekleyin
            new_core = self.create_instance(
                name=self.name,
                lifetime_seconds=self.lifetime_seconds,
                lifecycle=self.lifecycle,
                parent_id=parent1.id,
                parent_id_2=parent2.id,
            )

            # Olay dinleyici tetiği yapılandır
            new_core.trigger_event(self.instance_status)

            # Yeni core'ları instances listesine ekleyin
            self.instances.append(new_core)
            new_core.start()


# Example Usage
if __name__ == "__main__":
    name = "core"  # Parçacığın adı.
    lifetime_seconds = 1  # float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 60  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 2  # oluşturulacak örnek sayısı

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
