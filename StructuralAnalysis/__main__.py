from StructuralAnalysis.Structure import Structure
from StructuralAnalysis.Node import Node
from StructuralAnalysis.Material import Steel
from StructuralAnalysis.Section import ArbitrarySection
from StructuralAnalysis.Solver import analyze_first_order_elastic
from StructuralAnalysis import Visualization
import StructuralAnalysis.FrameElements as FE

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


section = ArbitrarySection(3000, 180*10**6, 180*10**6, 360*10**6, 0)

steel = Steel(250, 400, 200000, 0.2)

e15 = FE.FrameElement(n1, n5, section, steel)
e26 = FE.FrameElement(n2, n6, section, steel)
e37 = FE.FrameElement(n3, n7, section, steel)
e48 = FE.FrameElement(n4, n8, section, steel)

e56 = FE.FrameElement(n5, n6, section, steel)
e68 = FE.FrameElement(n6, n8, section, steel)
e87 = FE.FrameElement(n8, n7, section, steel)
e57 = FE.FrameElement(n5, n7, section, steel)

e59 = FE.FrameElement(n5, n9, section, steel)
e610 = FE.FrameElement(n10, n6, section, steel)
e711 = FE.FrameElement(n11, n7, section, steel)
e812 = FE.FrameElement(n8, n12, section, steel)

e910 = FE.FrameElement(n9, n10, section, steel)
e1112 = FE.FrameElement(n11, n12, section, steel)
e911 = FE.FrameElement(n11, n9, section, steel)
e1012 = FE.FrameElement(n10, n12, section, steel)

n1.dof_1.restrained = True
n1.dof_2.restrained = True
n1.dof_3.restrained = True
# n1.dof_4.restrained = True
# n1.dof_5.restrained = True
# n1.dof_6.restrained = True

n3.dof_1.restrained = True
n3.dof_2.restrained = True
n3.dof_3.restrained = True
n3.dof_4.restrained = True
n3.dof_5.restrained = True
n3.dof_6.restrained = True

n2.dof_1.restrained = True
n2.dof_2.restrained = True
n2.dof_3.restrained = True
n2.dof_4.restrained = True
n2.dof_5.restrained = True
n2.dof_6.restrained = True

n4.dof_1.restrained = True
n4.dof_2.restrained = True
n4.dof_3.restrained = True
n4.dof_4.restrained = True
n4.dof_5.restrained = True
n4.dof_6.restrained = True

n10.dof_1.force = 2000000
# n6.dof_3.force = 6000000


structure = Structure([e15, e26, e37, e48, e56, e68, e87, e57, e59, e610, e711, e812, e910, e1112, e911, e1012])
# structure = Structure([e15, e26, e59, e610, e56, e910])

analyze_first_order_elastic(structure)

Visualization.show_structure(structure)
Visualization.show_deformed_shape(structure, 10, 1)
Visualization.execute_qt()
