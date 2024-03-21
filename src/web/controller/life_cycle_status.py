# src/web/controller/life_cycle_status.py
from enum import Enum


class LifeCycleStatus(Enum):
    stopped = "stopped"
    started = "started"
    paused = "paused"
    continues = "continues"
