import os
import sqlobject as SO
from dotenv import load_dotenv
from sqlobject import DecimalCol

load_dotenv()

database = os.getenv("DATABASE_CONNECTION")

__connection__ = SO.connectionForURI(database)

class Usuarios(SO.SQLObject):
    user = SO.StringCol(length = 40, varchar = True)
    password =  SO.StringCol(length = 100, varchar = True)

class Cuentas(SO.SQLObject):
    idUser = SO.ForeignKey('Usuarios', default = None, cascade = True)
    moneda =  SO.StringCol(length = 40, varchar = True)
    saldo = DecimalCol(size = 12, precision = 4)

Usuarios.createTable(ifNotExists=True)
Cuentas.createTable(ifNotExists=True)