from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QFormLayout,
    QLayout,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QToolButton,
    QToolTip,
    QGroupBox,
    QComboBox,
    QLabel,
)
from PyQt6.QtGui import QAction, QDoubleValidator, QValidator, QIntValidator, QIcon
from typing import Callable
import os

BASE_DIR: str = os.path.dirname(__file__)

# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: None


class ScholarlyOutstandingStudentAwardsTab(QTabWidget):

    def __init__(self) -> None:
        super().__init__()

        # Main layout for widget
        main_layout: QVBoxLayout = QVBoxLayout()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    s = ScholarlyOutstandingStudentAwardsTab()
    s.show()
    a.exec()
