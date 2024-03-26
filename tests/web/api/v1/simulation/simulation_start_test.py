# tests/web/api/v1/simulation_start_test.py

import os
import unittest
from src.web.app import create_app
from src.web.controller.simulation_type import SimulationType

# Ensure that create_app returns the app instance directly
app = create_app()


class SimulationStartTest(unittest.TestCase):
    def setUp(self):
        try:
            # Get environment variables
            APP_ENV = os.environ.get("APP_ENV")

            # set
            self.app_env = APP_ENV

            # create app
            self.app = app
            self.app.config["ENV"] = self.app_env
            self.client = self.app.test_client()

        except Exception as e:
            raise Exception(f"Failed to set up the test environment: {e}")

    def tearDown(self):
        pass  # Clean up if needed

    def test_simulation_start_endpoint(self):
        # request
        number_of_instance = 3  # oluşturulacak örnek sayısı
        lifetime_seconds = float("inf")  # Parçacığın yaşam süresi saniye cinsinden.
        lifecycle = 60 / 1  # Parçacığın saniyedeki yaşam döngüsü.
        simulation_type = SimulationType.Particles  # Simulaston türü
        # init data
        data = {
            "number_of_instance": number_of_instance,
            "lifetime_seconds": lifetime_seconds,
            "lifecycle": lifecycle,
            "simulation_type": simulation_type.value,
        }

        response = self.client.post("/api/v1/simulation/start", json=data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["simulation_status"], "started")


if __name__ == "__main__":
    unittest.main()
