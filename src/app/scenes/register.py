from typing import override

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from database.db import DatabaseConnection
from src.app.scenes.base import BaseScene
from src.app.widgets.button import Button
from src.app.widgets.dialogs import InfoDialog
from src.app.widgets.form_layout import FormLayout
from src.app.widgets.input_edit import InputEdit, DateEdit
from src.utils.constants import FieldHints
from src.utils.validation import validate_phonenum, validate_dob, \
    validate_email, validate_password


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
        self.dob = DateEdit("Enter date of birth:")
        self.dob.set_tooltip(FieldHints.AGE_REQUIREMENT)
        # Phone number field + tooltip.
        self.phonenum = InputEdit("Enter phone number:")
        self.phonenum.set_tooltip(FieldHints.PHONENUM_FORMAT)
        # Email field + tooltip.
        self.email = InputEdit("Enter email address:")
        self.email.set_tooltip(FieldHints.EMAIL_FORMAT)
        self.address = InputEdit("Enter home address:")
        # Password fields + tooltips.
        self.create_pass = InputEdit("Create new password:")
        self.create_pass.set_tooltip(FieldHints.PASSWORD_FORMAT)
        self.confirm_pass = InputEdit("Confirm new password:")
        self.confirm_pass.set_tooltip(FieldHints.MATCHING_PASSWORD)

        self.fields = [
            self.firstname, self.lastname,
            self.dob, self.phonenum,
            self.email, self.address,
            self.create_pass,
            self.confirm_pass
        ]

        # Add fields to form layout.
        form_layout = FormLayout()
        form_layout.add_row(self.firstname, self.lastname)
        form_layout.add_row(self.dob, self.phonenum)
        form_layout.add_row(self.email)
        form_layout.add_row(self.address)
        form_layout.add_row(self.create_pass, self.confirm_pass)

        # Make form with layout.
        form = QWidget()
        form.setObjectName("register_form")
        form.setLayout(form_layout)

        # Make buttons.
        back_btn = Button("Return to Main Menu", self._return_to_menu)
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

    def _return_to_menu(self):
        self._reset_fields()
        self.signals.request_splash.emit()

    def _start_registration(self):
        """Start the registration process."""
        values = self._get_credentials()
        if not self._check_validation(values):
            return

        try:
            with DatabaseConnection() as cursor:
                cursor.execute("""
                    INSERT INTO user (role, firstname, lastname, dob, phonenum, email, address, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ("customer", values["firstname"], values["lastname"],
                     values["dob"].toString(), values["phonenum"],
                      values["email"], values["address"], values["create_pass"],))
        except Exception as e:
            message = "An error occurred! Please Try Again or contact support.\n"
            err_dialog = InfoDialog(f"{message}\nError: {e}", self)
            err_dialog.show()
        else:
            message = "Your account has been registered!"
            success_dialog = InfoDialog(message, self)
            success_dialog.show()



        self._return_to_menu()

    def _get_credentials(self):
        """Return dict of field values."""
        values = {
            "firstname": self.firstname.text().title(),
            "lastname":  self.lastname.text().title(),
            "dob": self.dob.date(),
            "phonenum": self.phonenum.text(),
            "email": self.email.text().lower(),
            "address": self.address.text(),
            "create_pass": self.create_pass.text(),
            "confirm_pass": self.confirm_pass.text()
        }
        return values

    def _check_validation(self, values) -> bool:
        """Validate credentials and show validation hints."""
        self._reset_validation_hints()
        # Map validation status to instance.
        validation_checks = {
            self.firstname: values["firstname"] != "",
            self.lastname: values["lastname"] != "",
            self.dob: validate_dob(values["dob"]),
            self.phonenum: validate_phonenum(values["phonenum"]),
            self.email: validate_email(values["email"]),
            self.address: values["address"] != "",
            self.create_pass: validate_password(values["create_pass"]),
            self.confirm_pass: values["create_pass"] == values["confirm_pass"]
        }

        flag = True
        for field, is_valid in validation_checks.items():
            if not is_valid:
                field.show_error()
                flag = False
        # Indication of whether any fields were invalid.
        return flag

    def _reset_validation_hints(self):
        """Remove error hinting."""
        for field in self.fields:
            field.clear_error()

    def _reset_fields(self):
        """Remove error hinting and clear fields."""
        for field in self.fields:
            field.reset()












