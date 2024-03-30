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
    QPixmap,
)
from PyQt6.QtCore import QEvent, Qt, QSize, QModelIndex, pyqtSlot
from student_table_model import StudentTableModel
from student_record import StudentRecord, read, write
from award_criteria_record import AwardCriteriaRecord
from scholarly_database import ScholarlyDatabase
from letter_writer import LetterVariables, LetterWriter
from scholarly_menu_bar import ScholarlyMenuBar
from scholarly_tab_bar import ScholarlyTabBar
from scholarly_scholarship_tab import ScholarlyScholarshipTab

# Absolute address for file to prevent issues with
# relative addresses when building app with PyInstaller
BASE_DIR:str = os.path.dirname(__file__)

class ScholarlyMainWindow(QMainWindow):
    """Class for implementing the GUI for the Scholarly app.

    Class for implementing the GUI for the Scholarly application.
    """

    def __init__(self):
        """Creates an instance of ScholarlyMainWindow.

        Creates an instance of ScholarlyMainWindow, the GUI for the application.
        """
        super().__init__()
        self.menu_bar:ScholarlyMainWindow = None
        self.student_table: StudentTableModel = None
        self.student_table_view: QTableView = None
        self.database: ScholarlyDatabase = ScholarlyDatabase(os.path.join(BASE_DIR, "database/scholarly.sqlite"))
        self.scholarship_tab:ScholarlyScholarshipTab = None
        self.tab_bar:ScholarlyTabBar = None

        self.initialize_ui()

    def initialize_ui(self):
        """Initializes GUI components on the GUI.

        Initializes the GUI components of the GUI for the application.
        """
        # Set window properties
        self.setWindowTitle("Scholarly")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "assets/icons/scholarly.ico")))
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
        central_widget_layout: QHBoxLayout = QHBoxLayout()

        # Create model and table view widget
        self.student_table = StudentTableModel()
        self.student_table_view: QTableView = QTableView()

        # Enable selecting multiple rows
        self.student_table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.student_table_view.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )

        # Add table view to central widget
        self.student_table_view.setModel(self.student_table)
        central_widget_layout.addWidget(self.student_table_view)
        
        self.scholarship_tab = ScholarlyScholarshipTab(
            find_button_clicked= self.find,
            select_directory_button_clicked=self.select_directory,
            select_template_button_clicked=self.select_template,
            generate_letters_button_clicked=self.generate_letters
            )
        self.load_combobox()
        self.scholarship_tab.toggleAll(False)

        self.tab_bar = ScholarlyTabBar(self.scholarship_tab, QWidget(), QWidget())
        central_widget_layout.addWidget(self.tab_bar)

        # Add layout to central widget, and add central widget to main window
        central_widget.setLayout(central_widget_layout)
        self.setCentralWidget(central_widget)

    def initialize_menubar(self):
        """Initializes the menu bar for the main window.

        Initializes the menu bar for the main window of the appllication.
        """
        self.menu_bar: ScholarlyMenuBar = ScholarlyMenuBar(self.open_file, self.save_file, self.close_file, self.about, self.help, self.close)
        self.setMenuBar(self.menu_bar)

    @pyqtSlot()
    def open_file(self) -> None:
        """Slot (event handler) for "Open" action.

        Function called when "Open" action is activated. Shows
        a file dialog for opening a file, then reads the data
        from the file into the database and the table.
        """
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        # Current user's Documents Directory
        user_documents_path: str = os.path.join(os.path.expanduser("~"), "Documents")

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

        # Enable scholarship combobox
        self.scholarship_tab.toggleAll(True)

    @pyqtSlot()
    def save_file(self) -> None:
        """Slot (event handler) for "Save" action.

        Function called when "Save" action is activated. Shows
        a file dialog for saving a file, then stores the data from the table
        into the selected CSV file.
        """
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        # Current user's Documents Directory
        user_documents_path: str = os.path.join(os.path.expanduser("~"), "Documents")

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

        # Write to CSV file
        write(file_path, student_data)

    @pyqtSlot()
    def close_file(self) -> None:
        """Slot (event handler) for close action.

        Function that is called when "Close" action is activated. Clears the database
        and clears the table.
        """
        self.scholarship_tab.toggleAll(False)
        self.scholarship_tab.scholarship_combobox.setCurrentText("")
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
            self.close_file()
            event.accept()
        else:
            event.ignore()

    @pyqtSlot()
    def about(self) -> None:
        """Slot (event handler) for "About" action.

        Function called when "About" action is activated.
        Opens the default web browser on the device and opens
        a tab to the link for the about information.
        """
        # TODO: Add functionality for About menu
        webbrowser.open(
            "https://github.com/It-Is-Legend27/scholarly_app/blob/main/README.md"
        )

    @pyqtSlot()
    def help(self) -> None:
        """Slot (event handler) for "Help" action.

        Function called when "Help" action is activated.
        Opens the default web browser on the device and opens
        a tab to the link for the manual for the application.
        """
        # TODO: Add functionality for Help menu
        webbrowser.open(
            "https://github.com/It-Is-Legend27/scholarly_app/blob/main/README.md"
        )

    @pyqtSlot()
    def generate_letters(self):
        """Slot (event handler) for "generate letters" button.

        Function that is called when "generate letters" button is pressed. Generates
        the letters based on the selections in the table.
        """
        student_data: list[StudentRecord] = self.get_selected_rows()
        
        # If no selection has been made, show warning message
        if not student_data:
            QMessageBox.warning(self, "No Selection", "No selection has been made. Make a selection on the table.")
            return

        curr_time:datetime = datetime.now()
        date:str = f"{curr_time.strftime("%B")} {curr_time.day}, {curr_time.year}"

        scholarship_name:str = self.scholarship_tab.getScholarshipComboBoxCurrentText()
        sender_name:str = self.scholarship_tab.getSenderNameTexBoxText()
        sender_title:str = self.scholarship_tab.getSenderTitleTextBoxText()
        sender_email:str = self.scholarship_tab.getSenderEmailTextBoxText()
        amount:str = self.scholarship_tab.getAmountTextBoxText()
        academic_year_fall:str = self.scholarship_tab.getAcademicYearFallTextBoxText()
        academic_year_spring:str = self.scholarship_tab.getAcademicYearSpringTextBoxText()
        template_path:str = self.scholarship_tab.getTemplateLetterPathTextBoxText()
        dir_path:str = self.scholarship_tab.getDestDirPathTextBoxText()

        # Ensure text boxes are not empty, if so, show warning
        if not sender_name:
            QMessageBox.warning(self, "Enter Sender Name", "Sender name is empty. Please enter the sender name.")
            return
        elif not sender_title:
            QMessageBox.warning(self, "Enter Sender Title", "Sender name is empty. Please enter the sender title.")
            return
        elif not sender_email:
            QMessageBox.warning(self, "Enter Sender Email", "Sender email is empty. Please enter the sender email.")
            return
        elif not amount:
            QMessageBox.warning(self, "Enter Amount", "The amount is empty. Please enter the amount.")
            return
        elif not academic_year_fall:
            QMessageBox.warning(self, "Enter Academic Year", "The academic year is empty. Please enter the academic year.")
            return
        elif not dir_path:
            QMessageBox.warning(self, "Enter Destination Directory", "Destination directory is empty. Please enter the destination directory.")
            return
        elif not scholarship_name:
            QMessageBox.warning(self, "Select a Scholarship", "A scholarship has not been selected. Please select a scholarship.")
            return

        for student in student_data:
            student_name:str = None

            try:
                student_last_name, student_first_name = student.name.replace(" ", "").split(",")

                student_name = f"{student_first_name} {student_last_name}"
            except ValueError as e:
                QMessageBox.critical(self, "Invalid Arguments", f"Invalid student name: '{student.name}'.\nMust be in the format 'last_name, first_name'.\n{type(e).__name__}: {e}")
                return
            
            letter_vars:LetterVariables = LetterVariables(student_name, date, amount, scholarship_name, academic_year_fall, academic_year_spring, sender_name, sender_email, sender_title)
            
            letter_writer:LetterWriter = LetterWriter(template_path, f"{dir_path}/{student_name}.docx", letter_vars)
            
            try:
                letter_writer.writer_letter()
            except Exception as e:
                QMessageBox.critical(self, "Invalid File Paths", f"Invalid template letter file path or destination directory path'.\n{type(e).__name__}: {e}")
                return
        
        # Open File Explorer to show letters
        reponse: QMessageBox.StandardButton = QMessageBox.question(
            self,
            "Open File Explorer",
            "The scholarship acceptance letters were successfully created.\nWould you like to view them in File Explorer?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reponse == QMessageBox.StandardButton.Yes:
            os.startfile(dir_path)
            
    def get_selected_rows(self)-> list[StudentRecord]:
        """Returns the student data from the selection.

        Returns the student data from the selected rows.

        Returns:
            A list of StudentRecord.
        """
        indices: list[QModelIndex] = (
            self.student_table_view.selectionModel().selectedRows()
        )

        data: list[StudentRecord] = []

        for index in indices:
            data.append(self.student_table.get_row(index.row()))

        return data

    @pyqtSlot()
    def select_directory(self):
        """Slot (event handler) for choosing destination directory.

        Function called when "Browse" button on the "Destination Directory" field
        section is pressed. Opens file dialog for selecting a directory.
        """
        user_documents_path: str = os.path.join(os.path.expanduser("~"), "Documents")

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
        self.scholarship_tab.setDestDirPathTextBoxText(dir_path)

    @pyqtSlot()
    def select_template(self):
        """Slot (event handler) for choosing template letter file.

        Function called when "Browse" button on the "Template Letter" field
        section is pressed. Opens file dialog for selecting a docx file.
        """
        templates_path: str = os.path.join(BASE_DIR, "assets/templates")

        # Open file dialog, and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select Template Letter",
            directory=templates_path,
            filter="Word Documents (*.docx)",
        )

        # If no file is specified, do nothing
        if not file_path:
            return

        # Change textbox text to directory path
        self.scholarship_tab.setTemplateLetterPathTextBoxText(file_path)

    @pyqtSlot()
    def find(self):
        """Called when selection is changed in scholarship_combobox

        Called when selection is changed in scholarship_combobox
        """
        scholarship_name:str = self.scholarship_tab.getScholarshipComboBoxCurrentText()
    
        if scholarship_name == "":
            # Clear selection
            self.student_table_view.clearSelection()
            
            # Reset table to have entire contents of database
            student_data:list[StudentRecord] = self.database.select_all_students()
            self.student_table = StudentTableModel(student_data)
            self.student_table_view.setModel(self.student_table)
        else:
            self.student_table_view.clearSelection()
            award_criteria_record:AwardCriteriaRecord = self.database.select_award_criteria(scholarship_name)
            student_data:list[StudentRecord] = self.database.select_students_by_criteria(award_criteria_record)
            self.student_table = StudentTableModel(student_data)
            self.student_table_view.setModel(self.student_table)

    @pyqtSlot()
    def scholarship_changed(self):
        """Called when selection is changed in scholarship_combobox

        Called when selection is changed in scholarship_combobox
        """
        scholarship_name:str = self.scholarship_combobox.currentText()

        if scholarship_name == "":
            # Clear selection
            self.student_table_view.clearSelection()
            
            # Reset table to have entire contents of database
            student_data:list[StudentRecord] = self.database.select_all_students()
            self.student_table = StudentTableModel(student_data)
            self.student_table_view.setModel(self.student_table)
        else:
            self.student_table_view.clearSelection()
            award_criteria_record:AwardCriteriaRecord = self.database.select_award_criteria(scholarship_name)
            student_data:list[StudentRecord] = self.database.select_students_by_criteria(award_criteria_record)
            self.student_table = StudentTableModel(student_data)
            self.student_table_view.setModel(self.student_table)

    def getScholarshipNames(self)-> list[str]:
        records:list[AwardCriteriaRecord] = self.database.select_all_award_criteria()
        scholarship_names:list[str] = [record.name for record in records]

        return scholarship_names

    def load_combobox(self)-> None:
        """Populates scholarship combobox with scholarship names.

        Populates scholarship combobox with scholarship names from the
        award criteria table in the database.
        """
        self.scholarship_tab.scholarshipComboBoxClear()

        # Add empty item for representing no filter / no selection
        self.scholarship_tab.scholarshipComboBoxAddItem("")
        
        # Retrieve all award criteria
        scholarship_names:list[str] = self.getScholarshipNames()

        self.scholarship_tab.scholarshipComboxBoxAddItems(scholarship_names)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window: ScholarlyMainWindow = ScholarlyMainWindow()
  
    # Displays the main window for the application
    window.show()
    
    # Run application
    sys.exit(app.exec())
