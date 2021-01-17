#Pyramid_Frame.py

from StructuralAnalysis import Node, Structure, Section, Material, Solver, Visualization
from StructuralAnalysis.FrameElements import *

node_1 = Node(0, 0, 0)
node_2 = Node(2, 0, 0)
node_3 = Node(1, 1, 1)
node_4 = Node(1, 0, 2)

circle = Section.Circle(0.05)

rectangle = Section.Rectangle(0.03, 0.06)

steel = Material.Steel(250000, 400000, 200*10**6, 0.2)

element_1 = FrameElement(node_1, node_3, rectangle, steel)
element_2 = FrameElement(node_2, node_3, rectangle, steel)

element_3 = TrussElement(node_4, node_3, circle, steel)

node_1.dof_1.restrained = True
node_1.dof_2.restrained = True
node_1.dof_3.restrained = True
node_1.dof_4.restrained = True
node_1.dof_5.restrained = True
node_1.dof_6.restrained = True

node_2.dof_1.restrained = True
node_2.dof_2.restrained = True
node_2.dof_3.restrained = True

node_4.dof_1.restrained = True
node_4.dof_2.restrained = True
node_4.dof_3.restrained = True

node_3.dof_3.force = 7000

node_2.dof_2.displacement = 0.003

structure = Structure([element_1, element_2, element_3])

Solver.analyze_first_order_elastic(structure)

Visualization.show_structure(structure)

Visualization.show_deformed_shape(structure, 10, 20)

Visualization.execute_qt()