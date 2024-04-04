# src/life/atoms/uranium.py


from src.life.particles.particle import Particle


class Quark(Particle):
    def __init__(self, name, charge, mass, flavor):
        super().__init__(name, charge, mass)
        self.flavor = flavor


class Lepton(Particle):
    def __init__(self, name, charge, mass):
        super().__init__(name, charge, mass)


class Electron(Lepton):
    def __init__(self):
        super().__init__("Electron", -1, 9.10938356e-31)  # Elektronun yükü ve kütlesi


class Muon(Lepton):
    def __init__(self):
        super().__init__("Muon", -1, 1.883531594e-28)  # Muonun yükü ve kütlesi


class Tau(Lepton):
    def __init__(self):
        super().__init__("Tau", -1, 3.16747e-27)  # Tau parçacığının yükü ve kütlesi


class Neutrino(Particle):
    def __init__(self, name, charge, mass):
        super().__init__(name, charge, mass)


class Hadron(Particle):
    def __init__(self, name, charge, mass):
        super().__init__(name, charge, mass)


class Proton(Hadron):
    def __init__(self):
        super().__init__("Proton", 1, 1.67262192369e-27)  # Protonun yükü ve kütlesi


class Neutron(Hadron):
    def __init__(self):
        super().__init__("Neutron", 0, 1.67492749804e-27)  # Nötronun yükü ve kütlesi


class Meson(Hadron):
    def __init__(self, name, charge, mass):
        super().__init__(name, charge, mass)


# Uranium atomunun oluşturulması
class Uranium:
    def __init__(self):
        self.protons = [Proton() for _ in range(92)]  # 92 proton
        self.neutrons = [Neutron() for _ in range(146)]  # Yaklaşık 146 nötron
        self.electrons = [Electron() for _ in range(92)]  # 92 elektron

    def __str__(self):
        return f"Uranium Atomu: Proton sayısı - {len(self.protons)}, Nötron sayısı - {len(self.neutrons)}, Elektron sayısı - {len(self.electrons)}"


# Uranium atomunu oluşturma
uranium_atom = Uranium()

# Atomun özelliklerini yazdırma
print(uranium_atom)
