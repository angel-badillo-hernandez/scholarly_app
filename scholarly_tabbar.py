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
)
from PyQt6.QtGui import QAction, QDoubleValidator, QValidator, QIntValidator


class ScholarlyTabBar(QWidget):
    def __init__(self) -> None:
        super().__init__()