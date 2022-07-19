# from pyqtgraph.Qt import QtCore, QtGui
# import pyqtgraph.opengl as gl
# import numpy as np
#
#
# app = QtGui.QApplication([])
# w = gl.GLViewWidget()
#
# w.setGeometry(50, 100, 700, 700)
# w.opts['distance'] = 3
# w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
# gz = gl.GLGridItem()
# size = 5
# gz.setSize(size, size, size)
# spacing = 1
# gz.setSpacing(spacing, spacing, spacing)
# w.addItem(gz)
# axis = gl.GLAxisItem()
# size = 1
# axis.setSize(size, size, size)
# axis.rotate(90, 0, 0, 90)
# axis.rotate(90, 0, 90, 0)
# w.addItem(axis)
# w_gl_item = gl.GLSurfacePlotItem(x=np.array([0, 1, 2, 3, 4]), y=np.array([1, 1, 1, 1, 1]), z=np.array([[0, 0, 0, 0, 0],
#                                                                            [0, 0, 0, 0, 0],
#                                                                            [0, 0, 0, 0, 0],
#                                                                            [0, 0, 0, 0, 0],
#                                                                            [0, 0, 0, 0, 0]]),
#                                   shader='normalColor', color=(0.5, 0.5, 1, 1), glOptions='additive')
# w_gl_item.rotate(90, 0, 90, 0)
# w.addItem(w_gl_item)
# w.show()
# QtGui.QApplication.instance().exec_()

# """
# Demonstration of some of the shader programs included with pyqtgraph that can be
# used to affect the appearance of a surface.
# """
#
# import numpy as np
#
# import pyqtgraph as pg
# import pyqtgraph.opengl as gl
#
# app = pg.mkQApp("GLShaders Example")
# w = gl.GLViewWidget()
# w.show()
# w.setWindowTitle('pyqtgraph example: GL Shaders')
# w.setCameraPosition(distance=15, azimuth=-90)
#
# g = gl.GLGridItem()
# g.scale(2,2,1)
# w.addItem(g)
#
# md = gl.MeshData.sphere(rows=10, cols=20)
# x = np.linspace(-8, 8, 6)
#
# m1 = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 0, 0, 0.2), shader='balloon', glOptions='additive')
# m1.translate(x[0], 0, 0)
# m1.scale(1, 1, 2)
# w.addItem(m1)
#
# m2 = gl.GLMeshItem(meshdata=md, smooth=True, shader='normalColor', glOptions='opaque')
# m2.translate(x[1], 0, 0)
# m2.scale(1, 1, 2)
# # w.addItem(m2)
#
# m3 = gl.GLMeshItem(meshdata=md, smooth=True, shader='viewNormalColor', glOptions='opaque')
# m3.translate(x[2], 0, 0)
# m3.scale(1, 1, 2)
# # w.addItem(m3)
#
# m4 = gl.GLMeshItem(meshdata=md, smooth=True, shader='shaded', glOptions='opaque')
# m4.translate(x[3], 0, 0)
# m4.scale(1, 1, 2)
# # w.addItem(m4)
#
# m5 = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 0, 0, 1), shader='edgeHilight', glOptions='opaque')
# m5.translate(x[4], 0, 0)
# m5.scale(1, 1, 2)
# # w.addItem(m5)
#
# m6 = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 0, 0, 1), shader='heightColor', glOptions='opaque')
# m6.translate(x[5], 0, 0)
# m6.scale(1, 1, 2)
# w.addItem(m6)
#
# if __name__ == '__main__':
#     pg.exec()