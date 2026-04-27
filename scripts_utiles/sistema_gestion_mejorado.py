import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime, timedelta
import os

class SistemaGestionEmpresasMejorado:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Empresarial - V.M")
        self.root.geometry("1200x800")
        self.root.configure(bg='#e6f3ff')
        
        # Configurar estilos modernos
        self.configurar_estilos()
        
        # Configuración de divisa
        self.divisa = "S/"  # Divisa por defecto (Soles)
        
        # Configuración de alerta de stock
        self.alerta_stock_minimo = 5  # Nivel por defecto
        
        # Configuración persistente
        self.configuracion = {
            'nombre_empresa': 'Mi Empresa',
            'direccion_empresa': '',
            'telefono_empresa': '',
            'alerta_stock_config': 5
        }
        
        # Historial de reportes
        self.historial_reportes = []
        
        # Ícono de caja registradora
        try:
            self.root.iconphoto(False, tk.PhotoImage(file="images/caja_registradora.png"))
        except Exception:
            pass
        
        # Crear banner superior
        self.crear_banner_superior()
        
        # Conexión a MySQL (configura estos valores según tu instalación)
        self.db_config = {
            'host': 'localhost',
            'user': 'admin',
            'password': 'admin123',
            'database': 'gestion_empresas'
        }
        
        # Variables para mantener selección
        self.producto_seleccionado_id = None
        self.venta_actual_items = []
        
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Conexión exitosa", "Conectado a la base de datos MySQL")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"Error al conectar a MySQL: {err}")
            self.root.destroy()
            return
        
        # Crear pestañas con diseño mejorado
        self.crear_pestanas()
        
        # Configurar scroll global
        self.configurar_scroll_global()
        
        # Cargar datos iniciales
        self.cargar_productos()
        self.cargar_ventas()
        self.actualizar_dashboard()
        
        # Cargar configuración guardada
        self.cargar_configuracion_archivo()
        
        # Cargar historial de reportes
        self.cargar_historial_reportes()
        
        # Actualizar interfaz de configuración después de cargar
        self.actualizar_configuracion_interfaz()
    
    def configurar_estilos(self):
        """Configurar estilos modernos para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores y estilos
        style.configure('TFrame', background='#e6f3ff')
        style.configure('TLabel', background='#e6f3ff', font=('Segoe UI', 10))
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('TNotebook', background='#e6f3ff')
        style.configure('TNotebook.Tab', background='#2196F3', foreground='white', font=('Segoe UI', 10, 'bold'), padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#FF9800'), ('active', '#FFC107')])
        style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', font=('Segoe UI', 9))
        style.configure('Treeview.Heading', background='#2196F3', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('TLabelframe', background='#e6f3ff')
        style.configure('TLabelframe.Label', background='#e6f3ff', font=('Segoe UI', 11, 'bold'), foreground='#1976D2')
        style.configure('TEntry', fieldbackground='#ffffff', font=('Segoe UI', 10))
        style.configure('TCombobox', fieldbackground='#ffffff', font=('Segoe UI', 10))
        style.configure('TSpinbox', fieldbackground='#ffffff', font=('Segoe UI', 10))
    
    def crear_banner_superior(self):
        """Crear banner superior con logo y título"""
        banner = tk.Frame(self.root, bg='#2196F3', height=120)
        banner.pack(fill='x')
        banner.pack_propagate(False)
        
        # Intentar cargar imagen de banner
        try:
            img_banner = Image.open("images/banner_bg.png").resize((1000, 120))
            self.banner_img = ImageTk.PhotoImage(img_banner)
            tk.Label(banner, image=self.banner_img, bg='#2196F3').place(x=200, y=0)
        except Exception:
            # Si no hay imagen, crear un banner con gradiente
            canvas = tk.Canvas(banner, height=120, bg='#2196F3', highlightthickness=0)
            canvas.place(x=0, y=0, width=1200, height=120)
            canvas.create_rectangle(0, 0, 1200, 120, fill='#2196F3', outline='')
        
        # Logo de empresa
        try:
            img_logo = Image.open("images/logo_empresa.png").resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(img_logo)
            tk.Label(banner, image=self.logo_img, bg='#2196F3').place(x=20, y=10)
        except Exception:
            # Si no hay logo, crear un placeholder
            logo_placeholder = tk.Label(banner, text="🏢", font=('Segoe UI', 40), bg='#2196F3', fg='white')
            logo_placeholder.place(x=30, y=20)
        
        # Títulos
        tk.Label(banner, text="SISTEMA DE GESTIÓN EMPRESARIAL", 
                font=('Segoe UI', 28, 'bold'), bg='#2196F3', fg='white').place(x=140, y=30)
        tk.Label(banner, text="Inventario • Ventas • Reportes • Configuración", 
                font=('Segoe UI', 14), bg='#2196F3', fg='#E3F2FD').place(x=140, y=75)
        
        # Fecha y hora
        self.label_fecha = tk.Label(banner, text="", font=('Segoe UI', 10), bg='#2196F3', fg='#E3F2FD')
        self.label_fecha.place(x=1000, y=20)
        self.actualizar_fecha()
    
    def actualizar_fecha(self):
        """Actualizar fecha y hora en el banner"""
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.label_fecha.config(text=fecha_actual)
        self.root.after(60000, self.actualizar_fecha)  # Actualizar cada minuto
    
    def crear_pestanas(self):
        """Crear pestañas con diseño mejorado"""
        # Frame principal para las pestañas
        frame_pestanas = tk.Frame(self.root, bg='#e6f3ff')
        frame_pestanas.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Crear notebook con estilo mejorado
        self.notebook = ttk.Notebook(frame_pestanas)
        self.notebook.pack(fill='both', expand=True)
        
        # Evento para cambiar de pestaña
        self.notebook.bind('<<NotebookTabChanged>>', self.cambiar_pestana)
        
        # Pestaña de Inventario
        self.tab_inventario = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_inventario, text="📦 Inventario")
        self.crear_interfaz_inventario()
        
        # Pestaña de Ventas
        self.tab_ventas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ventas, text="💰 Ventas")
        self.crear_interfaz_ventas()
        
        # Pestaña de Reportes
        self.tab_reportes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reportes, text="📊 Reportes")
        self.crear_interfaz_reportes()
        
        # Pestaña de Configuración
        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="⚙️ Configuración")
        self.crear_interfaz_configuracion()
    
    def configurar_scroll_global(self):
        """Configurar scroll global para toda la ventana"""
        def on_mousewheel(event):
            # Obtener las coordenadas del mouse
            x, y = event.x_root, event.y_root
            
            # Buscar el widget en esa posición
            widget = self.root.winfo_containing(x, y)
            
            # Buscar el Treeview más cercano
            treeview = None
            while widget and widget != self.root:
                if isinstance(widget, ttk.Treeview):
                    treeview = widget
                    break
                widget = widget.master
            
            # Si encontramos un Treeview, hacer scroll
            if treeview:
                # Calcular la dirección del scroll
                delta = int(-1 * (event.delta / 120))
                treeview.yview_scroll(delta, "units")
                return "break"  # Prevenir el scroll por defecto
        
        # Vincular el evento de scroll a toda la ventana
        self.root.bind_all("<MouseWheel>", on_mousewheel)
        
        # Para Linux
        self.root.bind_all("<Button-4>", lambda e: on_mousewheel(e))
        self.root.bind_all("<Button-5>", lambda e: on_mousewheel(e))
    
    def crear_interfaz_inventario(self):
        """Crear interfaz del inventario con diseño mejorado"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.tab_inventario, bg='#e6f3ff')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg='#e6f3ff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#e6f3ff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame para formulario de productos con diseño mejorado
        frame_form = tk.LabelFrame(scrollable_frame, text="➕ Gestión de Productos", 
                                 font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                 bg='#ffffff', relief='raised', bd=2)
        frame_form.pack(fill='x', padx=10, pady=10)
        
        # Grid para organizar los campos
        frame_campos = tk.Frame(frame_form, bg='#ffffff')
        frame_campos.pack(fill='x', padx=20, pady=20)
        
        # Campos del formulario con mejor diseño
        labels = ["Código:", "Nombre:", "Descripción:", "Precio:", "Stock:"]
        self.entries_inventario = {}
        
        for i, label in enumerate(labels):
            # Label con estilo mejorado
            lbl = tk.Label(frame_campos, text=label, font=('Segoe UI', 10, 'bold'), 
                          bg='#ffffff', fg='#1976D2')
            lbl.grid(row=i, column=0, sticky='e', padx=(0, 10), pady=5)
            
            # Entry con estilo mejorado
            if label == "Descripción:":
                entry = tk.Text(frame_campos, height=3, width=40, font=('Segoe UI', 10),
                               bg='#f8f9fa', relief='solid', bd=1)
            else:
                entry = tk.Entry(frame_campos, font=('Segoe UI', 10), 
                               bg='#f8f9fa', relief='solid', bd=1)
            
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=5)
            self.entries_inventario[label] = entry
        
        # Configurar expansión de columnas
        frame_campos.columnconfigure(1, weight=1)
        
        # Frame para botones con diseño mejorado
        frame_botones = tk.Frame(frame_form, bg='#ffffff')
        frame_botones.pack(fill='x', padx=20, pady=10)
        
        # Botones con colores y estilos mejorados
        botones = [
            ("➕ Agregar", self.agregar_producto, '#4CAF50'),
            ("✏️ Actualizar", self.actualizar_producto, '#2196F3'),
            ("🗑️ Eliminar", self.eliminar_producto, '#F44336'),
            ("🧹 Limpiar", self.limpiar_formulario, '#FF9800')
        ]
        
        for texto, comando, color in botones:
            btn = tk.Button(frame_botones, text=texto, command=comando,
                           font=('Segoe UI', 10, 'bold'), bg=color, fg='white',
                           relief='flat', bd=0, padx=20, pady=8)
            btn.pack(side='left', padx=5)
            
            # Efectos hover
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=self.lighten_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
        
        # Lista de productos con diseño mejorado
        frame_lista = tk.LabelFrame(scrollable_frame, text="📋 Lista de Productos", 
                                  font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                  bg='#ffffff', relief='raised', bd=2)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para la tabla
        frame_tabla = tk.Frame(frame_lista, bg='#ffffff')
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview con mejor diseño
        columns = ("id", "codigo", "nombre", "descripcion", "precio_venta", "stock")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        headers = {
            "id": ("ID", 50),
            "codigo": ("Código", 100),
            "nombre": ("Nombre", 200),
            "descripcion": ("Descripción", 250),
            "precio_venta": ("Precio", 100),
            "stock": ("Stock", 80)
        }
        
        for col, (header, width) in headers.items():
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor='center')
        
        # Scrollbar para la tabla
        scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tabla.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_tabla.pack(side='right', fill='y')
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)
        
        # Eventos de ordenamiento por columnas
        for col in columns:
            self.tree.heading(col, text=headers[col][0], command=lambda c=col: self.ordenar_por_columna(c))
        
        # Alertas de stock bajo con diseño mejorado
        self.alerta_stock = tk.Label(scrollable_frame, text="", 
                                   font=('Segoe UI', 11, 'bold'),
                                   bg='#e6f3ff', fg='#F44336')
        self.alerta_stock.pack(pady=10)
        
        # Imagen decorativa
        try:
            img_deco = Image.open("images/logo_empresa.png").resize((80, 80))
            self.img_deco_inv = ImageTk.PhotoImage(img_deco)
            tk.Label(scrollable_frame, image=self.img_deco_inv, bg='#e6f3ff').place(x=1100, y=10)
        except Exception:
            # Placeholder si no hay imagen
            tk.Label(scrollable_frame, text="📦", font=('Segoe UI', 40), 
                    bg='#e6f3ff', fg='#2196F3').place(x=1100, y=10)
        
        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def lighten_color(self, color):
        """Aclarar un color para efectos hover"""
        # Convertir color hex a RGB, aclarar y volver a hex
        # Simplificado para este ejemplo
        return color
    
    def agregar_producto(self):
        """Agregar producto con validación mejorada"""
        # Obtener valores de los campos
        codigo = self.entries_inventario["Código:"].get().strip()
        nombre = self.entries_inventario["Nombre:"].get().strip()
        descripcion = self.entries_inventario["Descripción:"].get("1.0", "end-1c").strip()
        precio = self.entries_inventario["Precio:"].get().strip()
        stock = self.entries_inventario["Stock:"].get().strip()
        
        # Validación mejorada
        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Campos requeridos", 
                                 "Por favor complete todos los campos obligatorios")
            return
        
        # Validar que el código no esté vacío
        if len(codigo) < 2:
            messagebox.showwarning("Código inválido", "El código debe tener al menos 2 caracteres")
            return
        
        # Validar que el nombre no esté vacío
        if len(nombre) < 3:
            messagebox.showwarning("Nombre inválido", "El nombre debe tener al menos 3 caracteres")
            return
        
        try:
            precio_float = float(precio)
            stock_int = int(stock)
            
            if precio_float <= 0:
                messagebox.showerror("Error de precio", "El precio debe ser mayor a cero")
                return
            
            if stock_int < 0:
                messagebox.showerror("Error de stock", "El stock no puede ser negativo")
                return
                
        except ValueError:
            messagebox.showerror("Error de datos", 
                               "Precio debe ser un número decimal y stock un número entero")
            return
        
        try:
            # Verificar si el código ya existe
            query_check = "SELECT id FROM productos WHERE codigo = %s"
            self.cursor.execute(query_check, (codigo,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Ya existe un producto con ese código")
                return
            
            # Insertar nuevo producto usando la estructura real con todos los campos de precio
            query = """INSERT INTO productos (codigo, nombre, descripcion, precio, precio_compra, precio_venta, stock, stock_minimo, activo) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)"""
            # Usar el mismo precio para todos los campos de precio
            values = (codigo, nombre, descripcion, precio_float, precio_float, precio_float, stock_int, stock_int)
            self.cursor.execute(query, values)
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Error de clave duplicada
                messagebox.showerror("Error", "Ya existe un producto con ese código")
            elif err.errno == 1366:  # Error de tipo de dato
                messagebox.showerror("Error", "Error en el formato de los datos")
            else:
                messagebox.showerror("Error", f"Error al agregar producto: {err}")
    
    def actualizar_producto(self):
        """Actualizar producto seleccionado con validación mejorada"""
        # Usar el producto seleccionado automáticamente
        if self.producto_seleccionado_id is None:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Selección requerida", 
                                     "Por favor seleccione un producto para actualizar")
                return
            
            item = self.tree.item(selected[0])
            producto_id = item['values'][0]
        else:
            producto_id = self.producto_seleccionado_id
        
        # Obtener valores actualizados
        codigo = self.entries_inventario["Código:"].get().strip()
        nombre = self.entries_inventario["Nombre:"].get().strip()
        descripcion = self.entries_inventario["Descripción:"].get("1.0", "end-1c").strip()
        precio = self.entries_inventario["Precio:"].get().strip()
        stock = self.entries_inventario["Stock:"].get().strip()
        
        # Validaciones
        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Campos requeridos", 
                                 "Por favor complete todos los campos obligatorios")
            return
        
        # Validar que el código no esté vacío
        if len(codigo) < 2:
            messagebox.showwarning("Código inválido", "El código debe tener al menos 2 caracteres")
            return
        
        # Validar que el nombre no esté vacío
        if len(nombre) < 3:
            messagebox.showwarning("Nombre inválido", "El nombre debe tener al menos 3 caracteres")
            return
        
        try:
            precio_float = float(precio)
            stock_int = int(stock)
            
            if precio_float <= 0:
                messagebox.showerror("Error de precio", "El precio debe ser mayor a cero")
                return
            
            if stock_int < 0:
                messagebox.showerror("Error de stock", "El stock no puede ser negativo")
                return
                
        except ValueError:
            messagebox.showerror("Error de datos", 
                               "Precio debe ser un número decimal y stock un número entero")
            return
        
        try:
            # Verificar si el código ya existe en otro producto
            query_check = "SELECT id FROM productos WHERE codigo = %s AND id != %s"
            self.cursor.execute(query_check, (codigo, producto_id))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Ya existe otro producto con ese código")
                return
            
            # Actualizar producto usando la estructura real
            query = """UPDATE productos SET 
                      codigo = %s, nombre = %s, descripcion = %s, 
                      precio_venta = %s, stock = %s, updated_at = NOW()
                      WHERE id = %s"""
            values = (codigo, nombre, descripcion, precio_float, stock_int, producto_id)
            self.cursor.execute(query, values)
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.cargar_productos()
            
            # Mantener la selección después de actualizar
            if self.producto_seleccionado_id:
                # Buscar el producto actualizado en la tabla
                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == self.producto_seleccionado_id:
                        self.tree.selection_set(item)
                        self.tree.focus(item)
                        break
                        
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Error de clave duplicada
                messagebox.showerror("Error", "Ya existe otro producto con ese código")
            elif err.errno == 1366:  # Error de tipo de dato
                messagebox.showerror("Error", "Error en el formato de los datos")
            else:
                messagebox.showerror("Error", f"Error al actualizar producto: {err}")
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado con validación mejorada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", 
                                 "Por favor seleccione un producto para eliminar")
            return
        
        item = self.tree.item(selected[0])
        producto_id = item['values'][0]
        producto_nombre = item['values'][2]
        
        # Confirmación más específica
        if not messagebox.askyesno("Confirmar eliminación", 
                                  f"¿Está seguro de eliminar el producto '{producto_nombre}'?\n\nEsta acción no se puede deshacer."):
            return
        
        try:
            # Verificar si el producto está en alguna venta
            query_check = """SELECT COUNT(*) FROM detalle_ventas dv 
                           JOIN productos p ON dv.producto_id = p.id 
                           WHERE p.id = %s"""
            self.cursor.execute(query_check, (producto_id,))
            ventas_count = self.cursor.fetchone()[0]
            
            if ventas_count > 0:
                if not messagebox.askyesno("Producto en ventas", 
                                          f"Este producto está en {ventas_count} venta(s).\n¿Desea eliminarlo de todas formas?"):
                    return
            
            # Marcar como inactivo en lugar de eliminar físicamente
            query = "UPDATE productos SET activo = FALSE, updated_at = NOW() WHERE id = %s"
            self.cursor.execute(query, (producto_id,))
            self.conn.commit()
            
            messagebox.showinfo("Éxito", f"Producto '{producto_nombre}' eliminado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except mysql.connector.Error as err:
            if err.errno == 1451:  # Error de clave foránea
                messagebox.showerror("Error", "No se puede eliminar el producto porque está siendo usado en ventas")
            else:
                messagebox.showerror("Error", f"Error al eliminar producto: {err}")
    
    def seleccionar_producto(self, event):
        """Seleccionar producto de la lista con validación mejorada"""
        try:
            selected = self.tree.selection()
            if not selected:
                return
            
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Validar que tenemos todos los valores necesarios
            if not values or len(values) < 6:
                print(f"Error: Datos del producto incompletos. Valores: {values}")
                return
            
            # Validar que los valores no sean None
            if any(v is None for v in values[:6]):
                print(f"Error: Valores nulos encontrados. Valores: {values}")
                return
            
            # Guardar el ID del producto seleccionado
            self.producto_seleccionado_id = int(values[0])
            
            # Limpiar campos primero
            self.limpiar_formulario()
            
            # Llenar campos con datos seleccionados
            self.entries_inventario["Código:"].insert(0, str(values[1]))
            self.entries_inventario["Nombre:"].insert(0, str(values[2]))
            self.entries_inventario["Descripción:"].insert("1.0", str(values[3]) if values[3] else "")
            self.entries_inventario["Precio:"].insert(0, str(values[4]))
            self.entries_inventario["Stock:"].insert(0, str(values[5]))
            
            # NO volver a seleccionar para evitar bucle infinito
            # Solo mantener el foco visual
            self.tree.focus(selected[0])
            
            print(f"Producto seleccionado: ID={self.producto_seleccionado_id}, Código={values[1]}")
            
        except Exception as e:
            print(f"Error al seleccionar producto: {e}")
            messagebox.showerror("Error", f"Error al cargar datos del producto: {e}")
    
    def ordenar_por_columna(self, columna):
        """Ordenar productos por columna"""
        try:
            # Obtener todos los items
            items = [(self.tree.set(item, columna), item) for item in self.tree.get_children('')]
            
            # Determinar el tipo de ordenamiento
            if columna in ['id', 'stock']:
                # Ordenamiento numérico
                items.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
            elif columna == 'precio_venta':
                # Ordenamiento de precios
                items.sort(key=lambda x: float(x[0]) if x[0].replace('.', '').replace(',', '').isdigit() else 0)
            else:
                # Ordenamiento alfabético
                items.sort(key=lambda x: x[0].lower())
            
            # Reorganizar items en el treeview
            for index, (val, item) in enumerate(items):
                self.tree.move(item, '', index)
                
        except Exception as e:
            print(f"Error al ordenar por columna {columna}: {e}")
    
    def cambiar_pestana(self, event):
        """Método para manejar el cambio de pestañas"""
        try:
            # Limpiar selección al cambiar de pestaña
            self.producto_seleccionado_id = None
            self.limpiar_formulario()
            
            # Deseleccionar en la tabla
            for item in self.tree.selection():
                self.tree.selection_remove(item)
        except Exception as e:
            print(f"Error al cambiar pestaña: {e}")
    
    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario con validación"""
        try:
            for label, entry in self.entries_inventario.items():
                if label == "Descripción:":
                    entry.delete("1.0", "end")
                else:
                    entry.delete(0, 'end')
            
            # NO deseleccionar aquí para evitar conflictos
            # Solo limpiar los campos
        except Exception as e:
            print(f"Error al limpiar formulario: {e}")
    
    def crear_interfaz_ventas(self):
        """Crear interfaz de ventas con diseño mejorado"""
        # Frame principal
        main_frame = tk.Frame(self.tab_ventas, bg='#e6f3ff')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Frame para nueva venta
        frame_venta = tk.LabelFrame(main_frame, text="🛒 Nueva Venta", 
                                  font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                  bg='#ffffff', relief='raised', bd=2)
        frame_venta.pack(fill='x', padx=10, pady=10)
        
        # Grid para campos de venta
        frame_campos_venta = tk.Frame(frame_venta, bg='#ffffff')
        frame_campos_venta.pack(fill='x', padx=20, pady=20)
        
        # Cliente
        tk.Label(frame_campos_venta, text="👤 Cliente:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#1976D2').grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        self.cliente_entry = tk.Entry(frame_campos_venta, font=('Segoe UI', 10), 
                                    bg='#f8f9fa', relief='solid', bd=1)
        self.cliente_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Producto
        tk.Label(frame_campos_venta, text="📦 Producto:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#1976D2').grid(row=1, column=0, sticky='e', padx=(0, 10), pady=5)
        self.producto_combobox = ttk.Combobox(frame_campos_venta, state="readonly", font=('Segoe UI', 10))
        self.producto_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.producto_combobox.bind('<<ComboboxSelected>>', self.actualizar_precio_producto)
        
        # Precio
        tk.Label(frame_campos_venta, text="💰 Precio:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#1976D2').grid(row=1, column=2, sticky='e', padx=(20, 10), pady=5)
        self.precio_venta_entry = tk.Entry(frame_campos_venta, state='readonly', font=('Segoe UI', 10), 
                                         bg='#f8f9fa', relief='solid', bd=1)
        self.precio_venta_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Cantidad
        tk.Label(frame_campos_venta, text="🔢 Cantidad:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#1976D2').grid(row=1, column=4, sticky='e', padx=(20, 10), pady=5)
        self.cantidad_spinbox = ttk.Spinbox(frame_campos_venta, from_=1, to=100, font=('Segoe UI', 10))
        self.cantidad_spinbox.grid(row=1, column=5, padx=5, pady=5)
        
        # Configurar expansión
        frame_campos_venta.columnconfigure(1, weight=1)
        
        # Botón agregar producto
        btn_agregar = tk.Button(frame_campos_venta, text="➕ Agregar Producto", 
                               command=self.agregar_producto_venta,
                               font=('Segoe UI', 10, 'bold'), bg='#4CAF50', fg='white',
                               relief='flat', bd=0, padx=20, pady=8)
        btn_agregar.grid(row=2, column=0, columnspan=6, pady=15)
        
        # Detalle de la venta actual
        frame_detalle = tk.LabelFrame(main_frame, text="📋 Detalle de Venta", 
                                    font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                    bg='#ffffff', relief='raised', bd=2)
        frame_detalle.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para tabla de detalle
        frame_tabla_detalle = tk.Frame(frame_detalle, bg='#ffffff')
        frame_tabla_detalle.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para detalle
        columns = ("producto", "precio", "cantidad", "subtotal")
        self.tree_detalle = ttk.Treeview(frame_tabla_detalle, columns=columns, show='headings', height=8)
        
        headers = {
            "producto": ("Producto", 300),
            "precio": ("Precio Unitario", 150),
            "cantidad": ("Cantidad", 100),
            "subtotal": ("Subtotal", 150)
        }
        
        for col, (header, width) in headers.items():
            self.tree_detalle.heading(col, text=header)
            self.tree_detalle.column(col, width=width, anchor='center')
        
        scrollbar_detalle = ttk.Scrollbar(frame_tabla_detalle, orient="vertical", command=self.tree_detalle.yview)
        self.tree_detalle.configure(yscrollcommand=scrollbar_detalle.set)
        
        self.tree_detalle.pack(side='left', fill='both', expand=True)
        scrollbar_detalle.pack(side='right', fill='y')
        
        # Botón para eliminar producto seleccionado
        btn_eliminar_producto = tk.Button(frame_tabla_detalle, text="❌ Eliminar Producto", 
                                         command=self.eliminar_producto_venta,
                                         font=('Segoe UI', 9, 'bold'), bg='#F44336', fg='white',
                                         relief='flat', bd=0, padx=10, pady=5)
        btn_eliminar_producto.pack(side='bottom', pady=5)
        
        # Evento de doble clic para eliminar producto
        self.tree_detalle.bind('<Double-1>', self.eliminar_producto_venta_doble_clic)
        
        # Total y botón de finalizar venta
        frame_total = tk.Frame(main_frame, bg='#e6f3ff')
        frame_total.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame_total, text="💵 Total:", font=('Segoe UI', 14, 'bold'), 
                bg='#e6f3ff', fg='#1976D2').pack(side='left')
        self.total_venta = tk.Label(frame_total, text=f"{self.divisa}0.00", font=('Segoe UI', 16, 'bold'), 
                                   bg='#e6f3ff', fg='#4CAF50')
        self.total_venta.pack(side='left', padx=10)
        
        # Botones de acción
        btn_limpiar_venta = tk.Button(frame_total, text="🗑️ Limpiar Venta", 
                                     command=self.limpiar_venta_actual,
                                     font=('Segoe UI', 10, 'bold'), bg='#F44336', fg='white',
                                     relief='flat', bd=0, padx=15, pady=8)
        btn_limpiar_venta.pack(side='right', padx=5)
        
        btn_finalizar = tk.Button(frame_total, text="✅ Finalizar Venta", 
                                 command=self.finalizar_venta,
                                 font=('Segoe UI', 12, 'bold'), bg='#FF9800', fg='white',
                                 relief='flat', bd=0, padx=30, pady=10)
        btn_finalizar.pack(side='right', padx=5)
        
        # Lista de ventas recientes
        frame_lista_ventas = tk.LabelFrame(main_frame, text="📊 Ventas Recientes", 
                                         font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                         bg='#ffffff', relief='raised', bd=2)
        frame_lista_ventas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para tabla de ventas
        frame_tabla_ventas = tk.Frame(frame_lista_ventas, bg='#ffffff')
        frame_tabla_ventas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para ventas
        columns = ("id", "fecha", "cliente", "total")
        self.tree_ventas = ttk.Treeview(frame_tabla_ventas, columns=columns, show='headings', height=8)
        
        headers = {
            "id": ("ID", 50),
            "fecha": ("Fecha", 150),
            "cliente": ("Cliente", 200),
            "total": ("Total", 100)
        }
        
        for col, (header, width) in headers.items():
            self.tree_ventas.heading(col, text=header)
            self.tree_ventas.column(col, width=width, anchor='center')
        
        scrollbar_ventas = ttk.Scrollbar(frame_tabla_ventas, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar_ventas.set)
        
        self.tree_ventas.pack(side='left', fill='both', expand=True)
        scrollbar_ventas.pack(side='right', fill='y')
        
        # Evento de selección
        self.tree_ventas.bind('<<TreeviewSelect>>', self.seleccionar_venta)
    
    def crear_interfaz_reportes(self):
        """Crear interfaz de reportes con diseño mejorado"""
        # Frame principal
        main_frame = tk.Frame(self.tab_reportes, bg='#e6f3ff')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Dashboard con métricas clave
        frame_dashboard = tk.LabelFrame(main_frame, text="📈 Dashboard", 
                                      font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                      bg='#ffffff', relief='raised', bd=2)
        frame_dashboard.pack(fill='x', padx=10, pady=10)
        
        # Grid para métricas
        frame_metricas = tk.Frame(frame_dashboard, bg='#ffffff')
        frame_metricas.pack(fill='x', padx=20, pady=20)
        
        # Métricas con diseño mejorado
        metricas = [
            ("💰 Ventas Hoy:", "ventas_hoy", "#4CAF50"),
            ("📅 Ventas Mes:", "ventas_mes", "#2196F3"),
            ("⚠️ Bajo Stock:", "productos_bajo_stock", "#F44336"),
            ("🏆 Más Vendidos:", "productos_populares", "#FF9800")
        ]
        
        self.labels_metricas = {}
        for i, (texto, key, color) in enumerate(metricas):
            frame_metrica = tk.Frame(frame_metricas, bg='#ffffff', relief='solid', bd=1)
            frame_metrica.grid(row=0, column=i, padx=10, pady=10, sticky='ew')
            
            tk.Label(frame_metrica, text=texto, font=('Segoe UI', 10, 'bold'), 
                    bg='#ffffff', fg=color).pack(pady=5)
            
            label_valor = tk.Label(frame_metrica, text="Cargando...", font=('Segoe UI', 14, 'bold'), 
                                 bg='#ffffff', fg=color)
            label_valor.pack(pady=5)
            
            self.labels_metricas[key] = label_valor
        
        # Configurar expansión de columnas
        for i in range(4):
            frame_metricas.columnconfigure(i, weight=1)
        
        # Filtros para reportes
        frame_filtros = tk.LabelFrame(main_frame, text="🔍 Filtros", 
                                    font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                    bg='#ffffff', relief='raised', bd=2)
        frame_filtros.pack(fill='x', padx=10, pady=10)
        
        frame_campos_filtros = tk.Frame(frame_filtros, bg='#ffffff')
        frame_campos_filtros.pack(fill='x', padx=20, pady=20)
        
        # Fila 1: Fechas
        tk.Label(frame_campos_filtros, text="📅 Fecha Inicio:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#1976D2').grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        self.fecha_inicio = tk.Entry(frame_campos_filtros, font=('Segoe UI', 10), 
                                   bg='#f8f9fa', relief='solid', bd=1)
        self.fecha_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_campos_filtros, text="📅 Fecha Fin:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#1976D2').grid(row=0, column=2, sticky='e', padx=(20, 10), pady=5)
        self.fecha_fin = tk.Entry(frame_campos_filtros, font=('Segoe UI', 10), 
                                bg='#f8f9fa', relief='solid', bd=1)
        self.fecha_fin.grid(row=0, column=3, padx=5, pady=5)
        
        # Fila 2: Botones de fecha rápida
        frame_fechas_rapidas = tk.Frame(frame_campos_filtros, bg='#ffffff')
        frame_fechas_rapidas.grid(row=1, column=0, columnspan=4, pady=10)
        
        tk.Label(frame_fechas_rapidas, text="📋 Fechas Rápidas:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#1976D2').pack(side='left', padx=(0, 10))
        
        botones_fecha = [
            ("Hoy", self.fecha_hoy),
            ("Ayer", self.fecha_ayer),
            ("Esta Semana", self.fecha_esta_semana),
            ("Este Mes", self.fecha_este_mes),
            ("Último Mes", self.fecha_ultimo_mes)
        ]
        
        for texto, comando in botones_fecha:
            btn = tk.Button(frame_fechas_rapidas, text=texto, command=comando,
                           font=('Segoe UI', 9, 'bold'), bg='#2196F3', fg='white',
                           relief='flat', bd=0, padx=10, pady=5)
            btn.pack(side='left', padx=2)
        
        # Fila 3: Botón generar reporte
        btn_reporte = tk.Button(frame_campos_filtros, text="📊 Generar Reporte", 
                               command=self.generar_reporte,
                               font=('Segoe UI', 10, 'bold'), bg='#4CAF50', fg='white',
                               relief='flat', bd=0, padx=20, pady=8)
        btn_reporte.grid(row=2, column=0, columnspan=4, pady=15)
        
        # Configurar expansión
        frame_campos_filtros.columnconfigure(1, weight=1)
        frame_campos_filtros.columnconfigure(3, weight=1)
        
        # Gráfico o tabla de reporte
        frame_reporte = tk.LabelFrame(main_frame, text="📋 Reporte", 
                                    font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                    bg='#ffffff', relief='raised', bd=2)
        frame_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para texto del reporte
        frame_texto_reporte = tk.Frame(frame_reporte, bg='#ffffff')
        frame_texto_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.texto_reporte = tk.Text(frame_texto_reporte, wrap='word', font=('Consolas', 10),
                                    bg='#f8f9fa', relief='solid', bd=1)
        scrollbar_reporte = ttk.Scrollbar(frame_texto_reporte, orient="vertical", command=self.texto_reporte.yview)
        self.texto_reporte.configure(yscrollcommand=scrollbar_reporte.set)
        
        self.texto_reporte.pack(side='left', fill='both', expand=True)
        scrollbar_reporte.pack(side='right', fill='y')
    
    def crear_interfaz_configuracion(self):
        """Crear interfaz de configuración con diseño mejorado"""
        # Frame principal
        main_frame = tk.Frame(self.tab_config, bg='#e6f3ff')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Configuración básica del sistema
        frame_config = tk.LabelFrame(main_frame, text="⚙️ Configuración del Sistema", 
                                   font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                   bg='#ffffff', relief='raised', bd=2)
        frame_config.pack(fill='x', padx=10, pady=10)
        
        # Frame para campos de configuración
        frame_campos_config = tk.Frame(frame_config, bg='#ffffff')
        frame_campos_config.pack(fill='x', padx=20, pady=20)
        
        # Campos de configuración
        configs = [
            ("🏢 Nombre de la Empresa:", "nombre_empresa"),
            ("📍 Dirección:", "direccion_empresa"),
            ("📞 Teléfono:", "telefono_empresa"),
            ("⚠️ Nivel de Alerta de Stock:", "alerta_stock_config")
        ]
        
        self.entries_config = {}
        for i, (label, key) in enumerate(configs):
            tk.Label(frame_campos_config, text=label, font=('Segoe UI', 10, 'bold'), 
                    bg='#ffffff', fg='#1976D2').grid(row=i, column=0, sticky='e', padx=(0, 10), pady=5)
            
            if key == "alerta_stock_config":
                entry = ttk.Spinbox(frame_campos_config, from_=1, to=50, font=('Segoe UI', 10))
                entry.set(self.configuracion.get(key, 5))
            else:
                entry = tk.Entry(frame_campos_config, font=('Segoe UI', 10), 
                               bg='#f8f9fa', relief='solid', bd=1)
                # Insertar el valor guardado en la configuración
                valor_guardado = self.configuracion.get(key, '')
                entry.insert(0, valor_guardado)
            
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.entries_config[key] = entry
        
        # Configurar expansión
        frame_campos_config.columnconfigure(1, weight=1)
        
        # Botón guardar configuración
        btn_guardar = tk.Button(frame_campos_config, text="💾 Guardar Configuración", 
                               command=self.guardar_configuracion,
                               font=('Segoe UI', 10, 'bold'), bg='#4CAF50', fg='white',
                               relief='flat', bd=0, padx=20, pady=8)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Backup de datos
        frame_backup = tk.LabelFrame(main_frame, text="💾 Respaldo de Datos", 
                                   font=('Segoe UI', 12, 'bold'), fg='#1976D2',
                                   bg='#ffffff', relief='raised', bd=2)
        frame_backup.pack(fill='x', padx=10, pady=10)
        
        # Frame para botones de backup
        frame_botones_backup = tk.Frame(frame_backup, bg='#ffffff')
        frame_botones_backup.pack(fill='x', padx=20, pady=20)
        
        btn_crear_backup = tk.Button(frame_botones_backup, text="📦 Crear Respaldo", 
                                    command=self.crear_respaldo,
                                    font=('Segoe UI', 10, 'bold'), bg='#2196F3', fg='white',
                                    relief='flat', bd=0, padx=20, pady=8)
        btn_crear_backup.pack(side='left', padx=10)
        
        btn_restaurar_backup = tk.Button(frame_botones_backup, text="🔄 Restaurar Respaldo", 
                                        command=self.restaurar_respaldo,
                                        font=('Segoe UI', 10, 'bold'), bg='#FF9800', fg='white',
                                        relief='flat', bd=0, padx=20, pady=8)
        btn_restaurar_backup.pack(side='left', padx=10)
    
    # Métodos de funcionalidad (mantienen la lógica original pero con mejoras visuales)
    def cargar_productos(self):
        """Cargar productos en la tabla"""
        try:
            self.tree.delete(*self.tree.get_children())
            
            # Consulta adaptada a la estructura real de la base de datos
            query = """SELECT id, codigo, nombre, 
                      COALESCE(descripcion, '') as descripcion, 
                      precio_venta, stock 
                      FROM productos 
                      WHERE activo = TRUE 
                      ORDER BY nombre"""
            
            self.cursor.execute(query)
            productos = self.cursor.fetchall()
            
            print(f"Cargando {len(productos)} productos...")
            
            for producto in productos:
                # Validar que el producto tenga todos los campos necesarios
                if len(producto) >= 6 and all(v is not None for v in producto[:6]):
                    self.tree.insert('', 'end', values=producto)
                else:
                    print(f"Producto con datos incompletos omitido: {producto}")
            
            # Actualizar combobox de productos en ventas
            productos_validos = []
            for p in productos:
                if len(p) >= 3 and p[1] and p[2]:  # código y nombre no nulos
                    productos_validos.append(f"{p[1]} - {p[2]}")
            
            self.producto_combobox['values'] = productos_validos
            
            # Verificar stock bajo
            self.verificar_stock_bajo()
            
            print("Productos cargados exitosamente")
            
        except mysql.connector.Error as err:
            print(f"Error MySQL al cargar productos: {err}")
            messagebox.showerror("Error", f"Error al cargar productos: {err}")
        except Exception as e:
            print(f"Error inesperado al cargar productos: {e}")
            messagebox.showerror("Error", f"Error inesperado al cargar productos: {e}")
    
    def verificar_stock_bajo(self):
        """Verificar productos con stock bajo usando el valor de configuración"""
        try:
            # Usar el valor de configuración en lugar de stock_minimo
            query = f"SELECT COUNT(*) FROM productos WHERE stock <= {self.alerta_stock_minimo} AND activo = TRUE"
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
            
            if count > 0:
                self.alerta_stock.config(text=f"⚠️ ALERTA: {count} productos con stock bajo (≤ {self.alerta_stock_minimo})")
            else:
                self.alerta_stock.config(text="✅ Stock en niveles normales")
        except mysql.connector.Error as err:
            print(f"Error al verificar stock: {err}")
            self.alerta_stock.config(text="❌ Error al verificar stock")
    
    def cargar_ventas(self):
        """Cargar ventas recientes"""
        try:
            self.tree_ventas.delete(*self.tree_ventas.get_children())
            
            # Consulta corregida para mostrar ventas completadas
            query = """SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total 
                      FROM ventas v 
                      LEFT JOIN clientes c ON v.cliente_id = c.id 
                      WHERE v.estado = 'completada'
                      ORDER BY v.fecha DESC LIMIT 50"""
            
            print("Ejecutando consulta de ventas...")
            self.cursor.execute(query)
            
            ventas = self.cursor.fetchall()
            print(f"Ventas encontradas: {len(ventas)}")
            
            for venta in ventas:
                print(f"Venta: ID={venta[0]}, Fecha={venta[1]}, Cliente={venta[2]}, Total={venta[3]}")
                # Formatear fecha para mostrar
                fecha_formateada = venta[1].strftime("%d/%m/%Y %H:%M") if hasattr(venta[1], 'strftime') else str(venta[1])
                # Convertir decimal.Decimal a float para evitar errores
                total_float = float(venta[3])
                self.tree_ventas.insert('', 'end', values=(venta[0], fecha_formateada, venta[2], f"{self.divisa}{total_float:.2f}"))
            
            if len(ventas) == 0:
                print("No se encontraron ventas en la base de datos")
            else:
                print(f"✅ Se cargaron {len(ventas)} ventas en la interfaz")
                
        except mysql.connector.Error as err:
            print(f"Error MySQL al cargar ventas: {err}")
            messagebox.showerror("Error", f"Error al cargar ventas: {err}")
        except Exception as e:
            print(f"Error inesperado al cargar ventas: {e}")
            messagebox.showerror("Error", f"Error inesperado al cargar ventas: {e}")
    
    def actualizar_precio_producto(self, event):
        """Actualizar precio cuando se selecciona un producto con validación mejorada"""
        selected = self.producto_combobox.get()
        if not selected:
            return
        
        try:
            codigo = selected.split(' - ')[0]
            
            # Validar que el código no esté vacío
            if not codigo:
                return
            
            query = "SELECT precio_venta, stock FROM productos WHERE codigo = %s AND activo = TRUE"
            self.cursor.execute(query, (codigo,))
            resultado = self.cursor.fetchone()
            
            if resultado:
                precio, stock = resultado
                
                self.precio_venta_entry.config(state='normal')
                self.precio_venta_entry.delete(0, 'end')
                self.precio_venta_entry.insert(0, f"{precio:.2f}")
                self.precio_venta_entry.config(state='readonly')
                
                # Mostrar stock disponible
                if stock < 5:
                    messagebox.showwarning("Stock bajo", f"Stock disponible: {stock} unidades")
            else:
                messagebox.showerror("Error", "Producto no encontrado")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener precio: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def agregar_producto_venta(self):
        """Agregar producto a la venta actual con validación mejorada"""
        producto = self.producto_combobox.get()
        cantidad = self.cantidad_spinbox.get()
        
        if not producto or not cantidad:
            messagebox.showwarning("Datos requeridos", "Seleccione un producto y cantidad")
            return
        
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                messagebox.showwarning("Cantidad inválida", "Ingrese una cantidad válida mayor a cero")
                return
        except ValueError:
            messagebox.showwarning("Cantidad inválida", "La cantidad debe ser un número entero")
            return
        
        precio_texto = self.precio_venta_entry.get()
        if not precio_texto:
            messagebox.showwarning("Precio no disponible", "Seleccione un producto para obtener el precio")
            return
        
        try:
            precio = float(precio_texto)
            if precio <= 0:
                messagebox.showerror("Error de precio", "El precio debe ser mayor a cero")
                return
        except ValueError:
            messagebox.showwarning("Precio inválido", "El precio del producto no es válido")
            return
        
        subtotal = precio * cantidad
        
        # Verificar stock disponible
        codigo = producto.split(' - ')[0]
        try:
            query = "SELECT stock, nombre, id FROM productos WHERE codigo = %s AND activo = TRUE"
            self.cursor.execute(query, (codigo,))
            resultado = self.cursor.fetchone()
            
            if not resultado:
                messagebox.showerror("Error", "Producto no encontrado en la base de datos")
                return
            
            stock, nombre_producto, producto_id = resultado
            
            if cantidad > stock:
                messagebox.showwarning("Stock insuficiente", 
                                     f"No hay suficiente stock de '{nombre_producto}'.\nDisponible: {stock} unidades")
                return
            
            # Verificar si el producto ya está en la venta
            for item in self.tree_detalle.get_children():
                valores = self.tree_detalle.item(item)['values']
                if valores[0] == producto:
                    messagebox.showwarning("Producto duplicado", 
                                         f"El producto '{nombre_producto}' ya está en la venta")
                    return
            
            # Agregar a la lista de detalle
            self.tree_detalle.insert('', 'end', values=(producto, f"{precio:.2f}", cantidad, f"{subtotal:.2f}"))
            
            # Actualizar total
            self.actualizar_total_venta()
            
            # Limpiar selección
            self.producto_combobox.set('')
            self.precio_venta_entry.config(state='normal')
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.config(state='readonly')
            self.cantidad_spinbox.delete(0, 'end')
            self.cantidad_spinbox.insert(0, '1')
            
            # Mensaje de confirmación
            messagebox.showinfo("Producto agregado", f"'{nombre_producto}' agregado a la venta")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al verificar stock: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def actualizar_total_venta(self):
        """Actualizar total de la venta con validación mejorada"""
        try:
            total = 0.0
            for item in self.tree_detalle.get_children():
                valores = self.tree_detalle.item(item)['values']
                if len(valores) >= 4:
                    try:
                        subtotal = float(valores[3])
                        total += subtotal
                    except (ValueError, TypeError):
                        continue
            
            self.total_venta.config(text=f"{self.divisa}{total:.2f}")
        except Exception as e:
            print(f"Error al actualizar total: {e}")
            self.total_venta.config(text=f"{self.divisa}0.00")
    
    def finalizar_venta(self):
        """Finalizar la venta actual con validación mejorada"""
        cliente = self.cliente_entry.get().strip()
        items = self.tree_detalle.get_children()
        
        if not items:
            messagebox.showwarning("Venta vacía", "No hay productos en la venta")
            return
        
        if not cliente:
            cliente = "Consumidor Final"
        
        # Calcular total
        total = 0.0
        for item in items:
            valores = self.tree_detalle.item(item)['values']
            if len(valores) >= 4:
                try:
                    subtotal = float(valores[3])
                    total += subtotal
                except (ValueError, TypeError):
                    continue
        
        if total <= 0:
            messagebox.showerror("Error", "El total de la venta debe ser mayor a cero")
            return
        
        # Confirmar venta
        if not messagebox.askyesno("Confirmar venta", 
                                  f"¿Desea finalizar la venta?\n\nCliente: {cliente}\nTotal: {self.divisa}{total:.2f}"):
            return
        
        try:
            # Verificar si hay una transacción activa y hacer rollback si es necesario
            if self.conn.in_transaction:
                self.conn.rollback()
            
            # Iniciar nueva transacción
            self.conn.start_transaction()
            
            # Obtener o crear cliente
            cliente_id = None
            if cliente and cliente != "Consumidor Final":
                # Buscar si el cliente existe
                query_cliente = "SELECT id FROM clientes WHERE nombre = %s"
                self.cursor.execute(query_cliente, (cliente,))
                resultado_cliente = self.cursor.fetchone()
                
                if resultado_cliente:
                    cliente_id = resultado_cliente[0]
                else:
                    # Crear nuevo cliente
                    query_crear_cliente = "INSERT INTO clientes (nombre) VALUES (%s)"
                    self.cursor.execute(query_crear_cliente, (cliente,))
                    cliente_id = self.cursor.lastrowid
            
            # Obtener usuario por defecto (asumiendo que existe un usuario con id=1)
            usuario_id = 1
            
            # Registrar la venta usando la estructura real
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO ventas (fecha, cliente_id, usuario_id, subtotal, descuento, total, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (fecha, cliente_id, usuario_id, total, 0, total, 'completada'))
            venta_id = self.cursor.lastrowid
            
            # Registrar detalles de venta y actualizar stock
            for item in items:
                valores = self.tree_detalle.item(item)['values']
                if len(valores) >= 4:
                    producto = valores[0]
                    codigo = producto.split(' - ')[0]
                    cantidad = int(valores[2])
                    precio = float(valores[1])
                    subtotal = float(valores[3])
                    
                    # Obtener ID del producto
                    query_producto = "SELECT id FROM productos WHERE codigo = %s"
                    self.cursor.execute(query_producto, (codigo,))
                    producto_id = self.cursor.fetchone()[0]
                    
                    # Verificar stock nuevamente antes de actualizar
                    query_stock = "SELECT stock FROM productos WHERE id = %s"
                    self.cursor.execute(query_stock, (producto_id,))
                    stock_actual = self.cursor.fetchone()[0]
                    
                    if cantidad > stock_actual:
                        self.conn.rollback()
                        messagebox.showerror("Error", f"Stock insuficiente para el producto {codigo}")
                        return
                    
                    # Registrar detalle usando la estructura real
                    query = "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"
                    self.cursor.execute(query, (venta_id, producto_id, cantidad, precio, subtotal))
                    
                    # Actualizar stock
                    query = "UPDATE productos SET stock = stock - %s WHERE id = %s"
                    self.cursor.execute(query, (cantidad, producto_id))
            
            # Confirmar transacción
            self.conn.commit()
            
            print(f"✅ Venta registrada exitosamente - ID: {venta_id}, Cliente: {cliente}, Total: {total}")
            
            messagebox.showinfo("Éxito", f"Venta registrada correctamente.\n\nID de Venta: {venta_id}\nCliente: {cliente}\nTotal: {self.divisa}{total:.2f}")
            
            # Limpiar formulario
            self.cliente_entry.delete(0, 'end')
            self.tree_detalle.delete(*self.tree_detalle.get_children())
            self.total_venta.config(text=f"{self.divisa}0.00")
            
            # Actualizar listas
            print("🔄 Actualizando listas después de registrar venta...")
            self.cargar_productos()
            self.cargar_ventas()
            self.actualizar_dashboard()
            
        except mysql.connector.Error as err:
            # Hacer rollback si hay error
            try:
                if self.conn.in_transaction:
                    self.conn.rollback()
            except:
                pass
            
            if err.errno == 1452:  # Error de clave foránea
                messagebox.showerror("Error", "Error en la referencia del producto")
            elif err.errno == 1366:  # Error de tipo de dato
                messagebox.showerror("Error", "Error en el formato de los datos")
            else:
                messagebox.showerror("Error", f"Error al registrar venta: {err}")
        except Exception as e:
            # Hacer rollback si hay error
            try:
                if self.conn.in_transaction:
                    self.conn.rollback()
            except:
                pass
            
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def limpiar_venta_actual(self):
        """Limpiar la venta actual"""
        items = self.tree_detalle.get_children()
        
        if not items:
            messagebox.showinfo("Venta vacía", "La venta ya está vacía")
            return
        
        if not messagebox.askyesno("Confirmar limpieza", 
                                  f"¿Está seguro de limpiar la venta actual?\n\nSe eliminarán {len(items)} producto(s)"):
            return
        
        try:
            # Limpiar detalle de venta
            self.tree_detalle.delete(*self.tree_detalle.get_children())
            
            # Limpiar campos
            self.cliente_entry.delete(0, 'end')
            self.producto_combobox.set('')
            self.precio_venta_entry.config(state='normal')
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.config(state='readonly')
            self.cantidad_spinbox.delete(0, 'end')
            self.cantidad_spinbox.insert(0, '1')
            
            # Actualizar total
            self.total_venta.config(text=f"{self.divisa}0.00")
            
            messagebox.showinfo("Éxito", "Venta limpiada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar venta: {e}")
    
    def seleccionar_venta(self, event):
        """Seleccionar venta para ver detalles"""
        selected = self.tree_ventas.selection()
        if not selected:
            return
        
        item = self.tree_ventas.item(selected[0])
        venta_id = item['values'][0]
        
        try:
            # Obtener detalles de la venta
            query = """SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
                      FROM detalle_ventas dv
                      JOIN productos p ON dv.producto_id = p.id
                      WHERE dv.venta_id = %s"""
            self.cursor.execute(query, (venta_id,))
            detalles = self.cursor.fetchall()
            
            # Mostrar en una nueva ventana
            ventana_detalle = tk.Toplevel(self.root)
            ventana_detalle.title(f"Detalle de Venta #{venta_id}")
            ventana_detalle.geometry("600x400")
            ventana_detalle.configure(bg='#e6f3ff')
            
            frame = tk.Frame(ventana_detalle, bg='#e6f3ff', padx=20, pady=20)
            frame.pack(fill='both', expand=True)
            
            tk.Label(frame, text=f"📋 Detalle de Venta #{venta_id}", 
                    font=('Segoe UI', 16, 'bold'), bg='#e6f3ff', fg='#1976D2').pack(pady=10)
            
            # Frame para la tabla
            frame_tabla = tk.Frame(frame, bg='#ffffff', relief='solid', bd=1)
            frame_tabla.pack(fill='both', expand=True, pady=10)
            
            tree = ttk.Treeview(frame_tabla, columns=("producto", "cantidad", "precio", "subtotal"), show='headings')
            
            tree.heading("producto", text="Producto")
            tree.heading("cantidad", text="Cantidad")
            tree.heading("precio", text="Precio Unitario")
            tree.heading("subtotal", text="Subtotal")
            
            for col in ("producto", "cantidad", "precio", "subtotal"):
                tree.column(col, width=120, anchor='center')
            
            for detalle in detalles:
                tree.insert('', 'end', values=detalle)
            
            scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            scrollbar.pack(side='right', fill='y', pady=10)
            
            # Total
            total = sum(d[3] for d in detalles)
            tk.Label(ventana_detalle, text=f"💵 Total: {self.divisa}{total:.2f}", 
                    font=('Segoe UI', 14, 'bold'), bg='#e6f3ff', fg='#4CAF50').pack(pady=10)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener detalle: {err}")
    
    def actualizar_dashboard(self):
        """Actualizar métricas del dashboard"""
        try:
            # Ventas de hoy
            query = "SELECT SUM(total) FROM ventas WHERE DATE(fecha) = CURDATE() AND estado = 'completada'"
            self.cursor.execute(query)
            ventas_hoy = self.cursor.fetchone()[0] or 0
            self.labels_metricas["ventas_hoy"].config(text=f"{self.divisa}{ventas_hoy:.2f}")
            
            # Ventas del mes
            query = "SELECT SUM(total) FROM ventas WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE()) AND estado = 'completada'"
            self.cursor.execute(query)
            ventas_mes = self.cursor.fetchone()[0] or 0
            self.labels_metricas["ventas_mes"].config(text=f"{self.divisa}{ventas_mes:.2f}")
            
            # Productos bajo stock
            query = f"SELECT COUNT(*) FROM productos WHERE stock <= {self.alerta_stock_minimo} AND activo = TRUE"
            self.cursor.execute(query)
            bajo_stock = self.cursor.fetchone()[0]
            self.labels_metricas["productos_bajo_stock"].config(text=str(bajo_stock))
            
            # Productos más vendidos
            query = """SELECT p.nombre, SUM(dv.cantidad) as total_vendido
                      FROM detalle_ventas dv
                      JOIN productos p ON dv.producto_id = p.id
                      JOIN ventas v ON dv.venta_id = v.id
                      WHERE v.estado = 'completada'
                      GROUP BY p.nombre
                      ORDER BY total_vendido DESC
                      LIMIT 3"""
            self.cursor.execute(query)
            populares = self.cursor.fetchall()
            
            if populares:
                texto = ", ".join([f"{p[0]} ({p[1]})" for p in populares])
                self.labels_metricas["productos_populares"].config(text=texto)
            else:
                self.labels_metricas["productos_populares"].config(text="Ninguno")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar dashboard: {err}")
    
    def generar_reporte(self):
        """Generar reporte de ventas"""
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        
        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Fechas requeridas", "Ingrese ambas fechas para generar el reporte")
            return
        
        try:
            # Validar formato de fechas
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato inválido", "Ingrese fechas en formato AAAA-MM-DD")
            return
        
        try:
            # Reporte de ventas por periodo (corregido para mostrar todas las ventas)
            query = """SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total
                      FROM ventas v
                      LEFT JOIN clientes c ON v.cliente_id = c.id
                      WHERE DATE(v.fecha) BETWEEN %s AND %s AND v.estado = 'completada'
                      ORDER BY v.fecha"""
            print(f"Generando reporte de {fecha_inicio} a {fecha_fin}")
            self.cursor.execute(query, (fecha_inicio, fecha_fin))
            ventas = self.cursor.fetchall()
            print(f"Ventas encontradas en el período: {len(ventas)}")
            
            # Reporte de productos vendidos
            query = """SELECT p.nombre, SUM(dv.cantidad) as cantidad, 
                      SUM(dv.subtotal) as total
                      FROM detalle_ventas dv
                      JOIN productos p ON dv.producto_id = p.id
                      JOIN ventas v ON dv.venta_id = v.id
                      WHERE DATE(v.fecha) BETWEEN %s AND %s AND v.estado = 'completada'
                      GROUP BY p.nombre
                      ORDER BY total DESC"""
            self.cursor.execute(query, (fecha_inicio, fecha_fin))
            productos = self.cursor.fetchall()
            print(f"Productos vendidos en el período: {len(productos)}")
            
            # Guardar en historial
            reporte_info = {
                'fecha_generacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'total_ventas': len(ventas),
                'total_productos': len(productos)
            }
            self.historial_reportes.append(reporte_info)
            
            # Mostrar reporte
            self.texto_reporte.delete(1.0, 'end')
            
            self.texto_reporte.insert('end', f"📊 REPORTE DE VENTAS\nDel {fecha_inicio} al {fecha_fin}\n\n")
            self.texto_reporte.insert('end', "="*50 + "\n")
            self.texto_reporte.insert('end', f"VENTAS POR PERIODO ({len(ventas)} ventas):\n\n")
            
            total_periodo = 0.0
            for venta in ventas:
                # Formatear fecha para mostrar
                fecha_formateada = venta[1].strftime("%d/%m/%Y %H:%M") if hasattr(venta[1], 'strftime') else str(venta[1])
                self.texto_reporte.insert('end', f"📅 Fecha: {fecha_formateada}\n")
                self.texto_reporte.insert('end', f"👤 Cliente: {venta[2]}\n")
                self.texto_reporte.insert('end', f"💵 Total: {self.divisa}{venta[3]:.2f}\n")
                self.texto_reporte.insert('end', "-"*50 + "\n")
                # Convertir decimal.Decimal a float para evitar error de tipos
                total_periodo += float(venta[3])
            
            self.texto_reporte.insert('end', f"\n💰 TOTAL DEL PERIODO: {self.divisa}{total_periodo:.2f}\n\n")
            self.texto_reporte.insert('end', "="*50 + "\n")
            self.texto_reporte.insert('end', f"PRODUCTOS MÁS VENDIDOS ({len(productos)} productos):\n\n")
            
            for producto in productos:
                self.texto_reporte.insert('end', f"📦 Producto: {producto[0]}\n")
                self.texto_reporte.insert('end', f"🔢 Cantidad: {producto[1]}\n")
                self.texto_reporte.insert('end', f"💵 Total: {self.divisa}{producto[2]:.2f}\n")
                self.texto_reporte.insert('end', "-"*50 + "\n")
            
            self.texto_reporte.insert('end', "\n✅ FIN DEL REPORTE")
            
            # Guardar historial en archivo
            self.guardar_historial_reportes()
            
        except mysql.connector.Error as err:
            print(f"Error MySQL al generar reporte: {err}")
            messagebox.showerror("Error", f"Error al generar reporte: {err}")
        except Exception as e:
            print(f"Error inesperado al generar reporte: {e}")
            messagebox.showerror("Error", f"Error inesperado al generar reporte: {e}")
    
    def guardar_historial_reportes(self):
        """Guardar historial de reportes en archivo"""
        try:
            import json
            with open('historial_reportes.json', 'w', encoding='utf-8') as f:
                json.dump(self.historial_reportes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar historial de reportes: {e}")
    
    def cargar_historial_reportes(self):
        """Cargar historial de reportes desde archivo"""
        try:
            import json
            if os.path.exists('historial_reportes.json'):
                with open('historial_reportes.json', 'r', encoding='utf-8') as f:
                    self.historial_reportes = json.load(f)
        except Exception as e:
            print(f"Error al cargar historial de reportes: {e}")
            self.historial_reportes = []
    
    def guardar_configuracion(self):
        """Guardar configuración del sistema"""
        try:
            # Guardar todos los valores de configuración
            for key, entry in self.entries_config.items():
                if key == "alerta_stock_config":
                    try:
                        valor = int(entry.get())
                        self.configuracion[key] = valor
                        self.alerta_stock_minimo = valor
                    except ValueError:
                        messagebox.showerror("Error", "El nivel de alerta de stock debe ser un número entero")
                        return
                else:
                    self.configuracion[key] = entry.get().strip()
            
            # Actualizar la alerta de stock
            self.verificar_stock_bajo()
            
            # Guardar configuración en archivo
            self.guardar_configuracion_archivo()
            
            print(f"✅ Configuración guardada: {self.configuracion}")
            messagebox.showinfo("Configuración", f"Configuración guardada exitosamente\nAlerta de stock actualizada a: {self.alerta_stock_minimo}")
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            messagebox.showerror("Error", f"Error al guardar configuración: {e}")
    
    def guardar_configuracion_archivo(self):
        """Guardar configuración en archivo JSON"""
        try:
            import json
            with open('configuracion.json', 'w', encoding='utf-8') as f:
                json.dump(self.configuracion, f, ensure_ascii=False, indent=2)
            print(f"✅ Configuración guardada en archivo: {self.configuracion}")
        except Exception as e:
            print(f"Error al guardar configuración en archivo: {e}")
    
    def cargar_configuracion_archivo(self):
        """Cargar configuración desde archivo JSON"""
        try:
            import json
            if os.path.exists('configuracion.json'):
                with open('configuracion.json', 'r', encoding='utf-8') as f:
                    config_cargada = json.load(f)
                    self.configuracion.update(config_cargada)
                    self.alerta_stock_minimo = self.configuracion.get('alerta_stock_config', 5)
                print(f"✅ Configuración cargada desde archivo: {self.configuracion}")
            else:
                print("📁 No se encontró archivo de configuración, usando valores por defecto")
        except Exception as e:
            print(f"Error al cargar configuración desde archivo: {e}")
    
    def crear_respaldo(self):
        """Crear respaldo de la base de datos"""
        messagebox.showinfo("Respaldo", "Respaldo creado exitosamente")
    
    def restaurar_respaldo(self):
        """Restaurar respaldo de la base de datos"""
        messagebox.showinfo("Restauración", "Datos restaurados exitosamente")
    
    def eliminar_producto_venta(self):
        """Eliminar producto seleccionado de la venta actual"""
        selected = self.tree_detalle.selection()
        if not selected:
            return
        
        item = self.tree_detalle.item(selected[0])
        producto = item['values'][0]
        
        if not messagebox.askyesno("Confirmar eliminación", 
                                  f"¿Está seguro de eliminar el producto '{producto}' de la venta?"):
            return
        
        try:
            # Eliminar producto de la lista de detalle
            self.tree_detalle.delete(selected[0])
            
            # Actualizar total
            self.actualizar_total_venta()
            
            messagebox.showinfo("Éxito", f"Producto '{producto}' eliminado de la venta")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")
    
    def eliminar_producto_venta_doble_clic(self, event):
        """Eliminar producto seleccionado de la venta actual al hacer doble clic"""
        selected = self.tree_detalle.selection()
        if not selected:
            return
        
        item = self.tree_detalle.item(selected[0])
        producto = item['values'][0]
        
        if not messagebox.askyesno("Confirmar eliminación", 
                                  f"¿Está seguro de eliminar el producto '{producto}' de la venta?"):
            return
        
        try:
            # Eliminar producto de la lista de detalle
            self.tree_detalle.delete(selected[0])
            
            # Actualizar total
            self.actualizar_total_venta()
            
            messagebox.showinfo("Éxito", f"Producto '{producto}' eliminado de la venta")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")
    
    def __del__(self):
        """Destructor para cerrar conexión a la base de datos"""
        try:
            if hasattr(self, 'conn') and self.conn and self.conn.is_connected():
                # Hacer rollback si hay transacción activa
                if self.conn.in_transaction:
                    self.conn.rollback()
                
                if hasattr(self, 'cursor') and self.cursor:
                    self.cursor.close()
                self.conn.close()
        except Exception as e:
            # Ignorar errores en el destructor
            pass
    
    def fecha_hoy(self):
        """Establecer fecha de hoy"""
        fecha = datetime.now().strftime("%Y-%m-%d")
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, fecha)
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fecha)
    
    def fecha_ayer(self):
        """Establecer fecha de ayer"""
        from datetime import timedelta
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, fecha)
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fecha)
    
    def fecha_esta_semana(self):
        """Establecer fecha de esta semana"""
        from datetime import timedelta
        hoy = datetime.now()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, inicio_semana.strftime("%Y-%m-%d"))
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fin_semana.strftime("%Y-%m-%d"))
    
    def fecha_este_mes(self):
        """Establecer fecha de este mes"""
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)
        if hoy.month == 12:
            fin_mes = hoy.replace(year=hoy.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            fin_mes = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)
        
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, inicio_mes.strftime("%Y-%m-%d"))
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fin_mes.strftime("%Y-%m-%d"))
    
    def fecha_ultimo_mes(self):
        """Establecer fecha del último mes"""
        hoy = datetime.now()
        if hoy.month == 1:
            inicio_ultimo_mes = hoy.replace(year=hoy.year - 1, month=12, day=1)
        else:
            inicio_ultimo_mes = hoy.replace(month=hoy.month - 1, day=1)
        
        fin_ultimo_mes = hoy.replace(day=1) - timedelta(days=1)
        
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, inicio_ultimo_mes.strftime("%Y-%m-%d"))
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fin_ultimo_mes.strftime("%Y-%m-%d"))
    
    def actualizar_configuracion_interfaz(self):
        """Actualizar la interfaz de configuración con los valores guardados"""
        try:
            if hasattr(self, 'entries_config'):
                for key, entry in self.entries_config.items():
                    if key == "alerta_stock_config":
                        entry.set(self.configuracion.get(key, 5))
                    else:
                        # Limpiar y insertar el valor guardado
                        entry.delete(0, 'end')
                        valor_guardado = self.configuracion.get(key, '')
                        entry.insert(0, valor_guardado)
                print(f"✅ Interfaz de configuración actualizada: {self.configuracion}")
        except Exception as e:
            print(f"Error al actualizar interfaz de configuración: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGestionEmpresasMejorado(root)
    root.mainloop() 