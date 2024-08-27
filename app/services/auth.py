from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"])

def get_hashed_password(raw_password:str):
    return bcrypt_context.hash(raw_password)

def verify_password(raw_password, hashed_password):
    return bcrypt_context.verify(raw_password, hashed_password)