# src/life/particles/particle.py

import random
from src.life.particles.vector import Vector
from src.life.particles.core import Core


class Particle(Core):
    """
    Parçacık sınıfı, LifeCycleManager sınıfından türetilir ve parçacıkların özelliklerini ve davranışlarını tanımlar.
    """

    def __init__(
        self,
        name: str,
        lifetime_seconds: float,
        lifecycle: float,
        charge: float,
        mass: float,
        spin: float,
        energy: float,
        position: Vector = Vector(),
        velocity: Vector = Vector(),
        momentum: Vector = Vector(),
        wave_function: Vector = None,
    ) -> None:
        """
        Parçacık sınıfını başlatır.

        :param name: Parçacığın adı.
        :param lifetime_seconds: Parçacığın ömrü.
        :param lifecycle: Parçacığın saniyedeki yaşam döngüsü.

        :param charge: Parçacığın yükü.
        :param mass: Parçacığın kütlesi.
        :param spin: Parçacığın spin'i.
        :param energy: Parçacığın enerjisi.

        :param position: Parçacığın pozisyonu.
        :param velocity: Parçacığın hızı.
        :param momentum: Parçacığın momentumu.
        :param wave_function: Parçacığın dalga fonksiyonu.
        """
        super().__init__(
            name=name, lifetime_seconds=lifetime_seconds, lifecycle=lifecycle
        )
        self.charge = charge  # Parçacığın yükü
        self.mass = mass  # Parçacığın kütlesi
        self.spin = spin  # Parçacığın spin'i
        self.energy = energy  # Parçacığın enerjisi
        self.position = position  # Parçacığın pozisyonu
        self.velocity = velocity  # Parçacığın hızı
        self.momentum = momentum  # Parçacığın momentumu
        self.wave_function = wave_function or Vector(
            0, 0, 0
        )  # Parçacığın dalga fonksiyonu

    def to_json(self) -> dict:
        """
        Parçacığı JSON formatına dönüştürür.

        :return: JSON formatında parçacık verisi.
        :rtype: dict
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
            "replicas": self.replicas,
            "generation": self.generation,
            "fitness": self.fitness,
            # particle information
            "charge": self.charge,
            "mass": self.mass,
            "spin": self.spin,
            "energy": self.energy,
            # particle activation
            "position": self.position.to_json(),
            "velocity": self.velocity.to_json(),
            "momentum": self.momentum.to_json(),
            "wave_function": self.wave_function.to_json(),
        }

    # Parçacığın spin özelliklerini güncelleme
    def calculate_new_spin(self, current_spin):
        # Spin'i rastgele bir miktar değiştirerek güncelle
        return current_spin + random.uniform(-0.1, 0.1)

    # Parçacığın kütle özelliklerini güncelleme
    def calculate_new_mass(self, current_mass):
        # Kütle değişimini rastgele bir miktar artırarak güncelle
        return current_mass * random.uniform(0.9, 1.1)

    # Parçacığın yükünü güncelleme
    def calculate_new_charge(self, current_charge):
        # Yük değişimini rastgele bir miktar artırarak güncelle
        return current_charge * random.uniform(0.9, 1.1)

    # Parçacığın enerjisini güncelleme
    def calculate_new_energy(self, current_energy):
        # Enerjiyi rastgele bir miktar artırarak güncelle
        return current_energy + random.uniform(0, 1)

    # Parçacığın enerjisini güncelleme
    def calculate_new_position(self):
        # Parçacığın yeni hızını ve konumunu belirlemek için güncellenmiş bir kuvvet fonksiyonu.
        random_force = Vector(
            random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
        )
        time_step = random.uniform(0.0001, 0.001)
        self.update(force=random_force, time_step=time_step)

    # Parçacığın özelliklerini güncelleme
    def update_properties(self):
        self.energy = self.calculate_new_energy(self.energy)
        self.charge = self.calculate_new_charge(self.charge)
        self.mass = self.calculate_new_mass(self.mass)
        self.spin = self.calculate_new_spin(self.spin)
        self.calculate_new_position()

    def evolve(self):
        super().evolve()

        # Parçacığın özelliklerini güncelle
        self.update_properties()

    def mesure(self):
        base_mesure = super().mesure()
        new_mesure = base_mesure
        return new_mesure

    def update(self, force: Vector, time_step: float) -> None:
        """
        Parçacığın durumunu günceller.

        :param force: Uygulanan kuvvet.
        :type force: Vector
        :param time_step: Zaman adımı.
        :type time_step: float
        """
        # Schrödinger denklemini kullanarak dalga fonksiyonunu güncelle
        self.wave_function += self.__schrodinger_eq() * time_step

        # Newton'un ikinci yasası: F = m * a
        acceleration = force * (1 / self.mass)

        # Hızı güncelleme: v = v0 + a * t
        self.velocity += acceleration * time_step

        # Momentumu güncelleme: p = m * v
        self.momentum = self.velocity * self.mass  # Çarpımı tersine çevirdik

        # Konumu güncelleme: x = x0 + v * t
        self.position += self.velocity * time_step

    def __schrodinger_eq(self):
        """
        Schrödinger denklemi ile dalga fonksiyonunu hesaplar.
        """
        # Burada kompleks bir işlem gerçekleştirilir, bu sadece bir örnektir.
        return self.position * self.velocity

    def pauli_exclusion_principle(self, other_particle: "Particle") -> bool:
        """
        Parçacıklar arasındaki Pauli dışlama prensibini kontrol eder.

        :param other_particle: Diğer parçacık.
        :type other_particle: Particle
        :return: Prensibe uygunsa True, aksi halde False.
        :rtype: bool
        """
        return self.spin == other_particle.spin

    def calculate_momentum(self, electric_field: Vector) -> Vector:
        """
        Parçacığın momentumunu hesaplar.

        :param electric_field: Elektrik alanı.
        :type electric_field: Vector
        :return: Momentum.
        :rtype: Vector
        """
        return self.__schrodinger_eq() * electric_field

    def electromagnetic_interaction(
        self, electric_field: Vector, magnetic_field: Vector
    ) -> Vector:
        """
        Elektromanyetik etkileşimi hesaplar.

        :param electric_field: Elektrik alanı.
        :type electric_field: Vector
        :param magnetic_field: Manyetik alan.
        :type magnetic_field: Vector
        :return: Elektromanyetik etkileşim.
        :rtype: Vector
        """
        return electric_field * self.charge + magnetic_field * self.charge

    def replicate(self):
        """
        Eşlenme işlemi gerçekleştiğinde çağrılır ve yeni programcıkların oluşturulmasını sağlar.
        """
        if self.generation >= self.max_generation or self.max_replicas <= 0:
            # Maksimum jenerasyon sayısına ulaşıldıysa veya max_replicas değeri 0 ise, eşleme yapmayı durdur
            return

        # # Yeni bir programcık oluştur
        # new_core = Particle(
        #     name=self.name,
        #     lifetime_seconds=self.lifetime_seconds,
        #     lifecycle=self.lifecycle,
        #     charge=self.charge,
        #     mass=self.mass,
        #     spin=self.spin,
        #     energy=self.energy,
        #     position=self.position,
        #     velocity=self.velocity,
        #     momentum=self.momentum,
        #     wave_function=self.wave_function,
        # ).trigger_event(self.event_function)
        # # Yeni programcık kodlarını kopyala
        # new_core.codes = self.codes[:]
        # # Yeni programcığın nesnesini başlat
        # new_core.start()
        # # Nesne oluşturma bilgisini güncelle
        # self.logger.info(f"Replicated [{new_core.id}]")


# Example Usage
if __name__ == "__main__":
    name = "particle"  # Parçacığın adı.
    lifetime_seconds = 1  # float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 60  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 3  # oluşturulacak örnek sayısı

    number_of_instance_created = 0

    def create_instance(name, lifetime_seconds, lifecycle):
        def instance_signal(instance):
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

        global number_of_instance_created
        number_of_instance_created += 1

        def force_function(t):
            return Vector(t**0.1, t**0.1, t**0.1)

        return (
            Particle(
                name=name,
                lifetime_seconds=lifetime_seconds,
                lifecycle=lifecycle,
                charge=-1.602176634e-19,
                mass=9.10938356e-31,
                spin=1 / 2,
                energy=0,
                position=Vector(0.2, 0.2, 0.2),
                velocity=Vector(0.1, 0.1, 0.1),
                momentum=Vector(0.1, 0.1, 0.1),
                wave_function=force_function(0.01),
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

        # örnekleri duraklatma
        for instance in instances:
            if instance.name == f"{name}_1":
                instance.pause()

        # öernekleri devam ettirme
        for instance in instances:
            if instance.name == f"{name}_1":
                instance.resume()

        # Thread'leri durdurma
        for instance in instances:
            instance.stop()
            instance.join()

    main()
