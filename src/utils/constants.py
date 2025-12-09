from pathlib import Path
# Root
ROOT_DIR = Path(__file__).resolve().parents[2]
# Root DIRs
LOG_DIR = ROOT_DIR / 'logs'
SRC_DIR = ROOT_DIR / 'src'
STYLE_FILE = SRC_DIR / 'styles.qss'

UI_DIR = SRC_DIR / 'ui'
ICONS_DIR = UI_DIR / 'icons'

# Logging
LOG_CONF = LOG_DIR / 'config.json'
LOG_FILE = LOG_DIR / 'app.log'
# Database
DB_FILE = ROOT_DIR / 'taxibooking.db'

