from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextOption
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QWidget


class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log")
        self.setGeometry(0, 0, 500, 500)
        self.logger = QTextEdit(self)
        self.logger.setReadOnly(True)
        self.logger.setFont(QFont("Arial", 12))
        self.logger.setLineWrapMode(QTextEdit.NoWrap)
        self.logger.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.logger.setWordWrapMode(QTextOption.NoWrap)
        self.logger.setGeometry(0, 0, 500, 500)
        self.move(1000,0)
        self.show()

    def log(self, text: str) -> None:
        # Get the current text
        self.logger.setText(f"{self.logger.toPlainText()}\n{text}")
        self.logger.moveCursor(self.logger.textCursor().End)
        self.update()

    def update(self) -> None:
        super().update()
        self.repaint()
