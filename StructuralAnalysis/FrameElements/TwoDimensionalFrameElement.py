import numpy as np
from StructuralAnalysis.FrameElements.Element import Element


class TwoDimensionalFrameElement(Element):
    """
    This class inherits from Element.
    properties:
        self._degrees_of_freedom: 6 degrees of freedom (3 per node) - 2D element
    """

    def __init__(self, start_node, end_node, section, material):
        start_node.z = 0
        end_node.z = 0
        super().__init__(start_node, end_node, section, material)

    def _local_matrix(self):

        le = self.length
        a = self.material.elasticity_modulus * self.section.area / le
        ei = self.material.elasticity_modulus * self.section.inertia_z
        b = 12*ei/(le**3)
        c = 6*ei/(le**2)
        d = 4*ei/le
        e = 2*ei/le
        self.number_of_stations = 10
        return np.array([[a, 0, 0, -a, 0, 0],
                        [0, b, c, 0, -b, c],
                        [0, c, d, 0, -c, e],
                        [-a, 0, 0, a, 0, 0],
                        [0, -b, -c, 0, b, -c],
                        [0, c, e, 0, -c, d]])

    def _transformation_matrix(self):
        x_diff = self.end_node.x - self.start_node.x
        y_diff = self.end_node.y - self.start_node.y

        lambda_x = x_diff / self.length
        lambda_y = y_diff / self.length

        gama_matrix = np.array([[lambda_x, lambda_y, 0],
                               [-lambda_y, lambda_x, 0],
                               [0, 0, 1]])
        transformation_matrix = np.zeros((6, 6))
        transformation_matrix[0:3, 0:3] = gama_matrix
        transformation_matrix[3:7, 3:7] = gama_matrix
        return transformation_matrix

    def shape_function_matrix(self, x):
        le = self.length
        n1 = 1 - x / le
        n2 = x / le
        n3 = 1 - 3 * (x / le) ** 2 + 2 * (x / le) ** 3
        n4 = 3 * (x / le) ** 2 - 2 * (x / le) ** 3
        n5 = x * (1 - x / le) ** 2
        n6 = x * ((x / le) ** 2 - x / le)

        return np.array([[n1, 0, 0, 0, 0, 0, n2, 0, 0, 0, 0, 0],
                        [0, n3, 0, 0, 0, n5, 0, n4, 0, 0, 0, n6]])

    def local_end_displacements(self):
        global_displacements = np.array([dof.displacement for dof in self.degrees_of_freedom])
        return np.dot(self._transformation_matrix(), global_displacements)

    @property
    def degrees_of_freedom(self):
        return [self.start_node.dof_1,
                self.start_node.dof_2,
                self.start_node.dof_6,
                self.end_node.dof_1,
                self.end_node.dof_2,
                self.end_node.dof_6]

    @property
    def matrix(self):
        return np.dot(np.dot(self._transformation_matrix().T, self._local_matrix()),
                      self._transformation_matrix())

    @property
    def elastic_geometric_matrix(self):
        return None
