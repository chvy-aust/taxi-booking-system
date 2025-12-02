import logging
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget

from src.signals import signals
from src.scenes import (
            RegisterScene, LoginScene,
            CustomerDashboardScene, BaseScene)
from src.core.models import User

STYLE_FILE = Path(__file__).parent / 'styles.qss'
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """
    Main window class for the taxi booking class.
    Handles window styling, configuration and scene management.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taxi Booking System")
        self.setFixedSize(600, 600)
        self.scene_manager = QStackedWidget()

        # Store application scenes.
        self.scenes = {
            "login": LoginScene(),
            "register": RegisterScene(),
            "customer_dash": CustomerDashboardScene(),
        }

        for scene in self.scenes:
            self.scene_manager.addWidget(self.scenes[scene])

        # Listen for signals.
        self._handle_signals()

        # Set scene manager + styling..
        self._center_window()
        self._set_style()
        self.setCentralWidget(self.scene_manager)

    def _handle_signals(self):
        """Respond to signals emitted from scenes."""
        signals.request_register.connect(lambda: self._switch_to('register'))
        signals.request_login.connect(lambda: self._switch_to('login'))

        signals.request_customer_dash.connect(
            lambda user: self._switch_to('customer_dash', user)
        )
        signals.request_driver_dash.connect(
            lambda: logger.info("This screen has not been added yet!")
        )
        signals.request_admin_dash.connect(
            lambda: logger.info("This screen has not been added yet!")
        )

        signals.trigger_refresh.connect(self.refresh)

    def _switch_to(self, scene_name: str, data: User | None = None):
        """Navigate to requested scene and populates data, if provided."""
        scene = self.scenes[scene_name]
        scene.user = data
        scene.populate_data()
        self.scene_manager.setCurrentWidget(scene)

    def refresh(self):
        """Reloads the current scene."""
        current_widget: BaseScene | None = self.scene_manager.currentWidget()
        if current_widget is not None:
            current_widget.refresh_scene()
        else:
            logger.warning("Could not reload application.")


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
        with open(STYLE_FILE, 'r') as file:
            style_sheet = file.read()
        self.setStyleSheet(style_sheet)