# main_offline.py
import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
import sqlite3
import threading
import time
import json
import hashlib
import gzip
from datetime import datetime, timedelta
import webbrowser

# Ajuste automático del sys.path para que los imports funcionen desde cualquier ubicación
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Importar módulos locales
try:
    from estilos import configurar_estilos, set_tema_global, get_tema_global, cargar_tema_desde_configuracion, get_colores_tema
    from modulo_autenticacion import LoginWindow
    from modulo_inventario import InventarioUI
    from modulo_ventas import VentasUI
    from modulo_reportes import ReportesUI
    from modulo_configuracion import ConfiguracionUI
    from config_bd import DB_CONFIG, get_db_type
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)

# La configuración de BD ahora se importa desde config_bd.py

ROLES_PESTANAS = {
    'admin': ['inventario', 'ventas', 'reportes', 'configuracion'],
    'vendedor': ['ventas', 'reportes'],
    'inventario': ['inventario', 'reportes']
}

SQLITE_DB = os.path.join(current_dir, 'offline_backup.db')

class SistemaGestionAppOffline:
    def __init__(self, usuario, rol):
        self.root = tk.Tk()
        self.root.title(f"🚀 Sistema de Gestión Empresarial - BD {get_db_type()} v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#e6f3ff')
        self.root.minsize(1200, 800)
        
        # Configurar icono de la ventana
        try:
            self.root.iconbitmap(os.path.join(current_dir, 'logo_empresa.ico'))
        except:
            pass
            
        self.usuario = usuario
        self.rol = rol
        self.online = self.check_online()
        self.ultima_sincronizacion = None
        self.historial_cambios = []
        
        # Barra de estado mejorada
        self.crear_barra_estado()
        
        # Configurar eventos de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        
        # Lanzar hilos para tareas automáticas
        self.monitor_thread = threading.Thread(target=self.monitor_reconexion, daemon=True)
        self.monitor_thread.start()
        
        self.tareas_automaticas_thread = threading.Thread(target=self.tareas_automaticas, daemon=True)
        self.tareas_automaticas_thread.start()
        
        # Verificar stock bajo al iniciar
        self.verificar_stock_bajo_automatico()
        
        self.root.mainloop()

    def check_online(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            conn.close()
            return True
        except Exception:
            return False

    def crear_barra_estado(self):
        """Crear barra de estado mejorada con información del sistema"""
        self.barra_estado = tk.Frame(self.root, bg='#2c3e50', height=30)
        self.barra_estado.pack(side='bottom', fill='x')
        
        # Información del usuario
        self.label_usuario = tk.Label(self.barra_estado, text=f"👤 {self.usuario} ({self.rol})", 
                                     font=("Segoe UI", 9), bg='#2c3e50', fg='white')
        self.label_usuario.pack(side='left', padx=10, pady=5)
        
        # Indicador de modo
        self.indicador_modo = tk.Label(self.barra_estado, text="", font=("Segoe UI", 9, "bold"), 
                                      bg='#2c3e50', fg='white')
        self.indicador_modo.pack(side='right', padx=10, pady=5)
        
        # Información de sincronización
        self.label_sync = tk.Label(self.barra_estado, text="🔄 Última sync: Nunca", 
                                  font=("Segoe UI", 9), bg='#2c3e50', fg='white')
        self.label_sync.pack(side='right', padx=10, pady=5)
        
        # Botón de sincronización manual
        self.btn_sync = tk.Button(self.barra_estado, text="🔄 Sincronizar", 
                                 command=self.sincronizar_manual, font=("Segoe UI", 8),
                                 bg='#3498db', fg='white', relief='flat', bd=0, padx=10)
        self.btn_sync.pack(side='right', padx=5, pady=5)

    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres cerrar la aplicación?"):
            try:
                if hasattr(self, 'conn'):
                    self.conn.close()
                self.root.destroy()
            except Exception as e:
                print(f"Error al cerrar: {e}")
                self.root.destroy()

    def sincronizar_manual(self):
        """Sincronización manual con feedback visual"""
        self.btn_sync.config(text="🔄 Sincronizando...", state='disabled')
        self.root.update()
        
        try:
            if self.online:
                self.sincronizar_bidireccional()
                self.ultima_sincronizacion = datetime.now()
                self.label_sync.config(text=f"🔄 Última sync: {self.ultima_sincronizacion.strftime('%H:%M:%S')}")
                messagebox.showinfo("Sincronización", "✅ Datos sincronizados exitosamente")
            else:
                messagebox.showwarning("Sin conexión", "❌ No hay conexión a internet para sincronizar")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error en sincronización: {e}")
        finally:
            self.btn_sync.config(text="🔄 Sincronizar", state='normal')

    def setup_sqlite(self):
        # Crear todas las tablas necesarias en SQLite si no existen
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            stock_minimo INTEGER DEFAULT 5,
            categoria TEXT DEFAULT 'General',
            activo INTEGER DEFAULT 1,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
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
        
        # Tabla de auditoría para historial de cambios
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabla TEXT NOT NULL,
            accion TEXT NOT NULL,
            registro_id INTEGER,
            datos_anteriores TEXT,
            datos_nuevos TEXT,
            usuario TEXT NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            sincronizado INTEGER DEFAULT 0
        )''')
        
        # Tabla de configuración del sistema
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS configuracion_sistema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clave TEXT UNIQUE NOT NULL,
            valor TEXT NOT NULL,
            descripcion TEXT,
            fecha_modificacion TEXT DEFAULT CURRENT_TIMESTAMP,
            sincronizado INTEGER DEFAULT 0
        )''')
        
        # Tabla de notificaciones
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            tipo TEXT DEFAULT 'info',
            leida INTEGER DEFAULT 0,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            sincronizado INTEGER DEFAULT 0
        )''')
        
        # Insertar configuración por defecto
        self.cursor.execute('''INSERT OR IGNORE INTO configuracion_sistema (clave, valor, descripcion) VALUES 
            ('alerta_stock_minimo', '5', 'Nivel mínimo de stock para alertas'),
            ('tema_aplicacion', 'claro', 'Tema visual de la aplicación'),
            ('auto_sync_interval', '300', 'Intervalo de sincronización automática en segundos'),
            ('backup_automatico', '1', 'Habilitar respaldo automático')
        ''')
        
        self.conn.commit()

    def crear_pestanas(self):
        notebook = tk.ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)
        pestanas = ROLES_PESTANAS.get(self.rol, [])
        self.tabs = {}
        
        # Agregar pestana de Dashboard para todos los usuarios
        tab_dashboard = tk.ttk.Frame(notebook)
        notebook.add(tab_dashboard, text="🏠 Dashboard")
        self.tabs['dashboard'] = self.crear_dashboard(tab_dashboard)
        
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
        
        # Agregar pestana de notificaciones para todos los usuarios
        tab_notificaciones = tk.ttk.Frame(notebook)
        notebook.add(tab_notificaciones, text="🔔 Notificaciones")
        self.tabs['notificaciones'] = self.crear_notificaciones(tab_notificaciones)
        
        # Agregar pestana de gráficos para todos los usuarios
        tab_graficos = tk.ttk.Frame(notebook)
        notebook.add(tab_graficos, text="📈 Gráficos")
        self.tabs['graficos'] = self.crear_graficos(tab_graficos)
        
        def on_tab_changed(event):
            idx = notebook.index(notebook.select())
            tab_text = notebook.tab(idx, 'text')
            if 'ventas' in pestanas and tab_text == "💰 Ventas":
                self.tabs['ventas'].cargar_productos_ventas()
            elif tab_text == "🏠 Dashboard":
                self.actualizar_dashboard()
            elif tab_text == "🔔 Notificaciones":
                self.actualizar_notificaciones()
            elif tab_text == "📈 Gráficos":
                self.actualizar_graficos()
                
        notebook.bind('<<NotebookTabChanged>>', on_tab_changed)

    def crear_dashboard(self, parent):
        """Crear dashboard con estadísticas del sistema"""
        c = get_colores_tema(self.tema)
        
        # Frame principal
        main_frame = tk.Frame(parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        titulo = tk.Label(main_frame, text="🏠 Dashboard del Sistema", 
                         font=('Segoe UI', 16, 'bold'), bg=c['bg'], fg=c['fg'])
        titulo.pack(pady=(0, 20))
        
        # Frame de estadísticas
        stats_frame = tk.Frame(main_frame, bg=c['bg'])
        stats_frame.pack(fill='x', pady=10)
        
        # Crear widgets de estadísticas
        self.stats_widgets = {}
        stats_info = [
            ("📦", "Total Productos", "productos"),
            ("💰", "Ventas Hoy", "ventas_hoy"),
            ("👥", "Total Clientes", "clientes"),
            ("📊", "Stock Bajo", "stock_bajo")
        ]
        
        for i, (icono, titulo, key) in enumerate(stats_info):
            frame_stat = tk.Frame(stats_frame, bg=c['frame_bg'], relief='raised', bd=2)
            frame_stat.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
            
            tk.Label(frame_stat, text=icono, font=('Segoe UI', 24), 
                    bg=c['frame_bg'], fg=c['accent']).pack(pady=5)
            tk.Label(frame_stat, text=titulo, font=('Segoe UI', 10, 'bold'), 
                    bg=c['frame_bg'], fg=c['fg']).pack()
            
            self.stats_widgets[key] = tk.Label(frame_stat, text="0", font=('Segoe UI', 18, 'bold'), 
                                             bg=c['frame_bg'], fg=c['accent'])
            self.stats_widgets[key].pack(pady=5)
        
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Frame de acciones rápidas
        acciones_frame = tk.LabelFrame(main_frame, text="⚡ Acciones Rápidas", 
                                     font=('Segoe UI', 12, 'bold'), fg=c['fg'], 
                                     bg=c['frame_bg'], relief='raised', bd=2)
        acciones_frame.pack(fill='x', pady=20)
        
        btn_frame = tk.Frame(acciones_frame, bg=c['frame_bg'])
        btn_frame.pack(pady=15)
        
        acciones = [
            ("🔄", "Sincronizar", self.sincronizar_manual),
            ("📊", "Ver Reportes", lambda: self.cambiar_pestana("📊 Reportes")),
            ("📈", "Ver Gráficos", lambda: self.cambiar_pestana("📈 Gráficos")),
            ("⚙️", "Configuración", lambda: self.cambiar_pestana("⚙️ Configuración")),
            ("💾", "Respaldo", self.crear_respaldo_rapido)
        ]
        
        # Segunda fila de botones para PDFs
        acciones_pdf = [
            ("📄", "PDF Inventario", lambda: self.exportar_reporte_pdf("inventario")),
            ("💰", "PDF Ventas", lambda: self.exportar_reporte_pdf("ventas")),
            ("📊", "PDF Completo", lambda: self.exportar_reporte_pdf("completo"))
        ]
        
        for i, (icono, texto, comando) in enumerate(acciones):
            btn = tk.Button(btn_frame, text=f"{icono} {texto}", command=comando,
                           font=('Segoe UI', 10, 'bold'), bg=c['button_bg'], 
                           fg=c['button_fg'], relief='flat', bd=0, padx=15, pady=8)
            btn.grid(row=0, column=i, padx=10)
        
        # Segunda fila para botones de PDF
        for i, (icono, texto, comando) in enumerate(acciones_pdf):
            btn = tk.Button(btn_frame, text=f"{icono} {texto}", command=comando,
                           font=('Segoe UI', 10, 'bold'), bg='#9C27B0', 
                           fg='white', relief='flat', bd=0, padx=15, pady=8)
            btn.grid(row=1, column=i, padx=10, pady=5)
        
        return main_frame

    def crear_notificaciones(self, parent):
        """Crear pestana de notificaciones"""
        c = get_colores_tema(self.tema)
        
        main_frame = tk.Frame(parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        titulo = tk.Label(main_frame, text="🔔 Notificaciones del Sistema", 
                         font=('Segoe UI', 16, 'bold'), bg=c['bg'], fg=c['fg'])
        titulo.pack(pady=(0, 20))
        
        # Frame de notificaciones
        notif_frame = tk.Frame(main_frame, bg=c['bg'])
        notif_frame.pack(fill='both', expand=True)
        
        # Lista de notificaciones (doble clic para ver detalle)
        self.lista_notificaciones = tk.Listbox(notif_frame, font=('Segoe UI', 10),
                                              bg=c['entry_bg'], fg=c['entry_fg'],
                                              selectbackground=c['accent'])
        self.lista_notificaciones.pack(fill='both', expand=True, pady=10)
        self.lista_notificaciones.bind('<Double-Button-1>', self.ver_detalle_notificacion)
        
        # Botones de acción
        btn_frame = tk.Frame(notif_frame, bg=c['bg'])
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="🗑️ Marcar como Leída", 
                 command=self.marcar_notificacion_leida,
                 font=('Segoe UI', 10), bg=c['error_fg'], fg='white',
                 relief='flat', bd=0, padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🗑️ Limpiar Todas", 
                 command=self.limpiar_notificaciones,
                 font=('Segoe UI', 10), bg=c['accent'], fg='white',
                 relief='flat', bd=0, padx=15, pady=5).pack(side='left', padx=5)
        
        return main_frame

    def crear_graficos(self, parent):
        """Crear pestana de gráficos estadísticos"""
        try:
            from graficos_estadisticas import GraficosEstadisticas
            
            # Crear instancia del generador de gráficos
            self.generador_graficos = GraficosEstadisticas(parent, self.conn, self.cursor, self.tema)
            
            # Crear panel completo de gráficos
            panel_graficos = self.generador_graficos.crear_panel_graficos_completo(parent)
            
            return panel_graficos
            
        except ImportError:
            # Si no se puede importar matplotlib, mostrar mensaje
            c = get_colores_tema(self.tema)
            main_frame = tk.Frame(parent, bg=c['bg'])
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            titulo = tk.Label(main_frame, text="📈 Gráficos Estadísticos", 
                             font=('Segoe UI', 16, 'bold'), bg=c['bg'], fg=c['fg'])
            titulo.pack(pady=20)
            
            mensaje = tk.Label(main_frame, 
                              text="⚠️ Para usar los gráficos, instala matplotlib:\n\npip install matplotlib\n\nLuego reinicia la aplicación.",
                              font=('Segoe UI', 12), bg=c['bg'], fg=c['fg'], justify='center')
            mensaje.pack(pady=20)
            
            # Botón para instalar matplotlib
            btn_instalar = tk.Button(main_frame, text="Instalar matplotlib", 
                                   command=lambda: os.system("pip install matplotlib"),
                                   font=('Segoe UI', 10, 'bold'), bg='#4CAF50', fg='white')
            btn_instalar.pack(pady=10)
            
            return main_frame
        except Exception as e:
            print(f"Error creando gráficos: {e}")
            return None

    def actualizar_graficos(self):
        """Actualizar gráficos cuando se cambia a la pestana"""
        try:
            if hasattr(self, 'generador_graficos'):
                # Actualizar el tema de los gráficos si cambió
                self.generador_graficos.tema = self.tema
                self.generador_graficos.configurar_estilo_matplotlib()
                
                # Forzar actualización de todos los gráficos
                self.generador_graficos.crear_panel_graficos_completo(self.tabs['graficos'])
        except Exception as e:
            print(f"Error actualizando gráficos: {e}")

    def cambiar_pestana(self, nombre_pestana):
        """Cambiar a una pestana específica"""
        try:
            # Buscar el notebook en los hijos de la ventana principal
            notebook = None
            for child in self.root.winfo_children():
                if isinstance(child, tk.ttk.Notebook):
                    notebook = child
                    break
            
            if notebook:
                # Buscar la pestana por nombre
                for i in range(notebook.index('end')):
                    if notebook.tab(i, 'text') == nombre_pestana:
                        notebook.select(i)
                        break
        except Exception as e:
            print(f"Error cambiando pestana: {e}")

    def crear_respaldo_rapido(self):
        """Crear respaldo rápido del sistema"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backup_sistema_{timestamp}.json"
            
            # Recopilar datos
            datos_backup = {
                'fecha': timestamp,
                'usuario': self.usuario,
                'productos': [],
                'clientes': [],
                'ventas': [],
                'configuracion': {}
            }
            
            # Exportar productos
            self.cursor.execute("SELECT * FROM productos")
            datos_backup['productos'] = self.cursor.fetchall()
            
            # Exportar clientes
            self.cursor.execute("SELECT * FROM clientes")
            datos_backup['clientes'] = self.cursor.fetchall()
            
            # Guardar archivo
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(datos_backup, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Respaldo", f"✅ Respaldo creado: {backup_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al crear respaldo: {e}")

    def actualizar_dashboard(self):
        """Actualizar estadísticas del dashboard"""
        try:
            # Total productos
            self.cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 1")
            total_productos = self.cursor.fetchone()[0]
            self.stats_widgets['productos'].config(text=str(total_productos))
            
            # Ventas hoy
            hoy = datetime.now().strftime('%Y-%m-%d')
            if self.online:
                self.cursor.execute("SELECT COUNT(*) FROM ventas WHERE DATE(fecha) = %s", (hoy,))
            else:
                self.cursor.execute("SELECT COUNT(*) FROM ventas WHERE DATE(fecha) = ?", (hoy,))
            ventas_hoy = self.cursor.fetchone()[0]
            self.stats_widgets['ventas_hoy'].config(text=str(ventas_hoy))
            
            # Total clientes
            self.cursor.execute("SELECT COUNT(*) FROM clientes")
            total_clientes = self.cursor.fetchone()[0]
            self.stats_widgets['clientes'].config(text=str(total_clientes))
            
            # Stock bajo
            self.cursor.execute("SELECT COUNT(*) FROM productos WHERE stock <= stock_minimo AND activo = 1")
            stock_bajo = self.cursor.fetchone()[0]
            self.stats_widgets['stock_bajo'].config(text=str(stock_bajo))
            
        except Exception as e:
            print(f"Error actualizando dashboard: {e}")

    def actualizar_notificaciones(self):
        """Actualizar lista de notificaciones"""
        try:
            self.lista_notificaciones.delete(0, tk.END)
            
            self.cursor.execute("SELECT titulo, mensaje, tipo, fecha_creacion FROM notificaciones WHERE leida = 0 ORDER BY fecha_creacion DESC")
            notificaciones = self.cursor.fetchall()
            
            for titulo, mensaje, tipo, fecha in notificaciones:
                icono = "🔴" if tipo == "error" else "🟡" if tipo == "warning" else "🔵"
                texto = f"{icono} {titulo} - {fecha}"
                self.lista_notificaciones.insert(tk.END, texto)
                
        except Exception as e:
            print(f"Error actualizando notificaciones: {e}")

    def marcar_notificacion_leida(self):
        """Marcar notificación seleccionada como leída"""
        try:
            seleccion = self.lista_notificaciones.curselection()
            if seleccion:
                self.cursor.execute("UPDATE notificaciones SET leida = 1 WHERE id = ?", (seleccion[0] + 1,))
                self.conn.commit()
                self.actualizar_notificaciones()
        except Exception as e:
            print(f"Error marcando notificación: {e}")

    def limpiar_notificaciones(self):
        """Limpiar todas las notificaciones"""
        try:
            self.cursor.execute("DELETE FROM notificaciones WHERE leida = 1")
            self.conn.commit()
            self.actualizar_notificaciones()
            messagebox.showinfo("Notificaciones", "✅ Notificaciones leídas eliminadas")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error limpiando notificaciones: {e}")

    def agregar_notificacion(self, titulo, mensaje, tipo="info"):
        """Agregar nueva notificación"""
        try:
            if self.online:
                # Para MySQL
                self.cursor.execute("INSERT INTO notificaciones (titulo, mensaje, tipo) VALUES (%s, %s, %s)",
                                  (titulo, mensaje, tipo))
            else:
                # Para SQLite
                self.cursor.execute("INSERT INTO notificaciones (titulo, mensaje, tipo) VALUES (?, ?, ?)",
                                  (titulo, mensaje, tipo))
            self.conn.commit()
        except Exception as e:
            print(f"Error agregando notificación: {e}")

    def ver_detalle_notificacion(self, event=None):
        try:
            idxs = self.lista_notificaciones.curselection()
            if not idxs:
                return
            idx = idxs[0]
            # Obtener la notificación correspondiente (orden DESC ya aplicado al cargar)
            self.cursor.execute("SELECT titulo, mensaje, tipo, fecha_creacion FROM notificaciones WHERE leida = 0 ORDER BY fecha_creacion DESC")
            notificaciones = self.cursor.fetchall()
            if idx < len(notificaciones):
                titulo, mensaje, tipo, fecha = notificaciones[idx]
                messagebox.showinfo(titulo, f"{mensaje}\n\n{fecha}")
        except Exception as e:
            print(f"Error mostrando detalle de notificación: {e}")

    def cambiar_tema(self, nuevo_tema):
        """Cambiar tema sin reiniciar la aplicación"""
        try:
            # Actualizar tema global
            set_tema_global(nuevo_tema)
            self.tema = nuevo_tema
            
            # Reconfigurar estilos
            configurar_estilos(nuevo_tema)
            
            # Actualizar colores en todos los módulos
            self.actualizar_tema_modulos(nuevo_tema)
            
            # Actualizar barra de estado
            self.actualizar_tema_barra_estado(nuevo_tema)
            
            # Guardar configuración
            self.guardar_configuracion_tema(nuevo_tema)
            
            # Actualizar gráficos si existen
            if hasattr(self, 'generador_graficos'):
                self.generador_graficos.tema = nuevo_tema
                self.generador_graficos.configurar_estilo_matplotlib()
            
            messagebox.showinfo("Tema cambiado", f"✅ Tema cambiado a {nuevo_tema} exitosamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error cambiando tema: {e}")

    def actualizar_tema_modulos(self, nuevo_tema):
        """Actualizar tema en todos los módulos"""
        try:
            colores = get_colores_tema(nuevo_tema)
            
            # Actualizar dashboard si existe
            if hasattr(self, 'tabs') and 'dashboard' in self.tabs:
                self.actualizar_tema_dashboard(colores)
            
            # Actualizar notificaciones si existe
            if hasattr(self, 'tabs') and 'notificaciones' in self.tabs:
                self.actualizar_tema_notificaciones(colores)
                
            # Actualizar módulos principales
            for tab_name, tab_module in self.tabs.items():
                if hasattr(tab_module, 'actualizar_tema'):
                    tab_module.actualizar_tema(nuevo_tema)
                
        except Exception as e:
            print(f"Error actualizando tema en módulos: {e}")

    def actualizar_tema_dashboard(self, colores):
        """Actualizar tema del dashboard"""
        try:
            # Actualizar colores de fondo
            for widget in self.tabs['dashboard'].winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(bg=colores['bg'])
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg=colores['bg'], fg=colores['fg'])
                        elif isinstance(child, tk.Frame):
                            child.config(bg=colores['frame_bg'])
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Label):
                                    grandchild.config(bg=colores['frame_bg'], fg=colores['fg'])
        except Exception as e:
            print(f"Error actualizando tema dashboard: {e}")

    def actualizar_tema_notificaciones(self, colores):
        """Actualizar tema de notificaciones"""
        try:
            # Actualizar colores de fondo
            for widget in self.tabs['notificaciones'].winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.config(bg=colores['bg'])
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg=colores['bg'], fg=colores['fg'])
                        elif isinstance(child, tk.Listbox):
                            child.config(bg=colores['entry_bg'], fg=colores['entry_fg'])
        except Exception as e:
            print(f"Error actualizando tema notificaciones: {e}")

    def actualizar_tema_barra_estado(self, nuevo_tema):
        """Actualizar tema de la barra de estado"""
        try:
            colores = get_colores_tema(nuevo_tema)
            self.barra_estado.config(bg='#2c3e50')  # Mantener color oscuro para contraste
        except Exception as e:
            print(f"Error actualizando tema barra estado: {e}")

    def guardar_configuracion_tema(self, nuevo_tema):
        """Guardar configuración del tema"""
        try:
            config = {
                'tema': nuevo_tema,
                'nombre_empresa': '',
                'direccion_empresa': '',
                'telefono_empresa': '',
                'alerta_stock_config': 5
            }
            
            # Cargar configuración existente si existe
            if os.path.exists('configuracion.json'):
                with open('configuracion.json', 'r', encoding='utf-8') as f:
                    config_existente = json.load(f)
                    config.update(config_existente)
            
            # Guardar configuración actualizada
            with open('configuracion.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error guardando configuración tema: {e}")

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
            
            # Registrar inicio de sincronización
            self.agregar_notificacion("Sincronización", "Iniciando sincronización con la nube...", "info")
            
            # --- SUBIR DATOS LOCALES PENDIENTES A LA NUBE ---
            # Productos
            self.cursor.execute("SELECT codigo, nombre, descripcion, precio, stock, stock_minimo, categoria, activo FROM productos WHERE sincronizado = 0")
            productos = self.cursor.fetchall()
            productos_sincronizados = 0
            
            for prod in productos:
                try:
                    cursor_mysql.execute("""
                        INSERT INTO productos (codigo, nombre, descripcion, precio, stock, stock_minimo, categoria, activo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                        nombre=VALUES(nombre), descripcion=VALUES(descripcion), precio=VALUES(precio), 
                        stock=VALUES(stock), stock_minimo=VALUES(stock_minimo), categoria=VALUES(categoria), 
                        activo=VALUES(activo), fecha_modificacion=NOW()
                    """, prod)
                    productos_sincronizados += 1
                except Exception as e:
                    print(f"Error sincronizando producto {prod[0]}: {e}")
            
            self.cursor.execute("UPDATE productos SET sincronizado = 1 WHERE sincronizado = 0")
            self.conn.commit()
            
            if productos_sincronizados > 0:
                self.agregar_notificacion("Sincronización", f"{productos_sincronizados} productos sincronizados", "info")
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
            self.agregar_notificacion("Error de Sincronización", f"Error: {e}", "error")

    def crear_respaldo_comprimido(self):
        """Crear respaldo comprimido del sistema"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backup_sistema_{timestamp}.json.gz"
            
            # Recopilar todos los datos
            datos_backup = {
                'metadata': {
                    'fecha': timestamp,
                    'usuario': self.usuario,
                    'version': '2.0',
                    'tipo': 'respaldo_completo'
                },
                'productos': [],
                'clientes': [],
                'ventas': [],
                'detalle_ventas': [],
                'usuarios': [],
                'configuracion': [],
                'notificaciones': [],
                'auditoria': []
            }
            
            # Exportar todas las tablas
            tablas = ['productos', 'clientes', 'ventas', 'detalle_ventas', 'usuarios', 
                     'configuracion_sistema', 'notificaciones', 'auditoria']
            
            for tabla in tablas:
                try:
                    self.cursor.execute(f"SELECT * FROM {tabla}")
                    datos_backup[tabla] = self.cursor.fetchall()
                except Exception as e:
                    print(f"Error exportando tabla {tabla}: {e}")
            
            # Comprimir y guardar
            datos_json = json.dumps(datos_backup, ensure_ascii=False, indent=2)
            datos_bytes = datos_json.encode('utf-8')
            
            with gzip.open(backup_file, 'wt', encoding='utf-8') as f:
                f.write(datos_json)
            
            # Calcular tamaño
            tamaño_mb = os.path.getsize(backup_file) / (1024 * 1024)
            
            messagebox.showinfo("Respaldo Comprimido", 
                              f"✅ Respaldo creado: {backup_file}\n📦 Tamaño: {tamaño_mb:.2f} MB")
            
            self.agregar_notificacion("Respaldo", f"Respaldo comprimido creado: {backup_file}", "info")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al crear respaldo: {e}")
            self.agregar_notificacion("Error de Respaldo", f"Error: {e}", "error")

    def exportar_reporte_pdf(self, tipo_reporte="inventario"):
        """Exportar reporte a PDF real"""
        try:
            from generador_pdf import GeneradorPDF
            from tkinter import filedialog
            
            # Seleccionar ubicación del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_sugerido = f"reporte_{tipo_reporte}_{timestamp}.pdf"
            
            archivo_pdf = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=nombre_sugerido
            )
            
            if not archivo_pdf:
                return
            
            # Crear generador de PDF
            generador = GeneradorPDF()
            
            if tipo_reporte == "inventario":
                # Obtener datos de inventario
                self.cursor.execute("""
                    SELECT codigo, nombre, descripcion, precio_venta, stock, stock_minimo, activo 
                    FROM productos WHERE activo = 1 ORDER BY nombre
                """)
                productos_raw = self.cursor.fetchall()
                
                # Convertir a formato de diccionario
                datos_productos = []
                for producto in productos_raw:
                    datos_productos.append({
                        'codigo': producto[0],
                        'nombre': producto[1],
                        'descripcion': producto[2],
                        'precio_venta': float(producto[3]) if producto[3] else 0,
                        'stock': int(producto[4]) if producto[4] else 0,
                        'stock_minimo': int(producto[5]) if producto[5] else 5,
                        'activo': int(producto[6]) if producto[6] else 1
                    })
                
                # Generar PDF
                archivo_generado = generador.generar_reporte_inventario(datos_productos, archivo_pdf)
                
            elif tipo_reporte == "ventas":
                # Obtener datos de ventas
                self.cursor.execute("""
                    SELECT v.id, v.fecha, v.total, v.estado, c.nombre as cliente_nombre
                    FROM ventas v 
                    LEFT JOIN clientes c ON v.cliente_id = c.id 
                    ORDER BY v.fecha DESC LIMIT 100
                """)
                ventas_raw = self.cursor.fetchall()
                
                # Convertir a formato de diccionario
                datos_ventas = []
                for venta in ventas_raw:
                    datos_ventas.append({
                        'id': venta[0],
                        'fecha': venta[1],
                        'total': float(venta[2]) if venta[2] else 0,
                        'estado': venta[3] or 'completada',
                        'cliente_nombre': venta[4] or 'Cliente General'
                    })
                
                # Generar PDF
                archivo_generado = generador.generar_reporte_ventas(datos_ventas, archivo_pdf)
                
            elif tipo_reporte == "completo":
                # Obtener datos de inventario
                self.cursor.execute("""
                    SELECT codigo, nombre, descripcion, precio_venta, stock, stock_minimo, activo 
                    FROM productos WHERE activo = 1 ORDER BY nombre
                """)
                productos_raw = self.cursor.fetchall()
                
                datos_productos = []
                for producto in productos_raw:
                    datos_productos.append({
                        'codigo': producto[0],
                        'nombre': producto[1],
                        'descripcion': producto[2],
                        'precio_venta': float(producto[3]) if producto[3] else 0,
                        'stock': int(producto[4]) if producto[4] else 0,
                        'stock_minimo': int(producto[5]) if producto[5] else 5,
                        'activo': int(producto[6]) if producto[6] else 1
                    })
                
                # Obtener datos de ventas
                self.cursor.execute("""
                    SELECT v.id, v.fecha, v.total, v.estado, c.nombre as cliente_nombre
                    FROM ventas v 
                    LEFT JOIN clientes c ON v.cliente_id = c.id 
                    ORDER BY v.fecha DESC LIMIT 50
                """)
                ventas_raw = self.cursor.fetchall()
                
                datos_ventas = []
                for venta in ventas_raw:
                    datos_ventas.append({
                        'id': venta[0],
                        'fecha': venta[1],
                        'total': float(venta[2]) if venta[2] else 0,
                        'estado': venta[3] or 'completada',
                        'cliente_nombre': venta[4] or 'Cliente General'
                    })
                
                # Generar PDF completo
                archivo_generado = generador.generar_reporte_completo(datos_productos, datos_ventas, archivo_pdf)
            
            else:
                messagebox.showerror("Error", "Tipo de reporte no válido")
                return
            
            # Verificar que el archivo se creó
            if os.path.exists(archivo_generado):
                tamaño_mb = os.path.getsize(archivo_generado) / (1024 * 1024)
                messagebox.showinfo("Exportar PDF", 
                                  f"✅ Reporte PDF generado exitosamente!\n\n"
                                  f"📁 Archivo: {os.path.basename(archivo_generado)}\n"
                                  f"📦 Tamaño: {tamaño_mb:.2f} MB\n"
                                  f"📍 Ubicación: {os.path.dirname(archivo_generado)}")
                self.agregar_notificacion("Exportación PDF", f"Reporte {tipo_reporte} exportado a PDF", "info")
            else:
                messagebox.showerror("Error", "No se pudo generar el archivo PDF")
            
        except ImportError:
            messagebox.showerror("Error", "❌ Error: reportlab no está instalado.\nEjecuta: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al exportar PDF: {e}")

    def verificar_stock_bajo_automatico(self):
        """Verificar stock bajo automáticamente"""
        try:
            # Consultar productos con stock bajo y notificar con detalle (máx 5 para no saturar)
            query = "SELECT nombre, stock, stock_minimo FROM productos WHERE stock_minimo IS NOT NULL AND stock <= stock_minimo AND activo = 1 ORDER BY stock ASC LIMIT 5"
            self.cursor.execute(query)
            productos_bajo_stock = self.cursor.fetchall()
            if productos_bajo_stock:
                detalle = ", ".join([f"{n} ({s}/{m})" for n, s, m in productos_bajo_stock])
                self.agregar_notificacion("Stock Bajo", f"{detalle}", "warning")
        except Exception as e:
            print(f"Error verificando stock: {e}")

    def limpiar_datos_antiguos(self, dias=30):
        """Limpiar datos antiguos para optimizar"""
        try:
            fecha_limite = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
            
            # Limpiar ventas antiguas (mantener solo las últimas 1000)
            self.cursor.execute("""
                DELETE FROM detalle_ventas 
                WHERE venta_id IN (
                    SELECT id FROM ventas 
                    WHERE fecha < ? 
                    AND id NOT IN (
                        SELECT id FROM ventas 
                        ORDER BY fecha DESC 
                        LIMIT 1000
                    )
                )
            """, (fecha_limite,))
            
            self.cursor.execute("""
                DELETE FROM ventas 
                WHERE fecha < ? 
                AND id NOT IN (
                    SELECT id FROM ventas 
                    ORDER BY fecha DESC 
                    LIMIT 1000
                )
            """, (fecha_limite,))
            
            self.conn.commit()
            
            self.agregar_notificacion("Limpieza", f"Datos antiguos eliminados (más de {dias} días)", "info")
            
        except Exception as e:
            print(f"Error limpiando datos: {e}")

    def tareas_automaticas(self):
        """Tareas automáticas en segundo plano"""
        while True:
            time.sleep(3600)  # Ejecutar cada hora
            
            try:
                # Sincronizar si está online
                if self.online:
                    self.sincronizar_bidireccional()
                
                # Verificar stock bajo
                self.verificar_stock_bajo_automatico()
                
                # Limpiar datos antiguos (cada 24 horas)
                hora_actual = datetime.now().hour
                if hora_actual == 2:  # A las 2 AM
                    self.limpiar_datos_antiguos()
                
            except Exception as e:
                print(f"Error en tareas automáticas: {e}")

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