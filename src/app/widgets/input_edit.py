from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QWidget, QDateEdit, \
    QHBoxLayout


class InputEdit(QWidget):
    def __init__(self,
                 label: str,
                 input_type: type[QDateEdit | QLineEdit] = QLineEdit,
                 object_name: str = None,
                 tooltip: str = None):
        super().__init__()
        self.label = QLabel(label)
        self.setObjectName(object_name)
        self.input_field = input_type()
        self.tooltip = QLabel("( i )")
        if tooltip:
            self.tooltip.setToolTip(tooltip)
        else:
            self.tooltip.setHidden(True)

        if isinstance(self.input_field, QDateEdit):
            self.input_field.setDisplayFormat("yyyy-MM-dd")

        # Add elements to layout.
        layout = QVBoxLayout()
        lbl_tltp = QHBoxLayout()
        lbl_tltp.addWidget(self.label)
        lbl_tltp.addWidget(self.tooltip)
        layout.addLayout(lbl_tltp)
        layout.addWidget(self.input_field)
        self.setLayout(layout)

    def value(self):
        """Return value from field."""
        if isinstance(self.input_field, QDateEdit):
            return self.input_field.date()
        else:
            return self.input_field.text().strip()

    def show_error(self):
        """Hint at errors with red highlighting."""
        self.tooltip.setStyleSheet("color: #521A1A;")
        self.label.setStyleSheet("color: #521A1A;")
        self.input_field.setStyleSheet("color: #521A1A; border: 3px solid #521A1A")

    def clear_error(self):
        """Remove error hint."""
        self.tooltip.setStyleSheet(None)
        self.label.setStyleSheet(None)
        self.input_field.setStyleSheet(None)


