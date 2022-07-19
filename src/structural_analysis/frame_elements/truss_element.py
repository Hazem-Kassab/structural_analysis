"""
Classes:
    TrussElement
"""

import numpy as np
from structural_analysis.frame_elements.element import Element


class TrussElement(Element):
    """
    A class to represent a truss element.
    Derived from Element Base class.
    The element has six translational degrees of freedom, three per each node.

    Methods
    -------
    local_stiffness_matrix(self) -> np.array:
        Represents a 2x2 local stiffness matrix in the local element coordinates.

    element_stiffness_transformation_matrix(self) -> np.ndarray:
        Represents a 2x6 transformation matrix of local stiffness matrix in
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
        axial_rigidity = self.material.elasticity_modulus * self.section.area / self.length
        return axial_rigidity * np.array([[1, -1],
                                          [-1, 1]])

    def element_stiffness_transformation_matrix(self):
        """
        Represents the transformation matrix of local stiffness matrix in
        local element coordinates to structure coordinate system.
        """
        gama_matrix = self._geometry_transformation_matrix()[0]
        transformation_matrix = np.zeros((2, 6))
        transformation_matrix[0, 0:3] = gama_matrix
        transformation_matrix[1, 3:6] = gama_matrix
        return transformation_matrix

    def shape_function_matrix(self, x):
        """
        Returns 3x1 array of local displacements of point,
        at position x, in the local coordinate system.
        """
        le = self.length
        n1 = 1 - x / le
        n2 = x / le

        return np.array([[n1,  0,   0,  0,   0,   0,  n2,   0,  0,   0,   0,  0],
                         [0,  n1,   0,  0,   0,   0,   0,  n2,  0,   0,   0,  0],
                         [0,   0,  n1,  0,   0,   0,   0,   0,  n2,   0,  0,  0]])

    @property
    def degrees_of_freedom(self):
        """
        Returns list of degrees of freedom of start node and end node.
        """
        return self.start_node.degrees_of_freedom[0:3] + self.end_node.degrees_of_freedom[0:3]

    def fixed_end_reactions_matrix_concentrated(self, location: float) -> np.ndarray:
        a = location
        b = self.length - location
        l = self.length
        fixed_end_reactions_matrix = np.array([-b/l, -a/l]).T
        return fixed_end_reactions_matrix

    def fixed_end_reactions_matrix_distributed(self) -> np.ndarray:
        l = self.length
        fixed_end_reactions_matrix = np.array([-l/2, -l/2]).T
        return fixed_end_reactions_matrix

    # def assign_concentrated_load(self, load, location):
    #     reactions = self.fixed_end_reactions_matrix_concentrated(location).dot(load[0])
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.fixed_end_reactions += reactions
    #
    # def assign_distributed_load(self, load: np.ndarray):
    #     reactions = self.fixed_end_reactions_matrix_distributed().dot(load[0])
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.fixed_end_reactions += reactions

    def shape_function_matrix_distributed_load(self, x) -> np.ndarray:
        pass

    def shape_function_matrix_concentrated_load(self, location, x) -> np.ndarray:
        pass

    def bending_moment_y(self, x):
        pass

    def bending_moment_z(self, x):
        pass

    @staticmethod
    def get_valid_load(load):
        return load[0]

    @property
    def elastic_geometric_matrix(self):
        """for future use of geometric stiffness matrix"""
        return None
