import re
from typing import override

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QDateEdit

from src.app.scenes.base import BaseScene
from src.app.widgets.button import Button
from src.app.widgets.form_layout import FormLayout
from src.app.widgets.input_edit import InputEdit, ToolTip
from src.utils.validation import validate_age, validate_null

PHONENUM = re.compile(r"(^\+?\d{1,3}[-\s]?)?(\(\d{1,3}\)|\d{1,3})[-\s]?\d{1,3}[-\s]?\d{1,4}$")
EMAIL = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$")
PASSWORD = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}")

class RegisterScene(BaseScene):
    """Register scene class for the application."""
    def __init__(self, signals):
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

        # Name fields.
        self.firstname = InputEdit("Enter first name:")
        self.lastname = InputEdit("Enter last name:")
        # Date of birth field + tooltip.
        self.dob = InputEdit("Enter date of birth:", QDateEdit)
        self.dob.setToolTip(ToolTip.AGE_REQUIREMENT)
        # Phone number field + tooltip.
        self.phonenum = InputEdit("Enter phone number:")
        self.phonenum.setToolTip(ToolTip.PHONENUM_FORMAT)
        # Email field + tooltip.
        self.email = InputEdit("Enter email address:")
        self.email.setToolTip(ToolTip.EMAIL_FORMAT)
        # Password fields + tooltips.
        self.create_pass = InputEdit("Create new password:")
        self.create_pass.setToolTip(ToolTip.PASSWORD_FORMAT)
        self.confirm_pass = InputEdit("Confirm new password:")
        self.confirm_pass.setToolTip(ToolTip.MATCHING_PASSWORD)

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
        self.register_btn = Button("Register", self._start_registration)

        # Add buttons to container.
        btns = QHBoxLayout()
        btns.addWidget(back_btn)
        btns.addStretch()
        btns.addWidget(self.register_btn)

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
        if self._check_validation(credentials):
            return
        print("VALID!")

    def _get_credentials(self):
        credentials = {
            self.firstname: self.firstname.value().title(),
            self.lastname:  self.lastname.value().title(),
            self.dob: self.dob.value(),
            self.phonenum: self.phonenum.value(),
            self.email: self.email.value(),
            self.create_pass: self.create_pass.value()
        }
        return credentials

    def _check_validation(self, credentials):
        """Validate credentials and return errors, if applicable."""
        # Reset validation hinting.
        for field in credentials.keys():
            field.clear_error()
        invalid_fields = []

        # Check for null fields.
        if not validate_null(credentials):
            invalid_fields.append("Null fields caught.")

        # Check if user meets age requirement.
        if not validate_age(credentials[self.dob]):
            self.dob.show_error()
            invalid_fields.append(self.dob)

        # Check phone format.
        if not re.match(PHONENUM, credentials[self.phonenum]):
            self.phonenum.show_error()
            invalid_fields.append(self.phonenum)

        # Check email format.
        if not re.match(EMAIL, credentials[self.email]):
            self.email.show_error()
            invalid_fields.append(self.email)

        # Check password format.
        if not re.match(PASSWORD, credentials[self.create_pass]):
            self.create_pass.show_error()
            invalid_fields.append(self.create_pass)

        # Check if passwords match.
        if self.create_pass.value() != self.confirm_pass.value():
            self.confirm_pass.show_error()
            invalid_fields.append(self.confirm_pass)

        return invalid_fields














