from pathlib import Path
from PyQt6.QtWidgets import QMainWindow

from src.app.scene_manager import SceneManager

STYLE_FILE = Path(__file__).parent / 'styles.qss'

class MainWindow(QMainWindow):
    """
    Main window class for the taxi booking class.

    Provides:
        - Scene manager
        - Window configuration (size, title)
        - Style sheet application
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taxi Booking System")
        self.scene_manager = SceneManager()
        self.setCentralWidget(self.scene_manager)
        self.setMaximumSize(800, 600)

        # Read style sheet and apply to application.
        with open(STYLE_FILE, 'r') as file:
            style_sheet = file.read()
        self.setStyleSheet(style_sheet)