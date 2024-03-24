from PyQt6.QtWidgets import QMenuBar, QMenu, QWidget
from PyQt6.QtGui import QAction
from typing import Callable


class ScholarlyMenuBar(QMenuBar):
    """Specialized QMenuBar for Scholarly app

    A specialized menu bar, inheriting from QMenuBar. It contains all the GUI
    components needed for the menu bar to be displayed in the Scholarly app.
    """

    def __init__(
        self,
        parent: QWidget,
        open_file_slot: Callable[[QWidget], None],
        save_file_slot: Callable[[QWidget], None],
        close_file_slot: Callable[[QWidget], None],
        about_slot: Callable[[QWidget], None],
        help_slot: Callable[[QWidget], None],
        exit_slot: Callable[[QWidget], bool],
    ) -> None:
        """Creates a new instance of ScholarlyMenuBar

        Creates a new instance of ScholarlyMenuBar. It can be added onto any
        compatible QWidget subclass, however it is designed primarily for
        ScholarlyMainWindow class.

        Args:
            parent (QWidget): A QWidget to add the menu bar to.
            open_file_slot (Callable): A function to be invoked when the "Open" action is activated.
            save_file_slot (Callable): A function to be invoked when the "Save" action is activated.
            close_file_slot (Callable): A function to be invoked when the "Close" action is activated.
            about_slot (Callable): A function to be invoked when the "About" action is activated.
            help_slot (Callable): A function to be invoked when the "Help" action is activated.
            exit_slot (Callable): A function to be invoked when the "Exit" action is activated.
        """
        super().__init__(parent)

        # File Menu Tab
        self.file_menu: QMenu = self.addMenu("&File")

        # Open Action
        self.open_action: QAction = QAction("Open File", parent)
        self.open_action.triggered.connect(open_file_slot)
        self.open_action.setShortcut("ctrl+o")
        self.file_menu.addAction(self.open_action)

        # Save Action
        self.save_action: QAction = QAction("Save File", parent)
        self.save_action.triggered.connect(save_file_slot)
        self.save_action.setShortcut("ctrl+s")
        self.file_menu.addAction(self.save_action)

        # Close Action
        self.close_action: QAction = QAction("Close File", parent)
        self.close_action.triggered.connect(close_file_slot)
        self.close_action.setShortcut("ctrl+f4")
        self.file_menu.addAction(self.close_action)

        # Exit Action
        self.exit_action: QAction = QAction("Exit", parent)
        self.exit_action.triggered.connect(exit_slot)
        self.file_menu.addAction(self.exit_action)

        # About Menu Tab
        about_action: QAction = QAction("&About", parent)
        about_action.triggered.connect(about_slot)
        self.addAction(about_action)

        # Help Menu Tab
        help_action: QAction = QAction("&Help", parent)
        help_action.triggered.connect(help_slot)
        self.addAction(help_action)
