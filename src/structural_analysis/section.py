"""
Classes:
    Section
    Circle
    Rectangle
    ArbitrarySection

Section class is an abstract class.
Other classes are derived from Section.
"""

from math import pi
from abc import ABCMeta, abstractmethod


class Section(metaclass=ABCMeta):
    """
    An abstract class to represent a section which will be assigned to element objects.
    ...
    """
    @property
    @abstractmethod
    def area(self):
        """area of the cross-section"""
        raise NotImplementedError

    @property
    @abstractmethod
    def inertia_y(self):
        """inertia of the cross-section around the element y-axis"""
        raise NotImplementedError

    @property
    @abstractmethod
    def inertia_z(self):
        """inertia of the cross-section around the element z-axis"""
        raise NotImplementedError

    @property
    @abstractmethod
    def polar_inertia(self):
        """inertia of the cross-section around the element x-axis"""
        raise NotImplementedError

    @property
    @abstractmethod
    def warping_rigidity(self):
        """warping rigidity of the cross-section"""
        raise NotImplementedError


class Circle(Section):
    """
        A class to represent a circular section which will be assigned to element objects.
        ...
    """
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    @property
    def area(self):
        """area of the cross-section"""
        return pi*self.radius**2

    @property
    def inertia_y(self):
        """inertia of the cross-section around the element y-axis"""
        return pi*self.radius**4/2

    @property
    def inertia_z(self):
        """inertia of the cross-section around the element z-axis"""
        return pi*self.radius**4/2

    @property
    def polar_inertia(self):
        """inertia of the cross-section around the element x-axis"""
        return self.inertia_y + self.inertia_z

    @property
    def warping_rigidity(self):
        """zero for circular cross-sections"""
        return 0


class Rectangle(Section):
    """
        A class to represent a rectangular section which will be assigned to element objects.
        ...
    """
    def __init__(self, breadth, depth):
        super().__init__()
        self.breadth = breadth
        self.depth = depth

    @property
    def area(self):
        """area of the cross-section"""
        return self.breadth * self.depth

    @property
    def inertia_y(self):
        """inertia of the cross-section around the element y-axis"""
        return self.depth * self.breadth**3 / 12

    @property
    def inertia_z(self):
        """inertia of the cross-section around the element z-axis"""
        return self.breadth * self.depth**3 / 12

    @property
    def polar_inertia(self):
        """inertia of the cross-section around the element x-axis"""
        return self.inertia_y + self.inertia_z

    @property
    def warping_rigidity(self):
        """warping rigidity of the cross-section"""
        return None


class ArbitrarySection(Section):
    """
        A class to represent an arbitrary shaped section with user-defined geometric properties
        which will be assigned to element objects.
        ...
    """
    def __init__(self, area, inertia_y, inertia_z, polar_inertia, warping_rigidity=None):
        super().__init__()
        self._area = area
        self._inertia_y = inertia_y
        self._inertia_z = inertia_z
        self._polar_inertia = polar_inertia
        self._warping_rigidity = warping_rigidity

    @property
    def area(self):
        """area of the cross-section"""
        return self._area

    @property
    def inertia_y(self):
        """inertia of the cross-section around the element y-axis"""
        return self._inertia_y

    @property
    def inertia_z(self):
        """inertia of the cross-section around the element z-axis"""
        return self._inertia_z

    @property
    def polar_inertia(self):
        """inertia of the cross-section around the element x-axis"""
        return self._polar_inertia

    @property
    def warping_rigidity(self):
        """warping rigidity of the cross-section"""
        return self._warping_rigidity
