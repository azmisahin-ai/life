# tests/web/api/v1/simulation_stop_test.py

import os
import unittest
from src.web.app import create_app

# Ensure that create_app returns the app instance directly
app = create_app()


class SimulationStopTest(unittest.TestCase):
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

    def test_simulation_stop_endpoint(self):
        # Test the simulation_continue endpoint
        response = self.client.get("/api/v1/simulation_stop")
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "stopped")


if __name__ == "__main__":
    unittest.main()
