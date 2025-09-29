from .currencyService import CurrencyService
from decimal import Decimal
from data import DbService

class AccVerifier:
    def __init__(self,user):
        self.service = CurrencyService()
        self.dbService = DbService()
        self.user = user

    def cod_verifier(self,acc):
        acc_list = [acc.lower() for acc in self.service.get_key_list()]
        if acc.lower() in acc_list:
            return True
        else:
            raise ValueError('Moneda invalida')

    def acc_exists(self,acc):
        user = self.dbService.get_user(self.user)
        if not user:
            raise ValueError('No existe el usuario.')
        
        cuenta = self.dbService.get_acc(self.user,acc)
        if not cuenta:
            raise ValueError('No existe cuenta en esta moneda para este usuario')
        
        return True

    def get_acc_balance(self,acc):
        self.cod_verifier(acc)

        user = self.dbService.get_user(self.user)
        if not user:
            raise ValueError('No existe el usuario.')
        
        cuenta = self.dbService.get_acc(self.user,acc)
        if not cuenta:
            raise ValueError('No existe cuenta en esta moneda para este usuario')
        
        return cuenta.saldo
    
    def get_all_accs(self):    
        cuentas = self.dbService.get_acc_by_user(self.user)
        return cuentas
                
    def negative_verifier(self,amount):
        decimal = Decimal(str(amount))
        if decimal <= 0:
            raise ValueError('No se admiten valores negativos')
        
    def create_acc(self,acc):
            user = self.dbService.get_user(self.user)
            if not user:
                raise ValueError('No existe el usuario. accverf')
            
            try:
                self.dbService.get_acc(self.user,acc)
                raise ValueError('Ya existe cuenta en esta moneda para este usuario')
            except ValueError:
                self.dbService.newAcc(self.user,acc)
                return True
    
    def deposit_verify(self,amount):
        self.negative_verifier(amount)        
        nuevo_saldo = self.dbService.deposit_amount(self.user,"ARS",amount)        
        return nuevo_saldo
    
    def buy_verifier(self,acc_org,acc_dest,amount_dest):
        self.acc_exists(acc_org)
        self.acc_exists(acc_dest)
        self.negative_verifier(amount_dest)
        
        amount_dest = Decimal(amount_dest)
        rate = self.service.get_rate(acc_dest)
        required_amount = amount_dest * rate

        saldo_origen = self.get_acc_balance(acc_org)

        if saldo_origen < required_amount:
            raise ValueError('Saldo insuficiente')
        
        try:
            saldo_origen_nuevo, saldo_destino_nuevo = self.dbService.transaction(self.user,acc_org,acc_dest,Decimal(amount_dest),required_amount)
        except ValueError as e:
            raise ValueError(f'No se pudo comprar: {e}')
        
        return saldo_origen_nuevo, saldo_destino_nuevo
    
    def sell_verifier(self,acc_org,acc_dest,amount_sell):
        self.acc_exists(acc_org)
        self.acc_exists(acc_dest)
        self.negative_verifier(amount_sell)

        amount_sell = Decimal(amount_sell)
        rate = self.service.get_rate(acc_org)
        obtained_amount = amount_sell * rate

        saldo_origen = self.get_acc_balance(acc_org)

        if saldo_origen < amount_sell:
            raise ValueError('Saldo insuficiente')
        
        try:
            saldo_origen_nuevo, saldo_destino_nuevo = self.dbService.transaction(self.user,acc_org,acc_dest,amout_in=obtained_amount,amount_out=amount_sell)
        except ValueError as e:
            raise ValueError(f'No se pudo comprar: {e}')
        
        return saldo_origen_nuevo, saldo_destino_nuevo