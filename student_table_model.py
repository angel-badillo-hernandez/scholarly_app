"""Provides a class that defines a model for student data

Provides the class `StudentTableModel` that allows student data
to be represented and displayed in a `TableView`.
"""

from typing import Any
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QObject, Qt, QSize, QAbstractTableModel, QModelIndex
from student_record import StudentRecord


class StudentTableModel(QAbstractTableModel):
    """Class that represents student data as a table.

    Class that represents student data as a table for use in
    a `TableView`.

    """

    def __init__(self, student_data: list[StudentRecord] = []) -> None:
        """Creates an instance of StudentTableModel

        Creates a new instance of StudentTableModel.

        Args:
            student_data (list[StudentRecord], optional): list of StudentRecord.
        """
        super(StudentTableModel, self).__init__()
        self.student_data: list[list] = None

        if student_data:
            self.student_data = [student.to_list() for student in student_data]
        else:
            self.student_data = []

        self._col_headers: list[str] = StudentRecord().headers()

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> str | None:
        """Overridden function for displaying data in table.

        Overriden function for displaying data in a table

        Args:
            index (QModelIndex): The index of the cell in the table.
            role (ItemDataRole): Enum specifying the role the data is taking.

        Returns:
            str representing the data, or `None` if invalid arguments.
        """
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self.student_data[index.row()][index.column()]
                return str(value)
        return None

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        """Overridden function for displaying data in table.

        Overriden function for displaying data in a table

        Args:
            index (QModelIndex): The index of the cell in the table.
            role (ItemDataRole): Enum specifying the role the data is taking.

        Returns:
            str representing the data, or `None` if invalid arguments.
        """
        if index.isValid():
            if role == Qt.ItemDataRole.EditRole:
                self.student_data[index.row()][index.column()] = value
                return True
        return False

    def rowCount(self, index: QModelIndex) -> int:
        """Returns the number of rows.

        Returns the number of rows in the table.

        Args:
            index (QModelIndex): Index of the cell in the table.
        Returns:
            The number of rows in the table.
        """
        return len(self.student_data)

    def columnCount(self, index: QModelIndex) -> int:
        """Returns the number of columns.

        Returns the number of columns in the table.

        Args:
            index (QModelIndex): Index of the cell in the table.
        Returns:
            The number of columns in the table.
        """
        return len(self._col_headers)

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ) -> str | None:
        """Returns the header name.

        Returns the header name for the rows and columns in the table.

        Args:
            section (int): The row or column number, depending on orientation.
            orientation (Orientation): The orientation of the header.
            role (ItemDataRole): The role or behavior the item is taking.
        Returns:
            The header for the row or column as a str.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._col_headers[section])
            if orientation == Qt.Orientation.Vertical:
                return str(section)

    def get_all_data(self) -> list[StudentRecord]:
        """Returns all of the data in the table.

        Returns all of the data in the table as StudentRecords.

        Returns:
            A list of StudentRecord.
        """
        data: list[StudentRecord] = [
            StudentRecord(*record) for record in self.student_data
        ]
        return data

    def get_row(self, row: int) -> StudentRecord:
        """Returns the data from a row in the table.

        Returns the data from a row in the table as a StudentRecord.

        Args:
            row (int): The row in the table.
        Returns:
            A StudentRecord.
        """
        record: StudentRecord = StudentRecord(*self.student_data[row])
        return record

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Describes the behavior items in the table.

        Describes and enables selecting items in the table.

        Args:
            index (QModelIndex): The index of the item.
        Returns:
            An ItemFlag describing the behavior of the item.
        """
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
