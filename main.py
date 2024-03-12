"""Main Program for creating the Scholarly App GUI

This file contains the `ScholarlyMainWindow` class, which is the
contains methods for creating the application's GUI.

"""

import sys
import webbrowser
import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QCloseEvent, QIcon
from PyQt6.QtCore import QEvent, Qt, QSize, QModelIndex
from student_table_model import StudentTableModel
from student_record import StudentRecord
from student_data_reader import StudentDataReader
from student_data_writer import StudentDataWriter
from scholarly_database import ScholarlyDatabase, StudentRecord


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

        # Add table to layout
        self.student_table = StudentTableModel()
        self.student_table_view: QTableView = QTableView()
        self.student_table_view.setModel(self.student_table)
        horizontal_layout.addWidget(self.student_table_view)
        self.student_table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.student_table_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

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

        # Insert data from file to database
        self.database.student_csv_to_table(file_path)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window: ScholarlyMainWindow = ScholarlyMainWindow()

    # Displays the main window for the application
    window.show()

    # Run application
    sys.exit(app.exec())
