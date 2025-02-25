from qtpy import QtCore, QtWidgets


class NodeTextItem(QtWidgets.QGraphicsTextItem):
    """
    NodeTextItem class used to display and edit the name of a NodeItem.
    """
    _locked:bool = False
    _text: str = ""

    text_update = QtCore.Signal(str)

    def __init__(self, text, parent=None):
        super(NodeTextItem, self).__init__(text, parent)
        self.set_locked(False)
        self.set_edit_mode(False)
        
    def mouseDoubleClickEvent(self, event):
        """
        Re-implemented to jump into edit mode when user clicks on node text.

        Args:
            event (QtWidgets.QGraphicsSceneMouseEvent): mouse event.
        """
        if not self._locked:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.set_edit_mode(True)
                
                event.ignore()
                return
        super(NodeTextItem, self).mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        """
        Re-implemented to catch the Return & Escape keys when in edit mode.

        Args:
            event (QtGui.QKeyEvent): key event.
        """
        if event.key() == QtCore.Qt.Key.Key_Return:
            current_text = self.toPlainText()
            self.text = current_text
            self.set_edit_mode(False)
        elif event.key() == QtCore.Qt.Key.Key_Escape:
            self.setPlainText(self.text)
            self.set_edit_mode(False)
        super(NodeTextItem, self).keyPressEvent(event)

    def focusOutEvent(self, event):
        """
        Re-implemented to jump out of edit mode.

        Args:
            event (QtGui.QFocusEvent):
        """
        current_text = self.toPlainText()
        self.text = current_text
        self.set_edit_mode(False)
        super(NodeTextItem, self).focusOutEvent(event)

    def set_edit_mode(self, value=False):
        """
        Set the edit mode for the text item.

        Args:
            value (bool):  true in edit mode.
        """
        if self._locked:
            return
        
        if value:
            self.setTextInteractionFlags(
                QtCore.Qt.TextInteractionFlag.TextEditable | QtCore.Qt.TextInteractionFlag.TextSelectableByMouse | QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard
            )
        else:
            self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)

    def set_locked(self, state=False):
        """
        Locks the text item so it can not be editable.

        Args:
            state (bool): lock state.
        """
        self._locked = state
        if self._locked:
            self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, False)
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
            self.setToolTip("")
        else:
            self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
            self.setToolTip("double-click to edit node name.")
            self.setCursor(QtCore.Qt.CursorShape.IBeamCursor)

    def update_alignment(self,parent_rect):
        h_offset, v_offset = (0, 0)
        text_rect = self.boundingRect()
        x = parent_rect.center().x() - (text_rect.width() / 2)
        self.setPos(x + h_offset, parent_rect.y() + v_offset)

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self.setPlainText(value)
        self.text_update.emit(value)

    # def set_node_name(self, name):
    #     """
    #     Updates the node name through the node "NodeViewer().node_name_changed"
    #     signal which then updates the node name through the BaseNode object this
    #     will register it as an undo command.

    #     Args:
    #         name (str): new node name.
    #     """
    #     name = name.strip()
    #     if name != self.node.name:
    #         viewer = self.node.viewer()
    #         viewer.node_name_changed.emit(self.node.id, name)


    # @property
    # def node(self):
    #     """
    #     Get the parent node item.

    #     Returns:
    #         NodeItem: parent node qgraphics item.
    #     """
    #     return self.parentItem()
