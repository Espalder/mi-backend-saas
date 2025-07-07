import tkinter as tk
from tkinter import ttk, messagebox
from estilos import configurar_estilos, get_colores_tema
import json, os

class ConfiguracionUI:
    def __init__(self, parent, conn, cursor, rol, tema='claro', callback_cambiar_tema=None):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.rol = rol
        self.tema = tema
        self.colores = get_colores_tema(self.tema)
        self.callback_cambiar_tema = callback_cambiar_tema
        self.crear_interfaz()

    def crear_interfaz(self):
        configurar_estilos(self.tema)
        c = self.colores
        main_frame = tk.Frame(self.parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        frame_config = tk.LabelFrame(main_frame, text="⚙️ Configuración del Sistema", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_config.pack(fill='x', padx=10, pady=10)
        frame_campos_config = tk.Frame(frame_config, bg=c['frame_bg'])
        frame_campos_config.pack(fill='x', padx=20, pady=20)
        tk.Label(frame_campos_config, text="🏢 Nombre de la Empresa:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        self.nombre_empresa = tk.Entry(frame_campos_config, font=('Segoe UI', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.nombre_empresa.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        tk.Label(frame_campos_config, text="📍 Dirección:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=1, column=0, sticky='e', padx=(0, 10), pady=5)
        self.direccion_empresa = tk.Entry(frame_campos_config, font=('Segoe UI', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.direccion_empresa.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        tk.Label(frame_campos_config, text="📞 Teléfono:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=2, column=0, sticky='e', padx=(0, 10), pady=5)
        self.telefono_empresa = tk.Entry(frame_campos_config, font=('Segoe UI', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.telefono_empresa.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        tk.Label(frame_campos_config, text="⚠️ Nivel de Alerta de Stock:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=3, column=0, sticky='e', padx=(0, 10), pady=5)
        self.alerta_stock_config = ttk.Spinbox(frame_campos_config, from_=1, to=50, font=('Segoe UI', 10))
        self.alerta_stock_config.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.alerta_stock_config.set(5)
        frame_campos_config.columnconfigure(1, weight=1)
        btn_guardar = tk.Button(frame_campos_config, text="💾 Guardar Configuración", command=self.guardar_configuracion, font=('Segoe UI', 10, 'bold'), bg=c['button_bg'], fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)
        if self.rol == 'admin' and self.callback_cambiar_tema:
            frame_tema = tk.LabelFrame(main_frame, text="🎨 Tema Visual", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
            frame_tema.pack(fill='x', padx=10, pady=10)
            tk.Label(frame_tema, text="Selecciona el tema:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).pack(side='left', padx=10, pady=10)
            self.var_tema = tk.StringVar(value=self.tema)
            rb_claro = tk.Radiobutton(frame_tema, text="Claro", variable=self.var_tema, value='claro', font=('Segoe UI', 10), bg=c['frame_bg'], fg=c['fg'], selectcolor=c['entry_bg'], command=self.cambiar_tema)
            rb_oscuro = tk.Radiobutton(frame_tema, text="Oscuro", variable=self.var_tema, value='oscuro', font=('Segoe UI', 10), bg=c['frame_bg'], fg=c['fg'], selectcolor=c['entry_bg'], command=self.cambiar_tema)
            rb_claro.pack(side='left', padx=10)
            rb_oscuro.pack(side='left', padx=10)
        frame_backup = tk.LabelFrame(main_frame, text="💾 Respaldo de Datos", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_backup.pack(fill='x', padx=10, pady=10)
        frame_botones_backup = tk.Frame(frame_backup, bg=c['frame_bg'])
        frame_botones_backup.pack(fill='x', padx=20, pady=20)
        btn_crear_backup = tk.Button(frame_botones_backup, text="📦 Crear Respaldo", command=self.crear_respaldo, font=('Segoe UI', 10, 'bold'), bg=c['accent'], fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
        btn_crear_backup.pack(side='left', padx=10)
        btn_restaurar_backup = tk.Button(frame_botones_backup, text="🔄 Restaurar Respaldo", command=self.restaurar_respaldo, font=('Segoe UI', 10, 'bold'), bg=c['ok_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
        btn_restaurar_backup.pack(side='left', padx=10)
        self.cargar_configuracion()

    def cargar_configuracion(self):
        self.configuracion = {
            'nombre_empresa': '',
            'direccion_empresa': '',
            'telefono_empresa': '',
            'alerta_stock_config': 5,
            'tema': 'claro'
        }
        if os.path.exists('configuracion.json'):
            with open('configuracion.json', 'r', encoding='utf-8') as f:
                self.configuracion.update(json.load(f))
        self.nombre_empresa.delete(0, 'end')
        self.nombre_empresa.insert(0, self.configuracion.get('nombre_empresa', ''))
        self.direccion_empresa.delete(0, 'end')
        self.direccion_empresa.insert(0, self.configuracion.get('direccion_empresa', ''))
        self.telefono_empresa.delete(0, 'end')
        self.telefono_empresa.insert(0, self.configuracion.get('telefono_empresa', ''))
        self.alerta_stock_config.delete(0, 'end')
        self.alerta_stock_config.insert(0, str(self.configuracion.get('alerta_stock_config', 5)))
        if hasattr(self, 'var_tema'):
            self.var_tema.set(self.configuracion.get('tema', 'claro'))

    def guardar_configuracion(self):
        import json
        self.configuracion['nombre_empresa'] = self.nombre_empresa.get().strip()
        self.configuracion['direccion_empresa'] = self.direccion_empresa.get().strip()
        self.configuracion['telefono_empresa'] = self.telefono_empresa.get().strip()
        self.configuracion['alerta_stock_config'] = int(self.alerta_stock_config.get())
        if hasattr(self, 'var_tema'):
            self.configuracion['tema'] = self.var_tema.get()
        with open('configuracion.json', 'w', encoding='utf-8') as f:
            json.dump(self.configuracion, f, ensure_ascii=False, indent=2)
        # Refrescar alerta de stock en inventario si existe
        try:
            from sistema_gestion_mejorado_modulos.main import SistemaGestionApp
            if hasattr(self.parent.master, 'tabs') and 'inventario' in self.parent.master.tabs:
                self.parent.master.tabs['inventario'].verificar_stock_bajo()
        except Exception:
            pass
        messagebox.showinfo("Configuración", "Configuración guardada exitosamente")

    def crear_respaldo(self):
        # Aquí puedes agregar lógica para exportar la base de datos local o remota según el modo
        messagebox.showinfo("Respaldo", "Respaldo creado exitosamente (simulado)")
    def restaurar_respaldo(self):
        # Aquí puedes agregar lógica para importar la base de datos local o remota según el modo
        messagebox.showinfo("Restauración", "Datos restaurados exitosamente (simulado)")
    def cambiar_tema(self):
        if self.callback_cambiar_tema:
            self.configuracion['tema'] = self.var_tema.get()
            import json
            with open('configuracion.json', 'w', encoding='utf-8') as f:
                json.dump(self.configuracion, f, ensure_ascii=False, indent=2)
            self.callback_cambiar_tema(self.var_tema.get()) 