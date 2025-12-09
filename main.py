import json
import logging.config
import sys

from PyQt6.QtWidgets import QApplication

from src import LOG_CONF, LOG_FILE, DB_FILE

if __name__ == '__main__':
    # Set global logger configurations.
    with open(LOG_CONF, 'r') as f:
        config = json.load(f)
        # Set relative config file location.
        config["handlers"]["file"]["filename"] = str(LOG_FILE)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

    try:
        # Initialize database if missing
        if not DB_FILE.exists():
            from scripts.init_db import initialize_database
            from scripts.seed_db import seed_database

            logger.warning("Database missing!")
            initialize_database()
            seed_database()

        # main window has to be imported after log config
        from src import MainWindow
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        # Start event loop
        sys.exit(app.exec())
    except Exception as e:
        logger.exception(e)
        sys.exit(1)





