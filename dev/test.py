import sys
from enum import auto
from typing import List

# Import Qt
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget
from scene import NodeScene
from viewer import PanZoomGraphicsView
from NodeGraphQt.qgraphics.node_base import NodeItem

class Viewer(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Viewer, self).__init__(parent)
        """
        Args:
            parent:
            undo_stack (QtWidgets.QUndoStack): undo stack from the parent
                                               graph controller.
        """
        self.viewer = PanZoomGraphicsView(self)
        self.scene = NodeScene(self)
        self.viewer.setScene(self.scene)

        self.viewer.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.viewer.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        self.viewer.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.viewer.setCacheMode(QtWidgets.QGraphicsView.CacheModeFlag.CacheBackground)
        self.viewer.setOptimizationFlag(QtWidgets.QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.viewer)
        self.setLayout(layout)

        # Create a node
        self.node = QtWidgets.QGraphicsRectItem(0, 0, 100, 100)
        self.node.setBrush(QtCore.Qt.GlobalColor.red)
        self.node.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.node.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.scene.addItem(self.node)

        self.node1 = QtWidgets.QGraphicsRectItem(600, 0, 100, 100)
        self.node1.setBrush(QtCore.Qt.GlobalColor.red)
        self.node1.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.node1.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)


        self.scene.addItem(self.node1)

        self.abstract_node = NodeItem("node", None)
        self.scene.addItem(self.abstract_node)

        self.abstract_nodeq = NodeItem("noqde", None)
        self.scene.addItem(self.abstract_nodeq)
        
        NodeItem.__base_color = QtGui.QColor(0,0,255,255)

        self.abstract_nodeqq = NodeItem("Blue Node", None)
        self.abstract_nodeqq.__base_color = QtGui.QColor(0,0,255,255)
        self.scene.addItem(self.abstract_nodeqq)

        # self.setAcceptDrops(True)
        # self.resize(850, 800)

        # self._scene_range = QtCore.QRectF(0, 0, self.size().width(), self.size().height())
        # self._update_scene()
        # self._last_size = self.size()

        # self._layout_direction = LayoutDirectionEnum.HORIZONTAL.value

        # self._pipe_layout = PipeLayoutEnum.CURVED.value
        # self._detached_port = None


class TestInterface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TestInterface, self).__init__(parent)
        self.viewer = Viewer(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.viewer)
        self.setLayout(layout)
        return
        # Create a graph object which can be manupulated by the user
        self.graph = QtWidgets.QGraphicsView(self)
        self.graph.setObjectName("graph")

        # Draw a rounded rectangle in the graph
        self.scene = QtWidgets.QGraphicsScene(self)
        self.graph.setScene(self.scene)

        # Create a node
        self.node = QtWidgets.QGraphicsRectItem(0, 0, 100, 100)
        self.node.setBrush(QtCore.Qt.GlobalColor.red)
        self.node.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.node.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.scene.addItem(self.node)
        # Allow user to move the scene around
        # Enable a 10x10 grid
        self.graph.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.graph.setCacheMode(QtWidgets.QGraphicsView.CacheModeFlag.CacheBackground)

        # Create a side panel to display the properties of the graph
        self.properties = QtWidgets.QWidget(self)
        self.properties.setObjectName("properties")

        # Create a layout to hold the graph and the properties panel
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.graph)
        self.layout.addWidget(self.properties)

        # Set the layout of the main window
        self.setLayout(self.layout)

        # Set the layout of the properties panel
        self.properties_layout = QtWidgets.QVBoxLayout(self.properties)
        self.properties.setLayout(self.properties_layout)

        # Create a button to add a node to the graph
        self.add_node_button = QtWidgets.QPushButton("Add Node", self)
        self.add_node_button.clicked.connect(self.add_node)
        self.properties_layout.addWidget(self.add_node_button)

    def add_node(self):
        print("Add Node")
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TestInterface()
    window.show()

    # Set the window size
    window.resize(800, 600)

    # bring it to the front
    window.raise_()
    sys.exit(app.exec_())
