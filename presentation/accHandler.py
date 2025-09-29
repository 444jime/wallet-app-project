from business import AccVerifier
from decimal import Decimal
import time

from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QMessageBox, QDialog

from .screens import Ui_WalletApp, Ui_DepositDialog

class AccHandler(QMainWindow,Ui_WalletApp):
    def __init__(self,login_window,user):
        self.user = user
        self.verifier = AccVerifier(self.user)
        self.login_window = login_window
        super().__init__()
        self.setupUi(self)

        self.tblAccs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.actionCerrar_sesion.triggered.connect(self.logOut)
        self.loadData()
        self.btnDeposit.clicked.connect(self.deposit)

        self.show()

    def loadData(self):
        accs = self.verifier.get_all_accs()
        for acc in accs:
            row = self.tblAccs.rowCount()
            self.tblAccs.insertRow(row)
            self.tblAccs.setItem(row,0,QTableWidgetItem(acc['moneda']))
            self.tblAccs.setItem(row,1,QTableWidgetItem(str(acc['saldo'])))

    def logOut(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Cerrar sesion')
        msg_box.setText('Volvera a la pantalla de iniciar sesion.')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) 
        
        msg_box.setStyleSheet("""
            QMessageBox {
                color: #e0ffe0;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #77dd77;
                color: #1b1b1b;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a7a4a;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #2d5d2d;
            }
        """)

        rta = msg_box.exec()

        if rta == QMessageBox.StandardButton.Yes:
            self.close()
            self.login_window.show()
            
    def deposit(self):
        self.depositDialog = DepositDialog()
        self.depositDialog.exec()
        
class DepositDialog(QDialog,Ui_DepositDialog):
    def __init__(self):
        super().__init__()

    def deposit(self):
        while True:
            print('\nIngrese el monto a depositar:')
            amount = input('ARS$')
            try:
                amount = Decimal(amount)
            except:
                print("Error: Ingrese un número valido")
                continue

            try:
                current_balance = self.verifier.deposit_verify(amount)
                print(f'Monto depositado correctamente, saldo actual en ARS: {current_balance}')
                break
            except ValueError as e:
                print(f'Error: {e}')
        print('\nVolviendo al menu...')
        return     