import os
import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Ajuste automático del sys.path para que los imports funcionen desde cualquier ubicación
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
for path in [current_dir, parent_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

from estilos import configurar_estilos, set_tema_global, get_tema_global, cargar_tema_desde_configuracion
from modulo_autenticacion import LoginWindow
from modulo_inventario import InventarioUI
from modulo_ventas import VentasUI
from modulo_reportes import ReportesUI
from modulo_configuracion import ConfiguracionUI
from config_bd import DB_CONFIG

ROLES_PESTANAS = {
    'admin': ['inventario', 'ventas', 'reportes', 'configuracion'],
    'vendedor': ['ventas', 'reportes'],
    'inventario': ['inventario', 'reportes']
}

class SistemaGestionApp:
    def __init__(self, usuario, rol):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión Empresarial - Módulos")
        self.root.geometry("1200x800")
        self.root.configure(bg='#e6f3ff')
        self.usuario = usuario
        self.rol = rol
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self.tema = cargar_tema_desde_configuracion()
        set_tema_global(self.tema)
        configurar_estilos(self.tema)
        self.crear_pestanas()
        self.root.mainloop()

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
        # Refrescar productos al cambiar a la pestaña de ventas
        def on_tab_changed(event):
            idx = notebook.index(notebook.select())
            if 'ventas' in pestanas and notebook.tab(idx, 'text') == "💰 Ventas":
                self.tabs['ventas'].cargar_productos_ventas()
        notebook.bind('<<NotebookTabChanged>>', on_tab_changed)

    def cambiar_tema(self, nuevo_tema):
        set_tema_global(nuevo_tema)
        messagebox.showinfo("Tema cambiado", "Por favor, reinicia la aplicación para aplicar el nuevo tema.")
        self.root.destroy()


def main():
    # Login
    login_root = tk.Tk()
    login = LoginWindow(login_root, DB_CONFIG)
    login_root.mainloop()
    if not login.usuario or not login.rol:
        return
    # Lanzar la app principal
    SistemaGestionApp(login.usuario, login.rol)

if __name__ == "__main__":
    main() 