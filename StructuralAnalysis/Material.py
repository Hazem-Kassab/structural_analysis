"""
Class Material is an abstract class.
attributes and properties:
    elasticity_modulus: should be initialized by the user
    poissons_ratio: should be initialized by the used
    shear_modulus (property & abstract method): each inheriting class has its own implementation of the shear_modulus

Derived classes:
    Steel:
        -attributes: yield_strength, ultimate_strength
    Concrete:
"""


from abc import ABC, abstractmethod


class Material(ABC):

    def __init__(self, elasticity_modulus, poissons_ratio):
        self.elasticity_modulus = elasticity_modulus
        self.poissons_ratio = poissons_ratio
        self.__shear_modulus = None

    @property
    @abstractmethod
    def shear_modulus(self):
        return self.__shear_modulus


class Steel(Material):

    def __init__(self, yield_strength, ultimate_strength, elasticity_modulus, poissons_ratio):
        super().__init__(elasticity_modulus, poissons_ratio)
        self.yield_strength = yield_strength
        self.ultimate_strength = ultimate_strength

    @property
    def shear_modulus(self):
        return self.elasticity_modulus / (2 * (1 + self.poissons_ratio))


class Concrete(Material):
    @property
    def shear_modulus(self):
        return None
