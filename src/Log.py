import asyncio
from threading import Thread
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextOption
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QWidget


class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.QUEUE = []
        self.thread = Thread(target=self._log)
        self.setWindowTitle("Log")
        self.setGeometry(0, 0, 500, 500)
        self.logger = QTextEdit(self)
        self.logger.setReadOnly(True)
        self.logger.setFont(QFont("Arial", 12))
        self.logger.setLineWrapMode(QTextEdit.NoWrap)
        self.logger.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.logger.setWordWrapMode(QTextOption.NoWrap)
        self.logger.setGeometry(0, 0, 500, 500)
        self.move(1000, 0)
        self.thread.start()
        self.show()

    def log(self, text: str) -> None:
        self.QUEUE.append(text)
        print(len(self.QUEUE))

    def _log(self) -> None:
        while True:
            if len(self.QUEUE) > 0:
                # Show text from queue in logger and clear queue
                self.logger.setText(f"{self.logger.toPlainText()}\n{self.QUEUE.pop(0)}")
            self.update()
            sleep(1/144)

    def update(self) -> None:
        super().update()
        self.repaint()
