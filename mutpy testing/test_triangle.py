from triangle import *
from unittest import TestCase


class TestTriangle(TestCase):
    def test_triangle_type_error(self):
        self.assertEqual(check_triangle("a", 1, 2), False)

    def test_triangle_zero_weight(self):
        self.assertEqual(check_triangle(0, 0, 0), False)

    def test_triangle_1(self):
        self.assertEqual(check_triangle(1, 2, 4), False)

    def test_triangle_2(self):
        self.assertEqual(check_triangle(1, 2, 3), False)
        self.assertEqual(check_triangle(1, 3, 2), False)
        self.assertEqual(check_triangle(3, 1, 2), False)

    def test_triangle_3(self):
        self.assertEqual(check_triangle(3, 4, 5), True)

    def test_triangle_4(self):
        self.assertEqual(check_triangle(2.0, 3.0, 4.0), True)

    def test_triangle_5(self):
        self.assertEqual(check_triangle(5, 6.0, 7.0), True)

    def test_triangle_6(self):
        self.assertEqual(check_triangle(1, 2, 2), True)
