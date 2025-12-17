from pathlib import Path
# File directories + paths
ROOT_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT_DIR / 'logs'
SRC_DIR = ROOT_DIR / 'src'
DB_FILE = ROOT_DIR / 'taxibooking.db'
LOG_CONF_FILE = LOG_DIR / 'config.json'
LOG_FILE = LOG_DIR / 'app.log'
STYLE_FILE = SRC_DIR / 'styles.qss'
UI_DIR = SRC_DIR / 'ui'
ICONS_DIR = UI_DIR / 'icons'

# Bookings
ACTIVE_BOOKING_STATUS = ('waiting_for_assignment','waiting_for_pickup','in_process')
NON_ACTIVE_BOOKING_STATUS = ('completed', 'cancelled')
ALL_BOOKING_STATUSES = NON_ACTIVE_BOOKING_STATUS + ACTIVE_BOOKING_STATUS

# Error messages
UNEXPECTED_ERROR = "An unknown exception was caught. Please Try Again or contact Support."
DB_ERROR = ("A database exception occurred during this transaction.\n"
"Please Try Again or contact Support.")
BOOKING_DB_ERROR = "Could not retrieve and/or access booking records."
USER_DB_ERROR = "Could not retrieve and/or access user records."
USER_ACCOUNT_DB_ERROR = "Could not access your account. Please Try Again or contact Support."

