# Pyramid_Frame.py

from structural_analysis import Node, Structure, section, material, Solver, Visualizer
from structural_analysis.frame_elements import *

# Create nodes
node_1 = Node(0, 0, 0)
node_2 = Node(2, 0, 0)
node_3 = Node(1, 1, 1)
node_4 = Node(1, 0, 2)

# Create circular section
circle = section.Circle(0.05)

# Create rectangular section
rectangle = section.Rectangle(0.03, 0.06)

# define steel material instance
steel = material.Steel(yield_strength=250000, ultimate_strength=400000, elasticity_modulus=200*10**6, poissons_ratio=0.2)

# Create element objects
element_1 = FrameElement(node_1, node_3, rectangle, steel)
element_2 = FrameElement(node_2, node_3, rectangle, steel)
element_3 = TrussElement(node_4, node_3, circle, steel)

# assign boundary conditions
node_1.dof_x.restrained = True
node_1.dof_y.restrained = True
node_1.dof_z.restrained = True
node_1.dof_rx.restrained = True
node_1.dof_ry.restrained = True
node_1.dof_rz.restrained = True

node_2.dof_x.restrained = True
node_2.dof_y.restrained = True
node_2.dof_z.restrained = True

node_4.dof_x.restrained = True
node_4.dof_y.restrained = True
node_4.dof_z.restrained = True

# assign forces
node_3.dof_z.assign_force(7000)

# assign initial displacement (settlement)
node_2.dof_y.assign_initial_displacement(0.003)

# create structure object
structure = Structure([element_1, element_2, element_3])

# run analysis
solver = Solver(structure)
solver.run()

# show structure and deformed shape
vs = Visualizer(structure)

vs.show_structure()

vs.show_deformed_shape(10)

vs.execute_qt()
