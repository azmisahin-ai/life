# src/life/particles/vector.py
class Vector:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """
        Vector sınıfını başlatır.

        :param x: X bileşeni.
        :param y: Y bileşeni.
        :param z: Z bileşeni.
        """
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_json(cls, data: dict) -> "Vector":
        """
        JSON verisinden bir vektör oluşturur.

        :param data: JSON verisi.
        :return: Vector nesnesi.
        """
        return cls(x=data.get("x", 0), y=data.get("y", 0), z=data.get("z", 0))

    def to_json(self) -> dict:
        """
        Vektörü JSON formatına dönüştürür.

        :return: JSON verisi.
        """
        return {"x": self.x, "y": self.y, "z": self.z}

    def __add__(self, other: "Vector") -> "Vector":
        """
        Vektörlerin toplamını hesaplar.

        :param other: Diğer vektör.
        :return: Toplam vektörü.
        """
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Operand must be a Vector.")

    def __mul__(self, scalar: float) -> "Vector":
        """
        Vektörü bir skalerle çarpar.

        :param scalar: Skaler değer.
        :return: Çarpım sonucu vektör.
        """
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
        elif isinstance(scalar, Vector):
            return Vector(self.x * scalar.x, self.y * scalar.y, self.z * scalar.z)
        else:
            raise TypeError("Scalar must be an integer, a float, or a Vector.")
