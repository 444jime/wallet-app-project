from data import DbService
import bcrypt

class UserVerifier:
    def __init__(self):
        self.dbService = DbService()

    def valid_entry(self,entry):
        #agregar validacion como q sea solo alfanumerico
        if len(entry) == 0:
            raise ValueError ('Ningun campo puede estar vacio')

    def pwd_match(self,pwd,pwd2):
        if pwd == pwd2:
            return True
        else:
            raise ValueError ('Las contrsaeñas no coinciden')        

    def hash_password(self,password):
        return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

    def create_user(self,user,pwd):
        self.valid_entry(user)
        self.valid_entry(pwd)
        password = self.hash_password(pwd)
        self.dbService.newUser(user,password)

        self.dbService.newAcc(user,"ARS")

    def verificar_login(self,username,pwd):
        self.valid_entry(username)
        self.valid_entry(pwd)
        user = self.dbService.get_user(username)
        if not bcrypt.checkpw(pwd.encode(),user.password.encode()):
            raise ValueError('Contraseña incorrecta')
        return True 