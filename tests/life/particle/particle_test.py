# tests/life/particle/particle_test.py

import unittest
from src.life.particles.particle import Particle
from src.life.particles.vector import Vector


class TestParticle(unittest.TestCase):
    def setUp(self):
        def force_function(t):
            return Vector(t**0.1, t**0.1, t**0.1)

        # Parçacık örnekleri oluşturulur
        self.particle_1 = Particle(
            name="Particle_1.test",
            lifetime_seconds=float("inf"),  # Parçacığın yaşam süresi saniye cinsinden.
            charge=-1.602176634e-19,
            mass=9.10938356e-31,
            spin=1 / 2,
            energy=0,
            position=Vector(0.1, 0.1, 0.1),
            velocity=Vector(0.1, 0.1, 0.1),
            momentum=Vector(0.1, 0.1, 0.1),
            wave_function=force_function(0.01),
        )

        self.particle_2 = Particle(
            name="Particle_2.test",
            lifetime_seconds=float("inf"),  # Parçacığın yaşam süresi saniye cinsinden.
            charge=-1.602176634e-19,
            mass=9.10938356e-31,
            spin=1 / 2,
            energy=0,
            position=Vector(0.2, 0.2, 0.2),
            velocity=Vector(0.1, 0.1, 0.1),
            momentum=Vector(0.1, 0.1, 0.1),
            wave_function=force_function(0.01),
        )

    def test_particle_creation(self):
        # Parçacık özelliklerinin doğru oluşturulduğunu kontrol etme
        self.assertEqual(self.particle_1.name, "Particle_1.test")
        self.assertEqual(self.particle_1.charge, -1.602176634e-19)
        self.assertEqual(self.particle_1.mass, 9.10938356e-31)
        self.assertEqual(self.particle_1.spin, 1 / 2)
        self.assertEqual(self.particle_1.energy, 0)

    def test_particle_interaction(self):
        # Parçacıklar arasındaki etkileşimi kontrol etme
        self.assertTrue(self.particle_1.pauli_exclusion_principle(self.particle_2))

    def test_particle_update(self):
        # Parçacığın güncellenmesini kontrol etme
        initial_position = self.particle_1.position
        initial_velocity = self.particle_1.velocity
        initial_momentum = self.particle_1.momentum
        self.particle_1.update(force=Vector(0.1, 0.1, 0.1), time_step=0.2)
        self.assertNotEqual(self.particle_1.position.x, initial_position.x)
        self.assertNotEqual(self.particle_1.position.y, initial_position.y)
        self.assertNotEqual(self.particle_1.position.z, initial_position.z)
        self.assertNotEqual(self.particle_1.velocity.x, initial_velocity.x)
        self.assertNotEqual(self.particle_1.velocity.y, initial_velocity.y)
        self.assertNotEqual(self.particle_1.velocity.z, initial_velocity.z)
        self.assertNotEqual(self.particle_1.momentum.x, initial_momentum.x)
        self.assertNotEqual(self.particle_1.momentum.y, initial_momentum.y)
        self.assertNotEqual(self.particle_1.momentum.z, initial_momentum.z)

    def test_schrodinger_eq(self):
        # Schrödinger denkleminin hesaplanmasını kontrol etme
        wave_function_before = self.particle_1.wave_function
        self.particle_1.signal(time_step=1)
        self.assertNotAlmostEqual(
            self.particle_1.wave_function.x, wave_function_before.x
        )
        self.assertNotAlmostEqual(
            self.particle_1.wave_function.y, wave_function_before.y
        )
        self.assertNotAlmostEqual(
            self.particle_1.wave_function.z, wave_function_before.z
        )


if __name__ == "__main__":
    unittest.main()
