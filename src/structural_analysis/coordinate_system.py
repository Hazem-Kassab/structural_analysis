"""
Classes:
    CoordinateSystem
"""

from __future__ import annotations
from structural_analysis.vector import Vector
import math
import numpy as np


class CoordinateSystem:
    """
    A class to represent a cartesian coordinate system.
    ...

    Attributes
    ----------
    _i : structural_analysis.Vector
        the i component of the coordinate system basis

    _j : structural_analysis.Vector
        the j component of the coordinate system basis

    _k : structural_analysis.Vector
        the k component of the coordinate system basis

    basis : numpy.ndarray
        a 3x3 numpy array holding the basis vectors [i, j, k]

    origin : structural_analysis.Vector
        the position vector of the origin of the coordinate system

    _global_i_vector:
        the i base vector described in a global coordinate system

    _global_twist_angle:
        the rotation angle of the coordinate_system around the i base vector

    Methods
    -------
    _get_rotation_matrix_around_vector(angle: float, rotation_axis: Vector) -> np.ndarray:
        static method, returns a 3x3 rotation matrix around the passed rotation axis vector with angle

    get_coord_transformation_matrix(self, coordinate_system: CoordinateSystem) -> np.ndarray:
        returns a 3x3 transformation matrix from the calling
        coordinate system to passed coordinate system instance
    """

    Global_i = Vector([1, 0, 0])
    Global_j = Vector([0, 1, 0])
    Global_k = Vector([0, 0, 1])

    def __init__(self, i_vector: Vector, twist_angle: float,
                 origin_vector: Vector):
        self._global_i_vector = i_vector
        self._global_twist_angle = twist_angle
        # self._i = Vector(self.global_transformation_matrix().dot(Vector([1, 0, 0])))
        # self._j = Vector(self.global_transformation_matrix().dot(Vector([0, 1, 0])))
        # self._k = Vector(self.global_transformation_matrix().dot(Vector([0, 0, 1])))
        # self.basis = np.array([self._i, self._j, self._k])
        self.origin = origin_vector

    @staticmethod
    def _get_rotation_matrix_around_vector(rotation_axis: Vector, angle: float) -> np.ndarray:
        """returns a 3x3 rotation matrix around the passed rotation axis vector
            Keyword arguments:
                rotation_axis -- vector which the rotation is around.
                angle -- amount of rotation in degrees.
        """
        i = rotation_axis.normalized[0]
        j = rotation_axis.normalized[1]
        k = rotation_axis.normalized[2]
        cos = math.cos(angle*math.pi/180)
        sin = math.sin(angle*math.pi/180)
        transformation_matrix = np.array([[cos + i**2 * (1-cos), i*j*(1-cos) - k*sin, i*k*(1-cos) + j*sin],
                                          [j*i*(1-cos) + k*sin, cos + j**2 * (1-cos), j*k*(1-cos) - i*sin],
                                          [k*i*(1-cos) - j*sin, k*j*(1-cos) + i*sin, cos + k**2*(1-cos)]])
        return transformation_matrix

    def get_global_coord_transformation_matrix(self) -> np.ndarray:
        """returns a 3x3 transformation matrix from the calling
        coordinate system to passed coordinate system instance
            Keyword arguments:
                coordinate_system -- coordinate system which objects will transform to.
        """
        vector_projection_on_xz = self._global_i_vector.project_vector_on_plane(CoordinateSystem.Global_j)
        vector_projection_on_x = self._global_i_vector.project_vector_on_vector_scaler(CoordinateSystem.Global_i)
        vector_projection_on_y = self._global_i_vector.project_vector_on_vector_scaler(CoordinateSystem.Global_j)
        vector_projection_on_z = self._global_i_vector.project_vector_on_vector_scaler(CoordinateSystem.Global_k)
        beta = math.degrees(math.atan2(vector_projection_on_x, vector_projection_on_z)) - 90
        if vector_projection_on_xz.magnitude == 0:
            beta = 0
            if vector_projection_on_y > 0:
                alpha = 90
            else:
                alpha = -90
        else:
            alpha = math.degrees(math.atan(vector_projection_on_y /
                                           vector_projection_on_xz.magnitude))
        rotation_1 = CoordinateSystem._get_rotation_matrix_around_vector(self.Global_i, self._global_twist_angle)
        rotation_2 = CoordinateSystem._get_rotation_matrix_around_vector(self.Global_k, alpha)
        rotation_3 = CoordinateSystem._get_rotation_matrix_around_vector(self.Global_j, beta)
        return rotation_3.dot(rotation_2.dot(rotation_1)).T

    def get_coordinate_transformation_matrix(self, coordinate_system: CoordinateSystem):
        return coordinate_system.get_global_coord_transformation_matrix().\
            dot(self.get_global_coord_transformation_matrix().T)

    @property
    def transformed_i(self):
        return self.get_global_coord_transformation_matrix().dot(Vector([1, 0, 0]))

    @property
    def transformed_j(self):
        return self.get_global_coord_transformation_matrix().dot(Vector([0, 1, 0]))

    @property
    def transformed_k(self):
        return self.get_global_coord_transformation_matrix().dot(Vector([0, 0, 1]))

    @property
    def transformed_basis(self):
        return np.array([self.transformed_i, self.transformed_j, self.transformed_k])


Global_Coordinate_System = CoordinateSystem(Vector([1, 0, 0]), 0, Vector([0, 0, 0]))

# vector_1 = np.array([1, 0, 0]).transpose()
# cs = CoordinateSystem()
#
# vector_2a = cs.rotate(vector_1, 45, BasisVector.k)
# vector_3a = cs.rotate(vector_2a, -90, BasisVector.i)
#
# vector_2b = cs.rotate_about_vector(45, np.array([0, 0, 5]), vector_1)
# vector_3b = cs.rotate_about_vector(-90, np.array([5, 0, 0]), vector_2b)
# print(vector_3b == vector_3b)

# app = QtGui.QApplication([])
# w = gl.GLViewWidget()
# w.setGeometry(50, 100, 700, 700)
# gz = gl.GLGridItem()
# size = 5
# gz.setSize(size, size, size)
# spacing = 1/5
# gz.setSpacing(spacing, spacing, spacing)
# w.addItem(gz)
# axis = gl.GLAxisItem()
# size = 1 / 5
# axis.setSize(size, size, size)
# axis.rotate(90, 0, 0, 90)
# axis.rotate(90, 0, 90, 0)
# w.addItem(axis)
#
# first_pt = np.array([0, 0, 0])
# second_pt = np.array([1, 0, 0])
# third_pt = np.array([0, 1, 0])
# fourth_pt = np.array([0, 0, 1])
# final_vector = np.array([-1, -1, 1])
# # angle = CoordinateSystem.angle(second_pt, final_vector)
# # angles = cs.cal_rotation_matrix(final_vector, 0)
# # print(angles[0])
# second_pt = cs.cal_transformation(final_vector, 0, cs).dot(second_pt)
# third_pt = cs.cal_transformation(final_vector, 0, cs).dot(third_pt)
# fourth_pt = cs.cal_transformation(final_vector, 0, cs).dot(fourth_pt)
#
# vector = np.array([first_pt, second_pt, first_pt, third_pt, first_pt, fourth_pt])
# plt = gl.GLLinePlotItem(pos=vector, color='w', width=2, antialias=True)
# plt.rotate(angle=90, x=90, y=0, z=0)
# plt.rotate(angle=90, x=0, y=0, z=90)
# w.addItem(plt)
# w.show()
# QtGui.QApplication.instance().exec_()
