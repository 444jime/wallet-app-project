from presentation import UserHandler
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication([])
    ventana = UserHandler()
    sys.exit(app.exec())