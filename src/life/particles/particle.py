# src/life/particles/particle.py


import asyncio
from src.life.particles.vector import Vector
from src.life.particles.core import Core


class Particle(Core):
    """
    Parçacık sınıfı, LifeCycleManager sınıfından türetilir ve parçacıkların özelliklerini ve davranışlarını tanımlar.
    """

    def __init__(
        self,
        name,
        lifetime_seconds,
        charge,
        mass,
        spin,
        energy,
        position=Vector(),
        velocity=Vector(),
        momentum=Vector(),
        wave_function=None,
    ):
        """
        Parçacık sınıfını başlatır.

        :param name: Parçacığın adı.
        :param lifetime_seconds: Parçacığın ömrü.

        :param charge: Parçacığın yükü.
        :param mass: Parçacığın kütlesi.
        :param spin: Parçacığın spin'i.
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

    def to_json(self):
        """
        Parçacığı JSON formatına dönüştürür.

        :return: JSON formatında parçacık verisi.
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

    def signal(self, time_step):
        """
        Parçacığın sinyalini gönderir.
        """
        self.update(force=self.wave_function, time_step=time_step)

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


# Example Usage
if __name__ == "__main__":
    simulation_time_step = 1
    number_of_instance = 2
    lifetime_seconds = float("inf")
    instance_prefix = "Particle"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    SOFT = "\033[98m"
    RESET = "\033[0m"

    def instance_signal(data):
        if not hasattr(data, "created_printed"):
            print(
                f"{WHITE}instance_signal{RESET} ",
                f"{PURPLE}Created{RESET}",
                f"{CYAN}{data.name}{RESET}",
                f"{SOFT}{data.elapsed_lifespan}{RESET}",
            )
            data.created_printed = True  # Created durumu yazıldı
        else:
            status = data.status()
            if status == "Running":
                status_color = GREEN
            elif status == "Paused":
                status_color = YELLOW
            elif status == "Stopped":
                status_color = RED
            else:
                status_color = PURPLE  # Created durumu
                status = "Created"
            print(
                f"{WHITE}instance_signal{RESET} ",
                f"{status_color}{status}{RESET}",
                f"{CYAN}{data.name}{RESET}",
                f"{SOFT}{data.elapsed_lifespan}{RESET}",
            )

    instance_created_counter = 0

    async def create_instance(name, lifetime_seconds):
        global instance_created_counter
        instance_created_counter += 1

        def force_function(t):
            return Vector(t**0.1, t**0.1, t**0.1)

        instance = Particle(
            name=f"{name}_{instance_created_counter}",
            lifetime_seconds=lifetime_seconds,
            charge=-1.602176634e-19,
            mass=9.10938356e-31,
            spin=1 / 2,
            energy=0,
            position=Vector(0, 0, 0),
            velocity=Vector(0, 0, 0),
            momentum=Vector(0, 0, 0),
            wave_function=force_function(0.1),
        )

        instance.trigger_event(instance_signal)
        instance.start()
        return instance

    async def main():
        # Örnek yönetimi
        instances = await asyncio.gather(
            *[
                create_instance(instance_prefix, lifetime_seconds=2)
                for _ in range(number_of_instance)
            ]
        )
        # Tüm işlemleri burada kontrol edebilirsiniz
        await asyncio.sleep(2)  #
        # örnekleri duraklatma
        for instance in instances:
            if instance.name == f"{instance_prefix}_1":
                instance.pause()

        await asyncio.sleep(2)  #
        # öernekleri devam ettirme
        for instance in instances:
            if instance.name == f"{instance_prefix}_1":
                instance.resume()

        await asyncio.sleep(2)  #
        # Thread'leri durdurma
        for instance in instances:
            instance.stop()
            instance.join()

    asyncio.run(main())
