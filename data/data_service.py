from .models import Usuarios, Cuentas
from decimal import Decimal
import sqlobject as SO

class DbService():
    def newUser(self,new_user,new_password):
        user = None
        try:
            Usuarios.selectBy(user=new_user).getOne()
            raise ValueError('Usuario existente')
        except SO.SQLObjectNotFound:
            user = Usuarios(user=new_user, password=new_password)
        return user
    

    def newAcc(self, username, currency, initial_balance=0):
        user = self.get_user(username)
        acc = Cuentas(idUser=user.id, moneda=currency, saldo=initial_balance)
        return acc
    
    def get_user(self,username):
        try:
            return Usuarios.selectBy(user=username).getOne()
        except SO.SQLObjectNotFound:
            raise ValueError('No existe el usuario')
        
    def get_acc(self,username,moneda):
        user = self.get_user(username)
        try:
            return Cuentas.selectBy(idUser=user.id, moneda=moneda).getOne()
        except (SO.SQLObjectNotFound, SO.SQLObjectIntegrityError):
            raise ValueError('No existe cuenta en esta moneda para este usuario')

    def get_acc_by_user(self,username):
        user = self.get_user(username)
        
        accs = Cuentas.selectBy(idUser = user.id)
        acc_list = [{'moneda': cuenta.moneda, 'saldo': cuenta.saldo} for cuenta in accs]
        
        if not acc_list:
            raise ValueError(f'El usuario no tiene cuentas registradas.')
        
        return acc_list
    
    def deposit_amount(self,username,acc,amount):
        try:
            user = Usuarios.selectBy(user=username).getOne()
            acc = Cuentas.selectBy(idUser=user.id, moneda=acc).getOne()
            acc.saldo = acc.saldo + Decimal(amount)
            return acc.saldo
        except SO.SQLObjectNotFound:
            raise ValueError('No se encontro la cuenta para ese usuario')
        
    def transaction(self,username,acc_org,acc_dest,amout_in,amount_out):
        user = Usuarios.selectBy(user=username).getOne()
        cuenta_origen = Cuentas.selectBy(idUser=user.id, moneda=acc_org).getOne()
        cuenta_destino = Cuentas.selectBy(idUser=user.id, moneda=acc_dest).getOne()
        
        out = cuenta_origen.saldo - Decimal(amount_out)
        inn = cuenta_destino.saldo + Decimal(amout_in)

        cuenta_destino.saldo = inn
        cuenta_origen.saldo = out

        return cuenta_origen.saldo, cuenta_destino.saldo