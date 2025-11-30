from PyQt6.QtWidgets import QWidget, QMessageBox, QDialog

from src.dialogs import InfoDialog, ConfirmationDialog, SystemFeedback
from src.signals import SignalBus
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

    def _depopulate_date(self):
        """
        Clear all populated data fields if user has logged out.
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

    def info_popup(self, info):
        """Display an informative message to the user."""
        popup = InfoDialog(info, self)
        popup.exec()

    def confirmation_popup(self, question = "", title: str = "Are you sure?") -> bool:
        """
        Display a confirmation question to user.
        Returns boolean confirmation indicator (ie, True if 'Confirm' clicked.)
        """
        popup = ConfirmationDialog(question, title, self)
        return popup.exec() == QDialog.DialogCode.Accepted

    def critical_popup(self,
                       text: str | SystemFeedback,
                       title: str = "Error!"):
        """Display a critical error message to the user."""
        QMessageBox.critical(self, title, text)

