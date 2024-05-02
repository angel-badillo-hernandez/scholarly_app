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
from PyQt6.QtGui import (
    QAction,
    QDoubleValidator,
    QValidator,
    QIntValidator,
    QIcon,
    QColor,
)
from PyQt6.QtCore import QSize, Qt
from scholarly_icons import ScholarlyIcon, IconSizes, Icons
from typing import Callable
import os


# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: None


class ScholarlyOutstandingStudentAwardsTab(QWidget):

    def __init__(self) -> None:
        super().__init__()

        # Main layout for widget
        main_layout: QVBoxLayout = QVBoxLayout()

        # Form layout for text box
        form_layout: QFormLayout = QFormLayout()

        # Button layout
        button_layout:QHBoxLayout = QHBoxLayout()

        # Textbox for number of candidates per category
        self.num_candidates:QLineEdit = QLineEdit()
        self.num_candidates.setValidator(QIntValidator())
        self.num_candidates.setToolTip("Number of candidates per category.")

        # Add textbox to layout
        form_layout.addRow("Candidates per category", self.num_candidates)

        # Button for creating form
        self.create_form_button:QToolButton = QToolButton()
        self.create_form_button.setText("Create Form")

        # Add button to layout
        button_layout.addWidget(self.create_form_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add sublayouts to layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        # Set main layout for widget
        self.setLayout(main_layout)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    s = ScholarlyOutstandingStudentAwardsTab()
    s.show()
    a.exec()
