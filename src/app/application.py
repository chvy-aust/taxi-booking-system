import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from database import db
from src.app.main_window import MainWindow


DB_FILE = Path(__file__).parent.parent.parent / 'taxibooking.db'

class TaxiBookingSystem(QApplication):
    """
    Application class for the taxi booking system.

    Provides:
        - Application event loop
        - Window centering
        - Database initialization
    """

    def __init__(self):
        """Initialize the application and main window."""
        super().__init__(sys.argv)
        self.window = MainWindow()

    def run(self):
        """Prepare application and start the event loop."""
        self._check_for_database()
        self.window.show()
        self._center_window()
        self.exec()

    def _check_for_database(self):
        """Initialize database if missing."""
        if not DB_FILE.exists():
            print("Initializing database..")
            db.init_db()

    def _center_window(self):
        """Center main window on screen."""
        # Get primary screen's center (x, y) from application.
        center = self.primaryScreen().availableGeometry().center()
        window = self.window.frameGeometry()
        # Set window's center to screen's center
        window.moveCenter(center)
        # Move window to center.
        self.window.move(window.topLeft())