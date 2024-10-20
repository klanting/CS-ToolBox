
class Vector:
    def get_elements(self):
        pass


class Matrix:
    def __init__(self, complex_array: list):

        self.dimensions = []

        current_array_subset = complex_array

        while isinstance(current_array_subset, list):
            self.dimensions.append(len(current_array_subset))
            current_array_subset = current_array_subset[0]

        self.complex_array = complex_array

    def get_dimensions(self):
        return self.dimensions

    def __mul__(self, other: Vector) -> Vector:
        assert len(self.dimensions) == 2

        result_values = []

        for row in self.complex_array:

            result = 0

            for i, el in enumerate(row):

                v_el = other.get_elements()[i]

                result += el*v_el

            result_values.append(result)

        return Vector(result_values)

from Math.LinearAlgebra.Vector.Vector import Vector
