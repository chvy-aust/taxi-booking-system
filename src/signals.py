from PyQt6.QtCore import pyqtSignal, QObject

class SignalBus(QObject):
    """A bus of signals shared throughout the system."""
    trigger_refresh = pyqtSignal()
    request_splash = pyqtSignal()
    request_register = pyqtSignal()
    request_login = pyqtSignal()
    request_customer_dash = pyqtSignal(object)
    request_driver_dash = pyqtSignal(object)
    request_admin_dash = pyqtSignal(object)

    def __init__(self):
        super().__init__()
