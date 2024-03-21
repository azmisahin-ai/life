# src/life/particles/particle.py

import json
from src.life.particles.vector import Vector
from src.life.particles.life_cycle_manager import LifeCycleManager


class Particle(LifeCycleManager):
    """
    Parçacık sınıfı, LifeCycleManager sınıfından türetilir ve parçacıkların özelliklerini ve davranışlarını tanımlar.
    """

    def __init__(
        self,
        name,
        charge,
        mass,
        spin,
        lifetime_seconds,
        energy,
        position=Vector(),
        velocity=Vector(),
        momentum=Vector(),
        wave_function=None,
    ):
        """
        Parçacık sınıfını başlatır.

        :param name: Parçacığın adı.
        :param charge: Parçacığın yükü.
        :param mass: Parçacığın kütlesi.
        :param spin: Parçacığın spin'i.
        :param lifetime_seconds: Parçacığın ömrü.
        :param energy: Parçacığın enerjisi.
        :param position: Parçacığın pozisyonu.
        :param velocity: Parçacığın hızı.
        :param momentum: Parçacığın momentumu.
        :param wave_function: Parçacığın dalga fonksiyonu.
        """
        super().__init__(name, lifetime_seconds)
        self.charge = charge
        self.mass = mass
        self.spin = spin
        self.energy = energy
        self.position = position
        self.velocity = velocity
        self.momentum = momentum
        self.wave_function = wave_function or Vector(0, 0, 0)

    def trigger_event(self, event_function):
        """
        Bir olay işlevini tetiklemek için kullanılır.

        :param event_function: Tetiklenen olayın işlevi.
        """
        self.event_function = event_function
        if self.event_function:
            self.event_function(self.to_json())

    def to_json(self):
        """
        Parçacığı JSON formatına dönüştürür.

        :return: JSON formatında parçacık verisi.
        """
        base_json = json.loads(super().to_json())
        particle_data = {
            "name": self.name,
            "charge": self.charge,
            "mass": self.mass,
            "spin": self.spin,
            "lifetime_seconds": self.lifetime_seconds,
            "energy": self.energy,
            "position": self.position.to_json(),
            "velocity": self.velocity.to_json(),
            "momentum": self.momentum.to_json(),
            "wave_function": self.wave_function.to_json(),
        }
        base_json.update(particle_data)  # Düzeltildi
        return json.dumps(base_json)

    def signal(self, time_step):
        """
        Parçacığın sinyalini gönderir.
        """
        self.update(force=self.wave_function, time_step=time_step)
        print(f"position: {self.position.to_json()}")
        print(f"velocity: {self.velocity.to_json()}")
        print(f"momentum: {self.momentum.to_json()}")

    def update(self, force, time_step):
        """
        Parçacığın durumunu günceller.

        :param force: Uygulanan kuvvet.
        :param time_step: Zaman adımı.
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

    def pauli_exclusion_principle(self, other_particle):
        """
        Parçacıklar arasındaki Pauli dışlama prensibini kontrol eder.

        :param other_particle: Diğer parçacık.
        :return: Prensibe uygunsa True, aksi halde False.
        """
        return self.spin == other_particle.spin

    def calculate_momentum(self, electric_field):
        """
        Parçacığın momentumunu hesaplar.

        :param electric_field: Elektrik alanı.
        :return: Momentum.
        """
        return self.__schrodinger_eq() * electric_field

    def electromagnetic_interaction(self, electric_field, magnetic_field):
        """
        Elektromanyetik etkileşimi hesaplar.

        :param electric_field: Elektrik alanı.
        :param magnetic_field: Manyetik alan.
        :return: Elektromanyetik etkileşim.
        """
        return electric_field * self.charge + magnetic_field * self.charge


if __name__ == "__main__":

    def force_function(t):
        return Vector(t**0.1, t**0.1, t**0.1)

    def event_function(data):
        print("event-particle", data)

    instance = Particle(
        name="Electron",
        charge=-1.602176634e-19,
        mass=9.10938356e-31,
        spin=1 / 2,
        lifetime_seconds=5,  # float("inf"),
        energy=0,
        position=Vector(0, 0, 0),
        velocity=Vector(0, 0, 0),
        momentum=Vector(0, 0, 0),
        wave_function=force_function(0.1),
    )
    instance.trigger_event(event_function)
