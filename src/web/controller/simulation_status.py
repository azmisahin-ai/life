from enum import Enum


class SimulationStatus(Enum):
    stopped = "stopped"
    started = "started"
    paused = "paused"
    continues = "continues"
