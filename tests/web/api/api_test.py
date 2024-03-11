# tests/web/app_test.py
import unittest
from src.web.app import create_app
from flask import current_app
from flask.blueprints import Blueprint

# Ensure that create_app returns the app instance directly
app = create_app()


class AppTest(unittest.TestCase):

    def setUp(self):
        # Set up a testing configuration and create a test app
        self.app = app
        self.app.config["TESTING"] = True

    def tearDown(self):
        pass  # Clean up if needed

    def test_api_blueprint_registered(self):
        # Test that the API blueprint is registered with the app
        with self.app.app_context():
            blueprints = [
                bp
                for bp in current_app.blueprints.values()
                if isinstance(bp, Blueprint)
            ]
            blueprint_names = [bp.name for bp in blueprints]
            self.assertIn("api", blueprint_names)

    def test_api_blueprint_v1_registered(self):
        # Test that the "v1" sub-blueprint is registered within the "api" blueprint
        pass

    def test_api_blueprint_v2_registered(self):
        # Test that the "v1" sub-blueprint is registered within the "api" blueprint
        pass


if __name__ == "__main__":
    unittest.main()
