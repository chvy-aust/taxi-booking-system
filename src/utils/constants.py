class FieldHints:
    AGE_REQUIREMENT = "You must be 18+ to use this service."
    PHONENUM_FORMAT = (
        "May contain optional country code. Must have area and local code.\n"
        "Examples of valid formats:\n"
        "+1 (123) 456 7890 | (123) 456 7890\n"
        "1 123 456 7890 | 1-123-456-7890\n"
        "123 456 7890 | 123-456-7890"
    )
    EMAIL_FORMAT = "Must contain '@' and '.'"
    PASSWORD_FORMAT = "Password must be 8 characters and contain 1 uppercase letter, 1 lowercase letter and 1 number."
    MATCHING_PASSWORD = "These passwords must match."
