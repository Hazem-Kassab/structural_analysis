"""
Classes:
    Structure
"""


from structural_analysis.frame_elements.element import Element
from structural_analysis.coordinate_system import CoordinateSystem
from structural_analysis.node import Node
from structural_analysis.degree_of_freedom import DegreeOfFreedom
from structural_analysis.vector import Vector


class Structure:
    """
    A class to represent a structure of elements.
    ...

    Attributes
    ----------
    elements : list[Element]
        list of element instances in the structure

    nodes : list[Node]
        list of node instances in the structure

    degrees_of_freedom : list[DegreeOfFreedom]
        list of structure degrees of freedom

    free_degrees_of_freedom : list[_DegreeOfFreedom]
        list of all unrestrained degrees of freedom instances in the structure

    restrained_degrees_of_freedom : list[_DegreeOfFreedom]
        list of all restrained degrees of freedom instances in the structure

    coordinate_system : CoordinateSystem
        global coordinate system in which the structure is defined.


    Methods
    -------
    _get_nodes_and_dofs(self) -> tuple[[Node], [_DegreeOfFreedom]]
        returns a tuple of all nodes and degrees of freedom in structure.

    _get_free_and_restrained_dofs(self):
        returns a tuple of all free and restrained degrees of freedom in structure.

    _assign_structure_to_nodes(self):
        assigns structure instance to node structure attribute

    _assign_structure_to_elements(self):
        assigns structure instance to element structure attribute
        assigns structure instance to element structure attribute
    """

    def __init__(self, elements: list[Element], name="structure"):
        self.elements = elements
        self.nodes, self.degrees_of_freedom = self._get_nodes_and_dofs()
        self.free_degrees_of_freedom, self.restrained_degrees_of_freedom = self._get_free_and_restrained_dofs()
        self.name = name
        self.solved = False

    def _get_nodes_and_dofs(self) -> tuple[[Node], [DegreeOfFreedom]]:
        """returns a tuple of all nodes and degrees of freedom in structure."""
        nodes = []
        dofs = []
        for element in self.elements:
            for dof in element.degrees_of_freedom:
                if dof not in dofs:
                    dofs.append(dof)
            if element.start_node not in nodes:
                nodes.append(element.start_node)
            if element.end_node not in nodes:
                nodes.append(element.end_node)
        return nodes, dofs

    def _get_free_and_restrained_dofs(self):
        """returns a tuple of all free and restrained degrees of freedom in structure."""
        free_dofs = []
        restrained_dofs = []
        for dof in self.degrees_of_freedom:
            if not dof.restrained:
                free_dofs.append(dof)
            else:
                restrained_dofs.append(dof)
        return free_dofs, restrained_dofs

    # def _assign_structure_to_nodes(self):
    #     """assigns structure instance to node structure attribute"""
    #     for node in self.nodes:
    #         node.position_vector.coordinate_system = self.coordinate_system
    #
    # def _assign_structure_to_elements(self):
    #     """assigns structure instance to element structure attribute"""
    #     for element in self.elements:
    #         element.structure = self
