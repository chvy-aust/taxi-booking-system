from typing import Optional
from PyQt6.QtWidgets import QWidget

from src.app.signals import SignalController
from src.models.user import User

class BaseScene(QWidget):
    """Base scene class for project scenes."""
    def __init__(self, scene_name: str, signals: SignalController, user: Optional[User] = None):
        """Initialize default scene behaviors."""
        super().__init__()
        self.setObjectName(scene_name)
        self.signals = signals
        self.user = user

    def _load_ui(self):
        """
        Return layout for scene.
        To be override by subclassed scenes.
        """
        pass


