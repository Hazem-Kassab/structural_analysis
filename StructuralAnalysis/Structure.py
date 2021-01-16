"""
This class assembles element objects and creates the structure.
Attributes:
    self.elements: list of Element objects that is initialized by user
    self.nodes: list of Node objects associated with elements sorted by the nodes ids
    self.degrees_of_freedom: list of DegreeOfFreedom objects associated with self.nodes sorted by the objects id
    self.free_degrees_of_freedom: list of the DegreeOfFreedom objects extracted from self.degrees_of_freedom
                                  that have their restrained property set to False. (sorted by id)
    self.restrained_degrees_of_freedom: list of the DegreeOfFreedom objects extracted from self.degrees_of_freedom
                                  that have their restrained property set to True. (sorted by id)
    self.no_of_degrees_of_freedom: the greatest dof.id number

Properties:
    self.global_matrix: assembles the global stiffness matrix where columns and rows are indexed by the sorted
                        self.degrees_of_freedom (id - 1)
Methods:
    self.__nodes: returns a tuple of two lists that are sorted by id(nodes, degrees_of_freedom) to
                  set self.nodes, self.degrees_of_freedom = self.__nodes()
    self.__free_and_restrained_dofs: returns a tuple of two lists that are sorted by id(free_dofs, restrained_dofs) to
                                     set (self.free_degrees_of_freedom,
                                          self.restrained_degree_of_freedom = self.__free_and_restrained_dofs()
    self.ff_matrix: assembles the Kff matrix and returns it as array
    self.__sf_matrix: assembles the Ksf matrix and returns it as array
    self.force_vector: assembles the forces of the self.free_degrees_of_freedom and returns it as array
    self.solve_for_displacements: multiplies the inverse of self.ff_matrix by self.force_vector and returns the result
                               as array
    self.solve_for_reactions: multiplies the self.__sf_matrix by self.solve_for_displacements and return the result as
                            array
    self.run: checks if the self.ff_matrix is invertible or singular. If invertible, a call is made to methods
              self.solve_for_displacments and self.solve_for_reactions. Then prints the results.

"""


from StructuralAnalysis.FrameElements import Element


class Structure:

    def __init__(self, elements: [Element]):
        self.elements = elements
        self.nodes, self.degrees_of_freedom = self.__nodes()
        self.free_degrees_of_freedom, self.restrained_degrees_of_freedom = self.__free_and_restrained_dofs()
        self.no_of_degrees_of_freedom = self.degrees_of_freedom[-1].id

    def __nodes(self):
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
        return sorted(nodes, key=lambda x: x.id), sorted(dofs, key=lambda x: x.id)

    def __free_and_restrained_dofs(self):
        free_dofs = []
        restrained_dofs = []
        for dof in self.degrees_of_freedom:
            if not dof.restrained:
                free_dofs.append(dof)
            else:
                restrained_dofs.append(dof)
        return sorted(free_dofs, key=lambda x: x.id), sorted(restrained_dofs, key=lambda x: x.id)
