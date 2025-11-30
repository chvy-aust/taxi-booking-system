from PyQt6.QtCore import Qt, QAbstractListModel


class BookingListModel(QAbstractListModel):
    def __init__(self, bookings=None):
        super().__init__()
        self.bookings = bookings or []

    def data(self, index, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.bookings[index.row()])

    def rowCount(self, parent = ...):
        return len(self.bookings)
