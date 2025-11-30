from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QApplication

from .scene_manager import SceneManager

STYLE_FILE = Path(__file__).parent / 'styles.qss'

class MainWindow(QMainWindow):
    """
    Main window class for the taxi booking class.

    Provides:
        - Scene manager
        - Window configuration (size, title, centering)
        - Style sheet application
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taxi Booking System")
        self.scene_manager = SceneManager()
        self.setCentralWidget(self.scene_manager)
        self.setMinimumSize(800, 600)
        self._center_window()

        # Read style sheet and apply to application.
        with open(STYLE_FILE, 'r') as file:
            style_sheet = file.read()
        self.setStyleSheet(style_sheet)

    def _center_window(self):
        """Center main window on screen."""
        # Get primary screen's center (x, y) from application.
        center = QApplication.primaryScreen().availableGeometry().center()
        window = self.frameGeometry()
        # Set window's center to screen's center
        window.moveCenter(center)
        # Move window to center.
        self.move(window.topLeft())