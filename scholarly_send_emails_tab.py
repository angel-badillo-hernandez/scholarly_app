from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QFormLayout,
    QLayout,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
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
from PyQt6.QtCore import QSize, Qt, pyqtSlot
from scholarly_icons import ScholarlyIcon, Icons, IconSizes
from typing import Callable
import os


# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: None


class ScholarlySendEmailsTab(QWidget):
    """Widget class for Scholarship Tab

    A class that is for the GUI component, Scholarship tab.
    """

    def __init__(
        self,
        parent: QWidget = None,
        find_button_clicked: Callable[[QWidget], None] = voidCallBack,
        select_template_button_clicked: Callable[[QWidget], None] = voidCallBack,
        email_button_clicked: Callable[[QWidget], None] = voidCallBack,
        clear_selection_button_clicked: Callable[[QWidget], None] = voidCallBack,
        scholarship_combo_box_items: list[str] = [],
    ) -> None:
        """Creates a new instance of ScholarlyScholarshipTab

        Creates a new instance of ScholarlyScholarShipTab.

        Args:
            find_button_clicked (Callable[[QWidget], None], optional): The function to be called when button is clicked. Defaults to voidCallBack.
            select_template_button_clicked (Callable[[QWidget], None], optional): The function to be called when button is clicked. Defaults to voidCallBack.
            clear_selection_button_clicked (Callable[[QWidget], None], optional): The function to be called when button is clicked. Defaults to voidCallBack.
            scholarship_combo_box_items (list[str], optional): The items to be displayed in the combobox. Defaults to [].
        """
        super().__init__()

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
        self.search_button.setIcon(ScholarlyIcon(Icons.Search, size=IconSizes.Medium))
        self.search_button.setIconSize(QSize(24, 24))
        self.search_button.clicked.connect(find_button_clicked)

        # Create groupbox for scholarship combobox and search button
        select_scholarship_group_box: QGroupBox = QGroupBox()
        select_scholarship_group_box.setTitle("Select a Scholarship")
        select_scholarship_group_box.setToolTip(
            "The name of the scholarship to filter applicants by."
        )
        select_scholarship_group_box.setObjectName("searchGroup")
        # select_scholarship_group_box.setFixedHeight(60)

        search_layout: QHBoxLayout = QHBoxLayout()
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.scholarship_combobox)

        select_scholarship_group_box.setLayout(search_layout)

        main_layout.addWidget(select_scholarship_group_box)

        # Fields and text boxes for generating letters
        letter_info_widget: QWidget = QWidget()
        form_layout: QFormLayout = QFormLayout()
        letter_info_widget.setLayout(form_layout)

        # Text boxes
        self.sender_name_textbox: QLineEdit = QLineEdit()
        self.sender_name_textbox.setToolTip("The name of the letter / email sender.")
        self.sender_title_textbox: QLineEdit = QLineEdit()
        self.sender_title_textbox.setToolTip("The title of the letter / email sender..")
        self.amount_textbox: QLineEdit = QLineEdit()
        self.amount_textbox.setToolTip(
            "The financial award amount in USD, rounded to the nearest cent."
        )
        self.amount_textbox.setValidator(QDoubleValidator())
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
        self.template_path_textbox: QLineEdit = QLineEdit()
        self.template_path_textbox.setToolTip(
            "The path to the template letter used for generating the acceptance letters."
        )
        self.email_subject_textbox:QLineEdit = QLineEdit()
        self.email_subject_textbox.setToolTip("Subject line of the email.")
        self.email_body_textbox:QTextEdit = QTextEdit()
        self.email_body_textbox.setToolTip("Body of the email.")

        # Select template letter button
        self.select_template_button: QToolButton = QToolButton()
        self.select_template_button.setObjectName("selectTemplateButton")
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

        # Add textboxes to form layout
        form_layout.addRow("Sender Name", self.sender_name_textbox)
        form_layout.addRow("Sender Title", self.sender_title_textbox)
        form_layout.addRow("Amount", self.amount_textbox)

        # Create layout for academic year
        academic_year_layout: QHBoxLayout = QHBoxLayout()
        academic_year_layout.addWidget(self.academic_year_fall_textbox)
        academic_year_layout.addWidget(QLabel("-"))
        academic_year_layout.addWidget(self.academic_year_spring_textbox)

        form_layout.addRow("Academic Year", academic_year_layout)

        # Add template letter layout to letter info layout
        form_layout.addRow("Template Letter", select_template_layout)

        # Add subject textbox to letter info layout
        form_layout.addRow("Email Subject Line", self.email_subject_textbox)

        # add email body textbox to letter info layout
        form_layout.addRow("Email Body", self.email_body_textbox)

        main_layout.addWidget(letter_info_widget)

        # Layout for bottom-most buttons
        bottom_buttons_widget: QWidget = QWidget()
        bottom_buttons_layout: QHBoxLayout = QHBoxLayout()

        # Clear Selection button
        self.clear_selection_button: QToolButton = QToolButton()
        self.clear_selection_button.setText("Clear Selection")
        self.clear_selection_button.setToolTip(
            "Clears the current selection on the table."
        )
        self.clear_selection_button.clicked.connect(clear_selection_button_clicked)

        # Clear email body button
        self.clear_email_body_button:QToolButton = QToolButton()
        self.clear_email_body_button.setText("Clear Email Body")
        self.clear_email_body_button.setToolTip("Clears the email body textbox.")
        self.clear_email_body_button.clicked.connect(self.emailBodyTextBoxClear)

        # Email Recipients Button
        self.email_button: QToolButton = QToolButton()
        self.email_button.setText("Email Recipients")
        self.email_button.setToolTip("Emails the selected recipients.")
        self.email_button.clicked.connect(email_button_clicked)

        # Add widget to scholarship components layout
        bottom_buttons_layout.addWidget(self.clear_selection_button)
        bottom_buttons_layout.addWidget(self.email_button)
        bottom_buttons_layout.addWidget(self.clear_email_body_button)

        bottom_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        bottom_buttons_widget.setLayout(bottom_buttons_layout)

        main_layout.addWidget(bottom_buttons_widget)

        # Set entire main layout for widget
        self.setLayout(main_layout)

    def emailSubjectTextBoxToggle(self, enabled:bool)-> None:
        """Toggles the email subject textbox.

        Args:
            enabled (bool): If True, enables the line edit. If False, disables it.
        """
        self.email_subject_textbox.setEnabled(enabled)

    def emailBodyTextBoxToggle(self, enabled:bool)-> None:
        """Toggles the email body textbox.

        Args:
            enabled (bool): If True, enables the text edit. If False, disables it.
        """
        self.email_body_textbox.setEnabled(enabled)

    def clearEmailBodyButtonToggle(self, enabled:bool)-> None:
        """Toggles the clear email body button.

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
        """
        self.clear_email_body_button.setEnabled(enabled)

    def emailButtonToggle(self, enabled: bool) -> None:
        """Toggles the Email Button

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
        """
        self.email_button.setEnabled(enabled)

    def clearSelectionButtonToggle(self, enabled: bool) -> None:
        """Toggles the clear selection button.

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
        """
        self.clear_selection_button.setEnabled(enabled)

    def findButtonToggle(self, enabled: bool) -> None:
        """Toggles the find button

        Toggles the find button.

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
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

    def selectTemplateButtonToggle(self, enabled: bool) -> None:
        """Toggles the select template button

        Toggles the select template button.

        Args:
            enabled (bool): If True, enables the button. If False, disables it.
        """
        self.select_template_button.setEnabled(enabled)

    def toggleAll(self, enabled: bool) -> None:
        """Toggles all of the buttons and textboxes in the tab

        Toggles all of the buttons and textboxes in the tab.

        Args:
            enabled (bool): If True, enables all of the buttons and textboxes in the tab. If False, disables it all.
        """
        self.senderNameTextBoxToggle(enabled)
        self.scholarshipComboBoxToggle(enabled)
        self.senderTitleTextBoxToggle(enabled)
        self.amountTextBoxToggle(enabled)
        self.academicYearFallTextBoxToggle(enabled)
        self.academicYearSpringTextBoxToggle(enabled)
        self.templateLetterPathTextBoxToggle(enabled)
        self.selectTemplateButtonToggle(enabled)
        self.findButtonToggle(enabled)
        self.clearSelectionButtonToggle(enabled)
        self.emailButtonToggle(enabled)
        self.emailSubjectTextBoxToggle(enabled)
        self.emailBodyTextBoxToggle(enabled)
        self.clearEmailBodyButtonToggle(enabled)

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

    def setEmailButtonClicked(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the clicked slot for the Email button.

        Args:
            callback (Callable[[QWidget], None]): The function to be assigned to the click event.
        """
        self.email_button.clicked.connect(callback)

    def setClearSelectionButtonClicked(
        self, callback: Callable[[QWidget], None]
    ) -> None:
        """Sets the clicked slot for the clear selection button.

        Args:
            callback (Callable[[QWidget], None]): The function to be assigned to the click event.
        """
        self.clear_selection_button.clicked.connect(callback)

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

    def setTemplateLetterPathTextBoxText(self, file_path: str) -> None:
        """Sets the text in the template letter path textbox.

        Args:
            file_path (str): File path to show in textbox.
        """
        self.template_path_textbox.setText(file_path)

    def getEmailSubjectTextBoxText(self)-> str:
        """Returns the text from the email subject textbox.

        Returns:
            str: Text from the textbox.
        """
        return self.email_subject_textbox.text()

    def getEmailBodyTextBoxText(self)-> str:
        """Returns the rich text from the email body textbox as HTML.

        Returns:
            str: Rich text from the textbox as HTML.
        """
        return self.email_body_textbox.toHtml()

    @pyqtSlot()
    def emailBodyTextBoxClear(self)-> None:
        """Clears the email body textbox.
        """
        self.email_body_textbox.clear()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    with open("style.qss", "r") as styleFile:
        a.setStyleSheet(styleFile.read())
    s = ScholarlySendEmailsTab()
    s.toggleAll(False)
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
