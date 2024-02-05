import sys
from enum import auto
from typing import List

# Import Qt
from qtpy import QtCore, QtWidgets
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget

class TestInterface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TestInterface, self).__init__(parent)

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
