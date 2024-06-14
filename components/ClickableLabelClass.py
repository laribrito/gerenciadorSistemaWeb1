from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class ClickableLabel(QLabel):
    def __init__(self, onClick, parent=None):
        super().__init__(parent)
        self.onClick = onClick

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Label clicado!")
            # Faça o que quiser quando o QLabel for clicado
