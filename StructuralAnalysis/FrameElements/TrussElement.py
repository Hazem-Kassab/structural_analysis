import numpy as np
from StructuralAnalysis.FrameElements.Element import Element


class TrussElement(Element):
    """
    This class inherits from Element.
    properties:
        self._degrees_of_freedom: 6 degrees of freedom (3 per node) - 3D element
    """

    def _local_matrix(self):
        axial_rigidity = self.material.elasticity_modulus * self.section.area / self.length
        return axial_rigidity * np.array([[1, -1],
                                          [-1, 1]])

    def _transformation_matrix(self):
        x_diff = self.end_node.x - self.start_node.x
        y_diff = self.end_node.y - self.start_node.y
        z_diff = self.end_node.z - self.start_node.z

        lambda_x = x_diff / self.length
        lambda_y = y_diff / self.length
        lambda_z = z_diff / self.length

        gama_matrix = np.array([lambda_x, lambda_y, lambda_z])
        transformation_matrix = np.zeros((2, 6))
        transformation_matrix[0, 0:3] = gama_matrix
        transformation_matrix[1, 3:6] = gama_matrix
        return transformation_matrix

    def shape_function_matrix(self, x):
        le = self.length
        n1 = 1 - x / le
        n2 = x / le

        return np.array([[n1,  0,   0,  0,   0,   0,  n2,   0,  0,   0,   0,  0],
                         [0,  n1,   0,  0,   0,   0,   0,  n2,  0,   0,   0,  0],
                         [0,   0,  n1,  0,   0,   0,   0,   0,  n2,   0,  0,  0]])

    def local_end_displacements(self):
        global_displacements = np.array([dof.displacement for dof in self.degrees_of_freedom])
        return np.dot(self._transformation_matrix(), global_displacements)

    @property
    def degrees_of_freedom(self):
        return [self.start_node.dof_1,
                self.start_node .dof_2,
                self.start_node.dof_3,
                self.end_node.dof_1,
                self.end_node.dof_2,
                self.end_node.dof_3]

    @property
    def matrix(self):
        return np.dot(np.dot(self._transformation_matrix().T, self._local_matrix()),
                      self._transformation_matrix())

    @property
    def elastic_geometric_matrix(self):
        return None
