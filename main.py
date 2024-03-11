"""Main Program for creating the Scholarly App GUI

This file contains the `ScholarlyMainWindow` class, which is the
contains methods for creating the applications GUI.

"""

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QCloseEvent, QIcon
from PyQt6.QtCore import QEvent, Qt, QSize, QModelIndex
from student_table_model import StudentTableModel
from student_record import StudentRecord
from student_data_reader import StudentDataReader
from student_data_writer import StudentDataWriter
from student_database import StudentDataBase


class ScholarlyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.student_table: StudentTableModel = None
        self.student_table_view: QTableView = None
        self.database: StudentDataBase = StudentDataBase("student_database.sqlite")

        self.initalize_ui()

    def initalize_ui(self):
        # Set window properties
        self.setWindowTitle("Scholarly")
        self.setWindowIcon(QIcon("images/scholarly.ico"))
        self.setGeometry(200, 200, 500, 500)

        # Initalize menu bar
        self.initialize_menubar()

        # Initilize table
        self.initalize_central_widget()

    def initalize_central_widget(self):
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

        # Add layout to central widget, and add central widget to main window
        central_widget.setLayout(horizontal_layout)
        self.setCentralWidget(central_widget)

    def initialize_menubar(self):
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        """Creates a QMenuBar on the main window

        Creates and displays a menu bar with "File" menu.
        File menu has "Open" action.
        """
        menu_bar: QMenuBar = self.menuBar()

        # File Menu Tab
        file_menu: QMenu = menu_bar.addMenu("&File")

        # Open Action
        open_action: QAction = QAction("Open", self)
        open_action.triggered.connect(self.open_file_slot)
        file_menu.addAction(open_action)

        # Save Action
        save_action: QAction = QAction("Save", self)
        save_action.triggered.connect(self.save_file_slot)
        file_menu.addAction(save_action)

        # Close Action
        close_action: QAction = QAction("Close", self)
        close_action.triggered.connect(self.close_file_slot)
        file_menu.addAction(close_action)

        # Exit Action
        close_action: QAction = QAction("Exit", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        # About Menu Tab
        about_action: QAction = QAction("About", self)
        about_action.triggered.connect(self.about_slot)
        menu_bar.addAction(about_action)

        # Help Menu Tab
        help_action: QAction = QAction("Help", self)
        help_action.triggered.connect(self.help_event)
        menu_bar.addAction(help_action)

        file_menu.show()

    def open_file_slot(self) -> None:
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        """Opens File Explorer for selecting CSV file.

        Opens File Explorer for selecting a CSV file with student data.
        """
        # Current user's Documents Directory
        user_documents_path: str = f"{os.path.expanduser('~')}/Documents"

        # Open file dialog, and gets the selected file path
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open File",
            directory=user_documents_path,
            filter="CSV (*.csv)",
        )

        # Insert data from file to database
        self.database.csv_to_table(file_path)

        # Retrieve data from the database
        student_data = self.database.select_all()

        # Store data into table
        self.student_table = StudentTableModel(student_data)
        self.student_table_view.setModel(self.student_table)

    def save_file_slot(self) -> None:
        # [1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button.". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
        """Opens File Explorer for saving a CSV file.

        Opens File Explorer for saving a CSV file with student data.
        """
        # Current user's Documents Directory
        user_documents_path: str = f"{os.path.expanduser('~')}/Documents"

        # Open file dialog, and gets the selected file path
        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Open File",
            directory=user_documents_path,
            filter="CSV (*.csv)",
        )

        # Retrieve data from table
        student_data:list[StudentRecord] = self.student_table.get_all_data()

        writer:StudentDataWriter = StudentDataWriter(file_path)
        writer.write_values(student_data)
        

    def close_file_slot(self) -> None:
        self.database.drop_table()
        self.student_table = StudentTableModel()
        self.student_table_view.setModel(self.student_table)

    def closeEvent(self, event: QCloseEvent) -> None:
        reponse: QMessageBox.StandardButton = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to close the program?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reponse == QMessageBox.StandardButton.Yes:
            # TODO: Add functionality for deleting the database file
            self.close_file_slot()
            event.accept()
        else:
            event.ignore()

    def about_slot(self) -> None:
        # TODO: Add functionality for About menu
        pass

    def help_event(self) -> None:
        # TODO: Add functionality for Help menu
        pass

    def selected_row(self) -> None:
        indices = self.student_table_view.selectRow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScholarlyMainWindow()
    window.show()

    # Run app
    sys.exit(app.exec())
