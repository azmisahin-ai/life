# tests/life/particle/vector_test.py

import unittest
from src.life.particles.vector import Vector


class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector(1, 2, 3)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_from_json(self):
        json_data = {"x": 1, "y": 2, "z": 3}
        v = Vector.from_json(json_data)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_to_json(self):
        v = Vector(1, 2, 3)
        json_data = v.to_json()
        self.assertEqual(json_data, {"x": 1, "y": 2, "z": 3})

    def test_add(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = v1 + v2
        self.assertEqual(result, Vector(5, 7, 9))

    def test_mul_scalar(self):
        v = Vector(1, 2, 3)
        result = v * 2
        self.assertEqual(result, Vector(2, 4, 6))

    def test_mul_vector(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        result = v1 * v2
        self.assertEqual(result, Vector(2, 6, 12))

    def test_eq(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2, 3)
        self.assertEqual(v1, v2)

    def test_repr(self):
        v = Vector(1, 2, 3)
        self.assertEqual(repr(v), "Vector(x=1, y=2, z=3)")

    def test_length(self):
        v = Vector(3, 4, 0)
        self.assertEqual(v.length(), 5)

    def test_is_zero(self):
        v = Vector(0, 0, 0)
        self.assertTrue(v.is_zero())


if __name__ == "__main__":
    unittest.main()
