from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton


class Button(QPushButton):
    """Custom QPushButton class."""
    def __init__(self, btn_label, signal, btn_name = None,):
        """Initialize and set default configurations."""
        super().__init__()
        self.setObjectName(btn_name)
        self.setText(btn_label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.signal = signal
        self.clicked.connect(self.signal)
