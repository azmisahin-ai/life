class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_json(cls, data):
        return cls(x=data.get("x", 0), y=data.get("y", 0), z=data.get("z", 0))

    def to_json(self):
        return {"x": self.x, "y": self.y, "z": self.z}

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Operand must be a Vector.")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
        elif isinstance(scalar, Vector):
            return Vector(self.x * scalar.x, self.y * scalar.y, self.z * scalar.z)
        else:
            raise TypeError("Scalar must be an integer, a float, or a Vector.")
