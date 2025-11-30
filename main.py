import sqlite3
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from scripts.init_db import initialize_database
from src.app import MainWindow

DB_FILE = Path(__file__).parent / 'taxibooking.db'

if __name__ == '__main__':
    if not DB_FILE.exists():
        print("( WARNING ⚠ ) Database missing!")
        try:
            initialize_database()
        except sqlite3.Error:
            sys.exit(1)

    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"( CRITICAL ⚠ ) ERROR: {e}")
        sys.exit(1)



