# References:

[1] ChatGPT, response to "Write me python code for a PyQT6 menu bar with a File tab and Open button". OpenAI [Online]. https://chat.openai.com/ (accessed February 29, 2024).
```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PyQt6 Menu Example")
        self.setGeometry(200, 200, 500, 300)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")

        # Open Action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            print(f"Opened file: {file_name}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

```