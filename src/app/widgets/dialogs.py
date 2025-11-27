from sys import flags
from time import sleep
from typing import override

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, \
    QWidget


class InfoDialog(QDialog):
    def __init__(self,
                 message: str,
                 exc: Exception = None,
                 parent: QWidget | None = None,
                 w: int = 200,
                 h: int = 100,
                 window_flag: Qt.WindowType = Qt.WindowType.FramelessWindowHint):

        super().__init__(parent)
        self.setWindowFlag(window_flag)
        self.resize(w, h)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btns.accepted.connect(self.accept)

        self.message = QLabel(f"{message}{exc}")
        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(btns)
        self.setLayout(layout)

    @override
    def show(self):
        self.exec()

    def __enter__(self):
        self.show()

