from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.app import SignalBus
from src.models import User
from .scenes import SplashScreen, RegisterScene, LoginScene, DashboardScene, \
    BaseScene
from .scenes.customer_dash import CustomerDashboardScene


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
            # Placeholder widgets
            "driver_dash": QWidget(),
            "admin_dash": QWidget()
        }

        # Add initialized scenes to manager.
        for scene in self.scenes:
            self.addWidget(self.scenes[scene])
        # Listen for signals.
        self._handle_signals()
        # TODO: REMOVE QWIDGET HINT WHEN PLACEHOLDER WIDGETS ARE REMOVED.
        self.current_widget: BaseScene | QWidget = self.currentWidget()

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

        self.signals.request_customer_dash.connect(
            lambda user: self._switch_to('customer_dash', user)
        )

        self.signals.request_driver_dash.connect(
            lambda user: self._switch_to('driver_dash', user)
        )

        self.signals.request_admin_dash.connect(
            lambda user: self._switch_to('admin_dash', user)
        )

        self.signals.trigger_refresh.connect(self.current_widget.refresh_scene)

    def _switch_to(self, scene_name: str, data: User | None = None):
        """Navigate to requested scene."""
        scene = self.scenes[scene_name]
        scene.user = data
        scene.populate_data()
        self.setCurrentWidget(scene)



