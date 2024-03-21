# tests/web/controller/life_cycle_simulation_test.py

# tests/web/controller/life_cycle_simulation_test.py

import unittest
from src.web.controller.life_cycle_simulation import LifeCycleSimulation


# life_cycle_event fonksiyonunu tanımlayalım
def life_cycle_event(data):
    print("life-cycle-event", data)


class TestLifeCycleSimulation(unittest.TestCase):
    def test_initialization(self):
        # Başlangıç durumunu doğru şekilde oluşturuyor mu?
        simulation = LifeCycleSimulation(number_of_instance=2, lifetime_seconds=5)
        self.assertEqual(simulation.number_of_instance, 2)
        self.assertEqual(simulation.lifetime_seconds, 5)
        self.assertEqual(simulation.number_of_instance_created, 0)
        self.assertIsNone(simulation.last_item)
        self.assertIsNone(simulation.event_function)
        self.assertFalse(simulation.event_trigger.is_set())

    def test_create_instance(self):
        # create_instance fonksiyonu yeni bir örnek oluşturuyor mu?
        simulation = LifeCycleSimulation(number_of_instance=2, lifetime_seconds=5)
        simulation.create_instance()
        self.assertIsNotNone(simulation.last_item)
        self.assertEqual(simulation.number_of_instance_created, 1)

    def test_trigger_event_function(self):
        # Event işlevini tetikliyor mu?
        simulation = LifeCycleSimulation(number_of_instance=2, lifetime_seconds=5)
        simulation.trigger(
            life_cycle_event
        )  # life_cycle_event fonksiyonunu burada kullanıyoruz
        self.assertIsNotNone(simulation.event_function)

    def test_to_json(self):
        # JSON çıktısını doğru şekilde oluşturuyor mu?
        simulation = LifeCycleSimulation(number_of_instance=2, lifetime_seconds=5)
        json_data = simulation.to_json()
        expected_json = {"number_of_instance": 2, "number_of_instance_created": 0}
        self.assertEqual(json_data, expected_json)

    def test_run_simulation(self):
        # run_simulation fonksiyonu simülasyon döngüsünü doğru şekilde çalıştırıyor mu?
        simulation = LifeCycleSimulation(number_of_instance=2, lifetime_seconds=5)
        self.assertTrue(simulation.run_simulation())  # İlk döngüyü çalıştır
        self.assertEqual(
            simulation.number_of_instance_created, 1
        )  # Bir örnek oluşturuldu
        self.assertTrue(simulation.run_simulation())  # İkinci döngüyü çalıştır
        self.assertEqual(
            simulation.number_of_instance_created, 2
        )  # İkinci örnek oluşturuldu
        self.assertFalse(
            simulation.run_simulation()
        )  # Üçüncü döngüyü çalıştırma, örnek sınırına ulaşıldı

    def test_run_simulation_increment(self):
        # run_simulation fonksiyonu çağrıldıktan sonra number_of_instance_created değeri artıyor mu?
        simulation = LifeCycleSimulation(number_of_instance=2, lifetime_seconds=5)
        self.assertEqual(
            simulation.number_of_instance_created, 0
        )  # Başlangıçta 0 olmalı
        simulation.run_simulation()  # Bir kez çağrıldı
        self.assertEqual(simulation.number_of_instance_created, 1)  # Artık 1 olmalı
        simulation.run_simulation()  # İkinci kez çağrıldı
        self.assertEqual(simulation.number_of_instance_created, 2)  # Artık 2 olmalı

    # Diğer test fonksiyonlarını buraya ekleyin


if __name__ == "__main__":
    unittest.main()
