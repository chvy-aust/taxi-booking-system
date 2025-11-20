from sys import flags
from time import sleep
from typing import override

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class InfoDialog(QDialog):
    def __init__(self,
                 text: str,
                 parent=None,
                 w: int = 200,
                 h: int = 100,
                 window_flag: Qt.WindowType = Qt.WindowType.FramelessWindowHint):

        super().__init__(parent)
        self.setWindowFlag(window_flag)
        self.resize(w, h)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btns.accepted.connect(self.accept)
        self.timer = QTimer()
        self.timer.setInterval(1500)

        self.text = QLabel(text)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(btns)
        self.setLayout(layout)

    @override
    def show(self):
        self.exec()