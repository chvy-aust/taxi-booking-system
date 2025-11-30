class FieldHint:
    AGE_REQUIREMENT = "You must be 18+ to use this service."
    PHONENUM_FORMAT = (
        "May contain optional country code. Must have area and local code.\n"
        "Examples of valid formats:\n"
        "+1 (123) 456 7890 | (123) 456 7890\n"
        "1 123 456 7890 | 1-123-456-7890\n"
        "123 456 7890 | 123-456-7890"
    )
    EMAIL_FORMAT = "Must contain '@' and '.'"
    PASSWORD_FORMAT = (
        "Password must contain atleast:\n"
        "   → 8 characters\n"
        "   → 1 uppercase letter\n"
        "   → 1 lowercase letter\n"
        "   → 1 number."
    )
    MATCHING_PASSWORD = "These passwords must match."

class ErrorMessage:
    DATABASE_ERROR = (
        "A database exception occurred during this transaction. "
        "Data was not stored and/or updated."
    )
    UNEXPECTED_ERROR = "An unknown exception was caught. Please Try Again or contact Support."