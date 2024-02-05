import sys
from enum import auto
from typing import List

# Import Qt
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget
from scene import NodeScene


class PanZoomGraphicsView(QtWidgets.QGraphicsView):
    _max_zoom = 2
    _min_zoom = 0.5

    def __init__(self, scene):
        super(PanZoomGraphicsView, self).__init__(scene)
        # Increase scene rect to allow infinite scrolling
        self.setSceneRect(QtCore.QRectF(-50000, -50000, 100000, 100000))
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def getZoom(self) -> float:
        """Get the current zoom level of the view."""
        return self.transform().m11()
    
    def get_zoom(self) -> float:
        """Deprecated: use getZoom() instead.
        """
        return self.getZoom()
    
    def wheelEvent(self, event: QtGui.QWheelEvent):
        """Zoom in or out of the view. based on the scroll wheel movement."""
        factor = 1.1
        if event.angleDelta().y() < 0:
            if self.getZoom() > self._max_zoom:
                return

            self.scale(factor, factor)

        else:
            # Zoom out
            if self.getZoom() < self._min_zoom:
                return

            self.scale(1.0 / factor, 1.0 / factor)
