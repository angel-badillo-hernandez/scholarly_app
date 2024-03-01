"""Main Program for creating the Scholarly App GUI

This file contains the `ScholarlyMainWindow` class, which is the
contains methods for creating the applications GUI.

"""
import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize


# ChatGPT Prompt: "Write me python code for a PyQT6 menu bar with a File tab and Open button."
# Citation: (OpenAI's ChatGPT, response to prompt from author, February 29, 2024)
class ScholarlyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initui()

    def initui(self):
        """Intializes the QMainWindow UI component

        Initializes main window's attributes such as: size, title, etc.
        Creates and adds other components pertaining to the window.
        """
        self.setWindowTitle("Scholarly")
        self.setGeometry(200, 200, 500, 500)
        self.create_menubar()

    def create_menubar(self):
        """Creates a QMenuBar on the main window

        Creates and displays a menu bar with "File" menu.
        File menu has "Open" action.
        """
        menu_bar: QMenuBar = self.menuBar()

        # File Menu Tab
        file_menu: QMenu = menu_bar.addMenu("&File")

        # Open Action
        open_action: QAction = QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)

        file_menu.addAction(open_action)
        file_menu.show()

    def open_file_dialog(self) -> str:
        """Opens File Explorer for selecting CSV file.

        Opens File Explorer for selecting a CSV file with student data.
        Once the file is selected, the file path is returned.

        Returns:
            The file path, a `str`.

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

        return file_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScholarlyMainWindow()
    window.show()

    # Run app
    sys.exit(app.exec())
