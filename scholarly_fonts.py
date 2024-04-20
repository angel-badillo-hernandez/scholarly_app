"""Provides classes for easily creating QFont objects for Scholarly App.

Provides the classes Fonts and Scholarly Font for making it simpler to create QFont objects.
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QFontDatabase
from PyQt6.QtCore import QSize
import os
from enum import Enum, StrEnum, auto
from typing import Final

# Absolute address for file to prevent issues with
# relative addresses when building app with PyInstaller
BASE_DIR: str = os.path.dirname(__file__)


class Fonts(StrEnum):
    RobotoFlex: str = auto()


class ScholarlyFont(QFont):

    def __init__(
        self,
        font: Fonts,
        pointSize: int = 12,
        weight: QFont.Weight = QFont.Weight.Normal,
        italic: bool = False,
    ) -> None:

        fontID: int = QFontDatabase.addApplicationFont(
            os.path.join(BASE_DIR, f"assets\\fonts\\{font}.ttf")
        )
        fontFamilies = QFontDatabase.applicationFontFamilies(fontID)

        # Create an icon from the modified pixmap
        super().__init__(fontFamilies, pointSize, weight, italic)


if __name__ == "__main__":
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QWidget,
        QHBoxLayout,
    )

    a = QApplication([])

    a.setFont(ScholarlyFont(Fonts.RobotoFlex, 24, QFont.Weight.Bold, True))
    w = QMainWindow()
    w.setCentralWidget(QPushButton("Hello there!"))
    w.show()
    a.exec()
