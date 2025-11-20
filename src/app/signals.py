from PyQt6.QtCore import pyqtSignal, QObject

class SignalBus(QObject):
    """A signal controller to manage signals shared throughout system."""
    request_splash = pyqtSignal()
    request_register = pyqtSignal()
    request_login = pyqtSignal()
    refresh_scene = pyqtSignal()

    def __init__(self):
        super().__init__()
