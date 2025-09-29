from business import AccVerifier
from decimal import Decimal
import time

from PyQt6.QtWidgets import QMainWindow
from .screens import Ui_WalletApp

class AccHandler(QMainWindow,Ui_WalletApp):
    def __init__(self,user):
        self.user = user
        super().__init__()
        self.setupUi(self)

        self.show()

