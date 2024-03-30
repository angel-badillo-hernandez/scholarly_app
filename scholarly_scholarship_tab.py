from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QFormLayout,
    QLayout,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QToolButton,
    QToolTip,
    QGroupBox,
    QComboBox,
    QLabel,
)
from PyQt6.QtGui import QAction, QDoubleValidator, QValidator, QIntValidator, QIcon
from typing import Callable
import os

BASE_DIR: str = os.path.dirname(__file__)

# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: print("works")


class ScholarlyScholarshipTab(QTabWidget):
    def __init__(
        self,
        find_button_clicked: Callable[[QWidget], None] = voidCallBack,
        select_template_button_clicked: Callable[[QWidget], None] = voidCallBack,
        select_directory_button_clicked: Callable[[QWidget], None] = voidCallBack,
        generate_letters_button_clicked: Callable[[QWidget], None] = voidCallBack,
        scholarship_combo_box_items: list[str] = [],
    ) -> None:
        super().__init__()

        # Main layout for widget
        main_layout: QVBoxLayout = QVBoxLayout()

        # Load items in comboxbox
        self.scholarship_combobox: QComboBox = QComboBox()
        self.scholarshipComboxBoxAddItems(scholarship_combo_box_items)

        # Set up auto complete
        self.scholarship_combobox.setEditable(True)

        # Create Find button
        self.find_button: QToolButton = QToolButton()
        self.find_button.setIcon(
            QIcon(os.path.join(BASE_DIR, "assets/icons/search.svg"))
        )
        self.find_button.clicked.connect(find_button_clicked)

        # Create groupbox for scholarship combobox and find button
        select_scholarship_group_box: QGroupBox = QGroupBox("Select a Scholarship")

        #
        search_layout: QHBoxLayout = QHBoxLayout()
        search_layout.addWidget(self.find_button)
        search_layout.addWidget(self.scholarship_combobox)

        select_scholarship_group_box.setLayout(search_layout)

        main_layout.addWidget(select_scholarship_group_box)

        # Fields and text boxes for generating letters
        letter_info_widget: QWidget = QWidget()
        letter_info_layout: QFormLayout = QFormLayout()
        letter_info_widget.setLayout(letter_info_layout)

        # Text boxes
        self.sender_name_textbox: QLineEdit = QLineEdit()
        self.sender_title_textbox: QLineEdit = QLineEdit()
        self.sender_email_textbox: QLineEdit = QLineEdit()
        self.amount_textbox: QLineEdit = QLineEdit()
        self.amount_textbox.setValidator(QDoubleValidator())
        self.template_path_textbox: QLineEdit = QLineEdit()
        self.dest_dir_path_textbox: QLineEdit = QLineEdit()
        self.academic_year_fall_textbox: QLineEdit = QLineEdit()
        self.academic_year_spring_textbox:QLineEdit = QLineEdit()

        # Select template letter button
        self.select_template_button: QToolButton = QToolButton()
        self.select_template_button.setText("Browse")
        self.select_template_button.setToolTip("Select template letter file.")
        self.select_template_button.clicked.connect(select_template_button_clicked)

        # Layout for selecting template letter button
        select_template_layout: QHBoxLayout = QHBoxLayout()
        select_template_layout.addWidget(self.select_template_button)
        select_template_layout.addWidget(self.template_path_textbox)

        # Select directory button
        self.select_directory_button: QToolButton = QToolButton()
        self.select_directory_button.setText("Browse")
        self.select_directory_button.setToolTip("Select the destination directory.")
        self.select_directory_button.clicked.connect(select_directory_button_clicked)

        # Add textboxes to form layout
        letter_info_layout.addRow("Sender Name", self.sender_name_textbox)
        letter_info_layout.addRow("Sender Title", self.sender_title_textbox)
        letter_info_layout.addRow("Sender Email", self.sender_email_textbox)
        letter_info_layout.addRow("Amount", self.amount_textbox)
        letter_info_layout.addRow("Academic Year", self.academic_year_fall_textbox)

        # Layout for selecting destination directory
        select_dir_layout: QHBoxLayout = QHBoxLayout()
        select_dir_layout.addWidget(self.select_directory_button)
        select_dir_layout.addWidget(self.dest_dir_path_textbox)

        # Add template letter layout to letter info layout
        letter_info_layout.addRow("Template Letter", select_template_layout)

        # Add layout to letter info layout
        letter_info_layout.addRow("Destination Directory", select_dir_layout)
        main_layout.addWidget(letter_info_widget)

        # Generate Letters button
        self.generate_letters_button: QToolButton = QToolButton()
        self.generate_letters_button.setText("Generate Letters")
        self.generate_letters_button.setToolTip(
            "Generates Scholarship Letter for selected students."
        )
        self.generate_letters_button.clicked.connect(generate_letters_button_clicked)

        # Add widget to scholarship components layout
        main_layout.addWidget(self.generate_letters_button)
        self.setLayout(main_layout)

    def findButtonToggle(self, enabled: bool) -> None:
        self.find_button.setEnabled(enabled)

    def scholarshipComboBoxToggle(self, enabled: bool) -> None:
        self.scholarship_combobox.setEnabled(enabled)

    def senderNameTextBoxToggle(self, enabled: bool) -> None:
        self.sender_name_textbox.setEnabled(enabled)

    def senderEmailTextBoxToggle(self, enabled: bool) -> None:
        self.sender_email_textbox.setEnabled(enabled)

    def senderTitleTextBoxToggle(self, enabled: bool) -> None:
        self.sender_title_textbox.setEnabled(enabled)

    def amountTextBoxToggle(self, enabled: bool) -> None:
        self.amount_textbox.setEnabled(enabled)

    def academicYearTextBoxToggle(self, enabled: bool) -> None:
        self.academic_year_fall_textbox.setEnabled(enabled)

    def templateLetterPathTextBoxToggle(self, enabled: bool) -> None:
        self.template_path_textbox.setEnabled(enabled)

    def destDirPathTextBoxToggle(self, enabled: bool) -> None:
        self.dest_dir_path_textbox.setEnabled(enabled)

    def selectTemplateButtonToggle(self, enabled: bool) -> None:
        self.select_template_button.setEnabled(enabled)

    def selectDirectoryButtonToggle(self, enabled: bool) -> None:
        self.select_directory_button.setEnabled(enabled)

    def generateLettersButtonToggle(self, enabled: bool) -> None:
        self.generate_letters_button.setEnabled(enabled)

    def toggleAll(self, enabled: bool) -> None:
        self.senderNameTextBoxToggle(enabled)
        self.scholarshipComboBoxToggle(enabled)
        self.senderEmailTextBoxToggle(enabled)
        self.senderTitleTextBoxToggle(enabled)
        self.amountTextBoxToggle(enabled)
        self.academicYearTextBoxToggle(enabled)
        self.templateLetterPathTextBoxToggle(enabled)
        self.selectTemplateButtonToggle(enabled)
        self.selectDirectoryButtonToggle(enabled)
        self.destDirPathTextBoxToggle(enabled)
        self.generateLettersButtonToggle(enabled)
        self.findButtonToggle(enabled)

    def scholarshipComboxBoxAddItems(self, items: list[str]) -> None:
        self.scholarship_combobox.addItems(items)

    def scholarshipComboBoxClear(self) -> None:
        self.scholarship_combobox.clear()

    def scholarshipComboBoxAddItem(self, item: str) -> None:
        self.scholarship_combobox.addItem(item)

    def setFindButtonClicked(self, callback: Callable[[QWidget], None]) -> None:
        self.find_button.clicked.connect(callback)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    s = ScholarlyScholarshipTab()
    s.toggleAll(1)
    s.scholarshipComboxBoxAddItems(
        [
            "",
            "Fortnite",
            "Minecraft",
            "The Best Scholarship Award",
            "Future Hero Scholarship",
        ]
    )
    s.show()
    a.exec()
