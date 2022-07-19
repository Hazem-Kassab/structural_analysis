"""
Classes:
    _DegreeOfFreedom
"""
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from structural_analysis.node import Node


class Direction(Enum):
    GLOBAL_X = 1
    GLOBAL_Y = 2
    GLOBAL_Z = 3
    GLOBAL_RX = 4
    GLOBAL_RY = 5
    GLOBAL_RZ = 6


class DegreeOfFreedom:
    """
    A class to represent a degree of freedom.
    ...

    Attributes
    ----------
    direction : Direction
        direction of the degree of freedom in structure coordinate system
    node : Node
        node containing the degree of freedom
    id : int
        node identifier unique for the degree of freedom instance
    displacement : float
        displacement of the degree of freedom in the respective direction.
        initial displacement shall be assigned using method assign_initial_displacement.
    restrained : bool
        false by default
    force : float
        assigned nodal forces to the degree of freedom instance


    Methods
    -------
    assign_force(self, value):
        assigns force to degree of freedom instance in the instance direction

    assign_initial_displacement(self, value):
        assigns initial displacement to the node in the instance direction
    """

    id = 1

    def __init__(self, node: Node, direction: Direction):
        self.direction = direction
        self.node = node
        self.id = DegreeOfFreedom.id
        DegreeOfFreedom.id += 1
        self.displacement = 0
        self.restrained = False
        self.force = 0
        self.fixed_end_reaction = 0

    def assign_force(self, value: float):
        """assign a force to the degree of freedom in its direction.

            Keyword arguments:
            value -- the magnitude of the force
            """
        self.force = value

    def assign_initial_displacement(self, value: float):
        """Assign an initial displacement boundary condition
        to the degree of freedom in its direction.

            Keyword arguments:
            value -- the amount of displacement
            """
        self.restrained = True
        self.displacement = value

    def __str__(self):
        return f"DOF ID: {self.id}"
