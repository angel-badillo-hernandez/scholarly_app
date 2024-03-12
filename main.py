"""Main Program for creating the Scholarly App GUI

This file contains the `ScholarlyMainWindow` class, which is the
contains methods for creating the application's GUI.

"""

import sys
import webbrowser
import os
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtGui import (
    QAction,
    QCloseEvent,
    QIcon,
    QPalette,
    QColor,
    QIntValidator,
    QDoubleValidator,
    QFont,
)
from PyQt6.QtCore import QEvent, Qt, QSize, QModelIndex, pyqtSlot
from student_table_model import StudentTableModel
from student_record import StudentRecord
from student_data_reader import StudentDataReader
from student_data_writer import StudentDataWriter
from scholarly_database import ScholarlyDatabase, StudentRecord
from letter_writer import LetterVariables, LetterWriter


class ScholarlyMainWindow(QMainWindow):
    """Class for implementing the GUI for the Scholarly app.

    Class for implementing the GUI for the Scholarly application.
    """

    def __init__(self):
        """Creates an instance of ScholarlyMainWindow.

        Creates an instance of ScholarlyMainWindow, the GUI for the application.
        """
        super().__init__()
        self.student_table: StudentTableModel = None
        self.student_table_view: QTableView = None
        self.database: ScholarlyDatabase = ScholarlyDatabase("student_database.sqlite")

        self.initialize_ui()

    def initialize_ui(self):
        """Initializes GUI components on the GUI.

        Initializes the GUI components of the GUI for the application.
        """
        # Set window properties
        self.setWindowTitle("Scholarly")
        self.setWindowIcon(QIcon("assets/scholarly.ico"))
        self.setGeometry(200, 200, 500, 500)

        # Initalize menu bar
        self.initialize_menubar()

        # Initilize table
        self.initialize_central_widget()

    def initialize_central_widget(self):
        """Initializes the central widget for the main window.

        Initializes the central widget for the main window of
        the application.
        """
        central_widget: QWidget = QWidget()
        horizontal_layout: QHBoxLayout = QHBoxLayout()

        # Set central widget background color to maroon
        # central_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # central_widget.setStyleSheet("background-color: maroon;")

        # Create model and table view widget
        self.student_table = StudentTableModel()
        self.student_table_view: QTableView = QTableView()

        # Set table view background color to white
        # self.student_table_view.setAttribute(
        #     Qt.WidgetAttribute.WA_StyledBackground, True
        # )
        # self.student_table_view.setStyleSheet("background-color: white;")

        # Enable selecting multiple rows
        self.student_table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.student_table_view.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )

        # Add table view to central widget
        self.student_table_view.setModel(self.student_table)
        horizontal_layout.addWidget(self.student_table_view)

        # Select Scholarship Groupbox
        scholarship_groupbox: QGroupBox = QGroupBox("Select Scholarship")
        scholarship_layout: QVBoxLayout = QVBoxLayout()
        scholarship_groupbox.setLayout(scholarship_layout)

        # TODO: Make the items displayed and retrieved dynamically
        self.select_scholarship: QComboBox = QComboBox()
        self.select_scholarship.addItem("S1")
        self.select_scholarship.addItem("S2")
        scholarship_layout.addWidget(self.select_scholarship)

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
        self.letter_path_textbox: QLineEdit = QLineEdit()
        self.academic_year_textbox: QLineEdit = QLineEdit()

        # Select directory button
        select_directory_button: QToolButton = QToolButton()
        select_directory_button.setText("...")
        select_directory_button.setToolTip("Select the destination directory.")
        select_directory_button.clicked.connect(self.select_directory_slot)

        # Add textboxes to form layout
        letter_info_layout.addRow("Sender Name", self.sender_name_textbox)
        letter_info_layout.addRow("Sender Title", self.sender_title_textbox)
        letter_info_layout.addRow("Sender Email", self.sender_email_textbox)
        letter_info_layout.addRow("Amount", self.award_amount_textbox)
        letter_info_layout.addRow("Academic Year", self.academic_year_textbox)

        #
        select_dir_layout: QHBoxLayout = QHBoxLayout()
        select_dir_layout.addWidget(select_directory_button)
        select_dir_layout.addWidget(self.letter_path_textbox)

        letter_info_layout.addRow("Directory Path", select_dir_layout)
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

        # Add scholarship groupbox to horizontal layout
        horizontal_layout.addWidget(scholarship_groupbox)

        # Add layout to central widget, and add central widget to main window
        central_widget.setLayout(horizontal_layout)
        self.setCentralWidget(central_widget)

    def initialize_menubar(self):
        """Initializes the menu bar for the main window.

        Initializes the menu bar for the main window of the appllication.
        """
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        """Creates a QMenuBar on the main window

        Creates and displays a menu bar with "File" menu.
        File menu has "Open" action.
        """
        menu_bar: QMenuBar = self.menuBar()

        # File Menu Tab
        file_menu: QMenu = menu_bar.addMenu("&File")

        # Open Action
        open_action: QAction = QAction("Open File", self)
        open_action.triggered.connect(self.open_file_slot)
        open_action.setShortcut("ctrl+o")
        file_menu.addAction(open_action)

        # Save Action
        save_action: QAction = QAction("Save File", self)
        save_action.triggered.connect(self.save_file_slot)
        save_action.setShortcut("ctrl+s")
        file_menu.addAction(save_action)

        # Close Action
        close_action: QAction = QAction("Close File", self)
        close_action.triggered.connect(self.close_file_slot)
        close_action.setShortcut("ctrl+f4")
        file_menu.addAction(close_action)

        # Exit Action
        close_action: QAction = QAction("Exit", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        # About Menu Tab
        about_action: QAction = QAction("&About", self)
        about_action.triggered.connect(self.about_slot)
        menu_bar.addAction(about_action)

        # Help Menu Tab
        help_action: QAction = QAction("&Help", self)
        help_action.triggered.connect(self.help_event)
        menu_bar.addAction(help_action)

        file_menu.show()

    # @pyqtSlot()
    def open_file_slot(self) -> None:
        """Slot (event handler) for "Open" action.

        Function called when "Open" action is activated. Shows
        a file dialog for opening a file, then reads the data
        from the file into the database and the table.
        """
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        # Current user's Documents Directory
        user_documents_path: str = f"{os.path.expanduser('~')}/Documents"

        # Open file dialog, and gets the selected file path
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open File",
            directory=user_documents_path,
            filter="CSV (*.csv)",
        )

        # If no file is specified, do nothing
        if not file_path:
            return

        try:
            # Insert data from file to database
            self.database.student_csv_to_table(file_path)
        # If invalid data file, show error message
        except Exception as e:
            QMessageBox.critical(
                self,
                "Invalid File",
                f"The file is not a CSV file, or is malformed.\n{type(e).__name__}: {e}",
            )

        # Retrieve data from the database
        student_data = self.database.select_all_students()

        # Store data into table
        self.student_table = StudentTableModel(student_data)
        self.student_table_view.setModel(self.student_table)

    def save_file_slot(self) -> None:
        """Slot (event handler) for "Save" action.

        Function called when "Save" action is activated. Shows
        a file dialog for saving a file, then stores the data from the table
        into the selected CSV file.
        """
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        # Current user's Documents Directory
        user_documents_path: str = f"{os.path.expanduser('~')}/Documents"

        # Open file dialog, and gets the selected file path
        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Open File",
            directory=user_documents_path,
            filter="CSV (*.csv)",
        )

        # If no file is specified, do nothing
        if not file_path:
            return

        # Retrieve data from table
        student_data: list[StudentRecord] = self.student_table.get_all_data()

        writer: StudentDataWriter = StudentDataWriter(file_path)
        writer.write_values(student_data)

    def close_file_slot(self) -> None:
        self.database.drop_table(ScholarlyDatabase.students_table_name())
        self.student_table = StudentTableModel()
        self.student_table_view.setModel(self.student_table)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Event handler for closing the application.

        Event handler triggered when the application is closed.
        Shows a message box asking the user if they are sure they want to close
        the application.
        """
        reponse: QMessageBox.StandardButton = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to close the program? Any unsaved data will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reponse == QMessageBox.StandardButton.Yes:
            self.close_file_slot()
            event.accept()
        else:
            event.ignore()

    def about_slot(self) -> None:
        """Slot (event handler) for "About" action.

        Function called when "About" action is activated.
        Opens the default web browser on the device and opens
        a tab to the link for the about information.
        """
        # TODO: Add functionality for About menu
        webbrowser.open(
            "https://github.com/It-Is-Legend27/scholarly_app/blob/main/README.md"
        )

    def help_event(self) -> None:
        """Slot (event handler) for "Help" action.

        Function called when "Help" action is activated.
        Opens the default web browser on the device and opens
        a tab to the link for the manual for the application.
        """
        # TODO: Add functionality for Help menu
        webbrowser.open(
            "https://github.com/It-Is-Legend27/scholarly_app/blob/main/README.md"
        )

    def generate_letters(self):
        student_data: list[StudentRecord] = self.get_selected_rows()
        
        curr_time:datetime = datetime.now()
        date:str = f"{curr_time.strftime("%B")} {curr_time.day}, {curr_time.year}"

        scholarship_name:str = self.select_scholarship.currentText()
        sender_name:str = self.sender_name_textbox.text()
        sender_title:str = self.sender_title_textbox.text()
        sender_email:str = self.sender_email_textbox.text()
        amount:str = self.award_amount_textbox.text()
        academic_year:str = self.academic_year_textbox.text()
        dir_path:str = self.letter_path_textbox.text()

        for student in student_data:

            student_first_name, student_last_name = student.name.strip(" ").split(",")

            student_name:str = f"{student_first_name}{student_last_name}"
            letter_vars:LetterVariables = LetterVariables(student_name, date, amount, scholarship_name, academic_year, sender_name, sender_email, sender_title)
            letter_writer:LetterWriter = LetterWriter("template_letter.docx", f"{dir_path}/{student_name}.docx", letter_vars.to_dict())
            letter_writer.writer_letter()
        
        os.startfile(dir_path)
            

    def get_selected_rows(self):
        indices: list[QModelIndex] = (
            self.student_table_view.selectionModel().selectedRows()
        )

        data: list[StudentRecord] = []

        for index in indices:
            data.append(self.student_table.get_row(index.row()))

        return data

    def select_directory_slot(self):
        user_documents_path: str = f"{os.path.expanduser('~')}/Documents"

        # Open file dialog, and gets the selected file path
        dir_path: str = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            directory=user_documents_path,
            options=QFileDialog.Option.ShowDirsOnly,
        )
        # If no file is specified, do nothing
        if not dir_path:
            return

        # Change textbox text to directory path
        self.letter_path_textbox.setText(dir_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window: ScholarlyMainWindow = ScholarlyMainWindow()

    # Displays the main window for the application
    window.show()

    # Run application
    sys.exit(app.exec())
