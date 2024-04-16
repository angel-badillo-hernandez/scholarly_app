from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QApplication,
    QLineEdit,
    QDialog,
    QAbstractItemView,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QLineEdit,
    QPlainTextEdit,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from award_criteria_record import AwardCriteriaRecord


class ScholarlyManageScholarshipsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.title_label = QLabel("Scholarship Criteria")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list_view = QListView()
        self.list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )  # Allow multiple selections

        self.new_button = QPushButton("New")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.clear_selection_button = QPushButton("Clear Selection")

        # Connect button signals to slots
        self.new_button.clicked.connect(self.add_new_item)
        self.edit_button.clicked.connect(self.edit_selected_item)
        self.delete_button.clicked.connect(self.delete_selected_items)
        self.clear_selection_button.clicked.connect(self.clear_selection)

        # Connect double-click signal to edit_selected_item method
        self.list_view.doubleClicked.connect(self.edit_selected_item)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.list_view)

        # Button layout (horizontal)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_selection_button)

        layout.addLayout(button_layout)

        # Set the main layout for the widget
        self.setLayout(layout)

        # Initialize the list view with an empty model
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

    def set_list_data(self, scholarships: list[AwardCriteriaRecord]):
        """Set scholarship data for list view.

        Args:
            scholarships (list[AwardCriteriaRecord]): Scholarship data to be stored.
        """
        self.model.clear()
        for scholarship in scholarships:
            item = QStandardItem(scholarship.name)
            item.setEditable(False)  # Make item non-editable
            item.setData(
                scholarship, Qt.ItemDataRole.UserRole
            )  # Store item data in UserRole
            self.model.appendRow(item)

    def add_new_item(self):
        """
        Add a new item to the list view.
        """
        item_data = self.get_scholarship_data_from_user()
        if item_data:
            item = QStandardItem(item_data.name)
            item.setEditable(False)  # Make item non-editable
            item.setData(
                item_data, Qt.ItemDataRole.UserRole
            )  # Store item data in UserRole
            self.model.appendRow(item)

    def edit_selected_item(self):
        """
        Edit the selected item in the list view.
        """
        selected_indexes = self.list_view.selectedIndexes()
        if not selected_indexes:
            return

        index = selected_indexes[0]
        item = self.model.itemFromIndex(index)
        if item:
            current_data = item.data(Qt.ItemDataRole.UserRole)
            new_data = self.get_scholarship_data_from_user(current_data, True)
            if new_data:
                item.setText(new_data.name)
                item.setData(new_data, Qt.ItemDataRole.UserRole)

    def delete_selected_items(self):
        """
        Delete the selected items from the list view.
        """
        selected_indexes = self.list_view.selectedIndexes()
        if not selected_indexes:
            return

        items_to_remove = []
        for index in selected_indexes:
            items_to_remove.append(index.row())

        # Remove items from bottom to top to avoid index issues
        items_to_remove.sort(reverse=True)
        for row in items_to_remove:
            self.model.removeRow(row)

    def get_scholarship_data_from_user(
        self, initial_data=None, is_edit: bool = False
    ) -> AwardCriteriaRecord:
        dialog = ScholarshipCriteriaDialog(initial_data, parent=self, is_edit=is_edit)
        if dialog.exec():
            return dialog.get_scholarship_data()
        return None

    def clear_selection(self):
        self.list_view.clearSelection()


class ScholarshipCriteriaDialog(QDialog):
    def __init__(self, initial_data=None, parent=None, is_edit: bool = False):
        super().__init__(parent)

        if is_edit:
            self.setWindowTitle("Edit Scholarship")
        else:
            self.setWindowTitle("Create Scholarship")

        self.name_edit = QLineEdit()
        self.name_edit.setDisabled(is_edit)

        self.criteria_edit = QPlainTextEdit()
        self.limit_edit = QLineEdit()
        self.sort_edit = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Criteria:", self.criteria_edit)
        form_layout.addRow("Limit:", self.limit_edit)
        form_layout.addRow("Sort:", self.sort_edit)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

        if initial_data:
            self.name_edit.setText(initial_data.get("name", ""))
            self.criteria_edit.setPlainText(initial_data.get("criteria", ""))
            self.limit_edit.setText(initial_data.get("limit", ""))
            self.sort_edit.setText(initial_data.get("sort", ""))

    def get_scholarship_data(self) -> AwardCriteriaRecord:
        """Get data entered in the input fields.

        Returns:
            AwardCriteriaRecord: Scholarship criteria entered in the fields
        """
        return AwardCriteriaRecord(self.name_edit.text(),) # Fix


# Example usage:
if __name__ == "__main__":
    import sys

    app: QApplication = QApplication([])
    tab: ScholarlyManageScholarshipsTab = ScholarlyManageScholarshipsTab()

    # Set data for the list view
    data = [
        {"name": "Item 1", "criteria": "A", "limit": "10", "sort": "asc"},
        {"name": "Item 2", "criteria": "B", "limit": "20", "sort": "desc"},
        {"name": "Item 3", "criteria": "C", "limit": "30", "sort": "asc"},
    ]
    tab.set_list_data(data)

    tab.show()
    sys.exit(app.exec())
