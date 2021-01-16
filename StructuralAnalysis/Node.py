"""
This class is used by element objects to instantiate start node and end node objects
Attributes:
    self.x = x co-ordinate
    self.y = y co-ordinate
    self.z = z co-ordinate
    self.dof_1 : displacement in the global x-direction
    self.dof_2 : displacement in the global y-direction
    self.dof_3 : displacement in the global z-direction
    self.dof_4 : rotation about the global x-direction
    self.dof_5 : rotation about the global y-direction
    self.dof_6 : rotation about the global z-direction
"""

from StructuralAnalysis.DegreeOfFreedom import DegreeOfFreedom


class Node:
    __node_id = 1

    def __init__(self, x, y, z):
        self.id = Node.__node_id
        Node.__node_id += 1
        self._x = x
        self._y = y
        self._z = z
        self.dof_1 = DegreeOfFreedom()
        self.dof_2 = DegreeOfFreedom()
        self.dof_3 = DegreeOfFreedom()
        self.dof_4 = DegreeOfFreedom()
        self.dof_5 = DegreeOfFreedom()
        self.dof_6 = DegreeOfFreedom()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def __repr__(self):
        return "NODE ID: %d" % self.id

    def __str__(self):
        return "NODE ID: %d" % self.id

