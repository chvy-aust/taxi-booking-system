import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QDialog, QWidget, \
    QComboBox, QTimeEdit

from src.app.widgets import InputEdit, Button, DateEdit


class InfoDialog(QDialog):
    def __init__(self, text, title: bool = False, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        text = QLabel(text)
        text.setMinimumHeight(80)
        ok_btn = Button("OK", self._on_ok_click)

        # Add elements to layout.
        container = QVBoxLayout()
        if title:
            title = QLabel("( ℹ ) Information ")
            title.setObjectName("header")
            container.addWidget(title)
        container.addWidget(text)
        container.addWidget(ok_btn)
        self.setLayout(container)

    def _on_ok_click(self):
        self.accept()


class ConfirmationDialog(QDialog):
    def __init__(self, text = "", title: str = "Are you sure?", parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        title = QLabel(title)
        title.setObjectName("header")
        text = QLabel(text)
        text.setMinimumHeight(80)
        confirm_btn = Button("Yes!", self._on_confirm_click)
        cancel_btn = Button("Cancel", self._on_cancel_click)

        btns = QHBoxLayout()
        btns.addWidget(confirm_btn)
        btns.addWidget(cancel_btn)

        # Add elements to layout.
        container = QVBoxLayout()
        container.addWidget(title)
        container.addWidget(text)
        container.addWidget(btns)
        self.setLayout(container)

    def _on_confirm_click(self):
        self.accept()

    def _on_cancel_click(self):
        self.reject()


class BookingForm(QWidget):
    start_booking = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("booking-form")
        self.today = datetime.datetime.today()

        booking_header = QLabel("Make a Booking")
        booking_header.setFixedHeight(80)
        booking_header.setObjectName("header")


        self.dropoff = InputEdit("Enter drop off location:")
        self.pickup = InputEdit("Enter pickup location:")

        self.datetime_option = QComboBox()
        self.datetime_option.addItems(("Book now ⓘ", "Book in advance ⓘ"))
        self.datetime_option.currentIndexChanged.connect(self._index_changed)
        self.booking_now = True

        minimum_date = self.today + datetime.timedelta(days=1)
        self.date = DateEdit("Enter date for pickup:")
        self.date.minimum_date(minimum_date)
        self.date.set_text(minimum_date)
        self.date.hide()

        self.time = InputEdit("Enter time for pickup:", QTimeEdit)
        self.time.hide()



        self.fields = [
            self.dropoff,
            self.pickup,
            self.date,
            self.time
        ]

        self.book_btn = Button("Confirm", self._on_button_click)

        container = QVBoxLayout()
        container.addWidget(booking_header)
        container.addWidget(self.pickup)
        container.addWidget(self.dropoff)
        container.addWidget(self.datetime_option)
        container.addWidget(self.date)
        container.addWidget(self.time)
        container.addWidget(self.book_btn)

        self.setLayout(container)

    def _index_changed(self, index):
        BOOK_NOW = 0
        ADVANCE_BOOKING = 1
        if index == BOOK_NOW:
            self.date.hide()
            self.time.hide()
            self.booking_now = True

        if index == ADVANCE_BOOKING:
            self.date.show()
            self.time.show()
            self.booking_now = False
        self.update()

    def _on_button_click(self):
        self._clear_errors()
        info = {
            "driver_id": None,
            "dropoff": self.dropoff.text().title(),
            "pickup": self.pickup.text().title(),
            "status": "waiting"
        }

        if not self.booking_now:
            info["date"] = self.date.date().toString("yyyy-MM-dd")
            info["time"] = self.time.text()
        else:
            info["date"] = self.today.strftime("%Y-%m-%d")
            info["time"] = self.today.strftime("%I:%M %p")

        if not self._validate_fields(info):
            return

        self.start_booking.emit(info)
        self._reset_fields()


    def _validate_fields(self, info):
        validation_checks = [
            info["dropoff"] != "",
            info ["pickup"] != ""
        ]

        flag = True

        for field, is_valid in zip(self.fields, validation_checks):
            if not is_valid:
                field.show_error()
                flag = False

        return flag

    def _reset_fields(self):
        for field in self.fields:
            field.reset()

    def _clear_errors(self):
        for field in self.fields:
            field.clear_error()


