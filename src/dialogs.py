from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QDialog

from src.widgets import Button


class InfoDialog(QDialog):
    def __init__(self, text, title: bool = False, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        text = QLabel(text)
        text.setMinimumHeight(80)
        ok_btn = Button("OK", self._on_ok_click)

        # Add elements to layout.
        container = QVBoxLayout()
        if title:
            title = QLabel("( ℹ ) Information ")
            title.setObjectName("header")
            container.addWidget(title)
        container.addWidget(text)
        container.addWidget(ok_btn)
        self.setLayout(container)

    def _on_ok_click(self):
        self.accept()


class ConfirmationDialog(QDialog):
    def __init__(self, text = "", title: str = "Are you sure?", parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        title = QLabel(title)
        title.setObjectName("header")
        text = QLabel(text)
        text.setMinimumHeight(80)
        confirm_btn = Button("Yes!", self._on_confirm_click)
        cancel_btn = Button("Cancel", self._on_cancel_click)

        btns = QHBoxLayout()
        btns.addWidget(confirm_btn)
        btns.addWidget(cancel_btn)

        # Add elements to layout.
        container = QVBoxLayout()
        container.addWidget(title)
        container.addWidget(text)
        container.addWidget(btns)
        self.setLayout(container)

    def _on_confirm_click(self):
        self.accept()

    def _on_cancel_click(self):
        self.reject()




