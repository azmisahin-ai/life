# src/life/particles/particle.py
from src.life.particles.base import Base
from src.life.particles.vector import Vector


class Particle(Base):
    def __init__(
        self,
        name,
        charge,
        mass,
        spin,
        lifetime,
        energy,
        position=Vector(),
        velocity=Vector(),
        momentum=Vector(),
        wave_function=None,
    ):
        super().__init__(name, lifetime)
        self.name = name
        self.charge = charge
        self.mass = mass
        self.spin = spin
        self.lifetime = lifetime
        self.energy = energy
        self.position = position
        self.velocity = velocity
        self.momentum = momentum
        self.wave_function = (
            wave_function if wave_function is not None else Vector(0, 0, 0)
        )

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data.get("name", ""),
            charge=data.get("charge", 0),
            mass=data.get("mass", 0.0),
            spin=data.get("spin", 0.0),
            energy=data.get("energy", 0.0),
            position=Vector.from_json(data.get("position", {})),
            velocity=Vector.from_json(data.get("velocity", {})),
            momentum=Vector.from_json(data.get("momentum", {})),
            wave_function=Vector.from_json(data.get("wave_function", {})),
        )

    def to_json(self):
        data = super().to_json()
        data.update(
            {
                "charge": self.charge,
                "mass": self.mass,
                "spin": self.spin,
                "lifetime": self.lifetime,
                "energy": self.energy,
                "position": self.position.to_json(),
                "velocity": self.velocity.to_json(),
                "momentum": self.momentum.to_json(),
                "wave_function": self.wave_function.to_json(),
            }
        )
        return data

    def signal(self):
        self.update(force=self.wave_function, time_step=0.01)
        print(
            f"position: {self.position.to_json()} velocity: {self.velocity.to_json()} momentum: {self.momentum.to_json()} "
        )

    def update(self, force=Vector(), time_step=0.1):
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
        # Schrödinger denklemi ile dalga fonksiyonunu hesapla
        # Burada kompleks bir işlem gerçekleştirilir, bu sadece bir örnektir.
        return self.position * self.velocity

    def pauli_exclusion_principle(self, other_particle):
        if self.spin == other_particle.spin:
            return True
        else:
            return False

    def calculate_momentum(self, electric_field):
        return self.__schrodinger_eq() * electric_field

    def electromagnetic_interaction(self, electric_field, magnetic_field):
        return electric_field * self.charge + magnetic_field * self.charge


if __name__ == "__main__":

    def force_function(t):
        return Vector(t**0.1, t**0.1, t**0.1)

    def eventFunction(data):
        print("event-particle", data)

    instance = Particle(
        name="Electron",
        charge=-1.602176634e-19,
        mass=9.10938356e-31,
        spin=1 / 2,
        lifetime=float("inf"),
        energy=0,
        position=Vector(0, 0, 0),
        velocity=Vector(0, 0, 0),
        momentum=Vector(0, 0, 0),
        wave_function=force_function(0.1),
    )
    instance.trigger(eventFunction)
