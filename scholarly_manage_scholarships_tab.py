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
    QComboBox,
    QPlainTextEdit,
    QMessageBox,
)
from PyQt6.QtCore import Qt
import json
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIntValidator
from award_criteria_record import AwardCriteriaRecord
from typing import Callable

# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: None


class ScholarlyManageScholarshipsTab(QWidget):
    def __init__(
        self,
        add_new_item_clicked: Callable[[QWidget], None] = voidCallBack,
        edit_button_clicked: Callable[[QWidget], None] = voidCallBack,
        delete_button_clicked: Callable[[QWidget], None] = voidCallBack,
        refresh_button_clicked: Callable[[QWidget], None] = voidCallBack,
    ):
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
        self.refresh_button = QPushButton("Refresh")
        self.clear_selection_button = QPushButton("Clear Selection")

        # Connect button signals to slots
        self.new_button.clicked.connect(add_new_item_clicked)
        self.edit_button.clicked.connect(edit_button_clicked)
        self.delete_button.clicked.connect(delete_button_clicked)
        self.refresh_button.clicked.connect(refresh_button_clicked)
        self.clear_selection_button.clicked.connect(self.clear_selection)

        # Connect double-click signal to edit_selected_item method
        self.list_view.doubleClicked.connect(edit_button_clicked)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.list_view)

        # Button layout (horizontal)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
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

    def get_scholarship_data_from_user(
        self, initial_data: AwardCriteriaRecord = None, is_edit: bool = False
    ) -> AwardCriteriaRecord:
        """Return AwardCriteriaRecord acquired from user input.

        Args:
            initial_data (AwardCriteriaRecord, optional): Initial data of the item, if the action is an edit. Defaults to None.
            is_edit (bool, optional): True if the action is an edit. If False, the action is adding a new item into the list. Defaults to False.

        Returns:
            AwardCriteriaRecord: _description_
        """
        dialog = ScholarshipCriteriaDialog(initial_data, parent=self, is_edit=is_edit)

        # Show dialog
        if dialog.exec():

            try:
                scholarship_criteria: AwardCriteriaRecord = (
                    dialog.get_scholarship_data()
                )

                return scholarship_criteria
            except Exception as e:
                QMessageBox.critical(self, "Invalid Data", str(e))
                return None
        return None

    def clear_selection(self):
        self.list_view.clearSelection()


class ScholarshipCriteriaDialog(QDialog):
    def __init__(
        self,
        initial_data: AwardCriteriaRecord = None,
        parent: QWidget = None,
        is_edit: bool = False,
    ):
        super().__init__(parent)

        # Set appropriate title for action being performed
        if is_edit:
            self.setWindowTitle("Edit Scholarship")
        else:
            self.setWindowTitle("Create Scholarship")

        # Create textbox for name
        self.name_textbox = QLineEdit()

        # If action is an edit, disable name textbox
        self.name_textbox.setDisabled(is_edit)

        # Create textbox for criteria
        self.criteria_textbox = QPlainTextEdit()

        # Create textbox for limit
        self.limit_textbox = QLineEdit()
        self.limit_textbox.setValidator(QIntValidator())

        # Create textbox for sort
        self.sort_textbox = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_textbox)
        form_layout.addRow("Criteria:", self.criteria_textbox)
        form_layout.addRow("Limit:", self.limit_textbox)
        form_layout.addRow("Sort:", self.sort_textbox)

        # Button box for dialog button options
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

        # If dialog is created with initial data passed in,
        # display the initial data text
        if initial_data:
            self.name_textbox.setText(initial_data.name)
            self.criteria_textbox.setPlainText(json.dumps(initial_data.criteria))
            self.limit_textbox.setText(json.dumps(initial_data.limit))
            self.sort_textbox.setText(json.dumps(initial_data.sort))

    def get_scholarship_data(self) -> AwardCriteriaRecord:
        """Get data entered in the input fields.

        Returns:
            AwardCriteriaRecord: Scholarship criteria entered in the fields
        """
        name: str = None
        criteria: dict = None
        limit: int = None
        sort: list[list[str, int]] = None

        name: str = self.name_textbox.text()

        # Name is primary key for scholarship table, so must not be empty
        if not name:
            raise Exception("Name is empty, please enter a name.")

        # Perform data validation criteria
        try:
            text: str = self.criteria_textbox.toPlainText()

            # If nothing is entered, use default criteria
            if not text:
                criteria = {}
            else:
                criteria = json.loads(text)

                # If not a dict object, invalid criteria
                if not isinstance(criteria, dict):
                    raise Exception(
                        "Invalid format for criteria. Please enter valid criteria."
                    )
        except json.JSONDecodeError as e:
            raise Exception("Invalid format for criteria. Please enter valid criteria.")

        # Perform data validation on limit
        try:
            text: str = self.limit_textbox.text()

            # If nothing is entered, use default criteria
            if not text:
                limit = 0
            else:
                limit = json.loads(text)

                # If limit is not a non-negative integer, invalid limit
                if not isinstance(limit, int) or limit < 0:
                    raise Exception(
                        "Invalid value for limit. Please enter a non-negative integer for limit."
                    )
        except json.JSONDecodeError as f:
            raise Exception(
                "Invalid value for limit. Please enter a non-negative integer for limit."
            )

        # Perform data validation on sort
        try:
            text: str = self.sort_textbox.text()

            # If nothing is entered, use default sort
            if not text:
                sort = sort = [["cum_gpa", -1]]
            else:
                sort = json.loads(text)

                # If sort is not a list, invalid sort
                if not isinstance(sort, list):
                    raise Exception(
                        "Invalid format for sort. Please enter a valid argument for sort."
                    )
        except json.JSONDecodeError as g:
            raise Exception(
                "Invalid format for sort. Please enter a valid argument for sort."
            )

        return AwardCriteriaRecord(name, criteria, limit, sort)


# Example usage:
if __name__ == "__main__":
    import sys
    from rich import print

    app: QApplication = QApplication([])
    tab: ScholarlyManageScholarshipsTab = ScholarlyManageScholarshipsTab()

    # Set data for the list view
    data = [
        AwardCriteriaRecord(
            **{
                "name": "Item 1",
                "criteria": {"a": "g"},
                "limit": 1,
                "sort": [["cum_gpa", 1]],
            }
        )
    ]
    tab.set_list_data(data)

    tab.show()
    sys.exit(app.exec())
