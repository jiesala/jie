from passlib.context import CryptContext

#密码加密
password_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def get_hash_password(password:str):
    return password_context.hash(password)

#密码验证
def verify_password(plain_password,hashed_password):
    return password_context.verify(plain_password,hashed_password)
