from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
import os

# Absolute address for file to prevent issues with
# relative addresses when building app with PyInstaller
BASE_DIR: str = os.path.dirname(__file__)


class ScholarlyIcons(QIcon):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def QIcon_from_svg(file_path: str, color: QColor = QColor("black")) -> QIcon:
        # https://stackoverflow.com/questions/15123544/change-the-color-of-an-svg-in-qt
        pixmap: QPixmap = QPixmap(file_path)
        qp: QPainter = QPainter(pixmap)
        qp.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        qp.fillRect(pixmap.rect(), color)
        qp.end()
        return QIcon(pixmap)
    
    pass


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow

    a = QApplication([])
    s = ScholarlyIcons.QIcon_from_svg(
        os.path.join(BASE_DIR, "assets/icons/about.svg"), QColor("red")
    )
    w = QMainWindow()
    w.setWindowIcon(s)
    w.show()
    a.exec()
