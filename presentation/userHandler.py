from PyQt6.QtWidgets import QApplication,QMainWindow,QLineEdit,QDialog
from .screens import Ui_Login, Ui_CreateUserDialog
from .accHandler import AccHandler
from business import UserVerifier


class UserHandler(QMainWindow,Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lblValidUser.hide()
        self.btnCreateUser.clicked.connect(self.createUser)
        self.btnShowPwd.clicked.connect(self.showPwd)
        self.btnLogin.clicked.connect(self.login)
        self.pwd_visible = False

        self.show()

        self.verifier = UserVerifier()

    def login(self):
        user = self.txtUser.text()
        pwd = self.txtPassword.text()

        self.lblValidUser.hide()
        try:
            self.verifier.verificar_login(user,pwd)
            self.hide()
            self.WalletApp = AccHandler(user)
            self.WalletApp.show()
        except ValueError as e:
            self.lblValidUser.show()
            self.lblValidUser.setText(f"Error: {e}. \nIntentelo nuevamente")

    def showPwd(self):
        if self.pwd_visible:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.pwd_visible = False
        else:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.pwd_visible = True

    def createUser(self): 
        self.dialog = CreateUserDialog()
        self.dialog.exec()
        
    
class CreateUserDialog(QDialog,Ui_CreateUserDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

