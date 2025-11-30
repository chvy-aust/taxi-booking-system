import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QWidget, QDateEdit, \
    QHBoxLayout, QSizePolicy, QTimeEdit

MIN_WIDTH = QSizePolicy.Policy.Minimum
MIN_HEIGHT = QSizePolicy.Policy.Minimum
class InputEdit(QWidget):
    def __init__(self,
                 prompt: str,
                 input_type: type[QLineEdit | QDateEdit | QTimeEdit] = QLineEdit,
                 object_name: str = None):
        super().__init__()
        self.setObjectName(object_name)
        self.setSizePolicy(MIN_WIDTH, MIN_HEIGHT)
        self.prompt = QLabel(prompt)
        self.prompt.setFixedHeight(25)
        self.input_field = input_type()
        self.input_field.setFixedHeight(40)
        self.tooltip = QLabel("( i )")
        self.setLayout(self._load_layout())

    def _load_layout(self) -> QVBoxLayout:
        container = QVBoxLayout()
        # Add container containing prompt + potential tooltip.
        self.lbl_tltp = QHBoxLayout()
        self.lbl_tltp.addWidget(self.prompt)
        container.addLayout(self.lbl_tltp)
        # Add input field to container.
        container.addWidget(self.input_field)
        return container

    def set_tooltip(self, hint: str):
        # Set text for tooltip.
        self.tooltip.setToolTip(hint)
        # Add tooltip to container next to prompt.
        self.lbl_tltp.addStretch()
        self.lbl_tltp.addWidget(self.tooltip)

    def set_prompt(self, text):
        self.prompt.setText(text)

    def set_echo_mode(self, mode: QLineEdit.EchoMode):
        self.input_field.setEchoMode(mode)

    def text(self):
        """Return value from field."""
        return self.input_field.text().strip()

    def set_text(self, text):
        self.input_field.setText(text)

    def reset(self):
        self.clear_error()
        self.input_field.clear()

    def show_error(self):
        """Hint at errors with red highlighting."""
        self.prompt.setStyleSheet("color: #5B0D0D")
        self.tooltip.setStyleSheet("color: #5B0D0D")
        self.input_field.setStyleSheet("border: 3px solid #5B0D0D;")

    def clear_error(self):
        """Remove error hint."""
        self.prompt.setStyleSheet("color: #293737;")
        self.tooltip.setStyleSheet("color: #293737;")
        self.input_field.setStyleSheet("border: 3px solid #293737;")

    @property
    def text_changed(self):
        return self.input_field.textChanged


class DateEdit(InputEdit):
    def __init__(self, prompt: str, object_name: str = None):
        super().__init__(prompt,
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
        self.input_field.setDate(date)

    def reset(self):
        self.clear_error()
        self.input_field.setDate(QDate.currentDate())

    @property
    def text_changed(self):
        return self.input_field.dateChanged


