"""
Configuración de base de datos - Cambiar entre local y remota
"""
import os
from dotenv import load_dotenv

# Intentar cargar variables de entorno desde el archivo .env en la raíz del proyecto
# Se busca en el directorio actual y en el directorio padre
load_dotenv() # Busca en el directorio actual
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path) # Busca en el directorio raíz del proyecto

# Configuración para base de datos LOCAL
DB_CONFIG_LOCAL = {
    'host': os.getenv('DB_HOST_LOCAL', 'localhost'),
    'user': os.getenv('DB_USER_LOCAL', 'root'),
    'password': os.getenv('DB_PASSWORD_LOCAL', 'KV7$LU%9k&tQ#ayU'),
    'database': os.getenv('DB_NAME_LOCAL', 'gestion_empresas'),
    'port': int(os.getenv('DB_PORT_LOCAL', 3306))
}

# Configuración para base de datos REMOTA (TiDB Cloud)
DB_CONFIG_REMOTE = {
    'host': os.getenv('DB_HOST', 'gateway01.us-east-1.prod.aws.tidbcloud.com'),
    'user': os.getenv('DB_USER', 'MunokedkawLVEvE.root'),
    'password': os.getenv('DB_PASSWORD', 'MRyB8oSmfK6j4Pp4'),
    'database': os.getenv('DB_NAME', 'gestion_empresas'),
    'port': int(os.getenv('DB_PORT', 4000)),
    'ssl_verify_cert': True,
    'ssl_ca': os.path.join(os.path.dirname(os.path.abspath(__file__)), os.getenv('DB_SSL_CA', 'isrgrootx1.pem'))
}

# Configuración actual - Cambia esto para usar local o remota
USAR_BD_LOCAL = False  # Cambia a False para usar la BD remota

def get_db_config():
    """Obtener configuración de base de datos según la configuración actual"""
    if USAR_BD_LOCAL:
        return DB_CONFIG_LOCAL
    else:
        return DB_CONFIG_REMOTE

def get_db_type():
    """Obtener tipo de base de datos actual"""
    return "LOCAL" if USAR_BD_LOCAL else "REMOTA"

# Configuración actual
DB_CONFIG = get_db_config()
