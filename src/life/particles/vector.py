# src/life/particles/vector.py
import math


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

    def __eq__(self, other: "Vector") -> bool:
        """
        Vektörlerin eşitliğini kontrol eder.

        :param other: Diğer vektör.
        :return: Eşitlik durumu.
        """
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False

    def __repr__(self) -> str:
        """
        Vektörün temsilini döndürür.

        :return: Vektörün temsili.
        """
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

    def length(self) -> float:
        """
        Vektörün uzunluğunu hesaplar.

        :return: Vektörün uzunluğu.
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def is_zero(self) -> bool:
        """
        Vektörün sıfır olup olmadığını kontrol eder.

        :return: Vektör sıfırsa True, aksi halde False.
        """
        return self.x == 0 and self.y == 0 and self.z == 0


if __name__ == "__main__":
    # Vektörlerin başlatılması
    v1 = Vector()
    print("Default vector:", v1)

    v2 = Vector(x=1, y=2, z=3)
    print("Custom vector:", v2)

    # JSON'dan vektör oluşturma
    json_data = {"x": 4, "y": 5, "z": 6}
    v3 = Vector.from_json(json_data)
    print("Vector from JSON:", v3)

    # Vektörün toplanması
    v4 = v2 + v3
    print("Addition result:", v4)

    # Vektörün skalerle çarpılması
    v5 = v4 * 2
    print("Multiplication result:", v5)

    # Vektörün uzunluğu
    length = v5.length()
    print("Length of the vector:", length)

    # Sıfır vektör kontrolü
    zero_vector = Vector()
    print("Is v5 zero vector?", v5.is_zero())
    print("Is zero_vector zero vector?", zero_vector.is_zero())
