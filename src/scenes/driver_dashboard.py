from src.scenes import BaseScene
from src.signals import signals
from src.ui import UiDriverDashboard
from src.ui import UiCustomerDashboard


class DriverDashboardScene(BaseScene, UiDriverDashboard):
    """
    View controller for the Driver Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("driver-dashboard")
        self.setupUi(self)

        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.driver_home_bn.clicked.connect(lambda: self.switch_to(self.driver_home_page))
        self.driver_logout_btn.clicked.connect(self._log_out)

        # VIEW ASSIGNED RIDES PAGE -----
        # --- button events (switch to panel)
        self.assigned_trips_btn.clicked.connect(lambda: self.switch_to(self.view_trip_page))
        self.back_to_home_btn_3.clicked.connect(lambda: self.switch_to(self.driver_home_page))

    def switch_to(self, page):
        self.refresh_scene()
        self.driver_stackedWidget.setCurrentWidget(page)

    def refresh_scene(self):
        self.depopulate_data()
        self.populate_data()

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def depopulate_data(self):
        pass

    def populate_data(self):
        if self.user is None:
            self.info_popup(
                "Could not access your account. Please Try Again or contact Support.")
            signals.request_login.emit()