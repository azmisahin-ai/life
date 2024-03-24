# tests/life/particle/core_test.py
import unittest
from unittest.mock import MagicMock
from src.life.particles.core import Core


class TestCore(unittest.TestCase):
    def setUp(self):
        # Core sınıfından bir örnek oluşturuluyor ve her test öncesinde kullanılıyor
        self.core_instance = Core(name="TestCycle", lifetime_seconds=10)

    def test_initialization(self):
        # Core sınıfının başlangıç değerlerinin doğru ayarlandığını kontrol eder
        self.assertEqual(self.core_instance.name, "TestCycle")
        self.assertEqual(self.core_instance.lifetime_seconds, 10)
        self.assertIsNone(self.core_instance.life_start_time)
        self.assertEqual(self.core_instance.elapsed_lifespan, 0)
        self.assertEqual(self.core_instance.lifecycle_rate_per_minute, 70)
        self.assertEqual(self.core_instance.lifecycle, 60.0 / 70)
        self.assertIsNotNone(self.core_instance.event_function)  # created event
        self.assertFalse(self.core_instance._paused)
        self.assertFalse(self.core_instance._stop_event.is_set())

    def test_trigger_event(self):
        # event_function'ın bir mock işlevle doğru şekilde ayarlandığını kontrol eder
        mock_function = MagicMock()
        self.core_instance.trigger_event(mock_function)
        self.assertEqual(self.core_instance.event_function, mock_function)

    def test_status_running(self):
        # Core örneğinin durumunun "Running" olduğunu kontrol eder
        self.assertEqual(self.core_instance.status(), "Running")

    def test_status_paused(self):
        # Core örneğinin durumunun "Paused" olduğunu kontrol eder
        self.core_instance._paused = True
        self.assertEqual(self.core_instance.status(), "Paused")

    def test_status_stopped(self):
        # Core örneğinin durumunun "Stopped" olduğunu kontrol eder
        self.core_instance._stop_event.set()
        self.assertEqual(self.core_instance.status(), "Stopped")

    def test_pause_method(self):
        # pause yönteminin
        # core örneğinin durumunu doğru şekilde değiştirdiğini
        # ve event_function'ı çağırdığını kontrol eder
        mock_event_function = MagicMock()
        self.core_instance.trigger_event(mock_event_function)  # event_function'ı ayarla
        self.assertFalse(
            self.core_instance._paused
        )  # Başlangıçta duraklatılmamış olmalı
        self.core_instance.pause()  # Yöntemi doğru şekilde çağırın
        self.assertTrue(self.core_instance._paused)  # Artık duraklatılmış olmalı
        mock_event_function.assert_called_once_with(
            self.core_instance
        )  # event_function'ın çağrıldığını kontrol et

    def test_resume_method(self):
        # resume yönteminin
        # core örneğinin durumunu doğru şekilde değiştirdiğini
        # ve event_function'ı çağırdığını kontrol eder
        mock_event_function = MagicMock()
        self.core_instance.trigger_event(mock_event_function)  # event_function'ı ayarla
        self.core_instance._paused = True  # Duraklatılmış duruma getir
        self.core_instance.resume()  # Yöntemi doğru şekilde çağırın
        self.assertFalse(self.core_instance._paused)  # Artık duraklatılmamış olmalı
        mock_event_function.assert_called_once_with(
            self.core_instance
        )  # event_function'ın çağrıldığını kontrol et

    def test_stop_method(self):
        # stop yönteminin
        # core örneğinin durumunu doğru şekilde değiştirdiğini
        # ve event_function'ı çağırdığını kontrol eder
        mock_event_function = MagicMock()
        self.core_instance.trigger_event(mock_event_function)  # event_function'ı ayarla
        self.assertFalse(
            self.core_instance._stop_event.is_set()
        )  # Başlangıçta durdurulmamış olmalı
        self.core_instance.stop()  # Yöntemi doğru şekilde çağır
        self.assertTrue(
            self.core_instance._stop_event.is_set()
        )  # Artık durdurulmuş olmalı
        mock_event_function.assert_called_once_with(
            self.core_instance
        )  # event_function'ın çağrıldığını kontrol et


if __name__ == "__main__":
    unittest.main()
