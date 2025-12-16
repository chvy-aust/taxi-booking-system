import datetime
import sqlite3
from typing import Literal

from PyQt6.QtCore import Qt, QDate, QAbstractListModel, pyqtSignal
from PyQt6.QtWidgets import QPushButton, QDateEdit, QLineEdit, QTimeEdit, \
    QLabel, QVBoxLayout, QWidget, QDialog, QSizePolicy, \
    QTableWidgetItem, QListWidget, QListWidgetItem, QComboBox

from src.core.database import DatabaseConnection


"""
Provides custom project widgets.
Includes:
    - Buttons,
    - Input Fields: InputEdit, DateEdit
    - Dialogs: Information, Confirm
"""


# Helper function to populate tables
def populate_table(table, items):
    table.setRowCount(len(items))
    for row, item in enumerate(items):
        for column_index, value in enumerate(item):
            table.setItem(row, column_index, QTableWidgetItem(str(value)))

class Button(QPushButton):
    """Custom QPushButton class."""

    def __init__(self, label, signal, object_name=None, ):
        """Initialize and set default configurations."""
        super().__init__()
        self.setObjectName(object_name)
        self.setText(label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.signal = signal
        self.clicked.connect(self.signal)

class Link(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent):
        super().__init__(parent)

    def mouseReleaseEvent(self, ev):
        """Emit signal when left-clicked."""
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class InputEdit(QWidget):
    def __init__(self,
                 parent=None,
                 input_type: type[QLineEdit | QDateEdit | QTimeEdit] = QLineEdit,
                 object_name: str = None):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.input_field = input_type()
        self.input_field.setFixedHeight(40)
        self.input_field.setSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Preferred)

        self.error_field = QLabel("")
        self.error_field.setStyleSheet("color: #5B0D0D;")
        self.error_field.setFixedHeight(20)
        self.error_field.setWordWrap(True)
        self.error_prompt = None

        self.container = QVBoxLayout()
        self.container.setContentsMargins(0,0,0,0)
        self.container.setSpacing(0)
        self.container.addWidget(self.input_field)
        self.container.addWidget(self.error_field)


        self.setLayout(self.container)

    def set_focus(self):
        self.input_field.setFocus()

    def set_echo_mode(self, mode: QLineEdit.EchoMode):
        self.input_field.setEchoMode(mode)

    def set_text(self, text):
        self.input_field.setText(text)


    def text(self):
        """Return value from field."""
        return self.input_field.text().strip()

    def reset(self):
        self.clear_error()
        self.input_field.clear()

    def set_error(self, text):
        self.error_prompt = text

    def show_error(self):
        """Hint at errors with red highlighting."""
        self.setProperty("invalid", True)
        self.error_field.setText(self.error_prompt)
        self._repolish()

    def clear_error(self):
        """Remove error hint."""
        self.setProperty("invalid", False)
        self.error_field.setText("")
        self._repolish()

    def _repolish(self):
        self.style().unpolish(self.input_field)
        self.style().unpolish(self.error_field)
        self.style().polish(self.input_field)
        self.style().polish(self.error_field)

    @property
    def text_changed(self):
        return self.input_field.textChanged


class DateEdit(InputEdit):
    def __init__(self, object_name: str = None, parent=None):
        super().__init__(parent,
                         input_type=QDateEdit,
                         object_name=object_name)
        self.input_field.setDisplayFormat("yyyy-MM-dd")
        self.input_field.setCalendarPopup(True)
        self.input_field.setDate(QDate.currentDate())

    def date(self) -> QDate:
        return self.input_field.date()

    def maximum_date(self, date: QDate | datetime.date):
        self.input_field.setMaximumDate(date)

    def minimum_date(self, date: QDate | datetime.date):
        self.input_field.setMinimumDate(date)

    def set_text(self, date):
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.input_field.setDate(date)

    def reset(self):
        self.clear_error()
        self.input_field.setDate(QDate.currentDate())

    @property
    def text_changed(self):
        return self.input_field.dateChanged

