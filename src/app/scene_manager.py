from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.app import SignalBus
from src.models import User
from .scenes import SplashScreen, RegisterScene, LoginScene, CustomerDashboardScene, \
    BaseScene


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
            "login" : LoginScene(self.signals),
            "customer_dash": CustomerDashboardScene(self.signals),
        }

        # Add initialized scenes to manager.
        for scene in self.scenes:
            self.addWidget(self.scenes[scene])
        # Listen for signals.
        self._handle_signals()

    def _handle_signals(self):
        """
        Respond to signals emitted from scenes.

        Handles:
            - Switching between different scenes. (ie, login -> customer dash)
            - Refreshing scenes
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

        self.signals.request_customer_dash.connect(
            lambda user: self._switch_to('customer_dash', user)
        )

        self.signals.request_driver_dash.connect(
            lambda: print("This screen has not been added yet!")
        )

        self.signals.request_admin_dash.connect(
            lambda: print("This screen has not been added yet!")
        )

        self.signals.trigger_refresh.connect(self.refresh)

    def _switch_to(self, scene_name: str, data: User | None = None):
        """Navigate to requested scene and populates data, if provided."""
        scene = self.scenes[scene_name]
        scene.user = data
        scene.populate_data()
        self.setCurrentWidget(scene)

    def refresh(self):
        """Reloads the current scene."""
        current_widget: BaseScene | None = self.currentWidget()
        if current_widget is not None:
            current_widget.refresh_scene()
        else:
            print("( WARNING ⚠ ) Could not reload application.")



