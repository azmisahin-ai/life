# tests/web/controller/particle_simulation_test.py
import unittest
from src.web.controller.particle_simulation import (
    ParticleSimulation,
)


class TestParticleSimulation(unittest.TestCase):
    def test_initialization(self):
        """
        Parçacık yaşam döngüsü simülasyonunun başlatılmasını test et.
        """
        number_of_instance = 2
        lifetime_seconds = 5

        simulation = ParticleSimulation(number_of_instance, lifetime_seconds)

        self.assertEqual(simulation.number_of_instance, number_of_instance)
        self.assertEqual(simulation.lifetime_seconds, lifetime_seconds)
        self.assertEqual(simulation.number_of_instance_created, 0)
        self.assertIsNone(simulation.last_item)
        self.assertIsNone(simulation.event_function)

    def test_create_instance(self):
        """
        Parçacık örneği oluşturma işlevini test et.
        """
        number_of_instance = 2
        lifetime_seconds = 5

        simulation = ParticleSimulation(number_of_instance, lifetime_seconds)

        # create_instance yöntemi çağrıldığında son öğenin oluşturulması gerektiğini doğrula
        simulation.create_instance()

        # number_of_instance_created özelliğinin arttığını doğrula
        self.assertEqual(simulation.number_of_instance_created, 1)

    def test_run_simulation(self):
        """
        Simülasyonun doğru çalıştığını test et.
        """
        number_of_instance = 2
        lifetime_seconds = 5

        simulation = ParticleSimulation(number_of_instance, lifetime_seconds)

        # run_simulation çağrıldığında bir parçacık örneğinin oluşturulduğunu doğrula
        self.assertTrue(simulation.run_simulation())
        self.assertEqual(simulation.number_of_instance_created, 1)

        # İkinci bir run_simulation çağrısının da bir parçacık örneği oluşturması gerektiğini doğrula
        self.assertTrue(simulation.run_simulation())
        self.assertEqual(simulation.number_of_instance_created, 2)

        # number_of_instance sayısına ulaştığında run_simulation'ın False döndürmesi gerektiğini doğrula
        self.assertFalse(simulation.run_simulation())


if __name__ == "__main__":
    unittest.main()
