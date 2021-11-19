import typing

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt


class NumpyModel(QAbstractTableModel):
    
    def __init__(self, data, horizontal_header=None, vertical_header=None):
        super().__init__()
        self._data = data
        self._horizontal_header = horizontal_header
        self._vertical_header = vertical_header

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[1]

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data[index.row(), index.column()]
                return str(value)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            self._data[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if self._horizontal_header and orientation == Qt.Orientation.Horizontal:
                return str(self._horizontal_header[section])
            if self._vertical_header and orientation == Qt.Orientation.Vertical:
                return str(self._vertical_header[section])

        return super().headerData(section, orientation, role)


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

        print(data)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data[0])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                value = self._data[index.row()][index.column()]
                return str(value)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled
