# tests/web/controller/particle_simulation_test.py

import unittest
from unittest.mock import MagicMock
from src.web.controller.particle_simulation import ParticleSimulation


class TestParticleSimulation(unittest.TestCase):
    def setUp(self):
        self.simulation = ParticleSimulation(
            name="Simulation.Particle.test",
            number_of_instance=3,
            lifetime_seconds=float("inf"),
            lifecycle=60 / 70,
        )

    def test_simulation_creation(self):
        self.assertEqual(self.simulation.name, "Simulation.Particle.test")
        self.assertEqual(self.simulation.number_of_instance, 3)
        self.assertEqual(self.simulation.lifetime_seconds, float("inf"))
        self.assertEqual(self.simulation.lifecycle, 60 / 70)

    def test_trigger_event(self):
        event_function = MagicMock()
        self.simulation.trigger_event(event_function)
        self.assertEqual(self.simulation.event_function, event_function)

    def test_trigger_event_instance(self):
        event_function = MagicMock()
        self.simulation.trigger_event_instance(event_function)
        self.assertEqual(self.simulation.event_function_instance, event_function)

    def test_pause_resume_simulation(self):
        # pause_simulation method
        self.simulation.pause_simulation()
        self.assertTrue(self.simulation._paused)
        # resume_simulation method
        self.simulation.resume_simulation()
        self.assertFalse(self.simulation._paused)

    def test_stop_simulation(self):
        self.simulation.stop_simulation()
        self.assertTrue(self.simulation._stop_event.is_set())
        self.assertTrue(self.simulation._exit_flag)

    def test_status(self):
        status = self.simulation.status()
        self.assertIn(status, ["Paused", "Running"])

    def test_force_function(self):
        t = 0.5
        ecpected = t**0.1
        force = self.simulation.force_function(t)
        self.assertAlmostEqual(force.x, ecpected)
        self.assertAlmostEqual(force.y, ecpected)
        self.assertAlmostEqual(force.z, ecpected)


if __name__ == "__main__":
    unittest.main()
