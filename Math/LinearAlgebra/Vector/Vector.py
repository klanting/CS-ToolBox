import math
from abc import abstractmethod
from Math.LinearAlgebra.Matrix.Matrix import Matrix


class NormType:

    @staticmethod
    @abstractmethod
    def calculate_norm(vector: "Vector"):
        pass


class NormOne(NormType):

    @staticmethod
    def calculate_norm(vector: "Vector") -> float:

        summed = 0
        for value in vector.get_elements():
            summed += abs(value)

        return summed


class NormTwo(NormType):

    @staticmethod
    def calculate_norm(vector: "Vector") -> float:

        temp_vector = vector.get_transpose()*vector

        return math.sqrt(temp_vector.get_elements()[0])


class NormInf(NormType):

    @staticmethod
    def calculate_norm(vector: "Vector") -> float:
        highest_abs = 0
        for value in vector.get_elements():
            highest_abs = max(highest_abs, abs(value))

        return highest_abs


class Vector(Matrix):
    def __init__(self, complex_numbers: list[complex]):

        super(Vector, self).__init__(complex_numbers)

    def norm(self, norm_type: NormType):
        return norm_type.calculate_norm(self)

    def get_elements(self):
        return self.complex_array

    def get_transpose(self) -> Matrix:

        return Matrix([self.get_elements()])


if __name__ == "__main__":
    v1 = Vector([1, 1, 0])

    assert 2 == v1.norm(NormOne())

    assert 1.41 == round(v1.norm(NormTwo()), 2)

    assert 1 == v1.norm(NormInf())
