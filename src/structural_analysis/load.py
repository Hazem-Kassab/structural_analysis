from abc import ABCMeta, abstractmethod
from structural_analysis.coordinate_system import Global_Coordinate_System
from structural_analysis import CoordinateSystem, Node, Vector
from structural_analysis.frame_elements.element import Element
import numpy as np


class Load(metaclass=ABCMeta):
    def __init__(self, fx=0, fy=0, fz=0, mx=0, my=0, mz=0):
        self._coordinate_system = Global_Coordinate_System
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.mx = mx
        self.my = my
        self.mz = mz
        self.load_array = [self.fx, self.fy, self.fz, self.mx, self.my, self.mz]
        self.load_vector = Vector([self.fx, self.fy, self.fz])
        self.load_vector.coordinate_system = Global_Coordinate_System
        self.moment_vector = Vector([self.mx, self.my, self.mz])
        self.moment_vector.coordinate_system = Global_Coordinate_System
        self.local = False

    def transformed(self, coordinate_system: CoordinateSystem):
        transformed_load_vector = self.load_vector.transform_vector(coordinate_system)
        transformed_moment_vector = self.moment_vector.transform_vector(coordinate_system)
        return np.append(transformed_load_vector, transformed_moment_vector)

    def local_load(self, coordinate_system: CoordinateSystem):
        transformed_load_vector = self.load_vector.transform_vector(coordinate_system)
        transformed_moment_vector = self.moment_vector.transform_vector(coordinate_system)
        return Load(transformed_load_vector[0], transformed_load_vector[1], transformed_load_vector[2],
                    transformed_moment_vector[0], transformed_moment_vector[1], transformed_moment_vector[2])

    @property
    def coordinate_system(self) -> CoordinateSystem:
        return self._coordinate_system

    @coordinate_system.setter
    def coordinate_system(self, value: CoordinateSystem):
        self._coordinate_system = value
        self.load_vector.coordinate_system = value
        self.moment_vector.coordinate_system = value

    def _get_fixed_end_reactions(self, element, fixed_end_matrix):
        local_load_vector = self.local_load(element.coordinate_system)
        # print(local_load_vector.load_array)
        load = element.get_valid_load(local_load_vector.load_array)
        # print(load)
        reactions = fixed_end_matrix.dot(load)
        return reactions

    @staticmethod
    def _assign_global_fixed_end_reactions(element, reactions):
        counter = 0
        global_reactions = element.element_stiffness_transformation_matrix().T.dot(reactions)

        for dof in element.degrees_of_freedom:
            dof.fixed_end_reaction += global_reactions[counter]
            counter += 1

        element.fixed_end_reactions += reactions

    def __getitem__(self, item):
        return self.load_array[item]


class PointLoad(Load):

    def assign_to_node(self, node: Node):
        node.loads.append(self)
        counter = 0
        for dof in node.degrees_of_freedom:
            dof.force += self[counter]
            counter += 1

    def assign_to_element(self, element: Element, location: float, local=False):
        if local:
            self.coordinate_system = element.coordinate_system
            self.local = True

        element.concentrated_loads[self] = location
        element.has_non_nodal_loads = True
        fixed_end_matrix = element.fixed_end_reactions_matrix_concentrated(location)
        reactions = self._get_fixed_end_reactions(element, fixed_end_matrix)
        Load._assign_global_fixed_end_reactions(element, reactions)


class DistributedLoad(Load):

    def assign_to_element(self, element: Element, local=False):
        if local:
            self.coordinate_system = element.coordinate_system
            self.local = True

        element.distributed_loads.append(self)
        element.has_non_nodal_loads = True
        fixed_end_matrix = element.fixed_end_reactions_matrix_distributed()
        reactions = self._get_fixed_end_reactions(element, fixed_end_matrix)
        Load._assign_global_fixed_end_reactions(element, reactions)


class ThermalLoad:
    def __init__(self, temperature_change):
        self.temperature_change = temperature_change

    def assign_to_element(self, element: Element):
        element.assign_thermal_load(self.temperature_change)

