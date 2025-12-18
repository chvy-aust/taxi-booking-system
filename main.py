import logging.config
import json
import sys

from PyQt6.QtWidgets import QApplication

from src import LOG_CONF_FILE, LOG_FILE, DB_FILE, MainWindow

if __name__ == '__main__':
    # Set global logger configurations.
    with open(LOG_CONF_FILE, 'r') as f:
        config = json.load(f)
        # Set config file location (prevent backslash complications).
        config["handlers"]["file"]["filename"] = str(LOG_FILE)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

    try:
        if not DB_FILE.exists():
            # Initialize database if missing.
            from scripts.init_db import initialize_database
            from scripts.seed_db import seed_database
            logger.warning("Database missing!")
            initialize_database()
            seed_database()

        # Start application event loop.
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.error(msg="A Fatal Error has occurred.\nExiting application.", exc_info=e)
        sys.exit(1)








