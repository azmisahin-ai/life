# tests/web/app_test.py
import unittest
from src.web.app import create_app

# Ensure that create_app returns the app instance directly
app, _, _, _ = create_app()


class AppTest(unittest.TestCase):

    def test_home_endpoint(self):
        client = app.test_client(self)
        response = client.get("/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
        self.assertIn("application", data)
        self.assertIn("environment", data)


if __name__ == "__main__":
    unittest.main()
