from PyQt6.QtWidgets import QWidget, QMessageBox

from src.app.signals import SignalBus
from src.models.user import User

class BaseScene(QWidget):
    """Base scene class for project scenes."""
    def __init__(self, scene_name: str, signals: SignalBus, user: User | None = None):
        """Initialize default scene behaviors."""
        super().__init__()
        self.setObjectName(scene_name)
        self.signals = signals
        self.user = user

    def _load_ui(self):
        """
        Return layout for scene.
        To be overridden by subclassed scenes.
        """
        pass

    def populate_data(self):
        """
        Initialize available data fields if user is logged in.
        To be overridden by subclassed scenes.
        """
        pass

    def refresh_scene(self):
        """
        Refresh available data fields within scene.
        To be overridden by subclassed scenes.
        """

    def info_popup(self,
                   info: str,
                   title: str = "Information"
                   ):
        """Display an informative message to the user."""
        QMessageBox.information(self, title, info)

    def confirmation_popup(self,
                           question: str = "",
                           title: str = "Are you sure?") -> bool:
        """
        Display a confirmation question to user.
        Returns boolean confirmation indicator (ie, True if 'Yes' clicked.)
        """
        button = QMessageBox.question(self, title, question)
        return button == QMessageBox.StandardButton.Yes

    def critical_popup(self,
                       text: str = "An unknown exception was caught. Please "
                                   "Try Again or contact Support.",
                       title: str = "Error!"):
        """Display a critical error message to the user."""
        QMessageBox.critical(self, title, text)

