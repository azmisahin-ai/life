# tests/life/particle/particle_test.py

import unittest
from unittest.mock import Mock
from src.life.particles.particle import Particle
from src.life.particles.vector import Vector


class TestParticle(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_particle_creation(self):
        """
        Parçacık oluşturma testi.
        """
        # Test verileri
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

        # Parçacık oluşturma
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

        # Özelliklerin doğru oluşturulduğunu doğrula
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
        # Mock event function
        event_function_mock = Mock()

        # Parçacık oluşturma
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

        # Olay tetikleme
        particle.trigger_event(event_function_mock)

        # Beklenen şekilde olay fonksiyonunun çağrıldığını doğrula
        event_function_mock.assert_called_once()

    def test_to_json(self):
        """
        JSON dönüşüm testi.
        """
        # Test verileri
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

        # JSON çıktısını al
        expected_json = particle.to_json()

        # Beklenen JSON çıktısının momentum içerip içermediğini kontrol et
        self.assertIn("momentum", expected_json)

        # JSON çıktısındaki momentumun değerini kontrol et
        self.assertEqual(expected_json["momentum"], {"x": 0, "y": 0, "z": 0})


if __name__ == "__main__":
    unittest.main()
