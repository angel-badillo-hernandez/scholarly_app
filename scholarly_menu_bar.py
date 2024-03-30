from PyQt6.QtWidgets import QMenuBar, QMenu, QWidget
from PyQt6.QtGui import QAction, QIcon
from typing import Callable, Any
import os

BASE_DIR: str = os.path.dirname(__file__)

# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: None


class ScholarlyMenuBar(QMenuBar):
    """Specialized QMenuBar for Scholarly app

    A specialized menu bar, inheriting from QMenuBar. It contains all the GUI
    components needed for the menu bar to be displayed in the Scholarly app.
    """

    def __init__(
        self,
        open_file_slot: Callable[[QWidget], None] = voidCallBack,
        save_file_slot: Callable[[QWidget], None] = voidCallBack,
        close_file_slot: Callable[[QWidget], None] = voidCallBack,
        about_slot: Callable[[QWidget], None] = voidCallBack,
        help_slot: Callable[[QWidget], None] = voidCallBack,
        exit_slot: Callable[[QWidget], bool] = voidCallBack,
    ) -> None:
        """Creates a new instance of ScholarlyMenuBar

        Creates a new instance of ScholarlyMenuBar. It can be added onto any
        compatible QWidget subclass, however it is designed primarily for
        ScholarlyMainWindow class.

        Args:
            open_file_slot (Callable): A function to be invoked when the "Open" action is activated.
            save_file_slot (Callable): A function to be invoked when the "Save" action is activated.
            close_file_slot (Callable): A function to be invoked when the "Close" action is activated.
            about_slot (Callable): A function to be invoked when the "About" action is activated.
            help_slot (Callable): A function to be invoked when the "Help" action is activated.
            exit_slot (Callable): A function to be invoked when the "Exit" action is activated.
        """
        super().__init__()

        # File Menu Tab
        self.file_menu: QMenu = self.addMenu("&File")

        # Open Action
        self.open_action: QAction = QAction("&Open File")
        self.open_action.setIcon(QIcon(os.path.join(BASE_DIR, "assets/icons/open.svg")))
        self.open_action.triggered.connect(open_file_slot)
        self.open_action.setShortcut("ctrl+o")
        self.file_menu.addAction(self.open_action)

        # Save Action
        self.save_action: QAction = QAction("&Save File", self)
        self.save_action.setIcon(QIcon(os.path.join(BASE_DIR, "assets/icons/save.svg")))
        self.save_action.triggered.connect(save_file_slot)
        self.save_action.setShortcut("ctrl+s")
        self.file_menu.addAction(self.save_action)

        # Close Action
        self.close_action: QAction = QAction("&Close File", self)
        self.close_action.setIcon(QIcon(os.path.join(BASE_DIR, "assets/icons/close.svg")))
        self.close_action.triggered.connect(close_file_slot)
        self.close_action.setShortcut("ctrl+f4")
        self.file_menu.addAction(self.close_action)

        # Exit Action
        self.exit_action: QAction = QAction("&Exit", self)
        self.exit_action.setIcon(QIcon(os.path.join(BASE_DIR, "assets/icons/exit.svg")))
        self.exit_action.triggered.connect(exit_slot)
        self.file_menu.addAction(self.exit_action)

        self.help_menu:QMenu = self.addMenu("&Help")

        # About Menu Tab
        self.about_action: QAction = QAction("&About", self)
        self.about_action.setIcon(QIcon(os.path.join(BASE_DIR, "assets/icons/about.svg")))
        self.about_action.setShortcut("ctrl+a")
        self.about_action.triggered.connect(about_slot)
        self.help_menu.addAction(self.about_action)

        # Help Menu Tab
        self.help_action: QAction = QAction("&Help", self)
        self.help_action.setIcon(QIcon(os.path.join(BASE_DIR, "assets/icons/help.svg")))
        self.help_action.setShortcut("F1")
        self.help_action.triggered.connect(help_slot)
        self.help_menu.addAction(self.help_action)

    def setOpenFileSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for open_file_action.

        Sets the slot for the "Open" action on the "File" menu.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.open_action.triggered.connect(callback)

    def setSaveFileSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for save_file_action.

        Sets the slot for the "Save" action on the "File" menu.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.save_action.triggered.connect(callback)

    def setCloseFileSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for close_file_action.

        Sets the slot for the "Close" action on the "File" menu.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.close_action.triggered.connect(callback)

    def setAboutSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for about_action.

        Sets the slot for the "About" action on the menu bar.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.about_action.triggered.connect(callback)

    def setHelpSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for help_action.

        Sets the slot for the "Help" action on the menu bar.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.help_action.triggered.connect(callback)

    def setCloseFileSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for the close_file_action.

        Sets the slot for the "Close" action on the "File" menu.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.close_action.triggered.connect(callback)

    def setExitSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for the exit_action.

        Sets the slot for the "Exit" action on the "File" menu.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.exit_action.triggered.connect(callback)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    s = ScholarlyMenuBar()

    s.setOpenFileSlot(lambda: print("Open"))
    s.setSaveFileSlot(lambda: print("Save"))
    s.setCloseFileSlot(lambda: print("Close"))
    s.setAboutSlot(lambda: print("About"))
    s.setHelpSlot(lambda: print("Help"))
    s.setExitSlot(lambda: print("Exit"))

    s.show()
    a.exec()
