from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class HashClass():
    def bcrypt(password : str):
        hashedPassword = pwd_context.hash(password)
        return hashedPassword
        
