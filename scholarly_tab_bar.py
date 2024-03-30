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
from PyQt6.QtGui import QAction, QDoubleValidator, QValidator, QIntValidator, QIcon
from typing import Callable
from scholarly_scholarship_tab import ScholarlyScholarshipTab
import os

BASE_DIR: str = os.path.dirname(__file__)

# Function that takes no parameters, and returns nothing
voidCallBack: Callable[[], None] = lambda: None

class ScholarlyTabBar(QTabWidget):
    def __init__(
        self,
        scholarship_tab:ScholarlyScholarshipTab = None,
        manage_scholarships_tab = None,
        outstanding_student_awards_tab = None,

    ) -> None:
        super().__init__()

        # Add scholarship tab
        self.scholarship_tab: ScholarlyScholarshipTab = scholarship_tab
        self.scholarship_tab_name:str = "Select Scholarship Recipients"
        self.setScholarshipTab(self.scholarship_tab)

        # Add manage scholarships tab
        self.manage_scholarships_tab = manage_scholarships_tab
        self.manage_scholarships_tab_name:str = "Manage Scholarships"
        self.setManageScholarShipsTab(manage_scholarships_tab)

        # Add outstanding student awards tab
        self.outstanding_student_awards_tab = outstanding_student_awards_tab
        self.outstanding_student_awards_tab_name:str = "Outstanding Student Awards"
        self.setOutstandingStudentAwardTab(self.outstanding_student_awards_tab)

        
    def setScholarshipTab(self, tab:ScholarlyScholarshipTab)-> None:
        self.removeTab(0)
        self.insertTab(0, tab, self.scholarship_tab_name)
        self.setTabIcon(0, QIcon(os.path.join(BASE_DIR, "assets/icons/education.svg")))

    def setManageScholarShipsTab(self, tab)-> None:
        self.removeTab(1)
        self.insertTab(1, tab, self.manage_scholarships_tab_name)
        self.setTabIcon(1, QIcon(os.path.join(BASE_DIR, "assets/icons/filter_settings.svg")))

    def setOutstandingStudentAwardTab(self, tab)-> None:
        self.removeTab(2)
        self.insertTab(2, tab, self.outstanding_student_awards_tab_name)
        self.setTabIcon(2, QIcon(os.path.join(BASE_DIR, "assets/icons/medal.svg")))



if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    a = QApplication([])
    s = ScholarlyTabBar(ScholarlyScholarshipTab(), QWidget(), QWidget())
    s.show()
    a.exec()
