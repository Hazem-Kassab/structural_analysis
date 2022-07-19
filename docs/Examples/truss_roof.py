# truss_roof.py
from structural_analysis import Node, frame_elements, material, section, structure, visualizer, Solver, output

# create node instances
n1 = Node(0, 0, 0)
n2 = Node(1000, 0, 0)
n3 = Node(2000, 0, 0)
n4 = Node(3000, 0, 0)
n5 = Node(4000, 0, 0)
n6 = Node(5000, 0, 0)
n7 = Node(6000, 0, 0)
n8 = Node(7000, 0, 0)
n9 = Node(8000, 0, 0)

n21 = Node(0, 1000, 0)
n22 = Node(1000, 1000, 0)
n23 = Node(2000, 1000, 0)
n24 = Node(3000, 1000, 0)
n25 = Node(4000, 1000, 0)
n26 = Node(5000, 1000, 0)
n27 = Node(6000, 1000, 0)
n28 = Node(7000, 1000, 0)
n29 = Node(8000, 1000, 0)

# create section
section_1 = section.Circle(20)

# define material
steel = material.Steel(200000, 0.3)

# create lower chords elements
lower_1 = frame_elements.TwoDimensionalTrussElement(n1, n2, section_1, steel)
lower_2 = frame_elements.TwoDimensionalTrussElement(n2, n3, section_1, steel)
lower_3 = frame_elements.TwoDimensionalTrussElement(n3, n4, section_1, steel)
lower_4 = frame_elements.TwoDimensionalTrussElement(n4, n5, section_1, steel)
lower_5 = frame_elements.TwoDimensionalTrussElement(n5, n6, section_1, steel)
lower_6 = frame_elements.TwoDimensionalTrussElement(n6, n7, section_1, steel)
lower_7 = frame_elements.TwoDimensionalTrussElement(n7, n8, section_1, steel)
lower_8 = frame_elements.TwoDimensionalTrussElement(n8, n9, section_1, steel)
lower_chords = [lower_1, lower_2, lower_3, lower_4, lower_5, lower_6, lower_7, lower_8]

# create upper chords elements
upper_1 = frame_elements.TwoDimensionalTrussElement(n22, n23, section_1, steel)
upper_2 = frame_elements.TwoDimensionalTrussElement(n23, n24, section_1, steel)
upper_3 = frame_elements.TwoDimensionalTrussElement(n24, n25, section_1, steel)
upper_4 = frame_elements.TwoDimensionalTrussElement(n25, n26, section_1, steel)
upper_5 = frame_elements.TwoDimensionalTrussElement(n26, n27, section_1, steel)
upper_6 = frame_elements.TwoDimensionalTrussElement(n27, n28, section_1, steel)
upper_chords = [upper_1, upper_2, upper_3, upper_4, upper_5, upper_6]

# create diagonal elements
diagonal_r = frame_elements.TwoDimensionalTrussElement(n1, n22, section_1, steel)
diagonal_1 = frame_elements.TwoDimensionalTrussElement(n22, n3, section_1, steel)
diagonal_2 = frame_elements.TwoDimensionalTrussElement(n23, n4, section_1, steel)
diagonal_3 = frame_elements.TwoDimensionalTrussElement(n24, n5, section_1, steel)
diagonal_4 = frame_elements.TwoDimensionalTrussElement(n26, n5, section_1, steel)
diagonal_5 = frame_elements.TwoDimensionalTrussElement(n27, n6, section_1, steel)
diagonal_6 = frame_elements.TwoDimensionalTrussElement(n28, n7, section_1, steel)
diagonal_l = frame_elements.TwoDimensionalTrussElement(n28, n9, section_1, steel)
diagonals = [diagonal_r, diagonal_1, diagonal_2, diagonal_3, diagonal_4, diagonal_5, diagonal_6, diagonal_l]

# create vertical elements
vertical_1 = frame_elements.TwoDimensionalTrussElement(n22, n2, section_1, steel)
vertical_2 = frame_elements.TwoDimensionalTrussElement(n23, n3, section_1, steel)
vertical_3 = frame_elements.TwoDimensionalTrussElement(n24, n4, section_1, steel)
vertical_4 = frame_elements.TwoDimensionalTrussElement(n25, n5, section_1, steel)
vertical_5 = frame_elements.TwoDimensionalTrussElement(n26, n6, section_1, steel)
vertical_6 = frame_elements.TwoDimensionalTrussElement(n27, n7, section_1, steel)
vertical_7 = frame_elements.TwoDimensionalTrussElement(n28, n8, section_1, steel)
verticals = [vertical_1, vertical_2, vertical_3, vertical_4, vertical_5, vertical_6, vertical_7]

# assign forces
n22.dof_y.assign_force(-10000)
n23.dof_y.assign_force(-10000)
n24.dof_y.assign_force(-10000)
n25.dof_y.assign_force(-10000)
n26.dof_y.assign_force(-10000)
n27.dof_y.assign_force(-10000)
n28.dof_y.assign_force(-10000)

# assign boundary conditions
n1.dof_y.restrained = True
n1.dof_x.restrained = True
n9.dof_y.restrained = True

# assemble structure object
truss = structure.Structure(lower_chords + upper_chords + verticals + diagonals)

# run analysis
truss_solver = Solver(truss)
truss_solver.run()

# show structure and deformed shape
truss_visualizer = visualizer.Visualizer(truss)
truss_visualizer.show_structure()
truss_visualizer.show_deformed_shape(30)
truss_visualizer.execute_qt()

# show results
disp_table = output.DisplacementTable(truss)
disp_table.print()
disp_table.write_to_csv()
reactions = output.ReactionsTable(truss)
reactions.write_to_csv()
