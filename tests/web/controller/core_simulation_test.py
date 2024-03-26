# tests/web/controller/core_simulation_test.py

import unittest
from unittest.mock import MagicMock
from src.web.controller.core_simulation import CoreSimulation


class TestCoreSimulation(unittest.TestCase):
    def setUp(self):
        self.simulation = CoreSimulation(
            name="test",
            number_of_instance=3,
            lifetime_seconds=float("inf"),
            lifecycle=60 / 70,
        )

    def test_simulation_creation(self):
        self.assertEqual(self.simulation.name, "test")
        self.assertEqual(self.simulation.number_of_instance, 3)
        self.assertEqual(self.simulation.lifetime_seconds, float("inf"))
        self.assertEqual(self.simulation.lifecycle, 60 / 70)

    def test_instance_creation(self):
        instance = self.simulation.create_instance("test", 10, 1)
        self.assertIsNotNone(instance)
        self.assertEqual(instance.name, "test_1")

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
