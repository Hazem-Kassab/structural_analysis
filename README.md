# StructuralAnalysis
 Library to perfrom framed structures analysis

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install StructuralAnalysis.

```bash
pip install StructuralAnalysis
```

## Requirements
The following packages must be installed first:

```bash
pip install numpy==1.19.5
pip install PyOpenGL==3.1.5
pip install PyQt5==5.15.2
pip install pyqtgraph==0.11.1
```
## Usage

```python
from StructuralAnalysis import Node, Structure, Section, Material, Solver, Visualization
from StructuralAnalysis.FrameElements import *

# General considerations:
#    - y-axis is upward
#    - use consistent units
#    - each node has 6 degrees of freedom dx: dof_1, dy: dof_2, dz: dof_3, rx: dof_4, ry: dof_5, rz: dof_6

#create node objects <Node(x, y, z)>
node_1 = Node(0, 0, 0)
node_2 = Node(2, 0, 0)
node_3 = Node(1, 1, 1)
node_4 = Node(1, 0, 2)

#create section object <Section.Circle(radius)>
circle = Section.Circle(0.05)

#create section object <Section.Square(breadth, depth)>
rectangle = Section.Rectangle(0.03, 0.06)

#create material object <Material.Steel(yield_strength, ultimate_strength, modulus_of_elasticity. poissons_ratio)>
steel = Material.Steel(250000, 400000, 200*10**6, 0.2)

#create frame element objects <FrameElement(start_node: Node, end_node: Node, section: Section, material: Material)>
element_1 = FrameElement(node_1, node_3, rectangle, steel)
element_2 = FrameElement(node_2, node_3, rectangle, steel)

#create truss element object <TrussElement(start_node: Node, end_node: Node, section: Section, material: Material)>
element_3 = TrussElement(node_4, node_3, circle, steel)

#define fixities; node_1 is fixed, node_2 & node_4 are hinged
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

#define acting forces; applied to node_3 in the z-direction
node_3.dof_3.force = 700

#set initial displacement to node 2 in the y-direction
node_2.dof_2.displacement = 0.001

#create sttucture object <Structure(elements: list(Element))>
structure = Structure([element_1, element_2, element_3])

#run first order elastic analysis
Solver.analyze_first_order_elastic(structure)

#display structure (x is blue, y is yellow, z is green)
Visualization.show_structure(structure)

#display deformed structure <show_deformed_shape(structure, element_signments, scale)> (displayed in red)
Visualization.show_deformed_shape(structure, 10, 200)

Visualization.execute_qt()



```

##Under Development
The following enhancements will be included soon:
 * Releases at element end nodes.
 * Non-nodal loading.
 * Straining actions diagrams
 * Initial thermal straining.
 * Second-order elastic analysis.
 * First-order inelastic analysis.
 * Second-order inelastic analysis.
 * Eigenvalue analysis of buckling.
 * Dynamic analysis
 
## Considerations
Kindly note that the library is still under development, errors may arise as
the library has not been tested and exceptions have not been handled. The visualization depends on graphics library 
"PyQtGraph" which is still in its early stages of development, as a result, some of the features of displaying texts
(i.e., node labels, axis labels, ..) have not been included yet.

