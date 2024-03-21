# tests/life/particle/particle_test.py

import unittest
from unittest.mock import Mock
from src.life.particles.particle import Particle
from src.life.particles.vector import Vector


class TestParticle(unittest.TestCase):
    def test_particle_creation(self):
        """
        Parçacık oluşturma testi.
        """
        name = "Electron"
        charge = -1.602176634e-19
        mass = 9.10938356e-31
        spin = 1 / 2
        lifetime_seconds = 5
        energy = 0
        position = Vector(0, 0, 0)
        velocity = Vector(0, 0, 0)
        momentum = Vector(0, 0, 0)
        wave_function = Vector(0, 0, 0)

        particle = Particle(
            name=name,
            charge=charge,
            mass=mass,
            spin=spin,
            lifetime_seconds=lifetime_seconds,
            energy=energy,
            position=position,
            velocity=velocity,
            momentum=momentum,
            wave_function=wave_function,
        )

        self.assertEqual(particle.name, name)
        self.assertEqual(particle.charge, charge)
        self.assertEqual(particle.mass, mass)
        self.assertEqual(particle.spin, spin)
        self.assertEqual(particle.lifetime_seconds, lifetime_seconds)
        self.assertEqual(particle.energy, energy)
        self.assertEqual(particle.position, position)
        self.assertEqual(particle.velocity, velocity)
        self.assertEqual(particle.momentum, momentum)
        self.assertEqual(particle.wave_function, wave_function)

    def test_event_triggering(self):
        """
        Olay tetikleme testi.
        """
        event_function_mock = Mock()
        particle = Particle(
            name="Electron",
            charge=-1.602176634e-19,
            mass=9.10938356e-31,
            spin=1 / 2,
            lifetime_seconds=5,
            energy=0,
            position=Vector(0, 0, 0),
            velocity=Vector(0, 0, 0),
            momentum=Vector(0, 0, 0),
            wave_function=Vector(0, 0, 0),
        )

        particle.trigger_event(event_function_mock)

        # Bekleyin, olay işlevinin çağrıldığını doğrulayın
        event_function_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