class BookingListModel(QAbstractListModel):
    def __init__(self, bookings=None):
        super().__init__()
        self.bookings = bookings or []
    def data(self, index, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.bookings[index.row()])

    def rowCount(self, parent=...):
        return len(self.bookings)

class SystemFeedback:
    DATABASE_ERROR = (
        "A database exception occurred during this transaction. "
        "Data was not stored and/or updated."
    )
    UNEXPECTED_ERROR = "An unknown exception was caught. Please Try Again or contact Support."

class InfoDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        text = QLabel(text)
        text.setMinimumHeight(80)
        ok_btn = Button("OK", self._on_ok_click)

        # Add elements to layout.
        container = QVBoxLayout()
        container.addWidget(text)
        container.addWidget(ok_btn)
        self.setLayout(container)

    def _on_ok_click(self):
        self.accept()


class ConfirmationDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        text = QLabel(text)
        text.setFixedWidth(200)
        text.setWordWrap(True)
        confirm_btn = Button("Yes!", self._on_confirm_click)
        cancel_btn = Button("Cancel", self._on_cancel_click)

        btns = QVBoxLayout()
        btns.addWidget(confirm_btn)
        btns.addWidget(cancel_btn)

        # Add elements to layout.
        container = QVBoxLayout()
        container.addWidget(text)
        container.addLayout(btns)
        self.setLayout(container)

    def _on_confirm_click(self):
        self.accept()

    def _on_cancel_click(self):
        self.reject()

class BookingItem(QDialog):
    def __init__(self, booking,
                 viewer: Literal["customer","driver","admin"] = "customer",parent=None):
        super().__init__(parent)
        self.booking = booking
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("booking-item-dialog")
        self.viewer = viewer

        title = f"""
        <b>Currently Viewing Booking (ID: {self.booking.id})<br>
        Booking Made: {self.booking.date} {self.booking.time}</b> 
        """

        self.additional_info = QLabel()
        self.status = QLabel()
        self.action_btn = QPushButton()
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.set_viewer_based_info()
        self.update_item_status()
        self.set_viewer_based_action()

        location = f"""
        <b>Pickup</b>:<br>\n{self.booking.pickup}<br>
        <b>Destination</b>:<br>\n{self.booking.dropoff}
        """

        # add elements to layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        layout.addWidget(self.additional_info)
        layout.addWidget(QLabel(location))
        layout.addWidget(self.status)
        layout.addWidget(self.action_btn)
        layout.addWidget(Button("Exit", self.accept))


        self.setLayout(layout)

    def set_viewer_based_info(self):
        if self.viewer == "customer":
            if self.booking.driver_id:
                info = f"<b>Assigned Driver</b>: {self.booking.driver.fullname}<br>"
                info += f"<b>Phone Number</b>: {self.booking.driver.phonenum}"
            else:
                info = f"<b>Assigned Driver</b>: N/A<br>"
            self.additional_info.setText(info)
        elif self.viewer == "driver":
            info = f"<b>Customer Name</b>: {self.booking.customer.fullname}<br>"
            info += f"<b>Phone Number</b>: {self.booking.customer.phonenum}"
            self.additional_info.setText(info)
        else:
            customer_info = f"""
                            <b>Customer</b>:<br>
                            \t<b>ID</b>: {self.booking.customer.id}<br>
                            \t<b>Name</b>: {self.booking.customer.fullname}<br>
                            \t<b>Phone</b>: {self.booking.customer.phonenum}<br>
                            \t<b>Email</b>: {self.booking.customer.email}"""
            if self.booking.driver_id:
                driver_info = f"""
                            <br><b>Assigned Driver</b>:<br>
                            \t<b>ID</b>: {self.booking.driver.id}<br>
                            \t<b>Name</b>: {self.booking.driver.fullname}<br>
                            \t<b>Phone</b>: {self.booking.driver.phonenum}<br>
                            \t<b>Email</b>: {self.booking.driver.email}"""
            else:
                driver_info = f"""
                            <br><b>Assigned Driver</b>:<br>
                            <b>N/A</b>"""
            self.additional_info.setText(customer_info + driver_info)
        self.update()

    def set_viewer_based_action(self):
        """
        Add a role-based action button to the layout.
        Depends on whether a certain condition is met.
        """
        try:
            # Prevent signal mis-firing.
            self.action_btn.disconnect()
        except TypeError:
            pass

        if self.viewer == "customer":
            # Disable customer cancellation if pending period is passed.
            if self.booking.status != "waiting_for_assignment":
                self.action_btn.hide()
                return
            # Enable cancellation for customers if booking is pending.
            self.action_btn.setText("Cancel Booking")
            self.action_btn.clicked.connect(self._cancel_booking)
            self.update()
        elif self.viewer == "driver":
            # Disable driver status progression if booking is not active.
            if self.booking.status in ("completed", "cancelled"):
                self.action_btn.hide()
                return
            # Enable driver status progression if booking is active.
            self.action_btn.setText("Progress the current status")
            self.action_btn.clicked.connect(self._progress_booking)
            self.update()
        else:
            # Disable driver assignment if driver is already assigned.
            if self.booking.driver_id:
                self.action_btn.hide()
                return
            # Enable driver assignment if booking has no assigned driver.
            self.action_btn.setText("Assign Driver")
            self.action_btn.clicked.connect(self._assign_driver)
            self.update()

    def update_item_status(self):
        self.status.setText(f"<b>Status</b>: {self.booking.formatted_status}")

    def _cancel_booking(self):
        question = f"Are you sure you'd like to cancel this booking? "
        question += f"<b>This cannot be undone.</b>"
        if self._get_confirmation(question):
            # Update db record + booking instance
            self.booking.cancel()
            # Refresh item with new status + hide action
            self.update_item_status()
            self.set_viewer_based_action()

    def _progress_booking(self):
        question = f"Are you sure you'd like to update the status of this "
        question += f"booking? <b>This cannot be undone.</b>"
        if self._get_confirmation(question):
            # Update db record + booking instance
            self.booking.update_status()
            # Refresh item with new status + hide action
            self.update_item_status()
            self.set_viewer_based_action()

    def _assign_driver(self):
        dialog = AssignDriverDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
                # Update db record + booking instance
                self.booking.assign_driver(dialog.selected_driver.id)
                # Refresh item with new status + hide action
                self.booking.update_status()
                self.set_viewer_based_info()
                self.set_viewer_based_action()

    def _get_confirmation(self, question) -> bool:
        dialog = ConfirmationDialog(question, self)
        return dialog.exec() == QDialog.DialogCode.Accepted


class AssignDriverDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")
        self.selected_driver = None

        self.dropdown = QComboBox()
        self.confirm_btn = Button("Confirm", self.select_driver)
        for driver in self._get_available_drivers():
            self.dropdown.addItem(
                f"Name: {driver.fullname} | ID: {driver.id}",
                driver
            )

        if not self.dropdown.count():
            self.confirm_btn.hide()
            self.dropdown.addItem(f"No drivers available.")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Available drivers:"))
        layout.addWidget(self.dropdown)
        layout.addWidget(self.confirm_btn)
        layout.addWidget(Button("Cancel", self.reject))
        self.setLayout(layout)


    def select_driver(self):
        driver = self.dropdown.currentData()
        question = f"Are you sure you'd like to assign this driver (ID: {driver.id}) "
        question += f"to this booking? <b>Driver re-assignment is not possible in the current system.</b>"
        if ConfirmationDialog(question, self).exec() == QDialog.DialogCode.Accepted:
                self.selected_driver = driver
                self.accept()

    @staticmethod
    def _get_available_drivers():
        try:
            with DatabaseConnection() as conn:
                drivers = conn.fetch_users(role="driver")
                available_drivers = []
                for driver in drivers:
                    active_booking = conn.fetch_bookings(
                        driver_id=driver.id,
                        status=("waiting_for_pickup", "in_process")
                    )
                    if not active_booking:
                        available_drivers.append(driver)
                return available_drivers
        except sqlite3.Error:
            raise

