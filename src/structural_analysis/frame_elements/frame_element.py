"""
Classes:
    FrameElement
"""

import numpy as np
from structural_analysis.frame_elements.element import Element
from structural_analysis.degree_of_freedom import DegreeOfFreedom


class FrameElement(Element):
    """
    A class to represent a frame element.
    Derived from Element Base class.
    The element has twelve degrees of freedom, three translational
    and three rotational degrees of freedom per each node.

    Methods
    -------
    local_stiffness_matrix(self) -> np.array:
        Represents a 12x12 local stiffness matrix in the local element coordinates.

    element_stiffness_transformation_matrix(self) -> np.ndarray:
        Represents a 12x12 transformation matrix of local stiffness matrix in
        local element coordinates to structure coordinate system.

    degrees_of_freedom(self) -> list[_DegreeOfFreedom]:
        Returns list of the twelve degrees of freedom.

    shape_function_matrix(self, x) -> np.ndarray:
        Returns 3x1 array of local displacements of point,
        at position x, in the local coordinate system.
    """

    def local_stiffness_matrix(self):
        """
        Represents the local stiffness matrix in the local element coordinates.
        """
        le = self._vector.magnitude
        a = self.material.elasticity_modulus * self.section.area / le
        eiz = self.material.elasticity_modulus * self.section.inertia_z
        eiy = self.material.elasticity_modulus * self.section.inertia_y
        bz = 12 * eiz / (le ** 3)
        cz = 6 * eiz / (le ** 2)
        dz = 4 * eiz / le
        ez = 2 * eiz / le
        by = 12 * eiy / (le ** 3)
        cy = 6 * eiy / (le ** 2)
        dy = 4 * eiy / le
        ey = 2 * eiy / le
        t = self.section.polar_inertia*self.material.shear_modulus / le
        return np.array([[a,    0,     0,    0,    0,    0,    -a,   0,    0,    0,    0,    0],
                         [0,    bz,    0,    0,    0,    cz,   0,    -bz,  0,    0,    0,    cz],
                         [0,    0,     by,   0,    -cy,  0,    0,    0,    -by,  0,    -cy,  0],
                         [0,    0,     0,    t,    0,    0,    0,    0,    0,    -t,    0,   0],
                         [0,    0,     -cy,  0,    dy,   0,    0,    0,    cy,   0,    ey,   0],
                         [0,    cz,    0,    0,    0,    dz,   0,    -cz,  0,    0,    0,    ez],
                         [-a,   0,     0,    0,    0,    0,    a,    0,    0,    0,    0,    0],
                         [0,    -bz,   0,    0,    0,    -cz,  0,    bz,   0,    0,    0,    -cz],
                         [0,    0,     -by,  0,    cy,   0,    0,    0,    by,   0,    cy,   0],
                         [0,    0,     0,   -t,    0,    0,    0,    0,    0,    t,    0,    0],
                         [0,    0,     -cy,  0,    ey,   0,    0,    0,    cy,   0,    dy,   0],
                         [0,    cz,    0,    0,    0,    ez,   0,    -cz,  0,    0,    0,    dz]])

    def element_stiffness_transformation_matrix(self):
        """
        Represents the transformation matrix of local stiffness matrix in
        local element coordinates to structure coordinate system.
        """
        transformation_matrix = np.zeros((len(self.degrees_of_freedom), len(self.degrees_of_freedom)))
        for i in range(4):
            transformation_matrix[(i*3):(i+1)*3, (i*3):(i+1)*3] = \
                self._geometry_transformation_matrix()
        return transformation_matrix

    def shape_function_matrix(self, x):
        """
        Returns 3x1 array of local displacements of point,
        at position x, in the local coordinate system.
        """
        le = self.length
        n1 = 1 - x / le
        n2 = x / le
        n3 = 1 - 3 * (x / le) ** 2 + 2 * (x / le) ** 3
        n4 = 3 * (x / le) ** 2 - 2 * (x / le) ** 3
        n5 = x * (1 - x / le) ** 2
        n6 = x * ((x / le) ** 2 - x / le)

        return np.array([[n1,  0,   0,  0,   0,   0,  n2,  0,  0,   0,   0,  0],
                         [0,  n3,   0,  0,   0,  n5,   0, n4,  0,   0,   0,  n6],
                         [0,   0,  n3,  0, -n5,   0,   0,  0, n4,   0, -n6,  0]])

    def shape_function_matrix_concentrated_load(self, location, x) -> np.ndarray:
        a = location
        b = self.length - a
        l = self.length
        v = 1/(self.material.elasticity_modulus * self.section.inertia_z)
        w = 1/(self.material.elasticity_modulus * self.section.inertia_y)
        f = (a*b**2 /l**2 * x**2/2 - b**2 * (3*a + b) / (6*l**3) * x**3) + max(0, (x-a))**3/6
        f2 = a*b/l**3 * x**3 - b*(2*a - b)/(2*l**2) * x**2 - 0.5 * max(0, x-a) ** 2
        n1 = v * f
        n2 = w * f
        n3 = v * f2
        n4 = -w * f2
        matrix = np.array([[0, 0, 0, 0, 0, 0],
                           [0, n1, 0, 0, 0, n3],
                           [0, 0, n2, 0, n4, 0]])
        return matrix

    def shape_function_matrix_distributed_load(self, x) -> np.ndarray:
        l = self.length
        v = 1/(self.material.elasticity_modulus * self.section.inertia_z)
        w = 1/(self.material.elasticity_modulus * self.section.inertia_y)
        f = x**4/24 - l/12 * x**3 + l**2/24 * x**2
        n1 = v*f
        n2 = w*f
        matrix = np.array([[0,  0, 0, 0, 0, 0],
                           [0, n1, 0, 0, 0, 0],
                           [0, 0, n2, 0, 0, 0]])
        return matrix

    @property
    def degrees_of_freedom(self) -> list[DegreeOfFreedom]:
        """
        Returns list of degrees of freedom of start node and end node.
        """
        return self.start_node.degrees_of_freedom + self.end_node.degrees_of_freedom

    def fixed_end_reactions_matrix_concentrated(self, location: float) -> np.ndarray:
        # TODO type hinting of all derived classes
        a = location
        b = self.length - location
        l = self.length
        fixed_end_reactions_matrix = np.array([[-b / l, 0, 0, 0, 0, 0],
                                               [0, -b ** 2 * (3 * a + b) / l ** 3, 0, 0, 0, 6 * a * b / l ** 3],
                                               [0, 0, -b ** 2 * (3 * a + b) / l ** 3, 0, -6 * a * b / l ** 3, 0],
                                               [0, 0, 0, -b / l, 0, 0],
                                               [0, 0, a * b ** 2 / l ** 2, 0, b * (2 * a - b) / l ** 2, 0],
                                               [0, -a * b ** 2 / l ** 2, 0, 0, 0, b * (2 * a - b) / l ** 2],
                                               [-a / l, 0, 0, 0, 0, 0],
                                               [0, -a ** 2 * (a + 3 * b) / l ** 3, 0, 0, 0, -6 * a * b / l ** 3],
                                               [0, 0, -a ** 2 * (a + 3 * b) / l ** 3, 0, 6 * a * b / l ** 3, 0],
                                               [0, 0, 0, -a / l, 0, 0],
                                               [0, 0, -a ** 2 * b / l ** 2, 0, a * (2 * b - a) / l ** 2, 0],
                                               [0, a ** 2 * b / l ** 2, 0, 0, 0, a * (2 * b - a) / l ** 2]])
        return fixed_end_reactions_matrix

    def fixed_end_reactions_matrix_distributed(self) -> np.ndarray:
        l = self.length
        fixed_end_reactions_matrix = np.array([[-l/2, 0, 0, 0, 0, 0],
                                               [0, -l/2, 0, 0, 0, 1],
                                               [0, 0, -l/2, 0, -1, 0],
                                               [0, 0, 0, -l/2, 0, 0],
                                               [0, 0, l**2/12, 0, 0, 0],
                                               [0, -l**2/12, 0, 0, 0, 0],
                                               [-l / 2, 0, 0, 0, 0, 0],
                                               [0, -l / 2, 0, 0, 0, -1],
                                               [0, 0, -l / 2, 0, 1, 0],
                                               [0, 0, 0, -l / 2, 0, 0],
                                               [0, 0, -l ** 2 / 12, 0, 0, 0],
                                               [0, l ** 2 / 12, 0, 0, 0, 0]
                                               ])
        return fixed_end_reactions_matrix

    # def assign_concentrated_load(self, load, location):
    #     reactions = self.fixed_end_reactions_matrix_concentrated(location).dot(load[:])
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.add_concentrated_load_local_displacement_field(load[:], location)
    #     self.fixed_end_reactions += reactions
    #
    # def assign_distributed_load(self, load):
    #     reactions = self.fixed_end_reactions_matrix_distributed().dot(load[:])
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.add_distributed_load_local_displacement_field(load[:])
    #     self.fixed_end_reactions += reactions

    def bending_moment_z(self, x):
        local_end_forces = self.fixed_end_reactions + self.local_end_forces()
        M = local_end_forces[5]
        P = local_end_forces[1]
        value = M - P*x
        for load, location in self.concentrated_loads:
            if not load.local:
                load = load.local_load(self.coordinate_system)
            value += -load.fy * max(x-location, 0)
            if x-location > 0:
                value += load.mz
        for load in self.distributed_loads:
            if not load.local:
                load = load.local_load(self.coordinate_system)
            value += -load.fy*x**2 / 2
            value += load.mz*x
        return value

    def bending_moment_y(self, x):
        local_end_forces = self.fixed_end_reactions + self.local_end_forces()
        M = local_end_forces[4]
        P = local_end_forces[2]
        value = M + P * x
        for load, location in self.concentrated_loads:
            value += load.fz * max(x - load.location, 0)
            if x - load.location > 0:
                value += load.my
        for load in self.distributed_loads:
            value += load.fz * x ** 2 / 2
            value += load.my * x
        return -value

    @staticmethod
    def get_valid_load(load):
        return load
    # def release(self, dofs: [int]):
    #     index = 0
    #     constrained_dofs = []
    #     released_dofs = []
    #     while index < self.local_stiffness_matrix().shape[0]:
    #         if index in dofs:
    #             released_dofs.append(index)
    #         else:
    #             constrained_dofs.append(index)
    #         index += 1
    #
    #     ordered_dofs = constrained_dofs + released_dofs
    #     reordered_stiffness_matrix = np.zeros(self.local_stiffness_matrix().shape)
    #
    #     x = 0
    #     for i in ordered_dofs:
    #         y = 0
    #         for j in ordered_dofs:
    #             reordered_stiffness_matrix[x, y] = self.local_stiffness_matrix()[i, j]
    #             y += 1
    #         x += 1

    @property
    def elastic_geometric_matrix(self):
        """for future use of geometric stiffness matrix"""
        raise NotImplementedError
