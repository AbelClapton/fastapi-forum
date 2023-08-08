from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_hash(plain_string: str, hashed_string: str) -> bool:
    return pwd_context.verify(plain_string, hashed_string)


def hash(string) -> str:
    return pwd_context.hash(string)
