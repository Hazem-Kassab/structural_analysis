from structural_analysis.structure import Structure
from structural_analysis.frame_elements.element import Element
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np


class Visualizer:

    def __init__(self, structure: Structure):
        self.app = QtGui.QApplication([])
        self.w = gl.GLViewWidget()
        self.structure = structure

    def _initiate_window(self):
        distance = self._get_camera_distance()
        self.w.setGeometry(50, 100, 700, 700)
        self.w.opts['distance'] = distance * 3
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        gz = gl.GLGridItem()
        size = distance * 5
        gz.setSize(size, size, size)
        spacing = distance / 5
        gz.setSpacing(spacing, spacing, spacing)
        self.w.addItem(gz)
        axis = gl.GLAxisItem()
        size = distance / 5
        axis.setSize(size, size, size)
        axis.rotate(90, 0, 0, 90)
        axis.rotate(90, 0, 90, 0)
        self.w.addItem(axis)

    def _get_camera_distance(self):
        maximum = 0
        for node in self.structure.nodes:
            abs_max = max(abs(node.x), abs(node.y), abs(node.z))
            if abs_max > maximum:
                maximum = abs_max
        return maximum

    def show_structure(self):
        for element in self.structure.elements:
            pts = np.stack([element.start_node.position_vector, element.end_node.position_vector])
            self.add_plot(pts, 'w', 2)

    def show_deformed_shape(self, scale: float):
        for element in self.structure.elements:
            pts = element.global_deformed_position(scale).T
            self.add_plot(pts, 'r', 1)

    def show_diagram(self, scale):
        for element in self.structure.elements:
            empty_array = (element.element_subdivisions+1)*[0]
            local_pts = np.array([empty_array, element.moment_z_values, empty_array]) * scale
            pts = (element._geometry_transformation_matrix().T.dot(local_pts)).T
            translation = element.global_mesh_coordinates
            global_position = pts+translation.T
            self.add_plot(global_position, 'c', 0.5)
            index = 0
            while index < element.element_subdivisions+1:
                pts = np.stack([element.global_mesh_coordinates.T[index], global_position[index]])
                self.add_plot(pts, 'c', 0.5)
                index += 1

    def add_plot(self, plot_points, color, width):
        plt = gl.GLLinePlotItem(pos=plot_points, color=color, width=width, antialias=True)
        plt.rotate(angle=90, x=90, y=0, z=0)
        plt.rotate(angle=90, x=0, y=0, z=90)
        self.w.addItem(plt)

    def execute_qt(self):
        self._initiate_window()
        self.w.show()
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()