from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)   

#this function is going to be used to verify the password that the user is trying to login with. It is going to compare the password that the user is trying to login with and the hashed password that is stored in the database. If they match, it will return True, otherwise it will return False.
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)