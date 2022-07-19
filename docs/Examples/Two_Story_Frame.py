# Two_Story_Frame.py
from structural_analysis import Node, Structure, section, material, Solver, Visualizer, DisplacementTable, ReactionsTable
from structural_analysis.frame_elements import *

# General considerations:
#    - y-axis is upward
#    - use consistent units
#    - each node has 6 degrees of freedom dx: dof_1, dy: dof_2, dz: dof_3, rx: dof_4, ry: dof_5, rz: dof_6

# create node objects <Node(x, y, z)>
n1 = Node(0, 0, 0)
n2 = Node(6000, 0, 0)
n3 = Node(0, 0, 6000)
n4 = Node(6000, 0, 6000)

n5 = Node(0, 6000, 0)
n6 = Node(6000, 6000, 0)
n7 = Node(0, 6000, 6000)
n8 = Node(6000, 6000, 6000)

n9 = Node(0, 12000, 0)
n10 = Node(6000, 12000, 0)
n11 = Node(0, 12000, 6000)
n12 = Node(6000, 12000, 6000)

dummy_node = Node(6000, 6000, 6000)
dummy_node.dof_x = n8.dof_x
dummy_node.dof_y = n8.dof_y
dummy_node.dof_z = n8.dof_z
dummy_node.dof_rx = n8.dof_rx
dummy_node.dof_ry = n8.dof_ry

# dummy_node_2 = Node(0, 6000, 6000)
# dummy_node_2.dof_x = n8.dof_x
# dummy_node_2.dof_y = n8.dof_y
# dummy_node_2.dof_z = n8.dof_z
# dummy_node_2.dof_rx = n8.dof_rx
# dummy_node_2.dof_ry = n8.dof_ry

# create section object
user_defined_section = section.ArbitrarySection(area=3000, inertia_y=180 * 10 ** 6, inertia_z=180 * 10 ** 6,
                                                polar_inertia=360*10**6, warping_rigidity=0)

# rectangular_section = section.Rectangle(breadth=150, depth=300)
rectangular_section = user_defined_section


# create material object
steel = material.Steel(yield_strength=250, ultimate_strength=400, elasticity_modulus=200000, poissons_ratio=0.2)

# create frame element objects <FrameElement(start_node: Node, end_node: Node, section: Section, material: Material)>
e15 = FrameElement(n1, n5, user_defined_section, steel)
e26 = FrameElement(n2, n6, user_defined_section, steel)
e37 = FrameElement(n3, n7, rectangular_section, steel)
e48 = FrameElement(n4, n8, rectangular_section, steel)

e56 = FrameElement(n5, n6, user_defined_section, steel)
e68 = FrameElement(n6, n8, user_defined_section, steel)
e87 = FrameElement(n7, dummy_node, rectangular_section, steel)
e57 = FrameElement(n5, n7, rectangular_section, steel)

e59 = FrameElement(n5, n9, user_defined_section, steel)
e610 = FrameElement(n10, n6, user_defined_section, steel)
e711 = FrameElement(n7, n11, rectangular_section, steel)
e812 = FrameElement(n8, n12, rectangular_section, steel)

e910 = FrameElement(n10, n9, rectangular_section, steel)
e1112 = FrameElement(n12, n11, rectangular_section, steel)
e911 = FrameElement(n11, n9, user_defined_section, steel)
e1012 = FrameElement(n12, n10, user_defined_section, steel)

# create truss element object
e16 = TrussElement(n1, n6, rectangular_section, steel)

# assign boundary conditions; node_1 is hinged, node_2, 3, 4 are fixed
n1.dof_x.restrained = True
n1.dof_y.restrained = True
n1.dof_z.restrained = True
n1.dof_rx.restrained = True
n1.dof_ry.restrained = True
n1.dof_rz.restrained = True

n2.dof_x.restrained = True
n2.dof_y.restrained = True
n2.dof_z.restrained = True
n2.dof_rx.restrained = True
n2.dof_ry.restrained = True
n2.dof_rz.restrained = True

n3.dof_x.restrained = True
n3.dof_y.restrained = True
n3.dof_z.restrained = True
n3.dof_rx.restrained = True
n3.dof_ry.restrained = True
n3.dof_rz.restrained = True

n4.dof_x.restrained = True
n4.dof_y.restrained = True
n4.dof_z.restrained = True
n4.dof_rx.restrained = True
n4.dof_ry.restrained = True
n4.dof_rz.restrained = True


# assign loads to node_10 in the x-direction, and to node_6 in the z-direction
# n7.dof_x.assign_force(2000000)
# n8.dof_x.assign_force(-2000000)
#
# # assign initial displacement to node_4 in the negative y-direction
# n4.dof_y.assign_initial_displacement(-1000)

from structural_analysis.load import PointLoad, ThermalLoad, DistributedLoad
# load = DistributedLoad(0, -500, 0, 0, 0, 0)
load_2 = PointLoad(fy=1e10)
# thermal_load = ThermalLoad(30)
# load.assign_to_element(e87, local=False)
load_2.assign_to_node(n8)
# thermal_load.assign_to_element(e87)

# create structure object
structure = Structure([e15, e26, e37, e48, e56, e68, e87, e57, e59, e610, e711, e812, e910, e1112, e911, e1012])
# run first_order_elastic analysis
solver = Solver(structure)
solver.run()

# show structure and deformed shape
vs = Visualizer(structure)
vs.show_structure()
vs.show_deformed_shape(scale=0.01)
# vs.show_diagram(0.000001)
vs.execute_qt()

# #####
# import numpy as np
# import matplotlib.pyplot as plt
# x = np.arange(0.0, e87.length + e87.length/100, e87.length/100)
# # print(x)
# bmd = np.zeros((x.shape))
# index = 0
# for l in x:
#     bmd[index] = e87.bending_moment_z(l)
#     index += 1
#
# # print(bmd)
# fig, ax = plt.subplots()
# ax.plot(x, bmd)
#
# ax.set(xlabel='x (mm)', ylabel='moment (N.mm)',
#        title='Bending Moment Diagram')
# ax.grid()
# plt.fill_between(x, bmd, color='red', alpha=.5)
# plt.show()
#####