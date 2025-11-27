from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout


class FormLayout(QVBoxLayout):
    """Custom form layout class."""
    def __init__(self):
        super().__init__()

    def add_row(self, *fields):
        """Add arbitrary amount of fields to row."""
        row = QHBoxLayout()
        for field in fields:
            row.addWidget(field)
        # Add row to layout.
        self.addLayout(row)
