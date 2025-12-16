import logging
from enum import Enum

from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget

from src.core.models import User
from src.scenes import (
    RegisterScene,
    LoginScene,
    CustomerDashboardScene,
    AdminDashboardScene,
    DriverDashboardScene, BaseScene)
from src.signals import signals
from src.utils.constants import STYLE_FILE

logger = logging.getLogger(__name__)

class Scene(Enum):
    Login = "login",
    Register = "register"
    CustomerDash = "customer_dashboard"
    DriverDash = "driver_dashboard"
    AdminDash = "admin_dashboard"

class MainWindow(QMainWindow):
    """
    Main window class for the taxi booking class.
    Handles window styling, configuration and scene management.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A&C Taxi Services")
        self.setFixedSize(770, 600)
        self.scene_manager = QStackedWidget()

        # Store application scenes.
        self.current_scene = None
        self.scenes: dict[Scene, BaseScene | None] = {
            Scene.Login: None,
            Scene.Register: None,
            Scene.CustomerDash: None,
            Scene.DriverDash: None,
            Scene.AdminDash: None
        }

        self._set_style()
        self._center_window()
        self._switch_to_login()
        self.setCentralWidget(self.scene_manager)

        # Listen for signals.
        self._handle_signals()

    def _handle_signals(self):
        """Respond to signals emitted from scenes."""
        signals.request_register.connect(self._switch_to_register)
        signals.request_login.connect(self._switch_to_login)
        signals.request_customer_dash.connect(self._switch_to_customer_dash)
        signals.request_driver_dash.connect(self._switch_to_driver_dash)
        signals.request_admin_dash.connect(self._switch_to_admin_dash)

    def _switch_to_login(self):
        login = self.scenes[Scene.Login]
        if login is None:
            self.scenes[Scene.Login] = LoginScene()
            self.scene_manager.addWidget(self.scenes[Scene.Login])
        self._switch_to(Scene.Login)

    def _switch_to_register(self):
        register = self.scenes[Scene.Register]
        if register is None:
            self.scenes[Scene.Register] = RegisterScene()
            self.scene_manager.addWidget(self.scenes[Scene.Register])
        self._switch_to(Scene.Register)

    def _switch_to_customer_dash(self, data):
        customer_dash = self.scenes[Scene.CustomerDash]
        if customer_dash is None:
            self.scenes[Scene.CustomerDash] = CustomerDashboardScene()
            self.scene_manager.addWidget(self.scenes[Scene.CustomerDash])
        self._switch_to(Scene.CustomerDash, data)

    def _switch_to_driver_dash(self, data):
        driver_dash = self.scenes[Scene.DriverDash]
        if driver_dash is None:
            self.scenes[Scene.DriverDash] = DriverDashboardScene()
            self.scene_manager.addWidget(self.scenes[Scene.DriverDash])
        self._switch_to(Scene.DriverDash, data)

    def _switch_to_admin_dash(self, data):
        admin_dash = self.scenes[Scene.AdminDash]
        if admin_dash is None:
            self.scenes[Scene.AdminDash] = AdminDashboardScene()
            self.scene_manager.addWidget(self.scenes[Scene.AdminDash])
        self._switch_to(Scene.AdminDash, data)

    def _switch_to(self, scene: Scene, data: User | None = None):
        """Navigate to requested scene and populate data if provided."""
        # Clean up current scene.
        self.current_scene = self.scene_manager.currentWidget()
        if self.current_scene:
            self.current_scene.depopulate_data()

        # Switch scene.
        scene = self.scenes[scene]
        if data:
            scene.user = data
        self.scene_manager.setCurrentWidget(scene)
        scene.refresh_scene()

    def _center_window(self):
            """Center main window on screen."""
            # Get primary screen's center (x, y) from application.
            center = QApplication.primaryScreen().availableGeometry().center()
            window = self.frameGeometry()
            # Set window's center to screen's center
            window.moveCenter(center)
            # Move window to center.
            self.move(window.topLeft())

    def _set_style(self):
        """Read style sheet and apply to application."""
        try:
            with open(STYLE_FILE, 'r') as file:
                style_sheet = file.read()
            self.setStyleSheet(style_sheet)
        except OSError as e:
            logger.error(
                msg="Failed to apply style sheet to application.",
                exc_info=e
            )