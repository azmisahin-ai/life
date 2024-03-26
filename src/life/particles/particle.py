# src/life/particles/particle.py

import time
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

    def signal(self, time_step: float) -> None:
        """
        Parçacığın sinyalini gönderir.

        :param time_step: Zaman adımı.
        :type time_step: float
        """
        self.update(force=self.wave_function, time_step=time_step)

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


# Example Usage
if __name__ == "__main__":
    name = "particle"  # Parçacığın adı.
    lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
    lifecycle = 60 / 70  # Parçacığın saniyedeki yaşam döngüsü.
    number_of_instance = 10  # oluşturulacak örnek sayısı

    instance_created_counter = 0

    def create_instance(name, lifetime_seconds, lifecycle):
        def instance_signal(instance):
            instance.status()

        global instance_created_counter
        instance_created_counter += 1
        instance_name = f"{name}_{instance_created_counter}"

        def force_function(t):
            return Vector(t**0.1, t**0.1, t**0.1)

        return (
            Particle(
                name=instance_name,
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
