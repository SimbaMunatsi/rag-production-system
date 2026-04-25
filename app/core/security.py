import hashlib
import bcrypt
from datetime import datetime, timedelta
import jwt

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

def _prehash_password(password: str) -> bytes:
    """
    Hashes the raw password with SHA-256 first. 
    bcrypt requires bytes, so we encode the resulting hex string.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 1. Pre-hash the incoming password
    prehashed = _prehash_password(plain_password)
    
    # 2. bcrypt.checkpw requires bytes for both arguments
    hashed_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(prehashed, hashed_bytes)

def get_password_hash(password: str) -> str:
    # 1. Pre-hash the password
    prehashed = _prehash_password(password)
    
    # 2. Generate a secure salt and hash it using native bcrypt
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(prehashed, salt)
    
    # 3. Decode back to a standard string so SQLAlchemy can save it to the database
    return hashed_bytes.decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt