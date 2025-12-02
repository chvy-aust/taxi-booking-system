import json
import logging.config
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

# Path constants
ROOT_DIR = Path(__file__).parent
LOG_DIR = ROOT_DIR / 'logs'
LOG_CONF = LOG_DIR / 'config.json'
DB_FILE = ROOT_DIR / 'taxibooking.db'

def main():
    # Set global logger configurations.
    with open(LOG_CONF, 'r') as f:
        logger_config = json.load(f)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger(__name__)

    try:
        # Initialize database if missing
        if not DB_FILE.exists():
            from scripts.init_db import initialize_database
            logger.warning("Database missing!")
            initialize_database()

        # Start event loop
        from src import MainWindow
        # main window has to be imported after log config
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

if __name__ == '__main__':
    main()





