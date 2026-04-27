import requests
import time
import schedule
from datetime import datetime

# URL de tu backend en Render
BACKEND_URL = "https://mi-backend-saas.onrender.com"

def ping_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now()}] ✅ Ping exitoso - Backend activo")
        else:
            print(f"[{datetime.now()}] ⚠️ Ping con status {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error en ping: {e}")

def main():
    print("🤖 Iniciando Keep Alive para Render...")
    print(f"🎯 URL objetivo: {BACKEND_URL}")
    print("⏰ Ping cada 10 minutos")
    
    # Programar ping cada 10 minutos
    schedule.every(10).minutes.do(ping_backend)
    
    # Hacer primer ping inmediatamente
    ping_backend()
    
    # Mantener el script corriendo
    while True:
        schedule.run_pending()
        time.sleep(60)  # Revisar cada minuto

if __name__ == "__main__":
    main() 