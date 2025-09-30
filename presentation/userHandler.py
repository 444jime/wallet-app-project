from PyQt6.QtWidgets import QMainWindow,QLineEdit,QDialog
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
            self.WalletApp = AccHandler(self,user)
            self.WalletApp.show()
            self.txtPassword.clear()
        except ValueError as e:
            self.lblValidUser.show()
            self.lblValidUser.setText(f"Error: {e}. \nIntentelo nuevamente.")

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
        self.lblValidUser.hide()
        self.btnCreateUser.clicked.connect(self.create_user)

        self.btnShowPwd.clicked.connect(self.showPwd)
        self.pwd_visible = False

        self.verifier = UserVerifier()

    def create_user(self):     
        try:
            user = self.txtUser.text()
            password = self.txtPassword.text()
            pwd_confirm = self.txtPassword_2.text()

            self.verifier.pwd_match(password,pwd_confirm)                
            self.verifier.create_user(user,password)

            self.lblValidUser.show()
            self.lblValidUser.setStyleSheet("font-size: 15px; font-weight: bold; color:green;")
            self.lblValidUser.setText("Usuario y cuenta en ARS creados correctamente.")
            
            self.txtUser.clear()
            self.txtPassword.clear()
            self.txtPassword_2.clear()
        except ValueError as e:
            self.lblValidUser.show()
            self.lblValidUser.setStyleSheet("font-size: 15px; font-weight: bold; color: #ff5555;")
            self.lblValidUser.setText(f"Error: {e}. \nIntentelo nuevamente.")

    def showPwd(self):
        if self.pwd_visible:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.txtPassword_2.setEchoMode(QLineEdit.EchoMode.Password)
            self.pwd_visible = False
        else:
            self.txtPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.txtPassword_2.setEchoMode(QLineEdit.EchoMode.Normal)
            self.pwd_visible = True