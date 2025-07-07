import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class SistemaGestionEmpresas:
    def __init__(self, root):
        self.root = root
        self.root.title("Software de Gestión para Pequeñas Empresas")
        self.root.geometry("1000x700")
        
        # Conexión a MySQL (configura estos valores según tu instalación)
        self.db_config = {
                'host': 'localhost',      # Esto no cambia (a menos que MySQL esté en otro servidor)
                'user': 'admin',          # Usuario creado en MySQL
                'password': 'admin123',   # Contraseña que definimos
                'database': 'gestion_empresas'  # Nombre de la base de datos
        }
        
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Conexión exitosa", "Conectado a la base de datos MySQL")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"Error al conectar a MySQL: {err}")
            self.root.destroy()
            return
        
        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña de Inventario
        self.tab_inventario = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_inventario, text="Inventario")
        self.crear_interfaz_inventario()
        
        # Pestaña de Ventas
        self.tab_ventas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ventas, text="Ventas")
        self.crear_interfaz_ventas()
        
        # Pestaña de Reportes
        self.tab_reportes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reportes, text="Reportes")
        self.crear_interfaz_reportes()
        
        # Pestaña de Configuración
        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="Configuración")
        self.crear_interfaz_configuracion()
        
        # Cargar datos iniciales
        self.cargar_productos()
        self.cargar_ventas()
        self.actualizar_dashboard()
    
    def crear_interfaz_inventario(self):
        # Frame para formulario de productos
        frame_form = ttk.LabelFrame(self.tab_inventario, text="Gestión de Productos", padding=10)
        frame_form.pack(fill='x', padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(frame_form, text="Código:").grid(row=0, column=0, sticky='e')
        self.codigo_entry = ttk.Entry(frame_form)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky='e')
        self.nombre_entry = ttk.Entry(frame_form)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Descripción:").grid(row=2, column=0, sticky='e')
        self.descripcion_entry = ttk.Entry(frame_form)
        self.descripcion_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Precio:").grid(row=3, column=0, sticky='e')
        self.precio_entry = ttk.Entry(frame_form)
        self.precio_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Stock:").grid(row=4, column=0, sticky='e')
        self.stock_entry = ttk.Entry(frame_form)
        self.stock_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botones de acción
        frame_botones = ttk.Frame(frame_form)
        frame_botones.grid(row=5, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Agregar", command=self.agregar_producto).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Actualizar", command=self.actualizar_producto).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_producto).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar_formulario).pack(side='left', padx=5)
        
        # Lista de productos
        frame_lista = ttk.LabelFrame(self.tab_inventario, text="Lista de Productos", padding=10)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ("id", "codigo", "nombre", "descripcion", "precio", "stock")
        self.tree = ttk.Treeview(frame_lista, columns=columns, show='headings')
        
        self.tree.heading("id", text="ID")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")
        
        self.tree.column("id", width=50)
        self.tree.column("codigo", width=100)
        self.tree.column("nombre", width=150)
        self.tree.column("descripcion", width=200)
        self.tree.column("precio", width=80)
        self.tree.column("stock", width=80)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)
        
        # Alertas de stock bajo
        self.alerta_stock = ttk.Label(self.tab_inventario, text="", foreground='red')
        self.alerta_stock.pack(pady=5)
    
    def crear_interfaz_ventas(self):
        # Frame para nueva venta
        frame_venta = ttk.LabelFrame(self.tab_ventas, text="Nueva Venta", padding=10)
        frame_venta.pack(fill='x', padx=10, pady=5)
        
        # Selección de cliente
        ttk.Label(frame_venta, text="Cliente:").grid(row=0, column=0, sticky='e')
        self.cliente_entry = ttk.Entry(frame_venta)
        self.cliente_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        # Selección de producto
        ttk.Label(frame_venta, text="Producto:").grid(row=1, column=0, sticky='e')
        self.producto_combobox = ttk.Combobox(frame_venta, state="readonly")
        self.producto_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        self.producto_combobox.bind('<<ComboboxSelected>>', self.actualizar_precio_producto)
        
        ttk.Label(frame_venta, text="Precio:").grid(row=1, column=2, sticky='e')
        self.precio_venta_entry = ttk.Entry(frame_venta, state='readonly')
        self.precio_venta_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(frame_venta, text="Cantidad:").grid(row=1, column=4, sticky='e')
        self.cantidad_spinbox = ttk.Spinbox(frame_venta, from_=1, to=100)
        self.cantidad_spinbox.grid(row=1, column=5, padx=5, pady=5)
        
        # Botón para agregar producto a la venta
        ttk.Button(frame_venta, text="Agregar Producto", command=self.agregar_producto_venta).grid(row=2, column=0, columnspan=6, pady=10)
        
        # Detalle de la venta actual
        frame_detalle = ttk.LabelFrame(self.tab_ventas, text="Detalle de Venta", padding=10)
        frame_detalle.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ("producto", "precio", "cantidad", "subtotal")
        self.tree_detalle = ttk.Treeview(frame_detalle, columns=columns, show='headings')
        
        self.tree_detalle.heading("producto", text="Producto")
        self.tree_detalle.heading("precio", text="Precio Unitario")
        self.tree_detalle.heading("cantidad", text="Cantidad")
        self.tree_detalle.heading("subtotal", text="Subtotal")
        
        for col in columns:
            self.tree_detalle.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_detalle, orient="vertical", command=self.tree_detalle.yview)
        self.tree_detalle.configure(yscrollcommand=scrollbar.set)
        
        self.tree_detalle.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Total y botón de finalizar venta
        frame_total = ttk.Frame(self.tab_ventas)
        frame_total.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_total, text="Total:").pack(side='left')
        self.total_venta = ttk.Label(frame_total, text="$0.00", font=('Arial', 12, 'bold'))
        self.total_venta.pack(side='left', padx=10)
        
        ttk.Button(frame_total, text="Finalizar Venta", command=self.finalizar_venta).pack(side='right')
        
        # Lista de ventas recientes
        frame_lista_ventas = ttk.LabelFrame(self.tab_ventas, text="Ventas Recientes", padding=10)
        frame_lista_ventas.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ("id", "fecha", "cliente", "total")
        self.tree_ventas = ttk.Treeview(frame_lista_ventas, columns=columns, show='headings')
        
        self.tree_ventas.heading("id", text="ID")
        self.tree_ventas.heading("fecha", text="Fecha")
        self.tree_ventas.heading("cliente", text="Cliente")
        self.tree_ventas.heading("total", text="Total")
        
        self.tree_ventas.column("id", width=50)
        self.tree_ventas.column("fecha", width=150)
        self.tree_ventas.column("cliente", width=200)
        self.tree_ventas.column("total", width=100)
        
        scrollbar = ttk.Scrollbar(frame_lista_ventas, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar.set)
        
        self.tree_ventas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Evento de selección
        self.tree_ventas.bind('<<TreeviewSelect>>', self.seleccionar_venta)
    
    def crear_interfaz_reportes(self):
        # Dashboard con métricas clave
        frame_dashboard = ttk.LabelFrame(self.tab_reportes, text="Dashboard", padding=10)
        frame_dashboard.pack(fill='x', padx=10, pady=5)
        
        # Métricas
        ttk.Label(frame_dashboard, text="Ventas Hoy:").grid(row=0, column=0, padx=10)
        self.ventas_hoy = ttk.Label(frame_dashboard, text="$0.00", font=('Arial', 12))
        self.ventas_hoy.grid(row=1, column=0)
        
        ttk.Label(frame_dashboard, text="Ventas Mes:").grid(row=0, column=1, padx=10)
        self.ventas_mes = ttk.Label(frame_dashboard, text="$0.00", font=('Arial', 12))
        self.ventas_mes.grid(row=1, column=1)
        
        ttk.Label(frame_dashboard, text="Productos Bajo Stock:").grid(row=0, column=2, padx=10)
        self.productos_bajo_stock = ttk.Label(frame_dashboard, text="0", font=('Arial', 12))
        self.productos_bajo_stock.grid(row=1, column=2)
        
        ttk.Label(frame_dashboard, text="Productos Más Vendidos:").grid(row=0, column=3, padx=10)
        self.productos_populares = ttk.Label(frame_dashboard, text="Ninguno", font=('Arial', 12))
        self.productos_populares.grid(row=1, column=3)
        
        # Filtros para reportes
        frame_filtros = ttk.LabelFrame(self.tab_reportes, text="Filtros", padding=10)
        frame_filtros.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_filtros, text="Fecha Inicio:").grid(row=0, column=0)
        self.fecha_inicio = ttk.Entry(frame_filtros)
        self.fecha_inicio.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_filtros, text="Fecha Fin:").grid(row=0, column=2)
        self.fecha_fin = ttk.Entry(frame_filtros)
        self.fecha_fin.grid(row=0, column=3, padx=5)
        
        ttk.Button(frame_filtros, text="Generar Reporte", command=self.generar_reporte).grid(row=0, column=4, padx=10)
        
        # Gráfico o tabla de reporte
        frame_reporte = ttk.LabelFrame(self.tab_reportes, text="Reporte", padding=10)
        frame_reporte.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.texto_reporte = tk.Text(frame_reporte, wrap='word')
        scrollbar = ttk.Scrollbar(frame_reporte, orient="vertical", command=self.texto_reporte.yview)
        self.texto_reporte.configure(yscrollcommand=scrollbar.set)
        
        self.texto_reporte.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def crear_interfaz_configuracion(self):
        # Configuración básica del sistema
        frame_config = ttk.LabelFrame(self.tab_config, text="Configuración del Sistema", padding=10)
        frame_config.pack(fill='both', padx=10, pady=5)
        
        ttk.Label(frame_config, text="Nombre de la Empresa:").grid(row=0, column=0, sticky='e')
        self.nombre_empresa = ttk.Entry(frame_config)
        self.nombre_empresa.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(frame_config, text="Dirección:").grid(row=1, column=0, sticky='e')
        self.direccion_empresa = ttk.Entry(frame_config)
        self.direccion_empresa.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(frame_config, text="Teléfono:").grid(row=2, column=0, sticky='e')
        self.telefono_empresa = ttk.Entry(frame_config)
        self.telefono_empresa.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(frame_config, text="Nivel de Alerta de Stock:").grid(row=3, column=0, sticky='e')
        self.alerta_stock_config = ttk.Spinbox(frame_config, from_=1, to=50)
        self.alerta_stock_config.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        self.alerta_stock_config.set(5)
        
        ttk.Button(frame_config, text="Guardar Configuración", command=self.guardar_configuracion).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Backup de datos
        frame_backup = ttk.LabelFrame(self.tab_config, text="Respaldo de Datos", padding=10)
        frame_backup.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_backup, text="Crear Respaldo", command=self.crear_respaldo).pack(pady=5)
        ttk.Button(frame_backup, text="Restaurar Respaldo", command=self.restaurar_respaldo).pack(pady=5)
    
    # Métodos para la funcionalidad del inventario
    def cargar_productos(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = "SELECT id, codigo, nombre, descripcion, precio, stock FROM productos"
            self.cursor.execute(query)
            
            productos = self.cursor.fetchall()
            for producto in productos:
                self.tree.insert('', 'end', values=producto)
            
            # Actualizar combobox de productos en ventas
            self.producto_combobox['values'] = [f"{p[1]} - {p[2]}" for p in productos]
            
            # Verificar stock bajo
            self.verificar_stock_bajo()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar productos: {err}")
    
    def verificar_stock_bajo(self):
        try:
            query = "SELECT COUNT(*) FROM productos WHERE stock < 5"
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
            
            if count > 0:
                self.alerta_stock.config(text=f"ALERTA: {count} productos con stock bajo")
            else:
                self.alerta_stock.config(text="")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al verificar stock: {err}")
    
    def agregar_producto(self):
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()
        
        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Campos requeridos", "Por favor complete todos los campos obligatorios")
            return
        
        try:
            query = "INSERT INTO productos (codigo, nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s, %s)"
            values = (codigo, nombre, descripcion, float(precio), int(stock))
            self.cursor.execute(query, values)
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al agregar producto: {err}")
    
    def actualizar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para actualizar")
            return
        
        item = self.tree.item(selected[0])
        producto_id = item['values'][0]
        
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()
        
        try:
            query = """UPDATE productos SET 
                      codigo = %s, nombre = %s, descripcion = %s, 
                      precio = %s, stock = %s 
                      WHERE id = %s"""
            values = (codigo, nombre, descripcion, float(precio), int(stock), producto_id)
            self.cursor.execute(query, values)
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.cargar_productos()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar producto: {err}")
    
    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para eliminar")
            return
        
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            return
        
        item = self.tree.item(selected[0])
        producto_id = item['values'][0]
        
        try:
            query = "DELETE FROM productos WHERE id = %s"
            self.cursor.execute(query, (producto_id,))
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar producto: {err}")
    
    def seleccionar_producto(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        self.codigo_entry.delete(0, 'end')
        self.codigo_entry.insert(0, values[1])
        
        self.nombre_entry.delete(0, 'end')
        self.nombre_entry.insert(0, values[2])
        
        self.descripcion_entry.delete(0, 'end')
        self.descripcion_entry.insert(0, values[3])
        
        self.precio_entry.delete(0, 'end')
        self.precio_entry.insert(0, values[4])
        
        self.stock_entry.delete(0, 'end')
        self.stock_entry.insert(0, values[5])
    
    def limpiar_formulario(self):
        self.codigo_entry.delete(0, 'end')
        self.nombre_entry.delete(0, 'end')
        self.descripcion_entry.delete(0, 'end')
        self.precio_entry.delete(0, 'end')
        self.stock_entry.delete(0, 'end')
        self.tree.selection_remove(self.tree.selection())
    
    # Métodos para la funcionalidad de ventas
    def cargar_ventas(self):
        try:
            self.tree_ventas.delete(*self.tree_ventas.get_children())
            query = "SELECT id, fecha, cliente, total FROM ventas ORDER BY fecha DESC LIMIT 50"
            self.cursor.execute(query)
            
            ventas = self.cursor.fetchall()
            for venta in ventas:
                self.tree_ventas.insert('', 'end', values=venta)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar ventas: {err}")
    
    def actualizar_precio_producto(self, event):
        selected = self.producto_combobox.get()
        if not selected:
            return
        
        codigo = selected.split(' - ')[0]
        
        try:
            query = "SELECT precio FROM productos WHERE codigo = %s"
            self.cursor.execute(query, (codigo,))
            precio = self.cursor.fetchone()[0]
            
            self.precio_venta_entry.config(state='normal')
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.insert(0, f"{precio:.2f}")
            self.precio_venta_entry.config(state='readonly')
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener precio: {err}")
    
    def agregar_producto_venta(self):
        producto = self.producto_combobox.get()
        cantidad = self.cantidad_spinbox.get()
        
        if not producto or not cantidad:
            messagebox.showwarning("Datos requeridos", "Seleccione un producto y cantidad")
            return
        
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Cantidad inválida", "Ingrese una cantidad válida mayor a cero")
            return
        
        precio_texto = self.precio_venta_entry.get()
        try:
            precio = float(precio_texto)
        except ValueError:
            messagebox.showwarning("Precio inválido", "El precio del producto no es válido")
            return
        
        subtotal = precio * cantidad
        
        # Verificar stock disponible
        codigo = producto.split(' - ')[0]
        query = "SELECT stock FROM productos WHERE codigo = %s"
        self.cursor.execute(query, (codigo,))
        stock = self.cursor.fetchone()[0]
        
        if cantidad > stock:
            messagebox.showwarning("Stock insuficiente", f"No hay suficiente stock. Disponible: {stock}")
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
    
    def actualizar_total_venta(self):
        total = 0.0
        for item in self.tree_detalle.get_children():
            valores = self.tree_detalle.item(item)['values']
            subtotal = float(valores[3])
            total += subtotal
        
        self.total_venta.config(text=f"${total:.2f}")
    
    def finalizar_venta(self):
        cliente = self.cliente_entry.get()
        items = self.tree_detalle.get_children()
        
        if not items:
            messagebox.showwarning("Venta vacía", "No hay productos en la venta")
            return
        
        if not cliente:
            cliente = "Consumidor Final"
        
        try:
            # Registrar la venta
            total = sum(float(self.tree_detalle.item(item)['values'][3]) for item in items)
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            query = "INSERT INTO ventas (fecha, cliente, total) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (fecha, cliente, total))
            venta_id = self.cursor.lastrowid
            
            # Registrar detalles de venta y actualizar stock
            for item in items:
                valores = self.tree_detalle.item(item)['values']
                producto = valores[0]
                codigo = producto.split(' - ')[0]
                cantidad = int(valores[2])
                precio = float(valores[1])
                
                # Registrar detalle
                query = "INSERT INTO detalle_ventas (venta_id, producto_codigo, cantidad, precio) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query, (venta_id, codigo, cantidad, precio))
                
                # Actualizar stock
                query = "UPDATE productos SET stock = stock - %s WHERE codigo = %s"
                self.cursor.execute(query, (cantidad, codigo))
            
            self.conn.commit()
            
            messagebox.showinfo("Éxito", f"Venta registrada correctamente. Total: ${total:.2f}")
            
            # Limpiar formulario
            self.cliente_entry.delete(0, 'end')
            self.tree_detalle.delete(*self.tree_detalle.get_children())
            self.total_venta.config(text="$0.00")
            
            # Actualizar listas
            self.cargar_productos()
            self.cargar_ventas()
            self.actualizar_dashboard()
        except mysql.connector.Error as err:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error al registrar venta: {err}")
    
    def seleccionar_venta(self, event):
        selected = self.tree_ventas.selection()
        if not selected:
            return
        
        item = self.tree_ventas.item(selected[0])
        venta_id = item['values'][0]
        
        try:
            # Obtener detalles de la venta
            query = """SELECT p.nombre, dv.cantidad, dv.precio, (dv.cantidad * dv.precio) as subtotal
                      FROM detalle_ventas dv
                      JOIN productos p ON dv.producto_codigo = p.codigo
                      WHERE dv.venta_id = %s"""
            self.cursor.execute(query, (venta_id,))
            detalles = self.cursor.fetchall()
            
            # Mostrar en una nueva ventana
            ventana_detalle = tk.Toplevel(self.root)
            ventana_detalle.title(f"Detalle de Venta #{venta_id}")
            
            frame = ttk.Frame(ventana_detalle, padding=10)
            frame.pack(fill='both', expand=True)
            
            tree = ttk.Treeview(frame, columns=("producto", "cantidad", "precio", "subtotal"), show='headings')
            
            tree.heading("producto", text="Producto")
            tree.heading("cantidad", text="Cantidad")
            tree.heading("precio", text="Precio Unitario")
            tree.heading("subtotal", text="Subtotal")
            
            for col in ("producto", "cantidad", "precio", "subtotal"):
                tree.column(col, width=120)
            
            for detalle in detalles:
                tree.insert('', 'end', values=detalle)
            
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Total
            total = sum(d[3] for d in detalles)
            ttk.Label(ventana_detalle, text=f"Total: ${total:.2f}", font=('Arial', 12, 'bold')).pack(pady=10)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener detalle: {err}")
    
    # Métodos para reportes y dashboard
    def actualizar_dashboard(self):
        try:
            # Ventas de hoy
            query = "SELECT SUM(total) FROM ventas WHERE DATE(fecha) = CURDATE()"
            self.cursor.execute(query)
            ventas_hoy = self.cursor.fetchone()[0] or 0
            self.ventas_hoy.config(text=f"${ventas_hoy:.2f}")
            
            # Ventas del mes
            query = "SELECT SUM(total) FROM ventas WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE())"
            self.cursor.execute(query)
            ventas_mes = self.cursor.fetchone()[0] or 0
            self.ventas_mes.config(text=f"${ventas_mes:.2f}")
            
            # Productos bajo stock
            query = "SELECT COUNT(*) FROM productos WHERE stock < 5"
            self.cursor.execute(query)
            bajo_stock = self.cursor.fetchone()[0]
            self.productos_bajo_stock.config(text=str(bajo_stock))
            
            # Productos más vendidos
            query = """SELECT p.nombre, SUM(dv.cantidad) as total_vendido
                      FROM detalle_ventas dv
                      JOIN productos p ON dv.producto_codigo = p.codigo
                      GROUP BY p.nombre
                      ORDER BY total_vendido DESC
                      LIMIT 3"""
            self.cursor.execute(query)
            populares = self.cursor.fetchall()
            
            if populares:
                texto = ", ".join([f"{p[0]} ({p[1]})" for p in populares])
                self.productos_populares.config(text=texto)
            else:
                self.productos_populares.config(text="Ninguno")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar dashboard: {err}")
    
    def generar_reporte(self):
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
            # Reporte de ventas por periodo
            query = """SELECT v.fecha, v.cliente, v.total, 
                      GROUP_CONCAT(p.nombre SEPARATOR ', ') as productos
                      FROM ventas v
                      JOIN detalle_ventas dv ON v.id = dv.venta_id
                      JOIN productos p ON dv.producto_codigo = p.codigo
                      WHERE DATE(v.fecha) BETWEEN %s AND %s
                      GROUP BY v.id
                      ORDER BY v.fecha"""
            self.cursor.execute(query, (fecha_inicio, fecha_fin))
            ventas = self.cursor.fetchall()
            
            # Reporte de productos vendidos
            query = """SELECT p.nombre, SUM(dv.cantidad) as cantidad, 
                      SUM(dv.cantidad * dv.precio) as total
                      FROM detalle_ventas dv
                      JOIN productos p ON dv.producto_codigo = p.codigo
                      JOIN ventas v ON dv.venta_id = v.id
                      WHERE DATE(v.fecha) BETWEEN %s AND %s
                      GROUP BY p.nombre
                      ORDER BY total DESC"""
            self.cursor.execute(query, (fecha_inicio, fecha_fin))
            productos = self.cursor.fetchall()
            
            # Mostrar reporte
            self.texto_reporte.delete(1.0, 'end')
            
            self.texto_reporte.insert('end', f"REPORTE DE VENTAS\nDel {fecha_inicio} al {fecha_fin}\n\n")
            self.texto_reporte.insert('end', "="*50 + "\n")
            self.texto_reporte.insert('end', "VENTAS POR PERIODO:\n\n")
            
            total_periodo = 0.0
            for venta in ventas:
                self.texto_reporte.insert('end', f"Fecha: {venta[0]}\n")
                self.texto_reporte.insert('end', f"Cliente: {venta[1]}\n")
                self.texto_reporte.insert('end', f"Productos: {venta[3]}\n")
                self.texto_reporte.insert('end', f"Total: ${venta[2]:.2f}\n")
                self.texto_reporte.insert('end', "-"*50 + "\n")
                total_periodo += venta[2]
            
            self.texto_reporte.insert('end', f"\nTOTAL DEL PERIODO: ${total_periodo:.2f}\n\n")
            self.texto_reporte.insert('end', "="*50 + "\n")
            self.texto_reporte.insert('end', "PRODUCTOS MÁS VENDIDOS:\n\n")
            
            for producto in productos:
                self.texto_reporte.insert('end', f"Producto: {producto[0]}\n")
                self.texto_reporte.insert('end', f"Cantidad: {producto[1]}\n")
                self.texto_reporte.insert('end', f"Total: ${producto[2]:.2f}\n")
                self.texto_reporte.insert('end', "-"*50 + "\n")
            
            self.texto_reporte.insert('end', "\nFIN DEL REPORTE")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al generar reporte: {err}")
    
    # Métodos para configuración
    def guardar_configuracion(self):
        # En una implementación real, esto guardaría en la base de datos
        messagebox.showinfo("Configuración", "Configuración guardada (simulado)")
    
    def crear_respaldo(self):
        # En una implementación real, esto generaría un backup de la base de datos
        messagebox.showinfo("Respaldo", "Respaldo creado exitosamente (simulado)")
    
    def restaurar_respaldo(self):
        # En una implementación real, esto restauraría la base de datos desde un backup
        messagebox.showinfo("Restauración", "Datos restaurados exitosamente (simulado)")
    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGestionEmpresas(root)
    root.mainloop()