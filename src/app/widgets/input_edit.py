from enum import Enum

from PyQt6.QtCore import QDate, QCalendar
from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QWidget, QDateEdit, QHBoxLayout


class ToolTip(Enum):
    AGE_REQUIREMENT = "You must be 18+ to use this service."
    PHONENUM_FORMAT = (
        "May contain optional country code. Must have area and local code.\n"
        "Examples of valid formats:\n"
        "+1 (123) 456 7890 | (123) 456 7890\n"
        "1 123 456 7890 | 1-123-456-7890\n"
        "123 456 7890 | 123-456-7890")
    EMAIL_FORMAT = "Must contain '@' and '.'"
    PASSWORD_FORMAT = "Password must contain 1 uppercase letter, 1 lowercase letter and 1 number."
    MATCHING_PASSWORD = "These passwords must match."

class InputEdit(QWidget):
    def __init__(self,
                 label: str,
                 input_type: type[QDateEdit | QLineEdit] = QLineEdit,
                 object_name: str = None):
        super().__init__()
        self.label = QLabel(label)
        self.setObjectName(object_name)
        self.input_field = input_type()
        self.tooltip = QLabel("( i )")
        self.tooltip.setHidden(True)
        if isinstance(self.input_field, QDateEdit):
            self._format_date_input()
        self._load_layout()


    def _load_layout(self):
        """Set layout for input edit."""
        layout = QVBoxLayout()
        # Make container for prompt label + tooltip.
        lbl_tltp = QHBoxLayout()
        lbl_tltp.addWidget(self.label)
        lbl_tltp.addStretch()
        lbl_tltp.addWidget(self.tooltip)
        # Add elements to layout
        layout.addLayout(lbl_tltp)
        layout.addWidget(self.input_field)
        self.setLayout(layout)

    def _format_date_input(self):
        self.input_field.setDisplayFormat("yyyy-MM-dd")
        self.input_field.setCalendarPopup(True)
        self.input_field.setCalendar(QCalendar())
        self.input_field.setDate(QDate.currentDate())

    def setToolTip(self, info: ToolTip):
        """Enable tooltip and set information."""
        self.tooltip.setToolTip(info.value)
        self.tooltip.setHidden(False)

    def value(self):
        """Return value from field."""
        if isinstance(self.input_field, QDateEdit):
            return self.input_field.date()
        else:
            return self.input_field.text().strip()

    def clear_value(self):
        if isinstance(self.input_field, QDateEdit):
            self.input_field.setDate(QDate.currentDate())
        else:
            self.input_field.clear()

    def show_error(self):
        """Hint at errors with red highlighting."""
        self.tooltip.setStyleSheet("color: #521A1A;")
        self.label.setStyleSheet("color: #521A1A;")
        self.input_field.setStyleSheet("border: 3px solid #521A1A")

    def clear_error(self):
        """Remove error hint."""
        self.tooltip.setStyleSheet("color: #293737;")
        self.label.setStyleSheet("color: #293737;")
        self.input_field.setStyleSheet("border: 3px solid #293737;")


