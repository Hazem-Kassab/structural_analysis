from StructuralAnalysis.__SolverHelper import *
from StructuralAnalysis import Structure
import warnings
import sys


def analyze_first_order_elastic(structure: Structure):
    global_matrix = global_elastic_matrix(structure)
    ff, fs, sf, ss = partition_global_matrix(structure, global_matrix)
    support_settlements = restrained_displacement_vector(structure)
    external_force_vector = force_vector(structure)

    if np.linalg.cond(ff) >= 1 / sys.float_info.epsilon:
        warnings.warn("Matrix is singular or ill-conditioned! Check for stability.")
    else:
        __print_input_to_txt(structure)
        displacements = solve_for_displacements(structure, ff, fs, support_settlements, external_force_vector)
        reactions = solve_for_reactions(structure, displacements, support_settlements, sf, ss)
        __print_results_to_txt(structure)
        print("*********DISPLACEMENTS***********")
        print(displacements)
        print("***********REACTIONS*************")
        print(reactions)



def analyze_second_order_elastic(structure: Structure):
    pass


def analyze_first_order_inelastic(structure: Structure):
    pass


def analyze_second_order_inelastic(structure: Structure):
    pass


def __print_input_to_txt(structure: Structure):
    txt = open("Input.txt", "w+")
    txt.truncate(0)
    txt.writelines("########################### INPUT ###########################\n\n")

    txt.writelines("******* NODES *******\n")
    txt.writelines("Node ID\t\t\tX\t\t\t\t\t\tY\t\t\t\t\t\tZ\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t\t%.2e\t\t\t\t\t\t%.2e\t\t\t\t\t\t%.2e\n" % (node.id, node.x, node.y, node.z))

    txt.writelines("\n")
    txt.writelines("******* ELEMENTS *******\n")
    txt.writelines("Element ID\t\t\tStart Node\t\t\tEnd Node\n")
    for element in structure.elements:
        txt.writelines("%d\t\t\t\t%d\t\t\t\t%d\n" %(element.id, element.start_node.id, element.end_node.id))
    txt.writelines("\n")
    txt.writelines("******* BOUNDARY CONDITIONS *******\n")
    txt.writelines("True: Restrained, False: Free\n")
    txt.writelines("Node ID\t\tX-Disp.\t\tY-Disp.\t\tZ-Disp.\t\tX-Rot.\t\tY-Rot.\t\tZ-Rot.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\n" %
                       (node.id, node.dof_1.restrained, node.dof_2.restrained,
                        node.dof_3.restrained, node.dof_4.restrained,
                        node.dof_5.restrained, node.dof_6.restrained))
    txt.writelines("\n")
    txt.writelines("******* INITIAL SETTLEMENT *******\n")
    txt.writelines("Node ID\t\tX-Disp.\t\tY-Disp.\t\tZ-Disp.\t\tX-Rot.\t\tY-Rot.\t\tZ-Rot.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\n" %
                       (node.id, node.dof_1.displaced, node.dof_2.displaced,
                        node.dof_3.displaced, node.dof_4.displaced,
                        node.dof_5.displaced, node.dof_6.displaced))
    txt.writelines("\n")
    txt.writelines("******* APPLIED FORCES *******\n")
    txt.writelines("Node ID\t\tFX.\t\tFY.\t\tFZ.\t\tMX.\t\tMY.\t\tMZ.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\t\t%.2e\n" %
                       (node.id, node.dof_1.force, node.dof_2.force,
                        node.dof_3.force, node.dof_4.force,
                        node.dof_5.force, node.dof_6.force))
    txt.close()


def __print_results_to_txt(structure: Structure):
    txt = open("Results.txt", "w+")
    txt.truncate(0)
    txt.writelines("########################### OUTPUT ###########################\n\n")

    txt.writelines("\n")
    txt.writelines("******* DISPLACEMENTS *******\n")
    txt.writelines("Node ID\t\t\tX-Disp.\t\t\t\tY-Disp.\t\t\t\tZ-Disp.\t\t\t\tX-Rot.\t\t\t\tY-Rot.\t\t\t\tZ-Rot.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\n" %
                       (node.id, node.dof_1.displaced, node.dof_2.displaced,
                        node.dof_3.displaced, node.dof_4.displaced,
                        node.dof_5.displaced, node.dof_6.displaced))
    txt.writelines("\n")
    txt.writelines("******* REACTIONS *******\n")
    txt.writelines("Node ID\t\t\tFX.\t\t\t\tFY.\t\t\t\tFZ.\t\t\t\tMX.\t\t\t\tMY.\t\t\t\tMZ.\n")
    for node in structure.nodes:
        txt.writelines("%d\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\t\t\t  %.2e\n" %
                       (node.id, node.dof_1.force, node.dof_2.force,
                        node.dof_3.force, node.dof_4.force,
                        node.dof_5.force, node.dof_6.force))
    txt.close()






