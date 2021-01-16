"""
This class is used by node objects to instantiate 6 degrees of freedom
Properties:
    displacement/rotation
    force: acting in the same direction as the degree of freedom
    restrained: used to set boundary condition as free or fixed.
                If fixed it sets the displacement to zero
"""


class DegreeOfFreedom:
    id = 1

    def __init__(self):
        self.id = DegreeOfFreedom.id
        DegreeOfFreedom.id += 1
        self.__displacement_value = 0
        self.__restrained = False
        self.__force = 0

    @property
    def displacement(self):
        return self.__displacement_value

    @displacement.setter
    def displacement(self, value):
        self.__displacement_value = value

    @property
    def force(self):
        return self.__force

    @force.setter
    def force(self, value):
        self.__force = value

    @property
    def restrained(self):
        return self.__restrained

    @restrained.setter
    def restrained(self, value: bool):
        self.__restrained = value
        if value:
            self.__displacement_value = 0

    @property
    def displaced(self):
        return self.__displacement_value

    @displaced.setter
    def displaced(self, value: float):
        self.__restrained = True
        self.__displacement_value = value

    def __str__(self):
        return "DOF ID: %d" % self.id

    def __repr__(self):
        return "DOF ID: %d" % self.id
