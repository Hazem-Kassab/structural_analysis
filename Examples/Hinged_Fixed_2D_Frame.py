# Hinged_Fixed_2D_Frame.py

from StructuralAnalysis import Node, Structure, Section, Material, Solver, Visualization
from StructuralAnalysis.FrameElements import *

# z-coordinate is set to zero when using TwoDimensionalFrameElement
n1 = Node(0, 0, 0)
n2 = Node(0, 6000, 0)
n3 = Node(8000, 6000, 0)
n4 = Node(8000, 0, 0)

# create arbitrary section with user defined properties
section = Section.ArbitrarySection(area=2000, inertia_z=2*10**6, inertia_y=2*10**5,
                                   polar_inertia=2*10**5, warping_rigidity=10**4)

# create material object
steel = Material.Steel(yield_strength=250, ultimate_strength=400, elasticity_modulus=200000, poissons_ratio=0.2)

e12 = TwoDimensionalFrameElement(n1, n2, section, steel)
e23 = TwoDimensionalFrameElement(n2, n3, section, steel)
e34 = TwoDimensionalFrameElement(n3, n4, section, steel)

# node_1 is hinged
n1.dof_1.restrained = True
n1.dof_2.restrained = True

# node_4 is fixed
n4.dof_1.restrained = True
n4.dof_2.restrained = True
n4.dof_6.restrained = True

# assign load to node_3 in the x-direction
n3.dof_1.force = 20*10**3

# create structure object
structure = Structure([e12, e23, e34])

# Solve
Solver.analyze_first_order_elastic(structure)

# Show structure and deformation
Visualization.show_structure(structure)
Visualization.show_deformed_shape(structure, 10, 1)
Visualization.execute_qt()
