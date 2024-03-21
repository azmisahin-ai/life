# src/web/controller/simulation_type.py
from enum import Enum


class SimulationType(Enum):
    LifeCycle = "LifeCycle"
    Particles = "Particles"
    Atoms = "Atoms"
    Molecules = "Molecules"
    Minerals = "Minerals"
    Crystals = "Crystals"
    Cells = "Cells"
    Organisms = "Organisms"
    Textures = "Textures"
    Organs = "Organs"
    Species = "Species"
