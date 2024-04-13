from PyQt6.QtWidgets import QMenuBar, QMenu, QWidget
from PyQt6.QtGui import QAction, QIcon, QColor
from scholarly_icons import ScholarlyIcon, IconSizes, Icons
from typing import Callable, Any
import os

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
        save_as_file_slot: Callable[[QWidget], None] = voidCallBack,
        close_file_slot: Callable[[QWidget], None] = voidCallBack,
        about_slot: Callable[[QWidget], None] = voidCallBack,
        about_qt_slot: Callable[[QWidget], None] = voidCallBack,
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
        self.open_action.setIcon(ScholarlyIcon(Icons.FileOpen))
        self.open_action.triggered.connect(open_file_slot)
        self.open_action.setShortcut("ctrl+o")
        self.file_menu.addAction(self.open_action)

        # Save Action
        self.save_action: QAction = QAction("&Save File", self)
        self.save_action.setIcon(ScholarlyIcon(Icons.Save))
        self.save_action.triggered.connect(save_file_slot)
        self.save_action.setShortcut("ctrl+s")
        self.file_menu.addAction(self.save_action)

        # Save As Action
        self.save_as_action: QAction = QAction("&Save As", self)
        self.save_as_action.setIcon(ScholarlyIcon(Icons.SaveAs))
        self.save_as_action.triggered.connect(save_as_file_slot)
        self.save_as_action.setShortcut("ctrl+shift+s")
        self.file_menu.addAction(self.save_as_action)

        # Close Action
        self.close_action: QAction = QAction("&Close File", self)
        self.close_action.setIcon(ScholarlyIcon(Icons.Close))
        self.close_action.triggered.connect(close_file_slot)
        self.close_action.setShortcut("ctrl+f4")
        self.file_menu.addAction(self.close_action)

        # Exit Action
        self.exit_action: QAction = QAction("&Exit", self)
        self.exit_action.setIcon(ScholarlyIcon(Icons.ExitToApp))
        self.exit_action.triggered.connect(exit_slot)
        self.exit_action.setShortcut("alt+f4")
        self.file_menu.addAction(self.exit_action)

        # Help Menu Tab
        self.help_menu: QMenu = self.addMenu("&Help")

        # Help Menu Action
        self.help_action: QAction = QAction("&Help", self)
        self.help_action.setIcon(ScholarlyIcon(Icons.Help))
        self.help_action.setShortcut("F1")
        self.help_action.triggered.connect(help_slot)
        self.help_menu.addAction(self.help_action)

        # About Menu Action
        self.about_action: QAction = QAction("&About", self)
        self.about_action.setIcon(ScholarlyIcon(Icons.Info))
        self.about_action.setShortcut("ctrl+a")
        self.about_action.triggered.connect(about_slot)
        self.help_menu.addAction(self.about_action)

        # About Qt Menu Action
        self.about_qt_action: QAction = QAction("&About Qt", self)
        self.about_qt_action.setIcon(ScholarlyIcon(Icons.Info))
        self.about_qt_action.setShortcut("ctrl+q")
        self.about_qt_action.triggered.connect(about_qt_slot)
        self.help_menu.addAction(self.about_qt_action)

    def setOpenFileSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for open_file_action.

        Sets the slot for the "Open" action on the "File" menu.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.open_action.triggered.connect(callback)

    def setSaveFileSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for the save_file_action.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.save_action.triggered.connect(callback)

    def setSaveAsFileSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for save_as_file_action.

        Sets the slot for the "Save" action on the "File" menu.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.save_as_action.triggered.connect(callback)

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

    def setAboutQtSlot(self, callback: Callable[[QWidget], None]) -> None:
        """Sets the slot for about_qt_action.

        Sets the slot for the "About Qt" action on the menu bar.

        Args:
            callback (Callable[[QWidget], None]): A function.
        """
        self.about_qt_action.triggered.connect(callback)

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

    def saveActionToggle(self, enabled: bool) -> None:
        """Toggles the Save action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.save_action.setEnabled(enabled)

    def saveAsActionToggle(self, enabled: bool) -> None:
        """Toggles the Save As action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.save_as_action.setEnabled(enabled)

    def closeActionToggle(self, enabled: bool) -> None:
        """Toggles the Close action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.close_action.setEnabled(enabled)

    def openActionToggle(self, enabled: bool) -> None:
        """Toggles the Open action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.open_action.setEnabled(enabled)

    def aboutActionToggle(self, enabled: bool) -> None:
        """Toggles the About action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.about_action.setEnabled(enabled)

    def aboutQtActionToggle(self, enabled: bool) -> None:
        """Toggles the About Qt action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.about_qt_action.setEnabled(enabled)

    def helpActionToggle(self, enabled: bool) -> None:
        """Toggles the Help action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.help_action.setEnabled(enabled)

    def exitActionToggle(self, enabled: bool) -> None:
        """Toggles the Exit action.

        Args:
            enabled (bool): If True, enables the action. If False, disables it.
        """
        self.exit_action.setEnabled(enabled)

    def toggleAll(self, enabled: bool) -> None:
        """Toggles all of the actions.

        Args:
            enabled (bool): If True, enables all of the actions. If False, disables them all.
        """
        self.saveActionToggle(enabled)
        self.exitActionToggle(enabled)
        self.saveAsActionToggle(enabled)
        self.helpActionToggle(enabled)
        self.closeActionToggle(enabled)
        self.openActionToggle(enabled)
        self.aboutActionToggle(enabled)
        self.aboutQtActionToggle(enabled)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    s = ScholarlyMenuBar()

    s.setOpenFileSlot(lambda: print("Open"))
    s.setSaveAsFileSlot(lambda: print("Save"))
    s.setCloseFileSlot(lambda: print("Close"))
    s.setAboutSlot(lambda: print("About"))
    s.setHelpSlot(lambda: print("Help"))
    s.setExitSlot(lambda: print("Exit"))
    s.toggleAll(False)

    s.show()
    a.exec()
