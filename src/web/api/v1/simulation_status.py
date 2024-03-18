# src/web/api/v1/simulation_status.py

from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


class SimulationStatus(Resource):
    def get(self):
        """
        Status the simulation.
        """
        return {
            "status": "continues",
            "particle": {
                "name": "Particle",
                "charge": -1.602176634e-19,
                "mass": 9.10938356e-31,
                "spin": 0.5,
                "lifetime": -1,
                "energy": 0,
                "position": {"x": 0, "y": 0, "z": 0},
                "velocity": {"x": 0, "y": 0, "z": 0},
                "momentum": {"x": 0, "y": 0, "z": 0},
            },
        }


if __name__ == "__main__":
    app.run(debug=True)
