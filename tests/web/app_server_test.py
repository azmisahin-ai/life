# tests/web/app_test.py
import os
import unittest
from src.web.app import create_app

# Ensure that create_app returns the app instance directly
app = create_app()


class AppTest(unittest.TestCase):

    def setUp(self):
        try:
            # Get environment variables
            APP_ENV = os.environ.get("APP_ENV")
            self.app_env = APP_ENV

            # set and create
            self.app = app
            self.app.config["ENV"] = self.app_env

            # set client
            self.client = self.app.test_client()

        except Exception as e:
            raise Exception(f"Failed to set up the test environment: {e}")

    def tearDown(self):
        pass  # Clean up if needed

    def test_server_via_http(self):
        # Must be able to connect to the server via http
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertIn("application", data)
        self.assertIn("environment", data)
        self.assertIn("paths", data)

    def test_server_via_https(self):
        # Must be able to connect to the server via https
        response = self.client.get("/", environ_base={"wsgi.url_scheme": "https"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertIn("application", data)
        self.assertIn("environment", data)
        self.assertIn("paths", data)


if __name__ == "__main__":
    unittest.main()
