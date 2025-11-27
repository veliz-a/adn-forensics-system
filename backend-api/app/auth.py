import bcrypt
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS

def hash_password(password: str) -> str:
    """Hash con bcrypt (factor 12 = ~250ms)"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed: str) -> bool:
    """Verifica password contra hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(user_id: str, email: str) -> str:
    """Genera JWT válido por 24 horas"""
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """Decodifica JWT (lanza excepción si es inválido)"""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])