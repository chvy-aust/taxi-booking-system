class FieldHint:
    AGE_REQUIREMENT_HINT = "You must be 18+ to use this service."
    PHONENUM_FORMAT_HINT = (
        "May contain optional country code. Must have area and local code.\n"
        "Examples of valid formats:\n"
        "+1 (123) 456 7890 | (123) 456 7890\n"
        "1 123 456 7890 | 1-123-456-7890\n"
        "123 456 7890 | 123-456-7890"
    )
    EMAIL_FORMAT_HINT = "Must contain '@' and '.'"
    PASSWORD_FORMAT_HINT = (
        "Password must contain atleast:\n"
        "   → 8 characters\n"
        "   → 1 uppercase letter\n"
        "   → 1 lowercase letter\n"
        "   → 1 number."
    )
    MATCHING_PASSWORD_HINT = "These passwords must match."