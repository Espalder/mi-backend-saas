import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sqlite3
import hashlib
# from estilos import configurar_estilos  # Solo si se usa

class LoginWindow:
    def __init__(self, root, db_config):
        self.root = root
        self.root.title("Login - Sistema de Gestión Empresarial")
        self.root.geometry("400x300")
        self.root.configure(bg='#e6f3ff')
        self.db_config = db_config
        self.usuario = None
        self.rol = None
        self.crear_interfaz()

    def crear_interfaz(self):
        frame = tk.Frame(self.root, bg='#e6f3ff', padx=30, pady=30)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Usuario:", font=('Segoe UI', 12, 'bold'), bg='#e6f3ff').grid(row=0, column=0, sticky='e', pady=10)
        self.entry_usuario = tk.Entry(frame, font=('Segoe UI', 12))
        self.entry_usuario.grid(row=0, column=1, pady=10)
        
        tk.Label(frame, text="Contraseña:", font=('Segoe UI', 12, 'bold'), bg='#e6f3ff').grid(row=1, column=0, sticky='e', pady=10)
        self.entry_password = tk.Entry(frame, font=('Segoe UI', 12), show='*')
        self.entry_password.grid(row=1, column=1, pady=10)
        
        btn_login = tk.Button(frame, text="Iniciar Sesión", command=self.login, font=('Segoe UI', 12, 'bold'), bg='#2196F3', fg='white', relief='flat', bd=0, padx=20, pady=8)
        btn_login.grid(row=2, column=0, columnspan=2, pady=20)

    def login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        if not usuario or not password:
            messagebox.showwarning("Campos requeridos", "Ingrese usuario y contraseña")
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        # Intentar conexión MySQL primero
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "SELECT username, rol FROM usuarios WHERE username = %s AND password = %s AND activo = 1"
            cursor.execute(query, (usuario, password_hash))
            result = cursor.fetchone()
            if result:
                self.usuario, self.rol = result
                self.root.destroy()
            else:
                messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos")
            cursor.close()
            conn.close()
        except Exception:
            # Si falla MySQL, intentar SQLite
            try:
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(current_dir, 'offline_backup.db')
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                query = "SELECT username, rol FROM usuarios WHERE username = ? AND password = ? AND activo = 1"
                cursor.execute(query, (usuario, password_hash))
                result = cursor.fetchone()
                if result:
                    self.usuario, self.rol = result
                    self.root.destroy()
                else:
                    messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos")
                cursor.close()
                conn.close()
            except Exception as err:
                messagebox.showerror("Error de conexión", f"No se pudo conectar a ninguna base de datos: {err}") 