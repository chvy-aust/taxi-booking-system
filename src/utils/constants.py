from pathlib import Path
# Root
ROOT_DIR = Path(__file__).resolve().parents[2]
# Root DIRs
LOG_DIR = ROOT_DIR / 'logs'
SRC_DIR = ROOT_DIR / 'src'

UI_DIR = SRC_DIR / 'ui'
ICONS_DIR = UI_DIR / 'icons'
STYLE_FILE = UI_DIR / 'styles.qss'

# Logging
LOG_CONF = LOG_DIR / 'config.json'
LOG_FILE = LOG_DIR / 'app.log'
# Database
DB_FILE = ROOT_DIR / 'taxibooking.db'

