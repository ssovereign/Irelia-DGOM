import sys
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path
from jinja2 import Template

# Subclass QMenuBar to enable hover functionality
class HoverMenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        action = self.actionAt(event.pos())
        if action and not action.isSeparator():
            self.setActiveAction(action)
        super().mouseMoveEvent(event)

class MyWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Main central widget and layout
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setStyleSheet("background-color: #2c2c2c; border: 1px solid red;")  # Debug border
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)  # Ensure no extra spacing between widgets

        # Top bar with fixed height
        self.top_bar = QtWidgets.QWidget()
        self.top_bar.setStyleSheet("background-color: #3c3c3c; border: 1px solid green;")  # Debug border
        self.top_bar.setFixedHeight(27.5)

        # Stacked layout to switch between hamburger and menu bar
        self.top_bar_layout = QtWidgets.QStackedLayout(self.top_bar)

        # Hamburger button
        self.hamburger_button = QtWidgets.QToolButton()
        icon_path = Path(__file__).parent / "icons" / "hamburger.png"
        self.hamburger_button.setIcon(QtGui.QIcon(str(icon_path)))
        self.hamburger_button.setToolTip("Open Menu")
        self.hamburger_button.setFixedSize(30, 30)
        self.hamburger_button.clicked.connect(self.show_menu_bar)
        self.hamburger_button.setStyleSheet("border: 1px solid blue;")  # Debug border

        # Menu bar with hover functionality
        self.menu_bar = HoverMenuBar()
        self.menu_bar.setStyleSheet("background-color: #4c4c4c; border: 1px solid orange;")  # Debug border
        self.create_menu_bar()

        # Add hamburger button and menu bar to stacked layout
        self.top_bar_layout.addWidget(self.hamburger_button)  # Index 0
        self.top_bar_layout.addWidget(self.menu_bar)          # Index 1

        # Initially show the hamburger button
        self.top_bar_layout.setCurrentIndex(0)

        # Add the top bar to the main layout
        self.main_layout.addWidget(self.top_bar)

        # Blank bar below the top bar
        self.blank_bar = QtWidgets.QWidget()
        self.blank_bar.setStyleSheet("background-color: #3c3c3c; border: 1px solid cyan;")  # Debug border
        self.blank_bar.setFixedHeight(27.5)  # Same height as the top bar
        self.main_layout.addWidget(self.blank_bar)

        # Third bar to act as the icon menu
        self.icon_bar = QtWidgets.QWidget()
        self.icon_bar.setStyleSheet("background-color: #5c5c5c; border: 1px solid yellow;")  # Debug border
        self.icon_bar.setFixedHeight(50)  # Same height as the icon buttons

        # Icon menu layout inside the third bar
        self.icon_bar_layout = QtWidgets.QHBoxLayout(self.icon_bar)
        self.icon_bar_layout.setContentsMargins(10, 5, 10, 5)
        self.icon_bar_layout.setSpacing(10)
        self.add_icon_menu_items()

        self.main_layout.addWidget(self.icon_bar)

        # Add a stretch below the icon bar to avoid filling extra space
        self.main_layout.addStretch()

        # Install event filter to detect clicks outside the menu bar
        QtWidgets.QApplication.instance().installEventFilter(self)

    def create_menu_bar(self):
        # Main menus
        file_menu = self.menu_bar.addMenu("&File")
        edit_menu = self.menu_bar.addMenu("&Edit")
        view_menu = self.menu_bar.addMenu("&View")
        settings_menu = self.menu_bar.addMenu("&Settings")

        file_menu.addAction("&Open...")
        file_menu.addAction("Open &Recent")
        file_menu.addAction("&Merge...")
        file_menu.addAction("&Close")
        file_menu.addSeparator()
        file_menu.addAction("&Save")
        file_menu.addAction("Save &As...")
        file_menu.addAction("E&xit")

    def add_icon_menu_items(self):
        icon_names = ["anchor.png", "android.png", "animal.png"]
        for icon_name in icon_names:
            button = QtWidgets.QToolButton()
            icon_path = Path(__file__).parent / "icons" / icon_name
            button.setIcon(QtGui.QIcon(str(icon_path)))
            button.setToolTip(icon_name.split('.')[0].capitalize())
            button.setFixedSize(40, 40)
            button.setStyleSheet(
                "QToolButton { border: 1px solid purple; border-radius: 5px; padding: 5px; }"
                "QToolButton:hover { background-color: #6c6c6c; }"
            )
            self.icon_bar_layout.addWidget(button)

        # Add a spacer to the right to push icons towards the left
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.icon_bar_layout.addWidget(spacer)

    def show_menu_bar(self):
        self.top_bar_layout.setCurrentIndex(1)

    def hide_menu_bar(self):
        self.top_bar_layout.setCurrentIndex(0)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if self.top_bar_layout.currentIndex() == 1:
                pos = self.menu_bar.mapFromGlobal(event.globalPos())
                if not self.menu_bar.rect().contains(pos):
                    self.hide_menu_bar()
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    stylesheet_path = Path(__file__).parent / "styles" / "index.css"
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
    else:
        print(f"Warning: Stylesheet file {stylesheet_path} not found.")

    widget = MyWidget()
    widget.setWindowTitle("Irelia-DGOM")

    # Set the window icon to 'rocket-fly.png'
    icon_path = Path(__file__).parent / "icons" / "rocket-fly.png"
    if icon_path.exists():
        widget.setWindowIcon(QtGui.QIcon(str(icon_path)))
    else:
        print(f"Warning: Icon file {icon_path} not found.")

    widget.showMaximized()

    sys.exit(app.exec())
