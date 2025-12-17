from PyQt6.QtCore import pyqtSignal, QObject

from .core.models import User

class SignalBus(QObject):
    """A bus of signals shared throughout the system."""
    request_register = pyqtSignal()
    request_login = pyqtSignal()
    request_customer_dash = pyqtSignal(User)
    request_driver_dash = pyqtSignal(User)
    request_admin_dash = pyqtSignal(User)

    def __init__(self):
        super().__init__()


signals = SignalBus() # <- global instance