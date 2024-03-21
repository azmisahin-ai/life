# tests/life/particle/life_cycle_manager_test.py
import unittest
import time
from unittest.mock import MagicMock
from src.life.particles.life_cycle_manager import LifeCycleManager


class TestLifeCycleManager(unittest.TestCase):
    def test_trigger_event(self):
        event_function_mock = MagicMock()
        instance = LifeCycleManager(name="TestParticle", lifetime_seconds=5)
        instance.trigger_event(event_function_mock)
        time.sleep(6)  # Bekleme, yaşam süresinin sona ermesini sağlar
        self.assertTrue(event_function_mock.called)

    def test_to_json(self):
        instance = LifeCycleManager(name="TestParticle", lifetime_seconds=5)
        json_data = instance.to_json()
        self.assertIsInstance(json_data, str)
        # JSON verilerini dönüştürerek geri alabilir ve kontrol edebilirsiniz,
        # ancak bu örnek testte bunu yapmıyorum.

    # Daha fazla test senaryosu eklenebilir


if __name__ == "__main__":
    unittest.main()
