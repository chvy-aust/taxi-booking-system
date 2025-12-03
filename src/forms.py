import datetime

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, \
    QComboBox, QTimeEdit, QFrame

from src.widgets import Button, InputEdit, DateEdit


class BookingForm(QFrame):
    make_booking = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("booking-form")
        self.today = datetime.datetime.today()
        self._setup_ui()
        self.fields = [
            self.dropoff,
            self.pickup,
            self.date,
            self.time
        ]

    def _setup_ui(self):
        booking_header = QLabel("Make a Booking")
        booking_header.setFixedHeight(80)
        booking_header.setObjectName("header")

        dropoff_ctn = QVBoxLayout()
        dropoff_lbl = QLabel("Enter drop off location:")
        self.dropoff = InputEdit()
        dropoff_ctn.addWidget(dropoff_lbl)
        dropoff_ctn.addWidget(self.dropoff)

        pickup_ctn = QVBoxLayout()
        pickup_lbl = QLabel("Enter pickup location:")
        self.pickup = InputEdit()
        pickup_ctn.addWidget(pickup_lbl)
        pickup_ctn.addWidget(self.pickup)

        self.datetime_option = QComboBox()
        self.datetime_option.addItems(("Book now ⓘ", "Book in advance ⓘ"))
        self.datetime_option.currentIndexChanged.connect(self._index_changed)
        self.pickup_now = True

        minimum_date = self.today + datetime.timedelta(days=1)
        date_ctn = QVBoxLayout()
        self.date_lbl = QLabel("Enter date for pickup:")
        self.date = DateEdit()
        self.date.minimum_date(minimum_date)
        self.date.set_text(minimum_date)
        date_ctn.addWidget(self.date_lbl)
        date_ctn.addWidget(self.date)

        time_ctn = QVBoxLayout()
        self.time_lbl = QLabel("Enter time for pickup:")
        self.time = InputEdit(input_type=QTimeEdit)
        time_ctn.addWidget(self.time_lbl)
        time_ctn.addWidget(self.time)

        # Hide date_time options on default.
        self.time.hide()
        self.time_lbl.hide()
        self.date.hide()
        self.date_lbl.hide()

        self.book_btn = Button("Confirm", self._on_confirm_click)

        container = QVBoxLayout()
        container.addWidget(booking_header)
        container.addLayout(pickup_ctn)
        container.addLayout(dropoff_ctn)
        container.addWidget(self.datetime_option)
        container.addLayout(date_ctn)
        container.addLayout(time_ctn)
        container.addWidget(self.book_btn)

        self.setLayout(container)

    def _index_changed(self, index):
        """Toggle the visibility of date_time fields."""
        PICKUP_NOW = 0
        ADVANCE_BOOKING = 1

        if index == PICKUP_NOW:
            self.date_lbl.hide()
            self.date.hide()
            self.time_lbl.hide()
            self.time.hide()
            self.pickup_now = True

        if index == ADVANCE_BOOKING:
            self.date_lbl.show()
            self.date.show()
            self.time_lbl.show()
            self.time.show()
            self.pickup_now = False
        self.update()

    def _get_info(self):
        info = {
            "driver_id": None,
            "dropoff": self.dropoff.text().title(),
            "pickup": self.pickup.text().title(),
            "status": "waiting_for_assignment"
        }

        if not self.pickup_now:
            # Collect dates for a future datetime.
            info["date"] = self.date.date().toString("yyyy-MM-dd")
            info["time"] = self.time.text()
        else:
            # Collect dates for the current datetime.
            info["date"] = self.today.strftime("%Y-%m-%d")
            info["time"] = self.today.strftime("%I:%M %p")

        return info

    def _on_confirm_click(self):
        """Collect information from fields and ensure validity."""
        self._clear_errors()

        info = self._get_info()
        if not self._validate_fields(info):
            return

        self.make_booking.emit(info)
        self._reset_fields()

    def _validate_fields(self, info):
        validation_checks: list[bool] = [
            info["dropoff"] != "",
            info["pickup"] != ""
        ]

        flag = True

        for field, is_valid in zip(self.fields, validation_checks):
            if not is_valid:
                field.show_error()
                flag = False

        return flag

    def _reset_fields(self):
        """Clear text + error hinting from fields."""
        for field in self.fields:
            field.reset()

    def _clear_errors(self):
        """Clear error hinting from fields."""
        for field in self.fields:
            field.clear_error()
