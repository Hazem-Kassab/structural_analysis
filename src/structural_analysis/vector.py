"""
Classes:
    Vector
"""

from __future__ import annotations
import math
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from structural_analysis.coordinate_system import CoordinateSystem


class Vector(np.ndarray):
    """
    A class to represent a vector.
    ...

    Attributes
    ----------
    array : list[float]
        list of size 3 holding i, j, k values of the vector instance

    _coordinate_system : CoordinateSystem
        coordinate system used to describe vector components (i, j, k)

    Methods
    -------
    transform_vector(coordinate_system: CoordinateSystem):
        returns a new transformed vector instance in the new coordinate system

    magnitude:
        returns the magnitude of the vector

    normalized:
        returns a new normalized vector instance

    project_vector_on_vector(vector: Vector):
        returns a new vector instance projected on the passed vector instance

    project_vector_on_vector_scaler(vector: Vector):
        returns a signed magnitude of vector projected on the passed vector instance

    project_vector_on_plane(vector: Vector):
        returns a new vector instance projected on a plane having the passed normal vector instance
    """

    def __new__(cls, array: list[float]):
        array = [float(x) for x in array]
        return super().__new__(cls, shape=(3,), buffer=np.array(array), dtype=float)

    def __init__(self, array: list[float]):
        super().__init__()
        self.array = array
        self._coordinate_system = None

    def transform_vector(self, coordinate_system: CoordinateSystem) -> Vector:
        """returns a new transformed vector instance in the new coordinate system.

            Keyword arguments:
            coordinate_system -- the coordinate system which the vector transforms to.
        """
        return Vector(self.coordinate_system.get_coordinate_transformation_matrix(coordinate_system).dot(self))

    @property
    def magnitude(self) -> float:
        """returns the magnitude of the vector."""
        return math.sqrt(self.dot(self))

    @property
    def normalized(self) -> Vector:
        """returns a new normalized vector instance."""
        return Vector(1 / np.sqrt(self.dot(self)) * self)

    def project_vector_on_vector(self, vector: Vector) -> Vector:
        """returns a new vector instance projected on the passed vector instance
            Keyword arguments:
                vector -- a vector instance to project on.
        """
        projection_magnitude = self.dot(vector) / vector.magnitude
        return Vector(projection_magnitude * vector.normalized)

    def project_vector_on_vector_scaler(self, vector_2: Vector):
        """returns a signed magnitude of vector projected on the passed vector instance
            Keyword arguments:
                vector -- a vector instance to project on.
        """
        return self.dot(vector_2.normalized)

    def project_vector_on_plane(self, plane_normal: Vector) -> Vector:
        """returns a new vector instance projected on
        a plane having the passed normal vector instance
            Keyword arguments:
                plane_normal -- a vector normal to plane.
        """
        return Vector(np.subtract(self, self.project_vector_on_vector(plane_normal)))

    @property
    def coordinate_system(self) -> CoordinateSystem:
        """coordinate system used to describe vector components (i, j, k)"""
        return self._coordinate_system

    @coordinate_system.setter
    def coordinate_system(self, value: CoordinateSystem):
        self._coordinate_system = value
