from typing import Any
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QObject, Qt, QSize, QAbstractTableModel, QModelIndex
from student_record import StudentRecord


class StudentTableModel(QAbstractTableModel):
    def __init__(self, student_data: list[StudentRecord] = []) -> None:
        super(StudentTableModel, self).__init__()
        self.student_data: list[list] = None

        if student_data:
            self.student_data = [student.to_list() for student in student_data]
        else:
            self.student_data = []

        self._col_headers: list[str] = StudentRecord().headers()

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self.student_data[index.row()][index.column()]
                return str(value)

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if index.isValid():
            if role == Qt.ItemDataRole.EditRole:
                self.student_data[index.row()][index.column()] = value

    def rowCount(self, index: QModelIndex) -> int:
        return len(self.student_data)

    def columnCount(self, index: QModelIndex) -> int:
        return len(self._col_headers)

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._col_headers[section])
            if orientation == Qt.Orientation.Vertical:
                return str(section)

    def get_all_data(self)-> list[StudentRecord]:
        data:list[StudentRecord] = [StudentRecord(*record) for record in self.student_data]
        return data

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        return super().sort(column, order)
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsSelectable
