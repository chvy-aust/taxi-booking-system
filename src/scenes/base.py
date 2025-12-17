from PyQt6.QtWidgets import QWidget, QDialog

from ..core.models import User
from ..widgets import InfoDialog, ConfirmationDialog


class BaseScene(QWidget):
    """Base scene class for project scenes."""
    def __init__(self, scene_name: str, user: User | None = None):
        """Initialize default scene behaviors."""
        super().__init__()
        self.setObjectName(scene_name)
        self.user = user

    def _load_ui(self):
        """
        Return layout for scene.
        To be overridden by subclassed scenes.
        """
        pass

    def depopulate_data(self):
        """
        Clear all data fields.
        To be overridden by subclassed scenes.
        """
        pass

    def populate_data(self):
        """
        Initialize available data fields if user is logged in.
        To be overridden by subclassed scenes.
        """
        pass

    def switch_to_home(self):
        """
        Switch back to home page on scene switch.
        Intended for scenes with nested layouts.
        """

    def refresh_scene(self):
        """Refresh available data fields within scene."""
        self.depopulate_data()
        self.populate_data()

    def info_popup(self, info):
        """Display an informative message to the user."""
        popup = InfoDialog(info, self)
        popup.exec()




