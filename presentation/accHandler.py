from .screens import Ui_WalletApp, Ui_DepositDialog, Ui_SellDialog,Ui_BuyDialog,Ui_CreateAccDialog
from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QMessageBox, QDialog
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from decimal import Decimal, ROUND_DOWN
from PyQt6.QtCore import pyqtSignal
from business import AccVerifier
import time

class AccHandler(QMainWindow,Ui_WalletApp):
    def __init__(self,login_window,user):
        super().__init__()
        self.user = user
        self.verifier = AccVerifier(self.user)
        self.login_window = login_window
        self.setupUi(self)

        self.tblAccs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.actionCerrar_sesion.triggered.connect(self.logOut)
        self.loadData()
        self.btnCreate.clicked.connect(self.createAcc)
        self.btnDeposit.clicked.connect(self.deposit)
        self.btnSell.clicked.connect(self.sell)
        self.btnBuy.clicked.connect(self.buy)
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
            
    def refresh_table(self):
        self.tblAccs.setRowCount(0)
        self.loadData()

    def deposit(self):
        self.depositDialog = DepositDialog(self.user)
        self.depositDialog.saldo_actualizado.connect(self.refresh_table)
        self.depositDialog.exec()
                
    def sell(self):
        self.sellDialog = SellDialog(self.user)
        self.sellDialog.saldo_actualizado.connect(self.refresh_table)
        self.sellDialog.exec()        
    
    def buy(self):
        self.buyDialog = BuyDialog(self.user)
        self.buyDialog.saldo_actualizado.connect(self.refresh_table)
        self.buyDialog.exec()

    def createAcc(self):
        self.createAccDialog = CreateAccDialog(self.user)
        self.createAccDialog.saldo_actualizado.connect(self.refresh_table)
        self.createAccDialog.exec()

class DepositDialog(QDialog,Ui_DepositDialog):
    saldo_actualizado = pyqtSignal()

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
            self.txtAmount.clear()
        except ValueError as e:
            self.lblValidDeposit.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidDeposit.setText(f'Error: {e}')
            self.lblValidDeposit.show()
        self.saldo_actualizado.emit()

class SellDialog(QDialog,Ui_SellDialog):
    saldo_actualizado = pyqtSignal()

    def __init__(self,user):
        super().__init__()
        self.user = user
        self.verifier = AccVerifier(user)
        self.setupUi(self)

        self.lblValidSell.hide()

        self.check_balance()
        self.btnSell.clicked.connect(self.sell)

    def check_balance(self):
        self.verifier.cod_verifier('ARS')
        saldo_cod = self.verifier.get_acc_balance('ARS')
        saldo = Decimal(saldo_cod).quantize(Decimal("0.01"),rounding=ROUND_DOWN)
        saldo = str(saldo).replace('.',',')
        self.lblBalance.setText(f"Saldo actual en ARS: \n ${saldo}")

    def sell(self):
        self.lblValidSell.hide()

        cod = self.txtCod.text().upper()

        try:
            self.verifier.cod_verifier(cod)
        except ValueError as e:
            self.lblValidSell.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidSell.setText(f'Error: {e}')
            self.lblValidSell.show()
            return

        if cod == 'ARS':
            self.lblValidSell.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidSell.setText('Ingreso invalido, no puede vender ARS.')
            self.lblValidSell.show()
            return

        amount_text = self.txtAmount.text()
        if not amount_text:
            self.lblValidSell.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidSell.setText("Error: Ingrese un número válido")
            self.lblValidSell.show()
            return
    
        try:
            amount = Decimal(amount_text.replace(',', '.'))
            saldo_origen, saldo_ARS = self.verifier.sell_verifier(cod,"ARS",amount)
            
            saldo_origen = saldo_origen.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            saldo_origen_str = str(saldo_origen).replace('.',',')
            
            saldo_ARS = saldo_ARS.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            saldo_ARS_str = str(saldo_ARS).replace('.',',')

            self.lblBalance.setText(
                f'Venta exitosa!\n Saldo actual en {cod.upper()}: {saldo_origen_str}\n' 
                f'Saldo actual en ARS: {saldo_ARS_str}'
            )
            self.txtCod.clear()
            self.txtAmount.clear()

        except ValueError as e:
            self.lblValidSell.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidSell.setText(f"Error: {e}")
            self.lblValidSell.show()
        self.saldo_actualizado.emit()

