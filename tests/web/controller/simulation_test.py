# tests/web/controller/simulation_test.py

import unittest
from src.web.controller.simulation import simulation
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType


class TestSimulation(unittest.TestCase):
    def test_setup(self):
        # Parametreleri doğru şekilde ayarlayarak simülasyonu başlatma
        simulation.setup(
            number_of_instance=3,
            lifetime_seconds=float("inf"),
            lifecycle=60 / 60,
            simulation_type=SimulationType.Particles,
        )
        self.assertEqual(simulation.simulation_status, SimulationStatus.stopped)
        self.assertIsNotNone(simulation.sampler)

    def test_trigger_functions(self):
        # Tetikleyici fonksiyonların çalışıp çalışmadığını kontrol etme
        def simulation_signal(simulation):
            pass

        def sampler_signal(sampler):
            pass

        def instance_signal(instance):
            pass

        simulation.trigger_simulation(simulation_signal)
        simulation.trigger_sampler(sampler_signal)
        simulation.trigger_instance(instance_signal)

        self.assertEqual(simulation.simulation_event_function, simulation_signal)
        self.assertEqual(simulation.sampler_event_function, sampler_signal)
        self.assertEqual(simulation.instance_event_function, instance_signal)


if __name__ == "__main__":
    unittest.main()
