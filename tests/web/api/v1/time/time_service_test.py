# tests/web/api/v1/test_time_service.py
import unittest
from src.web.api.v1.time.time_service import TimeService


class TimServiceTest(unittest.TestCase):

    def test_get_current_time(self):
        time_service = TimeService()
        response = time_service.get()

        assert "current_time" in response
        assert isinstance(response["current_time"], str)


if __name__ == "__main__":
    unittest.main()
