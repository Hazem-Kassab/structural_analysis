from StructuralAnalysis import Structure
from StructuralAnalysis.FrameElements import Element
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import math

__structure = None

app = QtGui.QApplication([])
w = gl.GLViewWidget()


def __initiate_window():
    distance = __get_camera_distance(__structure)
    w.setGeometry(50, 100, 700, 700)
    w.opts['distance'] = distance * 3
    w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
    gz = gl.GLGridItem()
    size = distance * 5
    gz.setSize(size, size, size)
    spacing = distance / 5
    gz.setSpacing(spacing, spacing, spacing)
    w.addItem(gz)
    axis = gl.GLAxisItem()
    size = distance / 5
    axis.setSize(size, size, size)
    axis.rotate(90, 0, 0, 90)
    axis.rotate(90, 0, 90, 0)
    w.addItem(axis)


def __get_camera_distance(structure):
    maximum = 0
    for node in structure.nodes:
        abs_max = max(abs(node.x), abs(node.y), abs(node.z))
        if abs_max > maximum:
            maximum = abs_max
    return maximum


def show_structure(structure: Structure):
    global __structure
    __structure = structure
    for element in structure.elements:
        x = np.array([element.start_node.x, element.end_node.x])
        y = np.array([element.start_node.y, element.end_node.y])
        z = np.array([element.start_node.z, element.end_node.z])

        pts = np.vstack([x, y, z]).T
        plt = gl.GLLinePlotItem(pos=pts, color='w', width=2, antialias=True)
        plt.rotate(angle=90, x=90, y=0, z=0)
        plt.rotate(angle=90, x=0, y=0, z=90)

        w.addItem(plt)
    global __max_coordinate


def show_deformed_shape(structure: Structure, number_of_stations: int, scale: int):
    global __structure
    __structure = structure
    for element in structure.elements:
        pts = __get_stations_global_displaced_position(element, number_of_stations, scale)
        plt = gl.GLLinePlotItem(pos=pts, color='r', width=2, antialias=True)
        plt.rotate(angle=90, x=90, y=0, z=0)
        plt.rotate(angle=90, x=0, y=0, z=90)
        w.addItem(plt)


def execute_qt():
    __initiate_window()
    w.show()
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


def __transformation_matrix(element):
    if element.start_node.x == element.end_node.x and element.start_node.y == element.end_node.y:
        if element.end_node.z > element.start_node.z:
            return np.array([[0, 0, 1],
                             [0, 1, 0],
                             [-1, 0, 0]])
        else:
            return np.array([[0, 0, -1],
                             [0, 1, 0],
                             [1, 0, 0]])
    else:
        cxx = (element.end_node.x - element.start_node.x) / element.length
        cyx = (element.end_node.y - element.start_node.y) / element.length
        czx = (element.end_node.z - element.start_node.z) / element.length
        d = math.sqrt(cxx ** 2 + cyx ** 2)
        cxy = -cyx / d
        cyy = cxx / d
        czy = 0
        cxz = -cxx * czx / d
        cyz = -cyx * czx / d
        czz = d
        return np.array([[cxx, cyx, czx],
                         [cxy, cyy, czy],
                         [cxz, cyz, czz]])


def __local_end_displacements(element: Element):
    gama_matrix = __transformation_matrix(element)
    global_displacements = np.array([element.start_node.dof_1.displacement,
                                    element.start_node.dof_2.displacement,
                                    element.start_node.dof_3.displacement,
                                    element.start_node.dof_4.displacement,
                                    element.start_node.dof_5.displacement,
                                    element.start_node.dof_6.displacement,
                                    element.end_node.dof_1.displacement,
                                    element.end_node.dof_2.displacement,
                                    element.end_node.dof_3.displacement,
                                    element.end_node.dof_4.displacement,
                                    element.end_node.dof_5.displacement,
                                    element.end_node.dof_6.displacement])
    transformation_matrix = np.zeros((12, 12))
    for i in range(4):
        transformation_matrix[(i * 3):(i + 1) * 3, (i * 3):(i + 1) * 3] = gama_matrix
    return np.dot(transformation_matrix, global_displacements)


def __get_stations_local_coordinates(element: Element, number_of_stations):
    local_coordinates = np.zeros((number_of_stations+1, 3))
    inter_station_length = element.length / number_of_stations
    for i in range(0, number_of_stations+1):
        local_coordinates[i] = np.array([i*inter_station_length, 0, 0])
    return local_coordinates


def __get_stations_global_coordinates(element: Element, number_of_stations, stations_local_coordinates):
    transformed_coordinates = np.zeros((number_of_stations+1, 3))
    transformation_matrrix = __transformation_matrix(element)
    i = 0
    for station_coordinates in stations_local_coordinates:
        transformed_coordinates[i] = np.dot(transformation_matrrix.T, station_coordinates.T) + \
                                     np.array([element.start_node.x, element.start_node.y, element.start_node.z])
        i += 1
    return transformed_coordinates


def __get_stations_local_displacement(element: Element, number_of_stations, stations_local_coordinates):
    stations_local_displacement = np.zeros((number_of_stations+1, 3))
    i = 0
    for station_coordinate in stations_local_coordinates:
        x = station_coordinate[0]
        local_displacement_vector = np.dot(element.shape_function_matrix(x), __local_end_displacements(element))
        columns = np.shape(local_displacement_vector)[0]
        stations_local_displacement[i, 0:columns] = local_displacement_vector
        i += 1
    return stations_local_displacement


def __get_stations_global_displaced_position(element: Element, number_of_stations, scale):
    stations_local_coordinates = __get_stations_local_coordinates(element, number_of_stations)
    stations_global_displaced_position = np.zeros((number_of_stations+1, 3))
    stations_local_displacements = __get_stations_local_displacement(element, number_of_stations,
                                                                     stations_local_coordinates)
    stations_global_coordinates = __get_stations_global_coordinates(element, number_of_stations,
                                                                    stations_local_coordinates)
    transformation_matrix = __transformation_matrix(element)
    i = 0
    for displacements in stations_local_displacements:
        global_displacement = np.dot(scale, np.dot(transformation_matrix.T, displacements.T))
        global_position = global_displacement + stations_global_coordinates[i]
        stations_global_displaced_position[i] = global_position
        i += 1
    return stations_global_displaced_position
