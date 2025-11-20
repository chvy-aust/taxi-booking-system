from typing import Optional
from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.app.scenes.login import LoginScene
from src.app.scenes.register import RegisterScene
from src.app.scenes.splash import SplashScreen
from src.app.signals import SignalBus
from src.models.user import User

class SceneManager(QStackedWidget):
    """Handles navigation and passing data between scenes."""
    def __init__(self):
        """Initialize project scenes and signals."""
        super().__init__()
        self.signals = SignalBus()
        # Store application scenes.
        self.scenes = {
            "splash" : SplashScreen(self.signals),
            "register" : RegisterScene(self.signals),
            "login" : LoginScene(self.signals)
        }

        # Add initialized scenes to manager.
        for scene in self.scenes:
            self.addWidget(self.scenes[scene])
        # Listen for signals.
        self._handle_signals()
        self.current_widget = self.currentWidget()

    def _handle_signals(self):
        """
        Respond to signals emitted from scenes.
        """
        self.signals.request_splash.connect(
            lambda: self._switch_to('splash')
        )
        self.signals.request_register.connect(
            lambda: self._switch_to('register')
        )
        self.signals.request_login.connect(
            lambda: self._switch_to('login')
        )

    def _switch_to(self, scene: str, data: Optional[User] = None):
        """Navigate to requested scene."""
        self.setCurrentWidget(self.scenes[scene])



