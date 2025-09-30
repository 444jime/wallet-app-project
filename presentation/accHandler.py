from business import AccVerifier
from decimal import Decimal, ROUND_DOWN, InvalidOperation
import time

from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QMessageBox, QDialog
from PyQt6.QtGui import QIntValidator, QDoubleValidator
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

            saldo = Decimal(acc['saldo']).quantize(Decimal("0.01"),rounding=ROUND_DOWN)
            saldo = str(saldo).replace('.',',')
            self.tblAccs.setItem(row,1,QTableWidgetItem(f"${saldo}"))

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
        self.depositDialog = DepositDialog(self.user)
        self.depositDialog.exec()
        
class DepositDialog(QDialog,Ui_DepositDialog):
    def __init__(self,user):
        super().__init__()
        self.user = user
        self.verifier = AccVerifier(user)
        self.setupUi(self)
        self.txtAmount.setValidator(QIntValidator(0,10000))
        self.txtAmount.setValidator(QDoubleValidator(0.0,9999.99,2))
        self.check_balance()
        self.btnDeposit.clicked.connect(self.deposit)

    def check_balance(self):
        self.lblValidDeposit.hide()
        self.verifier.cod_verifier('ARS')
        saldo_cod = self.verifier.get_acc_balance('ARS')
        saldo = Decimal(saldo_cod).quantize(Decimal("0.01"),rounding=ROUND_DOWN)
        saldo = str(saldo).replace('.',',')
        self.lblBalance.setText(f"Saldo actual: \n ${saldo}")

    def deposit(self):
        self.lblValidDeposit.hide()
        amount_text = self.txtAmount.text()

        if not amount_text:
            self.lblValidDeposit.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidDeposit.setText("Error: Ingrese un número válido")
            self.lblValidDeposit.show()
            return
        try:
            amount = Decimal(amount_text.replace(',', '.'))
            current_balance = self.verifier.deposit_verify(amount)
            current_balance = current_balance.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            balance_str = str(current_balance).replace('.', ',')
            self.lblBalance.setText(f'Monto depositado correctamente, saldo actual en ARS: {balance_str}')
        except ValueError as e:
            self.lblValidDeposit.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidDeposit.setText(f'Error: {e}')
            self.lblValidDeposit.show()