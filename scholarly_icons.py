from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import QSize
import os
from enum import Enum, StrEnum, auto
from typing import Final

# Absolute address for file to prevent issues with
# relative addresses when building app with PyInstaller
BASE_DIR: str = os.path.dirname(__file__)


class IconSizes(Enum):
    Small: QSize = QSize(16, 16)
    Medium: int = QSize(32, 32)
    Large: QSize = QSize(64, 64)
    XLarge: int = QSize(128, 128)
    XXLarge: int = QSize(256, 256)


class Icons(StrEnum):
    Scholarly: str = auto()
    Add: str = auto()
    AddCircle: str = auto()
    AttachFile: str = auto()
    Cancel: str = auto()
    Close: str = auto()
    CSV: str = auto()
    ExitToApp:str = auto()
    FileOpen: str = auto()
    FileOpenFill:str = auto()
    Filter: str = auto()
    FilterFill:str = auto()
    FolderOpen: str = auto()
    FolderOpenFill:str = auto()
    FormsAddOn: str = auto()
    Help: str = auto()
    HelpFill:str = auto()
    Info: str = auto()
    InfoFill:str = auto()
    Mail: str = auto()
    Remove: str = auto()
    Save: str = auto()
    SaveFill:str = auto()
    SaveAs: str = auto()
    SaveAsFill:str = auto()
    School: str = auto()
    Search: str = auto()
    Send: str = auto()
    StackedEmail: str = auto()
    Subject: str = auto()
    Trophy: str = auto()
    ZoomIn: str = auto()
    ZoomOut: str = auto()
    ExpandMore:str = auto()


class ScholarlyIcon(QIcon):

    def __init__(
        self,
        icon: Icons,
        color: QColor = QColor("black"),
        size: IconSizes = IconSizes.Small,
    ) -> None:
        # Build file path to icon SVG file
        file_path: str = os.path.join(BASE_DIR, f"assets\\icons\\{icon}.svg")

        # Convert IconSize to QSize
        qsize: QSize = size.value

        pixmap: QPixmap = QIcon(file_path).pixmap(qsize)

        # Change the color of the icon with painter
        painter: QPainter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        # Create an icon from the modified pixmap
        super().__init__(pixmap)

        # Set properties for self
        self.icon_name: Icons = icon
        self.color: QColor = color
        self.size: IconSizes = size

    def getIcon(self) -> Icons:
        return self.icon_name

    def getSize(self) -> IconSizes:
        return self.size

    def getColor(self) -> QColor:
        return self.color


if __name__ == "__main__":
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QWidget,
        QHBoxLayout,
    )

    a = QApplication([])
    w = QMainWindow()

    widget = QWidget()
    layout = QHBoxLayout()

    scholarlyIcon = ScholarlyIcon(Icons.Scholarly, QColor("maroon"), IconSizes.XLarge)

    for icon in Icons:
        sIcon = ScholarlyIcon(icon, size=IconSizes.Medium)
        button = QPushButton()
        button.setText(icon)
        button.setIcon(sIcon)
        button.setIconSize(sIcon.getSize().value)

        layout.addWidget(button)

    widget.setLayout(layout)

    w.setWindowIcon(scholarlyIcon)
    w.setIconSize(scholarlyIcon.size.value)
    w.setCentralWidget(widget)

    w.show()
    a.exec()
