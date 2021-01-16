"""
Section class is an abstract class.
Local axis of the section is as follows:
x-axis is the longitudinal axis that is directed from the start node to the end node of the element
y-axis is directed upward the section
z-axis is directed to the left
Properties(abstract methods):
    properties are overridden by the inheriting section classes.
    area = area of the section
    inertia_y = second moment of area about the y-axis
    inertia_z = second moment of area about the z-axis
    polar_inertia = polar moment of inertia about the x-axis (J)
    warping_rigidity = warping rigidity that applies to non-circular sections

Derived classes:
    Circle
    Square
    ArbitrarySection: section with user-defined properties
"""


from math import pi
from abc import ABC, abstractmethod


class Section(ABC):
    def __init__(self):
        self.__area = None
        self.__inertia_y = None
        self.__inertia_z = None
        self.__polar_inertia = None
        self.__warping_rigidity = None

    @property
    @abstractmethod
    def area(self):
        return self.__area

    @property
    @abstractmethod
    def inertia_y(self):
        return self.__inertia_y

    @property
    @abstractmethod
    def inertia_z(self):
        return self.__inertia_z

    @property
    @abstractmethod
    def polar_inertia(self):
        return self.__polar_inertia

    @property
    @abstractmethod
    def warping_rigidity(self):
        return self.__warping_rigidity


class Circle(Section):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    @property
    def area(self):
        return pi*self.radius**2

    @property
    def inertia_y(self):
        return pi*self.radius**4/2

    @property
    def inertia_z(self):
        return pi*self.radius**4/2

    @property
    def polar_inertia(self):
        return self.inertia_y + self.inertia_z

    @property
    def warping_rigidity(self):
        return None


class Rectangle(Section):
    def __init__(self, breadth, depth):
        super().__init__()
        self.breadth = breadth
        self.depth = depth

    @property
    def area(self):
        return self.breadth * self.depth

    @property
    def inertia_y(self):
        return self.depth * self.breadth**3 / 12

    @property
    def inertia_z(self):
        return self.breadth * self.depth**3 / 12

    @property
    def polar_inertia(self):
        return self.inertia_y + self.inertia_z

    @property
    def warping_rigidity(self):
        return None


class ArbitrarySection(Section):

    def __init__(self, area, inertia_y, inertia_z, polar_inertia, warping_rigidity):
        super().__init__()
        self.__area = area
        self.__inertia_y = inertia_y
        self.__inertia_z = inertia_z
        self.__polar_inertia = polar_inertia
        self.__warping_rigidity = warping_rigidity

    @property
    def area(self):
        return self.__area

    @property
    def inertia_y(self):
        return self.__inertia_y

    @property
    def inertia_z(self):
        return self.__inertia_z

    @property
    def polar_inertia(self):
        return self.__polar_inertia

    @property
    def warping_rigidity(self):
        return self.__warping_rigidity
