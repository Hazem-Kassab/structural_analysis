"""
Classes:
    Element (Abstract)
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from abc import abstractmethod, ABC
import numpy as np
from structural_analysis.node import Node
from structural_analysis.degree_of_freedom import DegreeOfFreedom
from structural_analysis.section import Section
from structural_analysis.material import Material
from structural_analysis.coordinate_system import CoordinateSystem, Global_Coordinate_System
from structural_analysis.vector import Vector

if TYPE_CHECKING:
    from structural_analysis.structure import Structure
    from structural_analysis.load import Load


class Element(ABC):
    """
    An abstract class to represent an element.
    ...

    Attributes
    ----------
    id : int
        unique identifier for the element.

    start_node : Node
        start node instance of the element.

    end_node : Node
        end node instance of the element.

    section : Section
        cross-section of the element

    _vector: Vector
        vector instance from start node to end node described in the structure coordinate system

    length: float
        length of the element

    twist_angle: float
        rotation angle of the element around its local x-axis, in degrees.

    coordinate_system : CoordinateSystem
        local coordinate system of the element. The element lies on the x-axis.

    _structure : Structure
        structure instance containing the element


    Methods
    -------
    _geometry_transformation_matrix(self) -> numpy.ndarray:
        returns a 3x3 transformation matrix from
        local coordinate system to structure coordinate system

    global_stiffness_matrix(self) -> np.array:
        returns the element global stiffness matrix in the structure coordinate system

    local_mesh_coordinates(self) -> np.ndarray:
        returns a 2-d array of local coordinates of points evenly spaced along element.

    global_mesh_coordinates(self) -> np.ndarray:
        transforms local_mesh_coordinates into structure
        coordinate system and returns global coordinates.

    local_displacement_field(self) -> np.ndarray:
        returns local displacements of local_mesh_coordinates points.

    global_displacement_field(self) -> np.ndarray:
        transforms local_displacement_field into structure
        coordinate system and returns global displacements.

    global_deformed_position(self, scale) -> np.ndarray:
        returns global deformed position of an element in structure.
        Sum of global displacement field and global mesh coordinates.

    local_end_displacement_vector(self) -> np.ndarray:
        returns displacements and rotations of
        element start and end node after analysis is completed.

    local_stiffness_matrix(self) -> np.array:
        abstract method to be implemented be derived classes.
        Represents the local stiffness matrix in the local element coordinates.

    element_stiffness_transformation_matrix(self) -> np.ndarray:
        abstract method to be implemented by derived classes.
        Represents the transformation matrix of local stiffness matrix in
        local element coordinates to structure coordinate system.

    degrees_of_freedom(self) -> list[_DegreeOfFreedom]:
        abstract method to be implemented by derived classes.
        Returns list of degrees of freedom of start node and end node degrees of freedom.

    shape_function_matrix(self, x) -> np.ndarray:
        abstract method to be implemented by derived classes.
        Returns 3x1 array of local displacements of point,
        at position x, in the local coordinate system.
    """

    id = 1
    element_subdivisions = 20

    def __init__(self, start_node: Node, end_node: Node,
                 section: Section, material: Material, beta_angle=0):
        self.id = Element.id
        Element.id += 1
        self.start_node = start_node
        self.end_node = end_node
        self.section = section
        self.material = material
        self._vector = Vector(np.subtract(end_node.position_vector, start_node.position_vector))
        self.length = self._vector.magnitude
        self.twist_angle = beta_angle
        self.coordinate_system = CoordinateSystem(self._vector, self.twist_angle, self.start_node.position_vector)
        # self._structure = None
        self.concentrated_loads: [Load] = {}
        self.distributed_loads: [Load] = []
        self.has_non_nodal_loads = False
        self.local_displacement_field_non_nodal_load = np.zeros((Element.element_subdivisions+1, 3))
        self.fixed_end_reactions = np.zeros((len(self.degrees_of_freedom)))
        self.moment_z_values = []
        self.moment_y_values = []

    def _geometry_transformation_matrix(self) -> np.ndarray:
        """returns a 3x3 geometry transformation matrix from
        element local coordinates to structure coordinate system.
        """
        return self.coordinate_system.get_global_coord_transformation_matrix()

    def global_stiffness_matrix(self) -> np.array:
        """returns the element global stiffness matrix in the structure coordinate system"""
        return np.dot(np.dot(self.element_stiffness_transformation_matrix().T,
                             self.local_stiffness_matrix()), self.element_stiffness_transformation_matrix())

    @property
    def local_mesh_coordinates(self) -> np.ndarray:
        """returns a 2-d array of local coordinates of points evenly spaced along element."""
        counter = 0
        subdivision_length = self.length/Element.element_subdivisions
        coordinates = np.zeros((Element.element_subdivisions+1, 3))
        while counter <= Element.element_subdivisions:
            coordinates[counter] = counter*subdivision_length, 0, 0
            counter += 1
        return coordinates

    @property
    def global_mesh_coordinates(self) -> np.ndarray:
        """
        transforms local_mesh_coordinates into structure
        coordinate system and returns global coordinates.
        """
        return self._geometry_transformation_matrix().T.dot(self.local_mesh_coordinates.T) + \
               np.array([self.coordinate_system.origin]*(Element.element_subdivisions+1)).T

    def local_displacement_field(self) -> np.ndarray:
        """returns local displacements of local_mesh_coordinates points."""
        displacement_field = np.zeros((Element.element_subdivisions+1, 3))
        index = 0
        for x in self.local_mesh_coordinates:
            displacement_vector = self.shape_function_matrix(x[0]).dot(self.local_end_displacement_vector())
            displacement_field[index] = displacement_vector
            index += 1
        return displacement_field + self.local_displacement_field_non_nodal_load

    def global_displacement_field(self, scale: float) -> np.ndarray:
        """transforms local_displacement_field into structure
        coordinate system and returns global displacements.
        """
        return self._geometry_transformation_matrix().T.dot(self.local_displacement_field().T) * scale

    def global_deformed_position(self, scale) -> np.ndarray:
        """
        returns global deformed position of an element in structure.
        Sum of global displacement field and global mesh coordinates.
        """
        return self.global_mesh_coordinates + self.global_displacement_field(scale)

    def local_end_displacement_vector(self) -> np.ndarray:
        """
        returns displacements and rotations of element start
        and end node after analysis is completed.
        """
        global_displacements = np.array([dof.displacement for dof in
                                         self.start_node.degrees_of_freedom + self.end_node.degrees_of_freedom])
        local_displacements = np.dot(self._geometry_transformation_matrix(),
                                     global_displacements.reshape((3, 4), order='F'))
        return local_displacements.reshape(12, order='F')

    @abstractmethod
    def local_stiffness_matrix(self) -> np.array:
        """abstract method to be implemented be derived classes.
        Represents the local stiffness matrix in the local element coordinates.
        """
        raise NotImplementedError

    @abstractmethod
    def element_stiffness_transformation_matrix(self) -> np.ndarray:
        """
        abstract method to be implemented by derived classes.
        Represents the transformation matrix of local stiffness matrix in
        local element coordinates to structure coordinate system.
        """
        raise NotImplementedError

    def fixed_end_reactions_thermal(self, temperature_change) -> np.ndarray:
        strain = self.material.thermal_coefficient * temperature_change
        reaction = self.material.elasticity_modulus * self.section.area * strain
        return np.array([[reaction, -reaction]])

    def assign_thermal_load(self, temperature_change):
        global_fixed_end_reactions = \
            np.array([self._geometry_transformation_matrix()[0]]).T.dot(self.fixed_end_reactions_thermal(temperature_change)).T
        self.start_node.dof_x.fixed_end_reaction += global_fixed_end_reactions[0][0]
        self.start_node.dof_y.fixed_end_reaction += global_fixed_end_reactions[0][1]
        self.start_node.dof_z.fixed_end_reaction += global_fixed_end_reactions[0][2]
        self.end_node.dof_x.fixed_end_reaction += global_fixed_end_reactions[1][0]
        self.end_node.dof_y.fixed_end_reaction += global_fixed_end_reactions[1][1]
        self.end_node.dof_z.fixed_end_reaction += global_fixed_end_reactions[1][2]

    @abstractmethod
    def fixed_end_reactions_matrix_concentrated(self, location: float) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def fixed_end_reactions_matrix_distributed(self) -> np.ndarray:
        raise NotImplementedError

    # @abstractmethod
    # def assign_concentrated_load(self, load: np.ndarray, location: float):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def assign_distributed_load(self, load: np.ndarray):
    #     raise NotImplementedError

    def _assign_global_fixed_end_reactions(self, reactions):
        counter = 0
        global_reactions = self.element_stiffness_transformation_matrix().T.dot(reactions)

        for dof in self.degrees_of_freedom:
            dof.fixed_end_reaction += global_reactions[counter]
            counter += 1

    def add_distributed_load_local_displacement_field(self, load: np.ndarray):
        index = 0
        for x in self.local_mesh_coordinates:
            self.local_displacement_field_non_nodal_load[index] += \
                self.shape_function_matrix_distributed_load(x[0]).dot(load)
            index += 1

    def add_concentrated_load_local_displacement_field(self, load: np.ndarray, location):
        index = 0
        for x in self.local_mesh_coordinates:
            self.local_displacement_field_non_nodal_load[index] += \
                self.shape_function_matrix_concentrated_load(location, x[0]).dot(load)
            index += 1

    def local_end_displacements(self):
        global_displacements = np.array([dof.displacement for dof in self.degrees_of_freedom])
        local_displacements = self.element_stiffness_transformation_matrix().dot(global_displacements)
        return local_displacements

    def local_end_forces(self):
        return self.local_stiffness_matrix().dot(self.local_end_displacements())

    # def assign_concentrated_load(self, load, location):
    #     load = self.get_valid_load(load)
    #     reactions = self.fixed_end_reactions_matrix_concentrated(location).dot(load)
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.add_concentrated_load_local_displacement_field(load, location)
    #     self.fixed_end_reactions += reactions
    #
    # def assign_distributed_load(self, load):
    #     load = self.get_valid_load(load)
    #     reactions = self.fixed_end_reactions_matrix_distributed().dot(load)
    #     self._assign_global_fixed_end_reactions(reactions)
    #     self.add_distributed_load_local_displacement_field(load)
    #     self.fixed_end_reactions += reactions

    @staticmethod
    @abstractmethod
    def get_valid_load(load):
        raise NotImplementedError

    # @abstractmethod
    # def bending_moment_z(self, x):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def bending_moment_y(self, x):
    #     raise NotImplementedError

    @property
    @abstractmethod
    def degrees_of_freedom(self) -> list[DegreeOfFreedom]:
        """
        abstract method to be implemented by derived classes.
        Returns list of degrees of freedom of start node and end node degrees of freedom.
        """
        raise NotImplementedError

    @abstractmethod
    def shape_function_matrix(self, x) -> np.ndarray:
        """
        abstract method to be implemented by derived classes.
        Returns 3x1 array of local displacements of point ,at position x,
        in the local coordinate system.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def elastic_geometric_matrix(self):
        """for future use of geometric stiffness matrix"""
        raise NotImplementedError

    @abstractmethod
    def shape_function_matrix_concentrated_load(self, location, x) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def shape_function_matrix_distributed_load(self, x) -> np.ndarray:
        raise NotImplementedError
