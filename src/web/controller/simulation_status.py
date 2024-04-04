# src/web/controller/simulation_status.py
from enum import Enum


class SimulationStatus(Enum):
    Running = "Running"
    Paused = "Paused"
    Resumed = "Resumed"
    Stopped = "Stopped"
