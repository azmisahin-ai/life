# tests/web/controller/simulation_test.py

import unittest
from src.web.controller.simulation import Simulation
from src.web.controller.simulation_status import SimulationStatus
from src.web.controller.simulation_type import SimulationType


class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.simulation = Simulation()

    def test_start_simulation(self):
        # Simülasyon başlatıldığında doğru durum ve başlatılma değeri kontrol edilmeli
        self.simulation.start(
            simulation_time_step=1,
            simulation_type=SimulationType.LifeCycle,
            number_of_instance=2,
            lifetime_seconds=5,
        )
        self.assertTrue(self.simulation.is_running)
        self.assertFalse(self.simulation.is_paused)
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.started)

    def test_stop_simulation(self):
        # Simülasyon durdurulduğunda durumun değiştiği ve çalıştırılmadığı kontrol edilmeli
        self.simulation.start(
            simulation_time_step=1,
            simulation_type=SimulationType.LifeCycle,
            number_of_instance=2,
            lifetime_seconds=5,
        )
        self.simulation.stop()
        self.assertFalse(self.simulation.is_running)
        self.assertFalse(self.simulation.is_paused)
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.stopped)

    def test_pause_simulation(self):
        # Simülasyon duraklatıldığında durumun değiştiği ve işlem yapılmadığı kontrol edilmeli
        self.simulation.start(
            simulation_time_step=1,
            simulation_type=SimulationType.LifeCycle,
            number_of_instance=2,
            lifetime_seconds=5,
        )
        self.simulation.pause()
        self.assertTrue(self.simulation.is_running)
        self.assertTrue(self.simulation.is_paused)
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.paused)

    def test_continue_simulation(self):
        # Duraklatılan simülasyonun devam ettirildiğinde durumun değiştiği ve işlem yapıldığı kontrol edilmeli
        self.simulation.start(
            simulation_time_step=1,
            simulation_type=SimulationType.LifeCycle,
            number_of_instance=2,
            lifetime_seconds=5,
        )
        self.simulation.pause()
        self.simulation.continues()
        self.assertTrue(self.simulation.is_running)
        self.assertFalse(self.simulation.is_paused)
        self.assertEqual(self.simulation.simulation_status, SimulationStatus.continues)

    def test_simulation_to_json(self):
        # Simülasyonun JSON dökümünün doğru olduğu kontrol edilmeli
        expected_json = {
            "simulation_status": SimulationStatus.stopped.value,
            "simulation_type": SimulationType.LifeCycle.value,
            "simulation_time_step": 1,
        }
        actual = self.simulation.to_json()
        self.assertEqual(actual, expected_json)

    def test_start_simulation_invalid_input(self):
        # Geçersiz girişlerle simülasyon başlatıldığında hata durumunun doğru işlendiği kontrol edilmeli
        with self.assertRaises(
            ValueError
        ):  # Hata durumu beklenen bir istisna türüne göre güncellenmeli
            self.simulation.start(
                simulation_time_step=1,
                simulation_type="InvalidType",  # Geçersiz bir simülasyon türü
                number_of_instance=2,
                lifetime_seconds=-5,  # Negatif bir ömür değeri
            )


if __name__ == "__main__":
    unittest.main()
