class ErrorMessage:
    DATABASE_ERROR = (
        "A database exception occurred during this transaction. "
        "Data was not stored and/or updated."
    )
    UNEXPECTED_ERROR = "An unknown exception was caught. Please Try Again or contact Support."