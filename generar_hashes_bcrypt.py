from passlib.context import CryptContext

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

usuarios = {
    "admin": "admin123",
    "vendedor1": "vendedor1",
    "inventario1": "inventario1"
}

print("Hashes bcrypt generados:")
for usuario, password in usuarios.items():
    hash_bcrypt = pwd_context.hash(password)
    print(f"{usuario}: {hash_bcrypt}") 