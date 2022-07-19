# Hinged_Fixed_2D_Frame.py

from structural_analysis import Node, Structure, section, material, Solver, Visualizer
from structural_analysis.frame_elements import *

# z-coordinate is set to zero when using TwoDimensionalFrameElement
n1 = Node(0, 0, 0)
n2 = Node(0, 6000, 0)
n3 = Node(8000, 6000, 0)
n4 = Node(8000, 0, 0)

# create arbitrary section with user defined properties
section = section.ArbitrarySection(area=2000, inertia_z=2*10**6, inertia_y=2*10**5,
                                   polar_inertia=2*10**5, warping_rigidity=10**4)

# create material object
steel = material.Steel(yield_strength=250, ultimate_strength=400, elasticity_modulus=200000, poissons_ratio=0.2)

e12 = TwoDimensionalFrameElement(n1, n2, section, steel)
e23 = TwoDimensionalFrameElement(n2, n3, section, steel)
e34 = TwoDimensionalFrameElement(n3, n4, section, steel)

# node_1 is hinged
n1.dof_x.restrained = True
n1.dof_y.restrained = True

# node_4 is fixed
n4.dof_x.restrained = True
n4.dof_y.restrained = True
n4.dof_rz.restrained = True

# assign load to node_3 in the x-direction
# n3.dof_x.assign_force(20 * 10 ** 3)

from structural_analysis.load import ThermalLoad, DistributedLoad, PointLoad
# thermal_load = ThermalLoad(300)
distributed_load = PointLoad(fx=-1000)
distributed_load.assign_to_element(e23, 4000)
# thermal_load.assign_to_element(e23)

# create structure object
structure = Structure([e12, e23, e34])

# Solve
solver = Solver(structure)
solver.run()

# Show structure and deformation
vs = Visualizer(structure)
vs.show_structure()
vs.show_deformed_shape(50)
vs.execute_qt()
