# tests/web/controller/simulation_test.py

import unittest
from src.web.controller.simulation import (
    Simulation,
    simulation_status,
    simulation_sampler_status,
    simulation_instance_status,
)
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType


class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.simulation = Simulation("test")
        # önce trigger_simulation ile gerekli işlevi tanımlayın
        self.simulation.trigger_simulation(simulation_status)
        # aynı şekilde trigger_sampler ve trigger_instance ile diğer işlevleri tanımlayın
        self.simulation.trigger_sampler(simulation_sampler_status)
        self.simulation.trigger_instance(simulation_instance_status)

    def tearDown(self):
        try:
            # tearDown() metodunda gerekli temizlik işlemleri
            self.simulation.stop()
        finally:
            self.simulation = None

    def test_start_simulation(self):
        self.simulation.start(
            number_of_instance=3,
            lifetime_seconds=float("inf"),
            lifecycle=60 / 1,
            simulation_type=SimulationType.Particles,
        )
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.started)

    def test_pause_simulation(self):
        self.simulation.start(
            number_of_instance=3,
            lifetime_seconds=float("inf"),
            lifecycle=60 / 1,
            simulation_type=SimulationType.Particles,
        )
        self.simulation.pause()
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.paused)

    def test_continue_simulation(self):
        self.simulation.start(
            number_of_instance=3,
            lifetime_seconds=float("inf"),
            lifecycle=60 / 1,
            simulation_type=SimulationType.Particles,
        )
        self.simulation.pause()
        self.simulation.continues()
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.continues)

    def test_stop_simulation(self):
        self.simulation.start(
            number_of_instance=3,
            lifetime_seconds=float("inf"),
            lifecycle=60 / 1,
            simulation_type=SimulationType.Particles,
        )
        self.simulation.stop()
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.stopped)

    def test_invalid_simulation_type(self):
        with self.assertRaises(ValueError):
            self.simulation.start(
                number_of_instance=3,
                lifetime_seconds=float("inf"),
                lifecycle=60 / 1,
                simulation_type="InvalidType",
            )

    def test_negative_lifetime(self):
        with self.assertRaises(ValueError):
            self.simulation.start(
                number_of_instance=3,
                lifetime_seconds=-10,
                lifecycle=60 / 1,
                simulation_type=SimulationType.Particles,
            )


if __name__ == "__main__":
    unittest.main()
