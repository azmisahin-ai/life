# tests/life/particle/core_test.py
import unittest
import time
from unittest.mock import MagicMock
from src.life.particles.core import Core

mockLifetime_seconds = 0.8577


class TestCore(unittest.TestCase):
    def test_trigger_event(self):
        # Test etkinliğinin tetiklenip tetiklenmediğini doğrulama
        event_function_mock = MagicMock()
        instance = Core(
            name="TestParticle", lifetime_seconds=mockLifetime_seconds
        )
        instance.trigger_event(event_function_mock)
        time.sleep(
            instance.lifetime_seconds
        )  # Bekleme, yaşam süresinin sona ermesini sağlar
        self.assertTrue(event_function_mock.called)

    def test_to_json(self):
        # JSON dönüşümünün doğruluğunu ve formatını doğrulama
        instance = Core(
            name="TestParticle", lifetime_seconds=mockLifetime_seconds
        )
        json_data = instance.to_json()

        self.assertIsInstance(json_data, dict)
        # JSON verisinin içeriğini kontrol etme
        expected_keys = {
            "name",
            "life_start_time",
            "elapsed_lifespan",
            "lifecycle_rate_per_minute",
            "lifecycle",
            "lifetime_seconds",
        }
        self.assertCountEqual(expected_keys, json_data.keys())
        self.assertEqual(json_data["name"], "TestParticle")
        # Diğer verilerin uygunluğunu kontrol etme

    def test_lifetime_zero_or_negative(self):
        # Yaşam süresi sıfır veya negatif olduğunda nasıl davrandığını test etme
        with self.assertRaises(ValueError):
            Core(name="TestParticle", lifetime_seconds=0)

        with self.assertRaises(ValueError):
            Core(name="TestParticle", lifetime_seconds=-1)

    def test_infinite_lifetime(self):
        # Sonsuz yaşam süresi için nasıl davrandığını test etme
        instance = Core(name="TestParticle", lifetime_seconds=float("inf"))

        # instance nesnesinin oluşturulduğunu doğrula
        self.assertEqual(instance.lifetime_seconds, float("inf"))

        # Bir olay işlevini tetikleme
        event_function_mock = MagicMock()
        instance.trigger_event(event_function_mock)

        # Olayın tetiklenmesini bekleyin ve ardından olayın çağrıldığını kontrol edin
        time.sleep(mockLifetime_seconds)  # Biraz bekleme süresi ekleyin
        self.assertTrue(event_function_mock.called)

    def test_invalid_instance_creation(self):
        # Geçersiz bir örnek oluşturulduğunda nasıl davrandığını test etme
        with self.assertRaises(ValueError):
            Core(name=None, lifetime_seconds=0.8577)

    def test_multiple_scenarios(self):
        # Farklı yaşam süreleri ve senaryolar altında testleri genişletme
        instance_1 = Core(
            name="Particle1", lifetime_seconds=mockLifetime_seconds
        )
        instance_2 = Core(
            name="Particle2", lifetime_seconds=mockLifetime_seconds * 2.1
        )

        # Farklı yaşam döngüsü olaylarını tetikleme ve doğrulama
        event_function_mock_1 = MagicMock()
        instance_1.trigger_event(event_function_mock_1)
        time.sleep(instance_1.lifetime_seconds)  # Beklemek için yeterli süre
        self.assertTrue(event_function_mock_1.called)

        event_function_mock_2 = MagicMock()
        instance_2.trigger_event(event_function_mock_2)
        time.sleep(instance_2.lifetime_seconds)  # Beklemek için yeterli süre
        self.assertTrue(event_function_mock_2.called)


if __name__ == "__main__":
    unittest.main(exit=False)
