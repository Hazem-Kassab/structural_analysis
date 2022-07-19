"""
Classes:
    Node
"""
from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from structural_analysis import Structure
    from structural_analysis.load import Load
    from structural_analysis.coordinate_system import CoordinateSystem
from structural_analysis.degree_of_freedom import DegreeOfFreedom, Direction
from structural_analysis.coordinate_system import Global_Coordinate_System
from structural_analysis.vector import Vector


class Node:
    """
    A class to represent a node.
    ...

    Attributes
    ----------
    x : float
        x coordinate of the node in the structure coordinate system

    y : float
        y coordinate of the node in the structure coordinate system

    z : float
        z coordinate of the node in the structure coordinate system

    _structure : Structure
        structure instance containing the node

    position_vector : Vector
        position vector instance holding x, y, and z coordinates of the node instance

    dof_x : DegreeOfFreedom
        translational degree of freedom instance in
        the x-axis direction of the structure coordinate system

    dof_y : DegreeOfFreedom
        translational degree of freedom instance in
        the y-axis direction of the structure coordinate system

    dof_z : DegreeOfFreedom
        translational degree of freedom instance in
        the z-axis direction of the structure coordinate system

    dof_rx : DegreeOfFreedom
        rotational degree of freedom instance around
        the x-axis of the structure coordinate system

    dof_ry : DegreeOfFreedom
        rotational degree of freedom instance around
        the y-axis of the structure coordinate system

    dof_rz : DegreeOfFreedom
        rotational degree of freedom instance around
        the z-axis of the structure coordinate system
    """
    __node_id = 1

    def __init__(self, x, y, z):
        self.id = Node.__node_id
        Node.__node_id += 1
        self.x = x
        self.y = y
        self.z = z
        # self._structure = None
        self.position_vector = Vector([self.x, self.y, self.z])
        self.position_vector.coordinate_system = Global_Coordinate_System
        self.dof_x = DegreeOfFreedom(self, Direction.GLOBAL_X)
        self.dof_y = DegreeOfFreedom(self, Direction.GLOBAL_Y)
        self.dof_z = DegreeOfFreedom(self, Direction.GLOBAL_Z)
        self.dof_rx = DegreeOfFreedom(self, Direction.GLOBAL_RX)
        self.dof_ry = DegreeOfFreedom(self, Direction.GLOBAL_RY)
        self.dof_rz = DegreeOfFreedom(self, Direction.GLOBAL_RZ)
        self.loads: [Load] = []

    @property
    def degrees_of_freedom(self) -> list[DegreeOfFreedom]:
        """returns a list holding the six degrees of freedom instances of the node"""
        return [self.dof_x, self.dof_y, self.dof_z, self.dof_rx, self.dof_ry, self.dof_rz]

    def transformed_dofs_matrix(self, coordinate_system: CoordinateSystem):
        return Global_Coordinate_System.get_coordinate_transformation_matrix(coordinate_system)

    # @property
    # def structure(self) -> Structure:
    #     """structure containing the node instance"""
    #     return self._structure
    #
    # @structure.setter
    # def structure(self, value: Structure):
    #     self._structure = value
    #
    # def __str__(self):
    #     return f"Node id: {self.id}, coordinates: {self.x}, {self.y}, {self.z})"
