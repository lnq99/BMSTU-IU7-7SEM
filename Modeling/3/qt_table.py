from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem


class TableItem(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flags = super().flags()
        flags &= ~Qt.ItemFlag.ItemIsSelectable
        flags &= ~Qt.ItemFlag.ItemIsEditable
        self.setFlags(flags)
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
