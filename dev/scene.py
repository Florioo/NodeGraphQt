from enum import Enum

from qtpy import QtCore, QtGui, QtWidgets


class NodeScene(QtWidgets.QGraphicsScene):
    """Node scene class.
        This draws the background scene

    Args:
        QtWidgets (QGraphicsScene): QGraphicsScene object.
    """

    class GridMode(Enum):
        """Enum class for grid mode."""

        NONE = 0
        DOTS = 1
        LINES = 2

    # Parameters
    _grid_mode = GridMode.DOTS
    _grid_color = QtGui.QColor(230, 230, 230)
    _background_color = QtGui.QColor(255, 255, 255)
    _grid_size = 50
    _point_size = 5

    def __init__(self, parent=None):
        super(NodeScene, self).__init__(parent)
        self.setBackgroundBrush(self._background_color)

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        super(NodeScene, self).drawBackground(painter, rect)

        painter.save()
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, False)
        painter.setBrush(self.backgroundBrush())

        zoom = self.viewer.getZoom()  # type: ignore

        if self._grid_mode == self.GridMode.DOTS:
            if zoom < 0.5:
                zoom = 0.5

            pen = QtGui.QPen(self._grid_color, 0.65 * 5 / zoom)
            self._draw_dots(painter, rect, pen, self._grid_size)

        elif self._grid_mode == self.GridMode.LINES:
            # Draw subgrid
            if zoom > 0.5:
                pen = QtGui.QPen(self._grid_color, 0.65)
                self._draw_grid(painter, rect, pen, self._grid_size)

            # Draw main grid
            color = self._grid_color.darker(200)
            pen = QtGui.QPen(color, 0.65)
            self._draw_grid(painter, rect, pen, self._grid_size * 8)

        painter.restore()

    def _draw_grid(self, painter: QtGui.QPainter, rect: QtCore.QRectF, pen: QtGui.QPen, grid_size: int):
        """
        Draws the grid lines in the scene.

        Args:
            painter (QtGui.QPainter): painter object.
            rect (QtCore.QRectF): rect object.
            pen (QtGui.QPen): pen object.
            grid_size (int): grid size.
        """

        # Size of the grid.
        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        # Find the first left and top point.
        first_left = left - (left % grid_size)
        first_top = top - (top % grid_size)

        # Create the grid lines.
        lines = []
        lines.extend([QtCore.QLineF(x, top, x, bottom) for x in range(first_left, right, grid_size)])
        lines.extend([QtCore.QLineF(left, y, right, y) for y in range(first_top, bottom, grid_size)])

        # Draw the grid lines with the pen.
        painter.setPen(pen)
        painter.drawLines(lines)

    def _draw_dots(self, painter: QtGui.QPainter, rect: QtCore.QRectF, pen: QtGui.QPen, grid_size: int):
        """
        draws the grid dots in the scene.

        Args:
            painter (QtGui.QPainter): painter object.
            rect (QtCore.QRectF): rect object.
            pen (QtGui.QPen): pen object.
            grid_size (int): grid size.
        """
        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        first_left = left - (left % grid_size)
        first_top = top - (top % grid_size)

        painter.setPen(pen)

        [
            painter.drawPoint(int(x), int(y))
            for x in range(first_left, right, grid_size)
            for y in range(first_top, bottom, grid_size)
        ]

    @property
    def viewer(self) -> QtWidgets.QGraphicsView:
        # Get handle to the viewer widget.
        return self.views()[0]

    @property
    def grid_mode(self) -> GridMode:
        return self._grid_mode

    @grid_mode.setter
    def grid_mode(self, mode: GridMode):
        self._grid_mode = mode
