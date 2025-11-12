from typing import Union

from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QWidget, QDateEdit


class InputEdit(QWidget):
    """Custom QLineEdit class."""
    def __init__(self,
                 label: str,
                 input_field: Union[QLineEdit, QDateEdit] = QLineEdit,
                 object_name: str = None):
        """
        Initialize the input edit.

        Args:
            label: Field prompt
            input_field: QLineEdit or QDateEdit instance (defaults to QLineEdit)
            object_name: Optional object name for styling.
        """
        super().__init__()
        # Set field label.
        self.label = QLabel(label)
        # Set object name, if provided.
        self.setObjectName(object_name)

        # Define input field.
        if isinstance(input_field, QDateEdit):
            self.input_field = QDateEdit()
            self.input_field.setDisplayFormat("yyyy-MM-dd")
        else:
            self.input_field = QLineEdit()

        # Add elements to layout.
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        # Set layout to widget.
        self.setLayout(layout)

    def value(self):
        """Return str text from field."""
        return self.input_field.text().strip()

    def show_error(self):
        """Hint at errors with red highlighting."""
        self.label.setStyleSheet("color: #521A1A;")
        self.input_field.setStyleSheet("color: #521A1A; border: 3px solid #521A1A")

    def clear_error(self):
        """Remove error hint."""
        self.label.setStyleSheet(None)
        self.input_field.setStyleSheet(None)


