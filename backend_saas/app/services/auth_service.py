from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.config import settings
from ..models.usuario import Usuario
from ..schemas.auth import TokenData

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera el hash de una contraseña"""
        return pwd_context.hash(password)
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[Usuario]:
        """Autentica un usuario con username y password"""
        user = db.query(Usuario).filter(Usuario.username == username, Usuario.activo == True).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.password):
            return None
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crea un token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """Verifica y decodifica un token JWT"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            empresa_id: int = payload.get("empresa_id")
            if username is None or user_id is None or empresa_id is None:
                return None
            token_data = TokenData(username=username, user_id=user_id, empresa_id=empresa_id)
            return token_data
        except JWTError:
            return None 