import sys
from pathlib import Path

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PySide6.QtCore import Qt


class MACRMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MACR - Materials Analysis and Computation Runtime")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("MACR GUI")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(header)

        # Content area (placeholder)
        content_layout = QHBoxLayout()
        content_layout.addWidget(QLabel("Welcome to MACR"))
        main_layout.addLayout(content_layout)

        # Button area
        button_layout = QHBoxLayout()
        new_button = QPushButton("New Project")
        open_button = QPushButton("Open Project")
        button_layout.addWidget(new_button)
        button_layout.addWidget(open_button)

        main_layout.addLayout(button_layout)

        # Editable Inputs
        input_layout = QVBoxLayout()
        self.dx_input = self._create_input_field("dx:", input_layout, QIntValidator())
        self.dy_input = self._create_input_field("dy:", input_layout, QIntValidator())

        main_layout.addLayout(input_layout)
        main_layout.addStretch()

    def _create_input_field(
        self, label_text: str, parent_layout: QVBoxLayout, validator=None
    ) -> QLineEdit:
        """Create a labeled input field with optional validator."""
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel(label_text))

        input_field = QLineEdit()
        if validator:
            input_field.setValidator(validator)
        h_layout.addWidget(input_field)

        parent_layout.addLayout(h_layout)
        return input_field


def main():
    app = QApplication(sys.argv)
    window = MACRMainWindow()
    window.show()
    sys.exit(app.exec())


def new_main():
    from main_2 import Ui_MainWindow

    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    new_main()
