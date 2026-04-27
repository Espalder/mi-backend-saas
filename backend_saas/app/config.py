import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
# Buscar en el directorio actual, en el directorio del backend y en la raíz del proyecto
load_dotenv() # Directorio actual
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(backend_root, '.env')) # Directorio backend_saas/
project_root = os.path.dirname(backend_root)
load_dotenv(os.path.join(project_root, '.env')) # Raíz del proyecto

class Settings:
    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "gateway01.us-east-1.prod.aws.tidbcloud.com")
    DB_USER: str = os.getenv("DB_USER", "MunokedkawLVEvE.root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "MRyB8oSmfK6j4Pp4")
    DB_NAME: str = os.getenv("DB_NAME", "gestion_empresas")
    DB_PORT: int = int(os.getenv("DB_PORT", "4000"))
    
    # SSL Configuration
    DB_SSL_CA: str = os.getenv("DB_SSL_CA", "")
    
    def __init__(self):
        # Si no se proporciona por env, buscar el archivo en el directorio raíz del backend
        if not self.DB_SSL_CA:
            backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cert_path = os.path.join(backend_root, "isrgrootx1.pem")
            if os.path.exists(cert_path):
                self.DB_SSL_CA = cert_path
            else:
                # Intento alternativo para entornos Docker
                self.DB_SSL_CA = "/app/isrgrootx1.pem"
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # App Configuration
    APP_NAME: str = os.getenv("APP_NAME", "Sistema de Gestión SaaS")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings() 
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_NAME = settings.DB_NAME
DB_SSL_CA = settings.DB_SSL_CA
