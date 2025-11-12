from typing import override

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDateEdit, QLabel, QHBoxLayout

from src.app.scenes.base import BaseScene
from src.app.widgets.button import Button
from src.app.widgets.form_layout import FormLayout
from src.app.widgets.input_edit import InputEdit

class RegisterScene(BaseScene):
    """Register scene class for the application."""
    def __init__(self, signals):
        """Initialize scene signals and UI."""
        super().__init__(
            scene_name="register",
            signals=signals)
        self.signals = signals
        self._load_ui()

    @override
    def _load_ui(self):
        """Setup UI."""
        # Register scene header label.
        header = QLabel("Create a new Account")
        header.setObjectName("HEADER")
        header.setFixedHeight(80)

        # Custom divider.
        divider = QWidget()
        divider.setObjectName("DIVIDER")
        divider.setFixedHeight(3)

        # Make credential fields.
        self.firstname = InputEdit("Enter first name:")
        self.lastname = InputEdit("Enter last name:")
        self.dob = InputEdit("Enter date of birth:", QDateEdit())
        self.phonenum = InputEdit("Enter phone number:")
        self.email = InputEdit("Enter email address:")
        self.create_pass = InputEdit("Create new password:")
        self.confirm_pass = InputEdit("Confirm new password:")

        # Add fields to form layout.
        form_layout = FormLayout()
        form_layout.add_row(self.firstname, self.lastname)
        form_layout.add_row(self.dob, self.phonenum)
        form_layout.add_row(self.email)
        form_layout.add_row(self.create_pass, self.confirm_pass)

        # Make form with layout.
        form = QWidget()
        form.setObjectName("register_form")
        form.setLayout(form_layout)

        # Make buttons.
        back_btn = Button("Return to Main Menu", self.signals.request_splash)
        register_btn = Button("Register", self._start_registration)

        # Add buttons to container.
        btns = QHBoxLayout()
        btns.addWidget(back_btn)
        btns.addStretch()
        btns.addWidget(register_btn)

        # Add all elements to scene's layout.
        container = QVBoxLayout()
        container.addWidget(header)
        container.addWidget(divider)
        container.addWidget(form)
        container.addLayout(btns)

        # Set layout to scene.
        self.setLayout(container)

    def _start_registration(self):
        """Start the registration process."""
        credentials = self._get_credentials()

    def _get_credentials(self):
        """
        Return mapping of field instances to their values.
        """
        credentials = {
            self.firstname: self.firstname.value().capitalize(),
            self.lastname: self.lastname.value().capitalize(),
            self.dob: self.dob.value(),
            self.phonenum: self.phonenum.value(),
            self.email: self.email.value().lower(),
            self.create_pass: self.create_pass.value(),
            self.confirm_pass: self.confirm_pass.value()
        }
        return credentials

