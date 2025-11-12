"""
A helper package for field validation.

Provides:
    - Null field check.
    - Age requirement check.
    - Match check between created and confirmed passwords.
"""

from src.app.widgets.input_edit import InputEdit

def null_validation(credentials: dict):
    """Validate against null credentials."""
    flag = True
    for instance, value in credentials.items():
        if value == "":
            instance.show_error()
            flag = False
    return flag

def password_validation(
        created_pass: str, confirmed_pass: str,
        create_pass_field: InputEdit, confirm_pass_field: InputEdit):
    """Check whether the created and confirmed passwords match."""
    if created_pass == confirmed_pass:
        return True
    else:
        create_pass_field.show_error()
        confirm_pass_field.show_error()
        return False
