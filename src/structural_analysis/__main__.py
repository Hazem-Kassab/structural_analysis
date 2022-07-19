from structural_analysis import Node, Structure, section, material, Solver, Visualization
from structural_analysis.frame_elements import *

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


section = Section.ArbitrarySection(3000, 180*10**6, 180*10**6, 360*10**6, 0)

steel = Material.Steel(250, 400, 200000, 0.2)

e15 = FrameElement(n1, n5, section, steel)
e26 = FrameElement(n2, n6, section, steel)
e37 = FrameElement(n3, n7, section, steel)
e48 = FrameElement(n4, n8, section, steel)

e56 = FrameElement(n5, n6, section, steel)
e68 = FrameElement(n6, n8, section, steel)
e87 = FrameElement(n8, n7, section, steel)
e57 = FrameElement(n5, n7, section, steel)

e59 = FrameElement(n5, n9, section, steel)
e610 = FrameElement(n10, n6, section, steel)
e711 = FrameElement(n11, n7, section, steel)
e812 = FrameElement(n8, n12, section, steel)

e910 = FrameElement(n9, n10, section, steel)
e1112 = FrameElement(n11, n12, section, steel)
e911 = FrameElement(n11, n9, section, steel)
e1012 = FrameElement(n10, n12, section, steel)

n1.dof_x.restrained = True
n1.dof_y.restrained = True
n1.dof_z.restrained = True


n3.dof_x.restrained = True
n3.dof_y.restrained = True
n3.dof_z.restrained = True
n3.dof_rx.restrained = True
n3.dof_ry.restrained = True
n3.dof_rz.restrained = True

n2.dof_x.restrained = True
n2.dof_y.restrained = True
n2.dof_z.restrained = True
n2.dof_rx.restrained = True
n2.dof_ry.restrained = True
n2.dof_rz.restrained = True

n4.dof_x.restrained = True
n4.dof_y.restrained = True
n4.dof_z.restrained = True
n4.dof_rx.restrained = True
n4.dof_ry.restrained = True
n4.dof_rz.restrained = True

n5.dof_z.assign_initial_displacement = -50

n10.dof_x.force = 2000000
n6.dof_z.force = 4000000


structure = Structure([e15, e26, e37, e48, e56, e68, e87, e57, e59, e610, e711, e812, e910, e1112, e911, e1012])

Solver.analyze_first_order_elastic(structure)

# Visualization.show_structure(structure)
# Visualization.show_deformed_shape(structure, 10, 1)
# Visualization.execute_qt()