class BuyDialog(QDialog,Ui_BuyDialog):
    saldo_actualizado = pyqtSignal()

    def __init__(self,user):
        super().__init__()
        self.user = user
        self.verifier = AccVerifier(user)
        self.setupUi(self)

        self.lblValidBuy.hide()

        self.check_balance()
        self.btnBuy.clicked.connect(self.buy)

    def check_balance(self):
        self.verifier.cod_verifier('ARS')
        saldo_cod = self.verifier.get_acc_balance('ARS')
        saldo = Decimal(saldo_cod).quantize(Decimal("0.01"),rounding=ROUND_DOWN)
        saldo = str(saldo).replace('.',',')
        self.lblBalance.setText(f"Saldo actual en ARS: \n ${saldo}")

    def confirm(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Comprar moneda')
        msg_box.setText('¿Esta seguro de realizar la compra?')
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

        return msg_box.exec()

    def buy(self):
        self.lblValidBuy.hide()
        cod = self.txtCod.text().upper()

        try:
            self.verifier.cod_verifier(cod)
        except ValueError as e:
            self.lblValidBuy.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidBuy.setText(f'Error: {e}')
            self.lblValidBuy.show()
            return

        if cod == 'ARS':
            self.lblValidBuy.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidBuy.setText('Ingreso invalido, no puede comprar ARS.')            
            self.lblValidBuy.show()
            return

        amount_text = self.txtAmount.text()
        if not amount_text:
            self.lblValidBuy.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidBuy.setText("Error: Ingrese un número válido")
            self.lblValidBuy.show()
            return

        start_time = time.time()


        user_input  = self.confirm()
        if (time.time()-start_time) > 120:
            user_input=QMessageBox.StandardButton.No
            self.lblValidBuy.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidBuy.setText('Tiempo agotado, compra cancelada.')
            self.lblValidBuy.show()
            return                 
        if user_input !=  QMessageBox.StandardButton.Yes :
            self.lblValidBuy.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidBuy.setText('Compra cancelada.')
            self.lblValidBuy.show()
            return
    
        try:
            amount = Decimal(amount_text.replace(',', '.'))
            saldo_ARS, saldo_cod = self.verifier.buy_verifier("ARS",cod.upper(),amount)

            saldo_ARS = saldo_ARS.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            saldo_ARS_str = str(saldo_ARS).replace('.',',')

            saldo_cod = saldo_cod.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            saldo_cod_str = str(saldo_cod).replace('.',',')

            self.lblBalance.setText(
                f'Compra exitosa! \nSaldo actual en ARS: {saldo_ARS_str}\n'
                f'Saldo actual en {cod.upper()}: {saldo_cod_str}'
            )
            self.txtCod.clear()
            self.txtAmount.clear()

        except ValueError as e:
            self.lblValidBuy.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidBuy.setText(f"Error: {e}")
            self.lblValidBuy.show()
        self.saldo_actualizado.emit()

class CreateAccDialog(QDialog,Ui_CreateAccDialog):
    saldo_actualizado = pyqtSignal()

    def __init__(self,user):
        super().__init__()
        self.user = user
        self.verifier = AccVerifier(user)
        self.setupUi(self)

        self.lblValidAcc.hide()

        self.btnCrear.clicked.connect(self.create_acc)

    def create_acc(self):
        cod = self.txtCod.text()

        try:
            self.verifier.cod_verifier(cod)
            self.verifier.create_acc(cod.upper())
            self.lblValidAcc.setStyleSheet(
                "color: #77dd77; font-size: 15px; font-weight: bold; font-family: Segoe UI; letter-spacing: 0.5px;"
            )
            self.lblValidAcc.setText('Cuenta creada correctamente')
            self.lblValidAcc.show()
        except ValueError as e:
            self.lblValidAcc.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #ff5555;"
            )
            self.lblValidAcc.setText(f"Error: {e}")
            self.lblValidAcc.show()
        self.saldo_actualizado.emit()