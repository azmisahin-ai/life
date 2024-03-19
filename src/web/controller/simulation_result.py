# web/controller/simulation_result.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationResult:
    status: str
    number_of_particles: int
    time_step: float
    particle: Optional["Particle"]

    @classmethod
    def from_json(cls, json_data):
        return cls(
            status=json_data["status"],
            number_of_particles=json_data["number_of_particles"],
            time_step=json_data["time_step"],
            particle=Particle.from_json(json_data.get("particle")),
        )

    def to_json(self):
        return {
            "status": self.status,
            "number_of_particles": self.number_of_particles,
            "time_step": self.time_step,
            "particle": self.particle.to_json() if self.particle else None,
        }


@dataclass
class Particle:
    name: str
    charge: float
    mass: float
    spin: float
    lifetime: int
    energy: float
    position: "Vector"
    velocity: "Vector"
    momentum: "Vector"

    @classmethod
    def from_json(cls, json_data):
        return cls(
            name=json_data.get("name", ""),
            charge=json_data.get("charge", 0),
            mass=json_data.get("mass", 0.0),
            spin=json_data.get("spin", 0.0),
            lifetime=json_data.get("lifetime", -1),
            energy=json_data.get("energy", 0.0),
            position=Vector.from_json(json_data.get("position", {})),
            velocity=Vector.from_json(json_data.get("velocity", {})),
            momentum=Vector.from_json(json_data.get("momentum", {})),
        )

    def to_json(self):
        return {
            "name": self.name,
            "charge": self.charge,
            "mass": self.mass,
            "spin": self.spin,
            "lifetime": self.lifetime,
            "energy": self.energy,
            "position": self.position.to_json(),
            "velocity": self.velocity.to_json(),
            "momentum": self.momentum.to_json(),
        }


@dataclass
class Vector:
    x: float
    y: float
    z: float

    @classmethod
    def from_json(cls, json_data):
        return cls(
            x=json_data.get("x", 0), y=json_data.get("y", 0), z=json_data.get("z", 0)
        )

    def to_json(self):
        return {"x": self.x, "y": self.y, "z": self.z}
