# src/web/api/v1/simulation_pause.py

from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


class SimulationPause(Resource):
    def get(self):
        """
        Pause the simulation.
        """
        return {"status": "paused"}


if __name__ == "__main__":
    app.run(debug=True)
