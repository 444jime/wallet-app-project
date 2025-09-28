from .accHandler import AccHandler
from business import UserVerifier
import pwinput

from PyQt6.QtWidgets import QApplication,QMainWindow
from .screens import Ui_MainWindow
import sys

class UserHandler(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()



