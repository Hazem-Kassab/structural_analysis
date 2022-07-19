import time

import numpy as np
from structural_analysis.structure import Structure
import sys


class Solver:

    def __init__(self, structure: Structure):
        self.structure = structure
        self._free_degree_of_freedom_ids = [dof.id for dof in self.structure.free_degrees_of_freedom]
        self._restrained_degree_of_freedom_ids = [dof.id for dof in self.structure.restrained_degrees_of_freedom]

    def _assemble_global_stiffness_elastic_matrix(self):
        degree_of_freedom_ids = self._free_degree_of_freedom_ids + self._restrained_degree_of_freedom_ids
        no_dof = len(degree_of_freedom_ids)
        initialized_matrix = np.zeros((no_dof, no_dof))
        for element in self.structure.elements:
            i = 0
            for row in element.global_stiffness_matrix():
                j = 0
                for col in row:
                    k, z = element.degrees_of_freedom[i].id, element.degrees_of_freedom[j].id
                    initialized_matrix[degree_of_freedom_ids.index(k), degree_of_freedom_ids.index(z)] += col
                    j += 1
                i += 1

        return initialized_matrix

    def _assemble_restrained_displacement_vector(self):
        displacements = np.zeros((len(self.structure.restrained_degrees_of_freedom)))
        i = 0
        dofs_ids = []
        for dof in self.structure.restrained_degrees_of_freedom:
            dofs_ids.append(dof.id)
            displacements[i] = dof.displacement
            i += 1
        return displacements

    def _assemble_force_vector(self):
        forces = np.zeros((len(self._free_degree_of_freedom_ids)))
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            forces[i] = dof.force
            i += 1
        return forces

    def _assemble_fixed_end_reactions(self):
        forces = np.zeros((len(self._free_degree_of_freedom_ids)))
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            forces[i] = dof.fixed_end_reaction
            i += 1
        return forces

    def _solve_for_unknown_displacements(self, ff_matrix, fs_matrix, force_vector, fixed_end_reactions,
                                         restrained_displacements_vector):

        displacements = np.dot(np.linalg.inv(ff_matrix),
                               (force_vector-fixed_end_reactions) - np.dot(fs_matrix, restrained_displacements_vector))
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            dof.displacement = displacements[i]
            i += 1
        return displacements

    def _solve_for_unknown_reactions(self, sf_matrix, ss_matrix,
                                     solved_displacements_vector, restrained_displacements_vector, fixed_end_reactions):
        reactions = np.dot(sf_matrix, solved_displacements_vector) + \
                    np.dot(ss_matrix, restrained_displacements_vector) #+ fixed_end_reactions
        i = 0
        for dof in self.structure.restrained_degrees_of_freedom:
            dof.force = reactions[i]

            i += 1
        return reactions

    def _calc_straining_actions(self):
        for element in self.structure.elements:
            for x in element.local_mesh_coordinates:
                element.moment_z_values.append(element.bending_moment_z(x[0]))
                element.moment_y_values.append(element.bending_moment_y(x[0]))

    def _add_local_displacement_field_of_non_nodal_loads(self):
        elements_with_non_nodal_loads = [element for element in self.structure.elements if element.has_non_nodal_loads]
        for element in elements_with_non_nodal_loads:
            for load, location in element.concentrated_loads.items():
                valid_load = element.get_valid_load(load.load_array)
                element.add_concentrated_load_local_displacement_field(valid_load, location)
            for load in element.distributed_loads:
                valid_load = element.get_valid_load(load.load_array)
                element.add_distributed_load_local_displacement_field(valid_load)

    def run(self):
        t1 = time.process_time()
        print("solving...")
        global_matrix = self._assemble_global_stiffness_elastic_matrix()
        f_dof = len(self._free_degree_of_freedom_ids)
        ff_matrix = global_matrix[0: f_dof, 0:f_dof]
        fs_matrix = global_matrix[0:f_dof:, f_dof:]
        sf_matrix = global_matrix[f_dof:, 0:f_dof]
        ss_matrix = global_matrix[f_dof:, f_dof:]
        restrained_displacement_vector = self._assemble_restrained_displacement_vector()
        force_vector = self._assemble_force_vector()
        fixed_end_reactions = self._assemble_fixed_end_reactions()
        if np.linalg.cond(ff_matrix) >= 1 / sys.float_info.epsilon:
            import warnings
            warnings.warn("Matrix is singular or ill-conditioned! Check for stability.")
        else:
            unknown_displacements = self._solve_for_unknown_displacements(ff_matrix, fs_matrix,
                                                                          force_vector, fixed_end_reactions,
                                                                          restrained_displacement_vector)
            self._solve_for_unknown_reactions(sf_matrix, ss_matrix,
                                              unknown_displacements, restrained_displacement_vector,
                                              fixed_end_reactions)
            self.structure.solved = True
            print("Adding local displacement fields from elements non-nodal loads...")
            self._add_local_displacement_field_of_non_nodal_loads()
            print("Calculating straining actions...")
            # self._calc_straining_actions()
            t2 = time.process_time()
            print("Analysis Finished")
            print("Analysis time: %.3f sec" % (t2-t1))
