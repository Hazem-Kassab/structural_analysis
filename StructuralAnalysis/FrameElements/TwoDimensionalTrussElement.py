import numpy as np
from StructuralAnalysis.FrameElements.Element import Element


class TwoDimensionalTrussElement(Element):
    """
    This class inherits from Element.
    properties:
        self._degrees_of_freedom: 4 degrees of freedom (2 per node) - 2D element
    """

    def __init__(self, start_node, end_node, section, material):
        start_node.z = 0
        end_node.z = 0
        super().__init__(start_node, end_node, section, material)

    def _local_matrix(self):
        axial_rigidity = self.material.elasticity_modulus * self.section.area / self.length
        return axial_rigidity * np.array([[1, -1],
                                         [-1, 1]])

    def _transformation_matrix(self):
        x_diff = self.end_node.x - self.start_node.x
        y_diff = self.end_node.y - self.start_node.y

        lambda_x = x_diff / self.length
        lambda_y = y_diff / self.length
        return np.array([[lambda_x, lambda_y, 0, 0],
                         [0, 0, lambda_x, lambda_y]])

    def shape_function_matrix(self, x):
        le = self.length
        n1 = 1 - x / le
        n2 = x / le
        return np.array([[n1, 0, 0, 0, 0, 0, n2, 0, 0, 0, 0, 0],
                         [0, n1, 0, 0, 0, 0, 0, n2, 0, 0, 0, 0]])

    def local_end_displacements(self):
        global_displacements = np.array([dof.displacement for dof in self.degrees_of_freedom])
        return np.dot(self._transformation_matrix(), global_displacements)

    @property
    def degrees_of_freedom(self):
        return [self.start_node.dof_1,
                self.start_node.dof_2,
                self.end_node.dof_1,
                self.end_node.dof_2]

    @property
    def matrix(self):
        return np.dot(np.dot(self._transformation_matrix().T, self._local_matrix()),
                      self._transformation_matrix())

    @property
    def elastic_geometric_matrix(self):
        return None
