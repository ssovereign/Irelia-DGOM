import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path
from jinja2 import Template


class MyWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.menu_bar = None
        self.hamburger_button = None
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
        self.add_hamburger_menu()

    def add_hamburger_menu(self):
        """Create a hamburger menu button and menu bar."""
        # Hamburger menu button
        self.hamburger_button = QtWidgets.QToolButton(self)
        icon_path = Path(__file__).parent / "icons" / "hamburger.png"
        print(f"Icon path: {icon_path}")
        print(f"Icon exists: {icon_path.exists()}")
        self.hamburger_button.setIcon(QtGui.QIcon(str(icon_path)))
        self.hamburger_button.setToolTip("Toggle Menu")
        self.hamburger_button.setFixedSize(30, 30)
        self.hamburger_button.setStyleSheet("""
            QToolButton {
                border: none;
                background-color: transparent;
                margin: 5px;
            }
            QToolButton:hover {
                background-color: #3c3c3c;
            }
        """)

        # Place the button in the top-left corner
        self.hamburger_button.move(5, 5)
        self.hamburger_button.clicked.connect(self.toggle_menu_bar)

        # Add the full menu bar
        self.menu_bar = self.menuBar()
        self.create_menu_bar()
        self.menu_bar.hide()  # Initially hide the menu bar

    def create_menu_bar(self):

        file_menu = self.menu_bar.addMenu("File")
        edit_menu = self.menu_bar.addMenu("Edit")
        view_menu = self.menu_bar.addMenu("View")

    def toggle_menu_bar(self):
        if self.menu_bar.isVisible():
            self.menu_bar.hide()
        else:
            self.menu_bar.show()

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    print("Reached!")
    stylesheet_path = Path(__file__).parent / "styles" / "index.css"
    print(stylesheet_path.absolute())
    if stylesheet_path.exists():
        with open(stylesheet_path, "r") as file:
            template = Template(file.read())
            stylesheet = template.render(
                primary_color="#121212",
                text_color="#ffffff",
                button_color="#2c2c2c",
                button_hover_color="#3c3c3c",
            )
            app.setStyleSheet(stylesheet)
            print("Stylesheet applied successfully.")

    else:
        print(f"Warning: Stylesheet file {stylesheet_path} not found.")

    widget = MyWidget()
    widget.setWindowTitle("Irelia-DGOM")
    widget.showMaximized()

    sys.exit(app.exec())
