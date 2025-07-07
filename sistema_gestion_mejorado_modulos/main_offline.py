import os
import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sqlite3
import threading
import time

# Ajuste automático del sys.path para que los imports funcionen desde cualquier ubicación
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from estilos import configurar_estilos, set_tema_global, get_tema_global, cargar_tema_desde_configuracion
from modulo_autenticacion import LoginWindow
from modulo_inventario import InventarioUI
from modulo_ventas import VentasUI
from modulo_reportes import ReportesUI
from modulo_configuracion import ConfiguracionUI

DB_CONFIG = {
    'host': 'hopper.proxy.rlwy.net',
    'user': 'root',
    'password': 'bLFNXiHRbOvKNRHbMPwZXJPeCmjGTAtK',
    'database': 'railway',
    'port': 57218
}

ROLES_PESTANAS = {
    'admin': ['inventario', 'ventas', 'reportes', 'configuracion'],
    'vendedor': ['ventas', 'reportes'],
    'inventario': ['inventario', 'reportes']
}

SQLITE_DB = os.path.join(current_dir, 'offline_backup.db')

class SistemaGestionAppOffline:
    def __init__(self, usuario, rol):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión Empresarial - Modo Offline/Online")
        self.root.geometry("1200x800")
        self.root.configure(bg='#e6f3ff')
        self.usuario = usuario
        self.rol = rol
        self.online = self.check_online()
        self.indicador_modo = tk.Label(self.root, text="", font=("Segoe UI", 10, "bold"), bg="#e6f3ff")
        self.indicador_modo.pack(side="top", anchor="ne", padx=10, pady=5)
        if self.online:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            self.indicador_modo.config(text="🟢 Modo Online (Railway)", fg="green")
        else:
            self.conn = sqlite3.connect(SQLITE_DB)
            self.cursor = self.conn.cursor()
            self.setup_sqlite()
            self.indicador_modo.config(text="🔴 Modo Offline (SQLite local)", fg="red")
        self.tema = cargar_tema_desde_configuracion()
        set_tema_global(self.tema)
        configurar_estilos(self.tema)
        self.tabs = {}
        self.crear_pestanas()
        self._last_online_state = self.online
        # Lanzar hilo para monitorear reconexión y sincronizar automáticamente
        self.monitor_thread = threading.Thread(target=self.monitor_reconexion, daemon=True)
        self.monitor_thread.start()
        self.root.mainloop()

    def check_online(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            conn.close()
            return True
        except Exception:
            return False

    def setup_sqlite(self):
        # Crear todas las tablas necesarias en SQLite si no existen
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            activo INTEGER DEFAULT 1,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            sincronizado INTEGER DEFAULT 0
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            sincronizado INTEGER DEFAULT 0
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL,
            activo INTEGER DEFAULT 1,
            sincronizado INTEGER DEFAULT 0
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            cliente_id INTEGER,
            usuario_id INTEGER,
            subtotal REAL,
            descuento REAL,
            total REAL,
            estado TEXT,
            sincronizado INTEGER DEFAULT 0,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER,
            precio_unitario REAL,
            subtotal REAL,
            sincronizado INTEGER DEFAULT 0,
            FOREIGN KEY(venta_id) REFERENCES ventas(id),
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )''')
        self.conn.commit()

    def crear_pestanas(self):
        notebook = tk.ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)
        pestanas = ROLES_PESTANAS.get(self.rol, [])
        self.tabs = {}
        if 'inventario' in pestanas:
            tab_inv = tk.ttk.Frame(notebook)
            notebook.add(tab_inv, text="📦 Inventario")
            self.tabs['inventario'] = InventarioUI(tab_inv, self.conn, self.cursor, self.rol, self.tema)
        if 'ventas' in pestanas:
            tab_ventas = tk.ttk.Frame(notebook)
            notebook.add(tab_ventas, text="💰 Ventas")
            self.tabs['ventas'] = VentasUI(tab_ventas, self.conn, self.cursor, self.rol, self.tema)
        if 'reportes' in pestanas:
            tab_reportes = tk.ttk.Frame(notebook)
            notebook.add(tab_reportes, text="📊 Reportes")
            self.tabs['reportes'] = ReportesUI(tab_reportes, self.conn, self.cursor, self.rol, self.tema)
        if 'configuracion' in pestanas:
            tab_config = tk.ttk.Frame(notebook)
            notebook.add(tab_config, text="⚙️ Configuración")
            self.tabs['configuracion'] = ConfiguracionUI(tab_config, self.conn, self.cursor, self.rol, self.tema, self.cambiar_tema)
        def on_tab_changed(event):
            idx = notebook.index(notebook.select())
            if 'ventas' in pestanas and notebook.tab(idx, 'text') == "💰 Ventas":
                self.tabs['ventas'].cargar_productos_ventas()
        notebook.bind('<<NotebookTabChanged>>', on_tab_changed)

    def cambiar_tema(self, nuevo_tema):
        set_tema_global(nuevo_tema)
        messagebox.showinfo("Tema cambiado", "Por favor, reinicia la aplicación para aplicar el nuevo tema.")
        self.root.destroy()

    def monitor_reconexion(self):
        while True:
            time.sleep(10)  # Chequear cada 10 segundos
            online = self.check_online()
            if online and not self._last_online_state:
                self._last_online_state = True
                def online_actions():
                    self.indicador_modo.config(text="🟢 Modo Online (Railway)", fg="green")
                    self.sincronizar_bidireccional()
                    messagebox.showinfo("Conexión restablecida", "¡Conexión restablecida! Los datos han sido sincronizados automáticamente entre local y nube.")
                self.root.after(0, online_actions)
            elif not online and self._last_online_state:
                self._last_online_state = False
                def offline_actions():
                    self.indicador_modo.config(text="🔴 Modo Offline (SQLite local)", fg="red")
                    messagebox.showwarning("Sin conexión", "Se ha perdido la conexión. Ahora trabajas en modo offline.")
                self.root.after(0, offline_actions)

    def sincronizar_bidireccional(self):
        try:
            # Conectar a MySQL
            conn_mysql = mysql.connector.connect(**DB_CONFIG)
            cursor_mysql = conn_mysql.cursor()
            # --- SUBIR DATOS LOCALES PENDIENTES A LA NUBE ---
            # Productos
            self.cursor.execute("SELECT codigo, nombre, descripcion, precio, stock, activo FROM productos WHERE sincronizado = 0")
            productos = self.cursor.fetchall()
            for prod in productos:
                cursor_mysql.execute("""
                    INSERT INTO productos (codigo, nombre, descripcion, precio, stock, activo)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), descripcion=VALUES(descripcion), precio=VALUES(precio), stock=VALUES(stock), activo=VALUES(activo)
                """, prod)
            self.cursor.execute("UPDATE productos SET sincronizado = 1 WHERE sincronizado = 0")
            self.conn.commit()
            # Clientes
            self.cursor.execute("SELECT nombre FROM clientes WHERE sincronizado = 0")
            clientes = self.cursor.fetchall()
            for cli in clientes:
                cursor_mysql.execute("INSERT IGNORE INTO clientes (nombre) VALUES (%s)", cli)
            self.cursor.execute("UPDATE clientes SET sincronizado = 1 WHERE sincronizado = 0")
            self.conn.commit()
            # Usuarios
            self.cursor.execute("SELECT username, password, nombre, rol, activo FROM usuarios WHERE sincronizado = 0")
            usuarios = self.cursor.fetchall()
            for usr in usuarios:
                cursor_mysql.execute("""
                    INSERT INTO usuarios (username, password, nombre, rol, activo)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE password=VALUES(password), nombre=VALUES(nombre), rol=VALUES(rol), activo=VALUES(activo)
                """, usr)
            self.cursor.execute("UPDATE usuarios SET sincronizado = 1 WHERE sincronizado = 0")
            self.conn.commit()
            # Ventas
            self.cursor.execute("SELECT fecha, cliente_id, usuario_id, subtotal, descuento, total, estado FROM ventas WHERE sincronizado = 0")
            ventas = self.cursor.fetchall()
            for venta in ventas:
                cursor_mysql.execute("""
                    INSERT INTO ventas (fecha, cliente_id, usuario_id, subtotal, descuento, total, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, venta)
            self.cursor.execute("UPDATE ventas SET sincronizado = 1 WHERE sincronizado = 0")
            self.conn.commit()
            # Detalle ventas
            self.cursor.execute("SELECT venta_id, producto_id, cantidad, precio_unitario, subtotal FROM detalle_ventas WHERE sincronizado = 0")
            detalles = self.cursor.fetchall()
            for det in detalles:
                cursor_mysql.execute("""
                    INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, det)
            self.cursor.execute("UPDATE detalle_ventas SET sincronizado = 1 WHERE sincronizado = 0")
            self.conn.commit()
            conn_mysql.commit()
            # --- DESCARGAR CAMBIOS RECIENTES DE LA NUBE A LOCAL ---
            # Productos
            cursor_mysql.execute("SELECT codigo, nombre, descripcion, precio, stock, activo FROM productos")
            productos_nube = cursor_mysql.fetchall()
            for prod in productos_nube:
                self.cursor.execute("SELECT id FROM productos WHERE codigo = ?", (prod[0],))
                existe = self.cursor.fetchone()
                if existe:
                    self.cursor.execute("UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=?, activo=?, sincronizado=1 WHERE codigo=?", (prod[1], prod[2], prod[3], prod[4], prod[5], prod[0]))
                else:
                    self.cursor.execute("INSERT INTO productos (codigo, nombre, descripcion, precio, stock, activo, sincronizado) VALUES (?, ?, ?, ?, ?, ?, 1)", prod)
            # Clientes
            cursor_mysql.execute("SELECT nombre FROM clientes")
            clientes_nube = cursor_mysql.fetchall()
            for cli in clientes_nube:
                self.cursor.execute("SELECT id FROM clientes WHERE nombre = ?", (cli[0],))
                if not self.cursor.fetchone():
                    self.cursor.execute("INSERT INTO clientes (nombre, sincronizado) VALUES (?, 1)", (cli[0],))
            # Usuarios
            cursor_mysql.execute("SELECT username, password, nombre, rol, activo FROM usuarios")
            usuarios_nube = cursor_mysql.fetchall()
            for usr in usuarios_nube:
                self.cursor.execute("SELECT id FROM usuarios WHERE username = ?", (usr[0],))
                if existe:
                    self.cursor.execute("UPDATE usuarios SET password=?, nombre=?, rol=?, activo=?, sincronizado=1 WHERE username=?", (usr[1], usr[2], usr[3], usr[4], usr[0]))
                else:
                    self.cursor.execute("INSERT INTO usuarios (username, password, nombre, rol, activo, sincronizado) VALUES (?, ?, ?, ?, ?, 1)", usr)
            # Ventas
            cursor_mysql.execute("SELECT id, fecha, cliente_id, usuario_id, subtotal, descuento, total, estado FROM ventas")
            ventas_nube = cursor_mysql.fetchall()
            for venta in ventas_nube:
                self.cursor.execute("SELECT id FROM ventas WHERE id = ?", (venta[0],))
                if not self.cursor.fetchone():
                    self.cursor.execute("INSERT INTO ventas (id, fecha, cliente_id, usuario_id, subtotal, descuento, total, estado, sincronizado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)", venta)
            # Detalle ventas
            cursor_mysql.execute("SELECT id, venta_id, producto_id, cantidad, precio_unitario, subtotal FROM detalle_ventas")
            detalles_nube = cursor_mysql.fetchall()
            for det in detalles_nube:
                self.cursor.execute("SELECT id FROM detalle_ventas WHERE id = ?", (det[0],))
                if not self.cursor.fetchone():
                    self.cursor.execute("INSERT INTO detalle_ventas (id, venta_id, producto_id, cantidad, precio_unitario, subtotal, sincronizado) VALUES (?, ?, ?, ?, ?, ?, 1)", det)
            self.conn.commit()
            cursor_mysql.close()
            conn_mysql.close()
        except Exception as e:
            messagebox.showerror("Error de sincronización", f"Ocurrió un error al sincronizar: {e}")

def main():
    # Login
    login_root = tk.Tk()
    login = LoginWindow(login_root, DB_CONFIG)
    login_root.mainloop()
    if not login.usuario or not login.rol:
        return
    # Lanzar la app principal
    SistemaGestionAppOffline(login.usuario, login.rol)

if __name__ == "__main__":
    main() 