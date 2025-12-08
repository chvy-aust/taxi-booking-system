import datetime

from PyQt6.QtCore import Qt, QDate, QAbstractListModel, pyqtSignal
from PyQt6.QtWidgets import QPushButton, QDateEdit, QLineEdit, QHBoxLayout, \
    QTimeEdit, QLabel, QVBoxLayout, QWidget, QDialog, QSizePolicy

"""
Provides custom project widgets.
Includes:
    - Buttons,
    - Input Fields: InputEdit, DateEdit
    - List Model for Bookings
    - Dialogs: Information, Confirm
"""

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
    def __init__(self, text="", title: str = "Are you sure?", parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup")

        # Create dialog elements.
        title = QLabel(title)
        title.setObjectName("conf-popup-header")
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
