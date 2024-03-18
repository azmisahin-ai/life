# tests/web/api/v1/simulation_start_test.py

import os
import unittest
from src.web.app import create_app

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
        # Test the simulation_start endpoint
        test_data = {"number_of_particles": 100, "time_step": 0.1}

        response = self.client.post("/api/v1/simulation_start", json=test_data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "started")
        self.assertEqual(
            response_data["number_of_particles"], test_data["number_of_particles"]
        )
        self.assertEqual(response_data["time_step"], test_data["time_step"])


if __name__ == "__main__":
    unittest.main()
