# src/web/api/v1/time_service.py

from datetime import datetime
from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


class TimeService(Resource):
    def get(self):
        """
        Get the current time.

        This endpoint is used to retrieve the current server time.

        Returns:
            dict: A JSON object with the current time in the format "YYYY-MM-DD HH:MM:SS".
        """
        current_time = datetime.now()
        return {"current_time": current_time.strftime("%Y-%m-%d %H:%M:%S")}


if __name__ == "__main__":
    app.run(debug=True)
