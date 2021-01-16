import numpy as np
from StructuralAnalysis.Structure import Structure


def global_elastic_matrix(structure: Structure):
    no_dof = structure.no_of_degrees_of_freedom
    initialized_matrix = np.zeros((no_dof, no_dof))
    for element in structure.elements:
        element_matrix = np.zeros((no_dof, no_dof))
        i = 0
        for row in element.matrix:
            j = 0
            for col in row:
                k, z = element.degrees_of_freedom[i].id - 1, element.degrees_of_freedom[j].id - 1
                element_matrix[k, z] = col
                j += 1
            i += 1
        initialized_matrix = np.add(initialized_matrix, element_matrix)

    return initialized_matrix


def global_elastic_geometric_matrix(structure: Structure):
    no_dof = structure.no_of_degrees_of_freedom
    initialized_matrix = np.zeros((no_dof, no_dof))
    for element in structure.elements:
        element_matrix = np.zeros((no_dof, no_dof))
        i = 0
        for row in element.elastic_geometric_matrix:
            j = 0
            for col in row:
                k, z = element.degrees_of_freedom[i].id - 1, element.degrees_of_freedom[j].id - 1
                element_matrix[k, z] = col
                j += 1
            i += 1
        initialized_matrix = np.add(initialized_matrix, element_matrix)

    return initialized_matrix


def partition_global_matrix(structure, global_matrix):

    def ff_matrix():
        no_dof = len(structure.free_degrees_of_freedom)
        matrix = np.zeros((no_dof, no_dof))
        i = 0
        for dof_i in structure.free_degrees_of_freedom:
            j = 0
            for dof_j in structure.free_degrees_of_freedom:
                current = global_matrix[dof_i.id - 1, dof_j.id - 1]
                matrix[i, j] = current
                j += 1
            i += 1
        return matrix

    def fs_matrix():
        no_doff = len(structure.free_degrees_of_freedom)
        no_dofs = len(structure.restrained_degrees_of_freedom)
        matrix = np.zeros((no_doff, no_dofs))
        i = 0
        for dof_i in structure.free_degrees_of_freedom:
            j = 0
            for dof_j in structure.restrained_degrees_of_freedom:
                current = global_matrix[dof_i.id - 1, dof_j.id - 1]
                matrix[i, j] = current
                j += 1
            i += 1
        return matrix

    def sf_matrix():
        no_doff = len(structure.free_degrees_of_freedom)
        no_dofs = len(structure.restrained_degrees_of_freedom)
        matrix = np.zeros((no_dofs, no_doff))
        i = 0
        for dof_i in structure.restrained_degrees_of_freedom:
            j = 0
            for dof_j in structure.free_degrees_of_freedom:
                matrix[i, j] = global_matrix[dof_i.id - 1, dof_j.id - 1]
                j += 1
            i += 1
        return matrix

    def ss_matrix():
        no_dof = len(structure.restrained_degrees_of_freedom)
        matrix = np.zeros((no_dof, no_dof))
        i = 0
        for dof_i in structure.restrained_degrees_of_freedom:
            j = 0
            for dof_j in structure.restrained_degrees_of_freedom:
                matrix[i, j] = global_matrix[dof_i.id - 1, dof_j.id - 1]
                j += 1
            i += 1
        return matrix

    return ff_matrix(), fs_matrix(), sf_matrix(), ss_matrix()


def force_vector(structure):
    forces = np.zeros((len(structure.free_degrees_of_freedom)))
    i = 0
    for dof in structure.free_degrees_of_freedom:
        forces[i] = dof.force
        i += 1
    return forces


def restrained_displacement_vector(structure):
    displacements = np.zeros((len(structure.restrained_degrees_of_freedom)))
    i = 0
    for dof in structure.restrained_degrees_of_freedom:
        displacements[i] = dof.displacement
        i += 1
    return displacements


def solve_for_displacements(structure, ff_matrix, fs_matrix, restrained_displacements, forces):
    displacements = np.dot(np.linalg.inv(ff_matrix),
                           forces - np.dot(fs_matrix, restrained_displacements))
    i = 0
    for dof in structure.free_degrees_of_freedom:
        dof.displacement = displacements[i]
        i += 1
    return displacements


def update_node_coordinates(structure):
    for node in structure.nodes:
        node.x = node.x + node.dof_1.displacement
        node.y = node.y + node.dof_2.displacement
        node.z = node.z + node.dof_3.displacement


def solve_for_reactions(structure, displacements, restrained_displacements, sf_matrix, ss_matrix):
    reactions = np.dot(sf_matrix, displacements) + \
                np.dot(ss_matrix, restrained_displacements)
    i = 0
    for dof in structure.restrained_degrees_of_freedom:
        dof.force = reactions[i]
        i += 1
    return reactions
