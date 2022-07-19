"""
Classes:
    Material
    Steel
    Concrete

Material is an abstract class.
Other classes are derived from Material class.
"""


from abc import ABCMeta, abstractmethod


class Material(metaclass=ABCMeta):
    """
    An abstract class to represent material instance assigned to an element.
    ...

    Attributes
    ----------
    elasticity_modulus : float
        Modulus of elasticity of the material

    poissons_ratio : float
        Poisson's ratio of the material

    Methods
    -------
    stress(self, strain):
        abstract method, implemented by derived classes.
        describes the constitutive relationship.
        returns stress value on a given strain.

    """

    def __init__(self, elasticity_modulus, poissons_ratio):
        self.elasticity_modulus = elasticity_modulus
        self.poissons_ratio = poissons_ratio
        self.thermal_coefficient = None

    @property
    @abstractmethod
    def shear_modulus(self):
        """
        abstract method, implemented by derived classes.
        Represents shear modulus of material.
        """
        raise NotImplementedError

    @abstractmethod
    def stress(self, strain):
        """
        abstract method, implemented by derived classes.
        describes the constitutive relationship.
        returns stress value on a given strain.
        """
        raise NotImplementedError


class Steel(Material):
    """
        A class to represent steel material instance assigned to an element.
        ...

        Attributes
        ----------
        elasticity_modulus : float
            Modulus of elasticity of steel usually around 200 GPa

        poissons_ratio : float
            Poisson's ratio of steel usually around 0.3

        yield_strength : float
            Yield strength of steel

        ultimate_strength : float
            ultimate strength of steel
        """

    def __init__(self, elasticity_modulus, poissons_ratio, yield_strength=None, ultimate_strength=None):
        super().__init__(elasticity_modulus, poissons_ratio)
        self.yield_strength = yield_strength
        self.ultimate_strength = ultimate_strength
        self.thermal_coefficient = 11.7e-6

    @property
    def shear_modulus(self):
        """shear modulus of steel usually around 79.3 GPa"""
        return self.elasticity_modulus / (2 * (1 + self.poissons_ratio))

    def stress(self, strain):
        """
        describes the constitutive relationship.
        returns stress value on a given strain.
        """
        raise NotImplementedError


class Concrete(Material):
    """
            A class to represent concrete material instance assigned to an element.
            ...

            Attributes
            ----------
            elasticity_modulus : float
                Modulus of elasticity concrete usually around 20 GPa

            poissons_ratio : float
                Poisson's ratio of concrete usually around 0.2

            yield_strength : float
                Yield strength of concrete at 0.2% offset in stress-strain diagram.

            characteristic_strength : float
                characteristic strength of concrete.

            """
    def __init__(self, elasticity_modulus, poissons_ratio, yield_strength=None, characteristic_strength=None):
        super().__init__(elasticity_modulus, poissons_ratio)
        self.yield_strength = yield_strength
        self.characteristic_strength = characteristic_strength
        self.thermal_coefficient = 10e-6

    @property
    def shear_modulus(self):
        """shear modulus of concrete"""
        return None

    def stress(self, strain):
        """
        describes the constitutive relationship.
        returns stress value on a given strain.
        """
        raise NotImplementedError
