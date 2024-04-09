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
from PyQt6.QtGui import (
    QAction,
    QDoubleValidator,
    QValidator,
    QIntValidator,
    QIcon,
    QColor,
)
from PyQt6.QtCore import QSize
from scholarly_icons import ScholarlyIcon, Icons, IconSizes
from typing import Callable
import os


# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: None


class ScholarlyScholarshipTab(QWidget):
    """Widget class for Scholarship Tab

    A class that is for the GUI component, Scholarship tab.
    """

    def __init__(
        self,
        parent: QWidget = None,
        find_button_clicked: Callable[[QWidget], None] = voidCallBack,
        select_template_button_clicked: Callable[[QWidget], None] = voidCallBack,
        select_directory_button_clicked: Callable[[QWidget], None] = voidCallBack,
        generate_letters_button_clicked: Callable[[QWidget], None] = voidCallBack,
        scholarship_combo_box_items: list[str] = [],
    ) -> None:
        """Creates a new instance of ScholarlyScholarshipTab

        Creates a new instance of ScholarlyScholarShipTab.

        Args:
            find_button_clicked (Callable[[QWidget], None], optional): The function to be called when button is clicked. Defaults to voidCallBack.
            select_template_button_clicked (Callable[[QWidget], None], optional): The function to be called when button is clicked. Defaults to voidCallBack.
            select_directory_button_clicked (Callable[[QWidget], None], optional): The function to be called when button is clicked. Defaults to voidCallBack.
            generate_letters_button_clicked (Callable[[QWidget], None], optional): The function to be called when button is clicked. Defaults to voidCallBack.
            scholarship_combo_box_items (list[str], optional): The items to be displayed in the combobox. Defaults to [].
        """
        super().__init__()

        self.setObjectName("scholarshipTab")

        # Main layout for widget
        main_layout: QVBoxLayout = QVBoxLayout()

        # Load items in comboxbox
        self.scholarship_combobox: QComboBox = QComboBox()
        self.scholarship_combobox.setObjectName("searchBox")
        self.scholarshipComboxBoxAddItems(scholarship_combo_box_items)

        # Set up auto complete
        self.scholarship_combobox.setEditable(True)

        # Create Search button
        self.search_button: QToolButton = QToolButton()
        self.search_button.setObjectName("searchButton")
        self.search_button.clicked.connect(find_button_clicked)

        # Create groupbox for scholarship combobox and search button
        select_scholarship_group_box: QGroupBox = QGroupBox()
        select_scholarship_group_box.setTitle("Select a Scholarship")
        select_scholarship_group_box.setToolTip("The name of the scholarship to filter applicants by.")
        select_scholarship_group_box.setObjectName("searchGroup")
        # select_scholarship_group_box.setFixedHeight(60)

        search_layout: QHBoxLayout = QHBoxLayout()
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.scholarship_combobox)

        select_scholarship_group_box.setLayout(search_layout)

        main_layout.addWidget(select_scholarship_group_box)

        # Fields and text boxes for generating letters
        letter_info_widget: QWidget = QWidget()
        letter_info_layout: QFormLayout = QFormLayout()
        letter_info_widget.setLayout(letter_info_layout)

        # Text boxes
        self.sender_name_textbox: QLineEdit = QLineEdit()
        self.sender_name_textbox.setToolTip("The name of the letter / email sender.")
        self.sender_title_textbox: QLineEdit = QLineEdit()
        self.sender_title_textbox.setToolTip("The title of the letter / email sender..")
        self.sender_email_textbox: QLineEdit = QLineEdit()
        self.sender_email_textbox.setToolTip(
            "The sender email to be shown in the letter, and used for sending the email."
        )
        self.amount_textbox: QLineEdit = QLineEdit()
        self.amount_textbox.setToolTip(
            "The financial award amount in USD, rounded to the nearest cent."
        )
        self.amount_textbox.setValidator(QDoubleValidator())
        self.template_path_textbox: QLineEdit = QLineEdit()
        self.template_path_textbox.setToolTip(
            "The path to the template letter used for generating the acceptance letters."
        )
        self.dest_dir_path_textbox: QLineEdit = QLineEdit()
        self.dest_dir_path_textbox.setToolTip(
            "The path to the destination folder for the generated acceptance letters."
        )
        self.academic_year_fall_textbox: QLineEdit = QLineEdit()
        self.academic_year_fall_textbox.setToolTip(
            "The academic year for the Fall semester."
        )
        self.academic_year_fall_textbox.setValidator(QIntValidator())
        self.academic_year_spring_textbox: QLineEdit = QLineEdit()
        self.academic_year_spring_textbox.setToolTip(
            "The academic year for the Spring semester."
        )
        self.academic_year_spring_textbox.setValidator(QIntValidator())

        # Select template letter button
        self.select_template_button: QToolButton = QToolButton()
        self.select_template_button.setIcon(
            ScholarlyIcon(
                Icons.FileOpenFill, size=IconSizes.Medium, color=QColor("blue")
            )
        )
        self.select_template_button.setIconSize(QSize(24, 24))
        self.select_template_button.setToolTip("Select template letter file.")
        self.select_template_button.clicked.connect(select_template_button_clicked)

        # Layout for selecting template letter button
        select_template_layout: QHBoxLayout = QHBoxLayout()
        select_template_layout.addWidget(self.select_template_button)
        select_template_layout.addWidget(self.template_path_textbox)

        # Select directory button
        self.select_directory_button: QToolButton = QToolButton()
        self.select_directory_button.setIcon(
            ScholarlyIcon(
                Icons.FolderOpenFill, size=IconSizes.Medium, color=QColor(204, 172, 0)
            ),
        )
        self.select_directory_button.setIconSize(QSize(24, 24))
        self.select_directory_button.setToolTip("Select the destination directory.")
        self.select_directory_button.clicked.connect(select_directory_button_clicked)

        # Add textboxes to form layout
        letter_info_layout.addRow("Sender Name", self.sender_name_textbox)
        letter_info_layout.addRow("Sender Title", self.sender_title_textbox)
        letter_info_layout.addRow("Sender Email", self.sender_email_textbox)
        letter_info_layout.addRow("Amount", self.amount_textbox)

        # Create layout for academic year
        academic_year_layout: QHBoxLayout = QHBoxLayout()
        academic_year_layout.addWidget(self.academic_year_fall_textbox)
        academic_year_layout.addWidget(QLabel("-"))
        academic_year_layout.addWidget(self.academic_year_spring_textbox)

        letter_info_layout.addRow("Academic Year", academic_year_layout)

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

        # Clear Selection button
        self.clear_selection_button: QToolButton = QToolButton()
        self.generate_letters_button.setText("Generate Letters")
        self.generate_letters_button.setToolTip(
            "Generates Scholarship Letter for selected students."
        )
        self.generate_letters_button.clicked.connect(generate_letters_button_clicked)

        self.setLayout(main_layout)

    def findButtonToggle(self, enabled: bool) -> None:
        """Toggles the find button

        Toggles the find button.

        Args:
            enabled (bool): If True, enables the button. If False, disabled it.
        """
        self.search_button.setEnabled(enabled)

    def scholarshipComboBoxToggle(self, enabled: bool) -> None:
        """Toggles the scholarship combobox

        Toggles the scholarship combobox.

        Args:
            enabled (bool): If True, enables the combobox. If False, disables it.
        """
        self.scholarship_combobox.setEnabled(enabled)

    def senderNameTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the sender name textbox

        Toggles the sender name textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.sender_name_textbox.setEnabled(enabled)

    def senderEmailTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the sender email textbox

        Toggles the sender email textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.sender_email_textbox.setEnabled(enabled)

    def senderTitleTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the sender title textbox

        Toggles the sender title textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.sender_title_textbox.setEnabled(enabled)

    def amountTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the amount textbox.

        Toggles the amount textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.amount_textbox.setEnabled(enabled)

    def academicYearFallTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the academic year fall textbox

        Toggles the academic year fall textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.academic_year_fall_textbox.setEnabled(enabled)

    def academicYearSpringTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the academic year spring textbox

        Toggles the academic year spring textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.academic_year_spring_textbox.setEnabled(enabled)

    def templateLetterPathTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the template letter path textbox

        Toggles the template letter path textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.template_path_textbox.setEnabled(enabled)

    def destDirPathTextBoxToggle(self, enabled: bool) -> None:
        """Toggles the dest dir path textbox

        Toggles the dest dir path textbox.

        Args:
            enabled (bool): If True, enables the textbox. If False, disables it.
        """
        self.dest_dir_path_textbox.setEnabled(enabled)

    def selectTemplateButtonToggle(self, enabled: bool) -> None:
        """Toggles the select template button

        Toggles the select template button.

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
        """
        self.select_template_button.setEnabled(enabled)

    def selectDirectoryButtonToggle(self, enabled: bool) -> None:
        """Toggles the select directory button

        Toggles the select directory button.

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
        """
        self.select_directory_button.setEnabled(enabled)

    def generateLettersButtonToggle(self, enabled: bool) -> None:
        """Toggles the generate letters button

        Toggles the generate letters button.

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
        """
        self.generate_letters_button.setEnabled(enabled)

    def toggleAll(self, enabled: bool) -> None:
        """Toggles all of the buttons and textboxes in the tab

        Toggles all of the buttons and textboxes in the tab.

        Args:
            enabled (bool): If True, enables all of the buttons and textboxes in the tab. If False, disables it all.
        """
        self.senderNameTextBoxToggle(enabled)
        self.scholarshipComboBoxToggle(enabled)
        self.senderEmailTextBoxToggle(enabled)
        self.senderTitleTextBoxToggle(enabled)
        self.amountTextBoxToggle(enabled)
        self.academicYearFallTextBoxToggle(enabled)
        self.academicYearSpringTextBoxToggle(enabled)
        self.templateLetterPathTextBoxToggle(enabled)
        self.selectTemplateButtonToggle(enabled)
        self.selectDirectoryButtonToggle(enabled)
        self.destDirPathTextBoxToggle(enabled)
        self.generateLettersButtonToggle(enabled)
        self.findButtonToggle(enabled)

    def scholarshipComboxBoxAddItems(self, items: list[str]) -> None:
        """Adds items to the scholarship combobox

        Adds items to the scholarship combobox.

        Args:
            items (list[str]): List of items to add to the combobox.
        """
        self.scholarship_combobox.addItems(items)

    def scholarshipComboBoxClear(self) -> None:
        """Clears the scholarship combobox.

        Clears the scholarship combobox. Removes all items.
        """
        self.scholarship_combobox.clear()

    def scholarshipComboBoxAddItem(self, item: str) -> None:
        """Adds an item to the scholarship combobox.

        Args:
            item (str): An item to add to the combobox.
        """
        self.scholarship_combobox.addItem(item)

    def setFindButtonClicked(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the clicked slot for the find button.

        Args:
            callback (Callable[[QWidget], None]): The function to be assigned to the click event.
        """
        self.search_button.clicked.connect(callback)

    def setSelectTemplateButtonClicked(
        self, callback: Callable[[QWidget], None]
    ) -> None:
        """Sets the clicked slot for the select template button.

        Args:
            callback (Callable[[QWidget], None]): The function to be assigned to the click event.
        """
        self.select_template_button.clicked.connect(callback)

    def setSelectDirectoryButtonClicked(
        self, callback: Callable[[QWidget], None]
    ) -> None:
        """Sets the clicked slot for the select directory button.

        Args:
            callback (Callable[[QWidget], None]): The function to be assigned to the click event.
        """
        self.select_directory_button.clicked.connect(callback)

    def getScholarshipComboBoxCurrentText(self) -> str:
        """Returns the current text in the scholarship combobox.

        Returns:
            str: The current item in the combobox.
        """
        return self.scholarship_combobox.currentText()

    def getSenderNameTexBoxText(self) -> str:
        """Returns the text in the sender name textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.sender_name_textbox.text()

    def getSenderTitleTextBoxText(self) -> str:
        """Returns the text in the sender title textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.sender_title_textbox.text()

    def getSenderEmailTextBoxText(self) -> str:
        """Returns the text in the sender email textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.sender_email_textbox.text()

    def getAmountTextBoxText(self) -> str:
        """Returns the text in the amount textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.amount_textbox.text()

    def getAcademicYearFallTextBoxText(self) -> str:
        """Returns the text from the academic year fall textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.academic_year_fall_textbox.text()

    def getAcademicYearSpringTextBoxText(self) -> str:
        """Returns the text from the academic year spring textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.academic_year_spring_textbox.text()

    def getTemplateLetterPathTextBoxText(self) -> str:
        """Returns the text from the template letter path textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.template_path_textbox.text()

    def getDestDirPathTextBoxText(self) -> str:
        """Returns the text from the dest dir path textbox.

        Returns:
            str: The text from the textbox.
        """
        return self.dest_dir_path_textbox.text()

    def setTemplateLetterPathTextBoxText(self, file_path: str) -> None:
        """Sets the text in the template letter path textbox.

        Args:
            file_path (str): File path to show in textbox.
        """
        self.template_path_textbox.setText(file_path)

    def setDestDirPathTextBoxText(self, dir_path: str) -> None:
        """Sets the text in the dest dir path textbox.

        Args:
            dir_path (str): Directory path to show in textbox.
        """
        self.dest_dir_path_textbox.setText(dir_path)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    with open("style.qss", "r") as styleFile:
        a.setStyleSheet(styleFile.read())
    s = ScholarlyScholarshipTab()
    s.toggleAll(True)
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
