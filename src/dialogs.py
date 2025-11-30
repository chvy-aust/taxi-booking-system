from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QDialog

from src.widgets import Button

class SystemFeedback:
    DATABASE_ERROR = (
        "A database exception occurred during this transaction. "
        "Data was not stored and/or updated."
    )
    UNEXPECTED_ERROR = "An unknown exception was caught. Please Try Again or contact Support."

class InfoDialog(QDialog):
    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        text = QLabel(info)
        text.setMinimumHeight(80)
        ok_btn = Button("OK", self._on_ok_click)

        # Add elements to layout.
        container = QVBoxLayout()
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
        title.setObjectName("conf-popup-header")
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




