"""
Classes:
    TwoDimensionalFrameElement
"""

import numpy as np
from structural_analysis.frame_elements.element import Element


class TwoDimensionalFrameElement(Element):
    """
    A class to represent a frame element in 2-d space.
    Derived from Element Base class.
    The element has six degrees of freedom, two translational
    and one rotational degrees of freedom per each node.

    Methods
    -------
    local_stiffness_matrix(self) -> np.array:
        Represents a 2x2 local stiffness matrix in the local element coordinates.

    element_stiffness_transformation_matrix(self) -> np.ndarray:
        Represents a 6x6 transformation matrix of local stiffness matrix in
        local element coordinates to structure coordinate system.

    degrees_of_freedom(self) -> list[_DegreeOfFreedom]:
        Returns list of the six degrees of freedom.

    shape_function_matrix(self, x) -> np.ndarray:
        Returns 3x1 array of local displacements of point,
        at position x, in the local coordinate system.
    """
    def local_stiffness_matrix(self):
        """
        Represents the local stiffness matrix in the local element coordinates.
        """
        le = self.length
        a = self.material.elasticity_modulus * self.section.area / le
        ei = self.material.elasticity_modulus * self.section.inertia_z
        b = 12*ei/(le**3)
        c = 6*ei/(le**2)
        d = 4*ei/le
        e = 2*ei/le
        return np.array([[a, 0, 0, -a, 0, 0],
                        [0, b, c, 0, -b, c],
                        [0, c, d, 0, -c, e],
                        [-a, 0, 0, a, 0, 0],
                        [0, -b, -c, 0, b, -c],
                        [0, c, e, 0, -c, d]])

    def element_stiffness_transformation_matrix(self):
        """
        Represents the transformation matrix of local stiffness matrix in
        local element coordinates to structure coordinate system.
        """
        gama_matrix = self._geometry_transformation_matrix()
        transformation_matrix = np.zeros((6, 6))
        transformation_matrix[0:3, 0:3] = gama_matrix
        transformation_matrix[3:7, 3:7] = gama_matrix
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

        return np.array([[n1, 0, 0, 0, 0, 0, n2, 0, 0, 0, 0, 0],
                        [0, n3, 0, 0, 0, n5, 0, n4, 0, 0, 0, n6],
                        [0]*12])

    @property
    def degrees_of_freedom(self):
        """
        Returns list of degrees of freedom of start node and end node.
        """
        return [self.start_node.dof_x,
                self.start_node.dof_y,
                self.start_node.dof_rz,
                self.end_node.dof_x,
                self.end_node.dof_y,
                self.end_node.dof_rz]

    def fixed_end_reactions_matrix_concentrated(self, location: float) -> np.ndarray:
        a = location
        b = self.length - location
        l = self.length
        fixed_end_reactions_matrix = np.array([[-b / l, 0, 0],
                                               [0, -b ** 2 * (3 * a + b) / l ** 3, 6 * a * b / l ** 3],
                                               [0, -a * b ** 2 / l ** 2, b * (2 * a - b) / l ** 2],
                                               [-a / l, 0, 0],
                                               [0, -a ** 2 * (a + 3 * b) / l ** 3, -6 * a * b / l ** 3],
                                               [0, a ** 2 * b / l ** 2, a * (2 * b - a) / l ** 2]])
        return fixed_end_reactions_matrix

    def fixed_end_reactions_matrix_distributed(self) -> np.ndarray:
        l = self.length
        fixed_end_reactions_matrix = np.array([[-l / 2, 0, 0],
                                               [0, -l / 2, 1],
                                               [0, -l ** 2 / 12, 0],
                                               [-l / 2, 0, 0],
                                               [0, -l / 2, -1],
                                               [0, l ** 2 / 12, 0]])
        return fixed_end_reactions_matrix

    # def assign_concentrated_load(self, load, location):
    #     applied_load = np.append(load[0:2], load[-1])
    #     reactions = self.fixed_end_reactions_matrix_concentrated(location).dot(applied_load)
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.add_concentrated_load_local_displacement_field(applied_load, location)
    #     self.fixed_end_reactions += reactions
    #
    # def assign_distributed_load(self, load: np.ndarray):
    #     applied_load = np.append(load[0:2], load[-1])
    #     reactions = self.fixed_end_reactions_matrix_distributed().dot(applied_load)
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.add_distributed_load_local_displacement_field(applied_load)
    #     self.fixed_end_reactions += reactions

    def shape_function_matrix_concentrated_load(self, location, x) -> np.ndarray:
        a = location
        b = self.length - a
        l = self.length
        v = 1 / (self.material.elasticity_modulus * self.section.inertia_z)
        f = (a * b ** 2 / l ** 2 * x ** 2 / 2 - b ** 2 * (3 * a + b) / (6 * l ** 3) * x ** 3) + max(0, (x - a)) ** 3 / 6
        f2 = a * b / l ** 3 * x ** 3 - b * (2 * a - b) / (2 * l ** 2) * x ** 2 - 0.5 * max(0, x - a) ** 2
        n1 = v * f
        n3 = v * f2
        matrix = np.array([[0, 0, 0],
                           [0, n1, n3],
                           [0, 0, 0]])
        return matrix

    def shape_function_matrix_distributed_load(self, x) -> np.ndarray:
        l = self.length
        v = 1 / (self.material.elasticity_modulus * self.section.inertia_z)
        f = x ** 4 / 24 - l / 12 * x ** 3 + l ** 2 / 24 * x ** 2
        n1 = v * f
        matrix = np.array([[0, 0, 0],
                           [0, n1, 0],
                           [0, 0, 0]])
        return matrix

    @staticmethod
    def get_valid_load(load):
        return load[0:2] + [load[-1]]

    @property
    def elastic_geometric_matrix(self):
        """for future use of geometric stiffness matrix"""
        return None
