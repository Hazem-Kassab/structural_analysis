import numpy as np
from StructuralAnalysis.FrameElements.Element import Element
from math import *


class FrameElement(Element):
    """
    This class inherits from Element.
    properties:
        self._degrees_of_freedom: 12 degrees of freedom (6 per node) - 3D element
        self._transformation_matrix: does not take into account tilt angle of the element
    """

    def _local_matrix(self):
        le = self.length
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

    def _transformation_matrix(self):
        if self.start_node.x == self.end_node.x and self.start_node.y == self.end_node.y:
            if self.end_node.z > self.start_node.z:
                gama_matrix = np.array([[0, 0, 1],
                                       [0, 1, 0],
                                       [-1, 0, 0]])
            else:
                gama_matrix = np.array([[0, 0, -1],
                                        [0, 1, 0],
                                        [1, 0, 0]])
        else:
            cxx = (self.end_node.x - self.start_node.x)/self.length
            cyx = (self.end_node.y - self.start_node.y)/self.length
            czx = (self.end_node.z - self.start_node.z)/self.length
            d = sqrt(cxx**2 + cyx**2)
            cxy = -cyx/d
            cyy = cxx/d
            czy = 0
            cxz = -cxx*czx/d
            cyz = -cyx*czx/d
            czz = d
            gama_matrix = np.array([[cxx, cyx, czx],
                                   [cxy, cyy, czy],
                                   [cxz, cyz, czz]])

        transformation_matrix = np.zeros((len(self.degrees_of_freedom), len(self.degrees_of_freedom)))
        for i in range(4):
            transformation_matrix[(i*3):(i+1)*3, (i*3):(i+1)*3] = gama_matrix

        return transformation_matrix

    def shape_function_matrix(self, x):
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

    def local_end_displacements(self):
        global_displacements = np.array([dof.displacement for dof in self.degrees_of_freedom])
        return np.dot(self._transformation_matrix(), global_displacements)

    @property
    def degrees_of_freedom(self):
        return [self.start_node.dof_1, self.start_node.dof_2, self.start_node.dof_3,
                self.start_node.dof_4, self.start_node.dof_5, self.start_node.dof_6,
                self.end_node.dof_1, self.end_node.dof_2, self.end_node.dof_3,
                self.end_node.dof_4, self.end_node.dof_5, self.end_node.dof_6]

    @property
    def matrix(self):
        return np.dot(np.dot(self._transformation_matrix().T, self._local_matrix()),
                      self._transformation_matrix())

    @property
    def elastic_geometric_matrix(self):
        return None
