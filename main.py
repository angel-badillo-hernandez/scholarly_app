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
    QFontDatabase,
    QFontInfo,
)
from PyQt6.QtCore import QEvent, Qt, QSize, QModelIndex, pyqtSlot
from student_table_model import StudentTableModel
from student_record import StudentRecord, read_student_data_from_csv, write_student_data_to_csv
from award_criteria_record import AwardCriteriaRecord
from scholarly_database import ScholarlyDatabase, FileIsOpenError
from letter_writer import LetterVariables, write_letter, write_letter_to_bytes
from scholarly_menu_bar import ScholarlyMenuBar
from scholarly_tab_bar import ScholarlyTabBar
from scholarly_generate_letters_tab import ScholarlyGenerateLettersTab
from scholarly_send_emails_tab import ScholarlySendEmailsTab
from scholarly_manage_scholarships_tab import ScholarlyManageScholarshipsTab
from scholarly_icons import ScholarlyIcon, Icons, IconSizes
from scholarly_fonts import ScholarlyFont, Fonts
from google.oauth2.credentials import Credentials
from scholarly_google_auth import google_oauth, get_user_email_address
from email_writer import gmail_send_email_from_bytes, gmail_send_email

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
        self.generate_letters_tab:ScholarlyGenerateLettersTab = None
        self.tab_bar:ScholarlyTabBar = None

        self.initialize_ui()

    def initialize_ui(self):
        """Initializes GUI components on the GUI.

        Initializes the GUI components of the GUI for the application.
        """
        # Set window properties
        self.setWindowTitle("Scholarly")
        self.setWindowIcon(ScholarlyIcon(Icons.Scholarly, QColor("maroon"), IconSizes.Medium))
        self.setWindowIconText("Fortnite")
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

        self.generate_letters_tab = ScholarlyGenerateLettersTab(
            find_button_clicked= self.letter_tab_find,
            select_directory_button_clicked=self.letter_tab_select_directory,
            select_template_button_clicked=self.letter_tab_select_template,
            generate_letters_button_clicked=self.generate_letters,
            clear_selection_button_clicked=self.clear_selection
            )

        self.send_emails_tab = ScholarlySendEmailsTab(
            find_button_clicked= self.emails_tab_find,
            select_template_button_clicked=self.emails_tab_select_template,
            email_button_clicked=self.send_emails,
            clear_selection_button_clicked=self.clear_selection
            )
        

        self.load_combobox()
        self.generate_letters_tab.toggleAll(False)
        self.send_emails_tab.toggleAll(False)

        self.manage_scholarshops_tab =  ScholarlyManageScholarshipsTab()

        self.tab_bar = ScholarlyTabBar(generate_letters_tab=self.generate_letters_tab, send_emails_tab=self.send_emails_tab, manage_scholarships_tab=self.manage_scholarshops_tab, outstanding_student_awards_tab=QWidget())
        central_widget_layout.addWidget(self.tab_bar)

        # Add layout to central widget
        central_widget.setLayout(central_widget_layout)

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
        self.student_table_view.resizeColumnsToContents()
        central_widget_layout.addWidget(self.student_table_view)
        
        # Add central widget to main window
        self.setCentralWidget(central_widget)

    def initialize_menubar(self):
        """Initializes the menu bar for the main window.

        Initializes the menu bar for the main window of the appllication.
        """
        self.menu_bar: ScholarlyMenuBar = ScholarlyMenuBar(self.open_file, self.save_file, self.save_as_file, self.close_file, self.about, self.about_qt, self.help, self.close)
        
        # Disable Save, Save As, and Close file actions
        self.menu_bar.saveActionToggle(False)
        self.menu_bar.saveAsActionToggle(False)
        self.menu_bar.closeActionToggle(False)

        # Set the menubar for the window
        self.setMenuBar(self.menu_bar)

    @pyqtSlot()
    def open_file(self) -> None:
        """Slot (event handler) for "Open" action.

        Function called when "Open" action is activated. Shows
        a file dialog for opening a file, then reads the data
        from the file into the database and the table.
        """
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

        # If file is open, drop the table from the database before proceeding
        if not self.database.get_students_table_name() is None:
            self.close_file()

        try:
            # Insert data from file to database
            self.database.student_csv_to_table(file_path)
        except FileIsOpenError as f:
            QMessageBox.warning(
                self,
                "File Is Open",
                f"{f}",
            )
            return
        # If invalid data file, show error message
        except Exception as e:
            QMessageBox.critical(
                self,
                "Invalid File",
                f"The file is not a CSV file, or is malformed.\n{type(e).__name__}: {e}",
            )
            print(self.database.get_students_table_name())
            self.database.drop_table(self.database.get_students_table_name())
            return

        # Retrieve data from the database
        student_data = self.database.select_all_students()

        # Store data into table
        self.student_table = StudentTableModel(student_data)
        self.student_table_view.setModel(self.student_table)
        self.student_table_view.resizeColumnsToContents()

        # Enable disabled components
        self.generate_letters_tab.toggleAll(True)
        self.send_emails_tab.toggleAll(True)

        # Enable Save, Save As, and Close file actions on the menu bar
        self.menu_bar.saveActionToggle(True)
        self.menu_bar.saveAsActionToggle(True)
        self.menu_bar.closeActionToggle(True)

    @pyqtSlot()
    def save_file(self) -> None:
        file_path:str =self.database.get_students_table_name()

        # If the name of the file is non-existent, prompt for path to store file
        if not file_path:
            self.save_as_file()
        else:
            student_data:list[StudentRecord] = self.student_table.get_all_data()
            write_student_data_to_csv(file_path, student_data)
            

    @pyqtSlot()
    def save_as_file(self) -> None:
        """Slot (event handler) for "Save" action.

        Function called when "Save" action is activated. Shows
        a file dialog for saving a file, then stores the data from the table
        into the selected CSV file.
        """
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
        write_student_data_to_csv(file_path, student_data)

    @pyqtSlot()
    def close_file(self) -> None:
        """Slot (event handler) for close action.

        Function that is called when "Close" action is activated. Clears the database
        and clears the table.
        """
        self.generate_letters_tab.toggleAll(False)
        self.generate_letters_tab.scholarship_combobox.setCurrentText("")

        self.send_emails_tab.toggleAll(False)
        self.send_emails_tab.scholarship_combobox.setCurrentText("")

        # Drop the table from the database
        self.database.drop_table(self.database.get_students_table_name())
        self.database.set_students_table_name(None)

        # Clear table view
        self.student_table = StudentTableModel()
        self.student_table_view.setModel(self.student_table)

        # Disable Save, Save As, and Close file actions
        self.menu_bar.saveActionToggle(False)
        self.menu_bar.saveAsActionToggle(False)
        self.menu_bar.closeActionToggle(False)
        
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
    def about_qt(self)-> None:
        """Displays a message box providing information about Qt.
        """
        QMessageBox.aboutQt(self)

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

        scholarship_name:str = self.generate_letters_tab.getScholarshipComboBoxCurrentText()
        sender_name:str = self.generate_letters_tab.getSenderNameTexBoxText()
        sender_title:str = self.generate_letters_tab.getSenderTitleTextBoxText()
        sender_email:str = self.generate_letters_tab.getSenderEmailTextBoxText()
        amount:str = self.generate_letters_tab.getAmountTextBoxText()
        academic_year_fall:str = self.generate_letters_tab.getAcademicYearFallTextBoxText()
        academic_year_spring:str = self.generate_letters_tab.getAcademicYearSpringTextBoxText()
        template_path:str = self.generate_letters_tab.getTemplateLetterPathTextBoxText()
        dir_path:str = self.generate_letters_tab.getDestDirPathTextBoxText()

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
                student_last_name, student_first_name = student.name.split(",")
                student_last_name = student_last_name.lstrip().rstrip()
                student_first_name = student_first_name.lstrip().rstrip()


                student_name = f"{student_first_name} {student_last_name}"
            except ValueError as e:
                QMessageBox.critical(self, "Invalid Arguments", f"Invalid student name: '{student.name}'.\nMust be in the format 'last_name, first_name'.\n{type(e).__name__}: {e}")
                return
            
            letter_vars:LetterVariables = LetterVariables(student_name, date, amount, scholarship_name, academic_year_fall, academic_year_spring, sender_name, sender_email, sender_title)
            
            try:
                write_letter(template_path, f"{dir_path}/{student_name}_{student.student_ID}.docx", letter_vars)
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

    @pyqtSlot()
    def send_emails(self)-> None:
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

        scholarship_name:str = self.send_emails_tab.getScholarshipComboBoxCurrentText()
        sender_email:str = None
        sender_name:str = self.send_emails_tab.getSenderNameTexBoxText()
        sender_title:str = self.send_emails_tab.getSenderTitleTextBoxText()
        amount:str = self.send_emails_tab.getAmountTextBoxText()
        academic_year_fall:str = self.send_emails_tab.getAcademicYearFallTextBoxText()
        academic_year_spring:str = self.send_emails_tab.getAcademicYearSpringTextBoxText()
        template_path:str = self.send_emails_tab.getTemplateLetterPathTextBoxText()
        email_subject:str = self.send_emails_tab.getEmailSubjectTextBoxText()
        email_body:str = self.send_emails_tab.getEmailBodyTextBoxText()

        # Ensure text boxes are not empty, if so, show warning
        if not sender_name:
            QMessageBox.warning(self, "Enter Sender Name", "Sender name is empty. Please enter the sender name.")
            return
        elif not sender_title:
            QMessageBox.warning(self, "Enter Sender Title", "Sender name is empty. Please enter the sender title.")
            return
        elif not amount:
            QMessageBox.warning(self, "Enter Amount", "The amount is empty. Please enter the amount.")
            return
        elif not academic_year_fall:
            QMessageBox.warning(self, "Enter Academic Year", "The academic year is empty. Please enter the academic year.")
            return
        elif not scholarship_name:
            QMessageBox.warning(self, "Select a Scholarship", "A scholarship has not been selected. Please select a scholarship.")
            return
        elif not email_subject:
            QMessageBox.warning(self, "Enter Email Subject", "The email subject is empty. Please enter the subject.")
            return
        elif not email_body:
            QMessageBox.warning(self, "Enter Email Body", "The email body is empty. Please enter the body.")
            return
        
        # Get credentials and authenticate user
        credentials:Credentials = google_oauth()
        # Get sender email address
        sender_email = get_user_email_address(credentials)
       
        for student in student_data:
            student_name:str = None

            try:
                student_last_name, student_first_name = student.name.split(",")
                student_last_name = student_last_name.lstrip().rstrip()
                student_first_name = student_first_name.lstrip().rstrip()


                student_name = f"{student_first_name} {student_last_name}"
            except ValueError as e:
                QMessageBox.critical(self, "Invalid Arguments", f"Invalid student name: '{student.name}'.\nMust be in the format 'last_name, first_name'.\n{type(e).__name__}: {e}")
                return
            
            letter_vars:LetterVariables = LetterVariables(student_name, date, amount, scholarship_name, academic_year_fall, academic_year_spring, sender_name, sender_email, sender_title)
            
            try:
                letter_bytes:bytes = write_letter_to_bytes(template_path, letter_vars)

                gmail_send_email_from_bytes(credentials=credentials, recipient_email_address=student.email, subject=email_subject, body=email_body, attachment_bytes=letter_bytes, attachment_file_name=f"{scholarship_name}.docx")

            except Exception as e:
                QMessageBox.critical(self, "Invalid File Paths", f"Invalid template letter file path or destination directory path'.\n{type(e).__name__}: {e}")
                return
            
        # Open Browser to Gmail to show sent letters
        reponse: QMessageBox.StandardButton = QMessageBox.question(
            self,
            "Open GMail in Browser",
            "The emails were successful delivered.\nWould you like to view them in your browser?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reponse == QMessageBox.StandardButton.Yes:
            webbrowser.open("https://mail.google.com/")

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
    def letter_tab_select_directory(self):
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
        self.generate_letters_tab.setDestDirPathTextBoxText(dir_path)

    @pyqtSlot()
    def letter_tab_select_template(self):
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
        self.generate_letters_tab.setTemplateLetterPathTextBoxText(file_path)

    @pyqtSlot()
    def emails_tab_select_template(self):
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
        self.send_emails_tab.setTemplateLetterPathTextBoxText(file_path)

    @pyqtSlot()
    def letter_tab_find(self):
        """Called when selection is changed in scholarship_combobox

        Called when selection is changed in scholarship_combobox
        """
        scholarship_name:str = self.generate_letters_tab.getScholarshipComboBoxCurrentText()

        # Display entire contents of file / database
        if scholarship_name == "":
            # Clear selection
            self.student_table_view.clearSelection()
            
            # Reset table to have entire contents of database
            student_data:list[StudentRecord] = self.database.select_all_students()
            self.student_table = StudentTableModel(student_data)
            self.student_table_view.setModel(self.student_table)
        # Display results of query performed on data
        else:
            # Clear selection
            self.student_table_view.clearSelection()
            award_criteria_record:AwardCriteriaRecord = self.database.select_award_criteria(scholarship_name)

            # If award criteria is valid, perform query and display results in table
            if isinstance(award_criteria_record, AwardCriteriaRecord):
                student_data:list[StudentRecord] = self.database.select_students_by_criteria(award_criteria_record)
                self.student_table = StudentTableModel(student_data)
                self.student_table_view.setModel(self.student_table)
            # If award criteriai is not valid, scholarship does not exist.
            else:
                QMessageBox.information(self, "Invalid Scholarship", f"The scholarship '{scholarship_name}' does not exist. Please enter or select an existing scholarship.")

    @pyqtSlot()
    def emails_tab_find(self):
        """Called when selection is changed in scholarship_combobox

        Called when selection is changed in scholarship_combobox
        """
        scholarship_name:str = self.send_emails_tab.getScholarshipComboBoxCurrentText()

        # Display entire contents of file / database
        if scholarship_name == "":
            # Clear selection
            self.student_table_view.clearSelection()
            
            # Reset table to have entire contents of database
            student_data:list[StudentRecord] = self.database.select_all_students()
            self.student_table = StudentTableModel(student_data)
            self.student_table_view.setModel(self.student_table)
        # Display results of query performed on data
        else:
            # Clear selection
            self.student_table_view.clearSelection()
            award_criteria_record:AwardCriteriaRecord = self.database.select_award_criteria(scholarship_name)

            # If award criteria is valid, perform query and display results in table
            if isinstance(award_criteria_record, AwardCriteriaRecord):
                student_data:list[StudentRecord] = self.database.select_students_by_criteria(award_criteria_record)
                self.student_table = StudentTableModel(student_data)
                self.student_table_view.setModel(self.student_table)
            # If award criteriai is not valid, scholarship does not exist.
            else:
                QMessageBox.information(self, "Invalid Scholarship", f"The scholarship '{scholarship_name}' does not exist. Please enter or select an existing scholarship.")

    @pyqtSlot()
    def clear_selection(self)-> None:
        """Clears the selection in the table.
        """
        self.student_table_view.clearSelection()

    def getScholarshipNames(self)-> list[str]:
        records:list[AwardCriteriaRecord] = self.database.select_all_award_criteria()
        scholarship_names:list[str] = [record.name for record in records]

        return scholarship_names

    def load_combobox(self)-> None:
        """Populates scholarship combobox with scholarship names.

        Populates scholarship combobox with scholarship names from the
        award criteria table in the database.
        """
        self.generate_letters_tab.scholarshipComboBoxClear()
        self.send_emails_tab.scholarshipComboBoxClear()

        # Add empty item for representing no filter / no selection
        self.generate_letters_tab.scholarshipComboBoxAddItem("")
        self.send_emails_tab.scholarshipComboBoxAddItem("")
        
        # Retrieve all award criteria
        scholarship_names:list[str] = self.getScholarshipNames()

        self.generate_letters_tab.scholarshipComboxBoxAddItems(scholarship_names)
        self.send_emails_tab.scholarshipComboxBoxAddItems(scholarship_names)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # appFont:ScholarlyFont = ScholarlyFont(Fonts.RobotoFlex, 12)

    # # Setting Up App font
    # app.setFont(appFont)

    window: ScholarlyMainWindow = ScholarlyMainWindow()
    with open("style.qss", "r") as styleFile:
        app.setStyleSheet(styleFile.read())

    # Displays the main window for the application
    window.show()
    
    # Run application
    sys.exit(app.exec())
