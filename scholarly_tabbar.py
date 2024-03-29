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
    QComboBox
)
from PyQt6.QtGui import QAction


class ScholarlyTabWidget(QTabWidget):
    def __init__(self) -> None:
        super().__init__()

        # Select Scholarship Groupbox
        scholarship_groupbox: QGroupBox = QGroupBox("Select Scholarship")
        scholarship_layout: QVBoxLayout = QVBoxLayout()
        scholarship_groupbox.setLayout(scholarship_layout)

        # Load items in comboxbox
        self.scholarship_combobox: QComboBox = QComboBox()
        self.load_scholarship_combobox()

        self.scholarship_combobox.currentTextChanged.connect(self.scholarship_changed)
        # Keep disabled until file is opened
        self.scholarship_combobox.setDisabled(True)
        scholarship_layout.addWidget(self.scholarship_combobox)

        # Fields and text boxes for generating letters
        letter_info_widget: QWidget = QWidget()
        letter_info_layout: QFormLayout = QFormLayout()
        letter_info_widget.setLayout(letter_info_layout)

        # Text boxes
        self.sender_name_textbox: QLineEdit = QLineEdit()
        self.sender_title_textbox: QLineEdit = QLineEdit()
        self.sender_email_textbox: QLineEdit = QLineEdit()
        self.award_amount_textbox: QLineEdit = QLineEdit()
        self.award_amount_textbox.setValidator(QDoubleValidator())
        self.template_path_textbox:QLineEdit = QLineEdit()
        self.dest_dir_path_textbox: QLineEdit = QLineEdit()
        self.academic_year_textbox: QLineEdit = QLineEdit()

        # Select template letter button
        self.select_template_button: QToolButton = QToolButton()
        self.select_template_button.setText("Browse")
        self.select_template_button.setToolTip("Select template letter file.")
        self.select_template_button.clicked.connect(self.select_template)

        # Layout for selecting template letter button
        select_template_layout: QHBoxLayout = QHBoxLayout()
        select_template_layout.addWidget(self.select_template_button)
        select_template_layout.addWidget(self.template_path_textbox)

        # Select directory button
        self.select_directory_button: QToolButton = QToolButton()
        self.select_directory_button.setText("Browse")
        self.select_directory_button.setToolTip("Select the destination directory.")
        self.select_directory_button.clicked.connect(self.select_directory)

        # Add textboxes to form layout
        letter_info_layout.addRow("Sender Name", self.sender_name_textbox)
        letter_info_layout.addRow("Sender Title", self.sender_title_textbox)
        letter_info_layout.addRow("Sender Email", self.sender_email_textbox)
        letter_info_layout.addRow("Amount", self.award_amount_textbox)
        letter_info_layout.addRow("Academic Year", self.academic_year_textbox)

        # Layout for selecting destination directory
        select_dir_layout: QHBoxLayout = QHBoxLayout()
        select_dir_layout.addWidget(self.select_directory_button)
        select_dir_layout.addWidget(self.dest_dir_path_textbox)

        # Add template letter layout to letter info layout
        letter_info_layout.addRow("Template Letter", select_template_layout)

        # Add layout to letter info layout
        letter_info_layout.addRow("Destination Directory", select_dir_layout)
        scholarship_layout.addWidget(letter_info_widget)

        # Generate Letters button
        generate_letters: QToolButton = QToolButton()
        generate_letters.setText("Generate Letters")
        generate_letters.setToolTip(
            "Generates Scholarship Letter for selected students."
        )
        generate_letters.clicked.connect(self.generate_letters)

        # Add widget to scholarship components layout
        scholarship_layout.addWidget(generate_letters)


if __name__ == "__main__":
    