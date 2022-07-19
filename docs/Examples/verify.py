from structural_analysis import Node, Structure, section, material, Solver, Visualizer, load
from structural_analysis.frame_elements import *

a = 1000
P = 10000
node_1 = Node(0, 0, 0)
node_2 = Node(2*a, 0, 0)

dummy_node = Node(node_2.x, node_2.y, node_2.z)
dummy_node.dof_x = node_2.dof_x
dummy_node.dof_y = node_2.dof_y


section = section.Circle(25)
steel = material.Steel(200000, 0.2, 250, 400)

element_1 = TwoDimensionalFrameElement(node_1, dummy_node, section, steel)

node_1.dof_x.restrained = True
node_1.dof_y.restrained = True
node_1.dof_rz.restrained = True

node_2.dof_x.restrained = True
node_2.dof_y.restrained = True
node_2.dof_rz.restrained = True



tip_load = load.PointLoad(fy=-P)
tip_load.assign_to_element(element_1, a)
print(element_1.concentrated_loads)

beam = Structure([element_1])

solver = Solver(beam)
solver.run()

vs = Visualizer(beam)
vs.show_structure()
vs.show_deformed_shape(30)
vs.execute_qt()
print(dummy_node.dof_rz.displacement)


