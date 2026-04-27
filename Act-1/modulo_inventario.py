import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from estilos import configurar_estilos, get_colores_tema
import json, os

class InventarioUI:
    def __init__(self, parent, conn, cursor, rol, tema='claro'):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.rol = rol
        self.tema = tema
        self.colores = get_colores_tema(self.tema)
        self.producto_seleccionado_id = None
        self.entries_inventario = {}
        self.alerta_stock_minimo = 5
        self.crear_interfaz()
        self.cargar_productos()
        self.cargar_categorias()
        self.refrescar_automatico()

    def crear_interfaz(self):
        configurar_estilos(self.tema)
        c = self.colores
        main_frame = tk.Frame(self.parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        canvas = tk.Canvas(main_frame, bg=c['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=c['bg'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        frame_form = tk.LabelFrame(scrollable_frame, text="➕ Gestión de Productos", 
                                 font=('Segoe UI', 12, 'bold'), fg=c['fg'],
                                 bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_form.pack(fill='x', padx=10, pady=10)
        frame_campos = tk.Frame(frame_form, bg=c['frame_bg'])
        frame_campos.pack(fill='x', padx=20, pady=20)
        labels = ["Código:", "Nombre:", "Descripción:", "Precio:", "Stock:"]
        for i, label in enumerate(labels):
            lbl = tk.Label(frame_campos, text=label, font=('Segoe UI', 10, 'bold'), 
                          bg=c['frame_bg'], fg=c['fg'])
            lbl.grid(row=i, column=0, sticky='e', padx=(0, 10), pady=5)
            if label == "Descripción:":
                entry = tk.Text(frame_campos, height=3, width=40, font=('Segoe UI', 10),
                               bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
            else:
                entry = tk.Entry(frame_campos, font=('Segoe UI', 10), 
                               bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=5)
            self.entries_inventario[label] = entry
        frame_campos.columnconfigure(1, weight=1)
        frame_botones = tk.Frame(frame_form, bg=c['frame_bg'])
        frame_botones.pack(fill='x', padx=20, pady=10)
        botones = [
            ("➕ Agregar", self.agregar_producto, c['button_bg']),
            ("✏️ Actualizar", self.actualizar_producto, c['accent']),
            ("🗑️ Eliminar", self.eliminar_producto, c['error_fg']),
            ("🧹 Limpiar", self.limpiar_formulario, c['ok_fg']),
            ("📤 Exportar", self.exportar_inventario, '#9C27B0')
        ]
        for texto, comando, color in botones:
            btn = tk.Button(frame_botones, text=texto, command=comando,
                           font=('Segoe UI', 10, 'bold'), bg=color, fg=c['button_fg'],
                           relief='flat', bd=0, padx=20, pady=8)
            btn.pack(side='left', padx=5)
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=color))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=color))
        # Frame de búsqueda avanzada
        frame_busqueda = tk.LabelFrame(scrollable_frame, text="🔍 Búsqueda Avanzada", 
                                     font=('Segoe UI', 12, 'bold'), fg=c['fg'],
                                     bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_busqueda.pack(fill='x', padx=10, pady=10)
        
        busqueda_frame = tk.Frame(frame_busqueda, bg=c['frame_bg'])
        busqueda_frame.pack(fill='x', padx=20, pady=15)
        
        # Campo de búsqueda
        tk.Label(busqueda_frame, text="🔍 Buscar:", font=('Segoe UI', 10, 'bold'), 
                bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        
        self.busqueda_entry = tk.Entry(busqueda_frame, font=('Segoe UI', 10), 
                                     bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.busqueda_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.busqueda_entry.bind('<KeyRelease>', self.buscar_productos)
        
        # Filtros
        tk.Label(busqueda_frame, text="📂 Categoría:", font=('Segoe UI', 10, 'bold'), 
                bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=2, sticky='e', padx=(20, 10), pady=5)
        
        self.filtro_categoria = ttk.Combobox(busqueda_frame, state="readonly", font=('Segoe UI', 10))
        self.filtro_categoria.grid(row=0, column=3, padx=5, pady=5)
        self.filtro_categoria.bind('<<ComboboxSelected>>', self.aplicar_filtros)
        
        # Filtro de stock
        tk.Label(busqueda_frame, text="📊 Stock:", font=('Segoe UI', 10, 'bold'), 
                bg=c['frame_bg'], fg=c['fg']).grid(row=1, column=0, sticky='e', padx=(0, 10), pady=5)
        
        self.filtro_stock = ttk.Combobox(busqueda_frame, state="readonly", font=('Segoe UI', 10),
                                       values=["Todos", "Stock Bajo", "Sin Stock", "Stock Normal"])
        self.filtro_stock.grid(row=1, column=1, padx=5, pady=5)
        self.filtro_stock.set("Todos")
        self.filtro_stock.bind('<<ComboboxSelected>>', self.aplicar_filtros)
        
        # Botones de búsqueda
        btn_buscar = tk.Button(busqueda_frame, text="🔍 Buscar", command=self.buscar_productos,
                              font=('Segoe UI', 10, 'bold'), bg=c['accent'], fg='white',
                              relief='flat', bd=0, padx=15, pady=5)
        btn_buscar.grid(row=1, column=2, padx=10, pady=5)
        
        btn_limpiar = tk.Button(busqueda_frame, text="🧹 Limpiar", command=self.limpiar_busqueda,
                               font=('Segoe UI', 10, 'bold'), bg=c['ok_fg'], fg='white',
                               relief='flat', bd=0, padx=15, pady=5)
        btn_limpiar.grid(row=1, column=3, padx=5, pady=5)
        
        busqueda_frame.columnconfigure(1, weight=1)
        
        frame_lista = tk.LabelFrame(scrollable_frame, text="📋 Lista de Productos", 
                                  font=('Segoe UI', 12, 'bold'), fg=c['fg'],
                                  bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        frame_tabla = tk.Frame(frame_lista, bg=c['frame_bg'])
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        columns = ("id", "codigo", "nombre", "descripcion", "precio_venta", "stock")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=12)
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
        scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tabla.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_tabla.pack(side='right', fill='y')
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)
        for col in columns:
            self.tree.heading(col, text=headers[col][0], command=lambda c=col: self.ordenar_por_columna(c))
        self.alerta_stock = tk.Label(scrollable_frame, text="", 
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=c['bg'], fg=c['error_fg'])
        self.alerta_stock.pack(pady=10)
        try:
            img_deco = Image.open("images/logo_empresa.png").resize((80, 80))
            self.img_deco_inv = ImageTk.PhotoImage(img_deco)
            tk.Label(scrollable_frame, image=self.img_deco_inv, bg=c['bg']).place(x=1100, y=10)
        except Exception:
            tk.Label(scrollable_frame, text="📦", font=('Segoe UI', 40), 
                    bg=c['bg'], fg=c['accent']).place(x=1100, y=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def lighten_color(self, color):
        return color

    def agregar_producto(self):
        codigo = self.entries_inventario["Código:"].get().strip()
        nombre = self.entries_inventario["Nombre:"].get().strip()
        descripcion = self.entries_inventario["Descripción:"].get("1.0", "end-1c").strip()
        precio = self.entries_inventario["Precio:"].get().strip()
        stock = self.entries_inventario["Stock:"].get().strip()
        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Campos requeridos", "Por favor complete todos los campos obligatorios")
            return
        if len(codigo) < 2:
            messagebox.showwarning("Código inválido", "El código debe tener al menos 2 caracteres")
            return
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
            messagebox.showerror("Error de datos", "Precio debe ser un número decimal y stock un número entero")
            return
        try:
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query_check = "SELECT id FROM productos WHERE codigo = ?"
                self.cursor.execute(query_check, (codigo,))
                if self.cursor.fetchone():
                    messagebox.showerror("Error", "Ya existe un producto con ese código")
                    return
                query = "INSERT INTO productos (codigo, nombre, descripcion, precio, stock, activo) VALUES (?, ?, ?, ?, ?, 1)"
                values = (codigo, nombre, descripcion, precio_float, stock_int)
                self.cursor.execute(query, values)
                self.conn.commit()
            else:
                query_check = "SELECT id FROM productos WHERE codigo = %s"
                self.cursor.execute(query_check, (codigo,))
                if self.cursor.fetchone():
                    messagebox.showerror("Error", "Ya existe un producto con ese código")
                    return
                query = "INSERT INTO productos (codigo, nombre, descripcion, precio, stock, activo) VALUES (%s, %s, %s, %s, %s, 1)"
                values = (codigo, nombre, descripcion, precio_float, stock_int)
                self.cursor.execute(query, values)
                self.conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
            self.verificar_stock_bajo()
        except Exception as err:
            messagebox.showerror("Error", f"Error al agregar producto: {err}")

    def actualizar_producto(self):
        if self.producto_seleccionado_id is None:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para actualizar")
                return
            item = self.tree.item(selected[0])
            producto_id = item['values'][0]
        else:
            producto_id = self.producto_seleccionado_id
        codigo = self.entries_inventario["Código:"].get().strip()
        nombre = self.entries_inventario["Nombre:"].get().strip()
        descripcion = self.entries_inventario["Descripción:"].get("1.0", "end-1c").strip()
        precio = self.entries_inventario["Precio:"].get().strip()
        stock = self.entries_inventario["Stock:"].get().strip()
        if not all([codigo, nombre, precio, stock]):
            messagebox.showwarning("Campos requeridos", "Por favor complete todos los campos obligatorios")
            return
        if len(codigo) < 2:
            messagebox.showwarning("Código inválido", "El código debe tener al menos 2 caracteres")
            return
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
            messagebox.showerror("Error de datos", "Precio debe ser un número decimal y stock un número entero")
            return
        try:
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query_check = "SELECT id FROM productos WHERE codigo = ? AND id != ?"
                self.cursor.execute(query_check, (codigo, producto_id))
                if self.cursor.fetchone():
                    messagebox.showerror("Error", "Ya existe otro producto con ese código")
                    return
                query = "UPDATE productos SET codigo=?, nombre=?, descripcion=?, precio=?, stock=? WHERE id=?"
                values = (codigo, nombre, descripcion, precio_float, stock_int, producto_id)
                self.cursor.execute(query, values)
                self.conn.commit()
            else:
                query_check = "SELECT id FROM productos WHERE codigo = %s AND id != %s"
                self.cursor.execute(query_check, (codigo, producto_id))
                if self.cursor.fetchone():
                    messagebox.showerror("Error", "Ya existe otro producto con ese código")
                    return
                query = "UPDATE productos SET codigo=%s, nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id=%s"
                values = (codigo, nombre, descripcion, precio_float, stock_int, producto_id)
                self.cursor.execute(query, values)
                self.conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
            self.verificar_stock_bajo()
            if self.producto_seleccionado_id:
                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == self.producto_seleccionado_id:
                        self.tree.selection_set(item)
                        self.tree.focus(item)
                        break
        except Exception as err:
            messagebox.showerror("Error", f"Error al actualizar producto: {err}")

    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para eliminar")
            return
        item = self.tree.item(selected[0])
        producto_id = item['values'][0]
        producto_nombre = item['values'][2]
        if not messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el producto '{producto_nombre}'?\n\nEsta acción no se puede deshacer."):
            return
        try:
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query = "DELETE FROM productos WHERE id = ?"
                self.cursor.execute(query, (producto_id,))
                self.conn.commit()
            else:
                query = "DELETE FROM productos WHERE id = %s"
                self.cursor.execute(query, (producto_id,))
                self.conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
            self.verificar_stock_bajo()
        except Exception as err:
            messagebox.showerror("Error", f"Error al eliminar producto: {err}")

    def seleccionar_producto(self, event):
        try:
            selected = self.tree.selection()
            if not selected:
                return
            item = self.tree.item(selected[0])
            values = item['values']
            if not values or len(values) < 6:
                print(f"Error: Datos del producto incompletos. Valores: {values}")
                return
            if any(v is None for v in values[:6]):
                print(f"Error: Valores nulos encontrados. Valores: {values}")
                return
            self.producto_seleccionado_id = int(values[0])
            self.limpiar_formulario()
            self.entries_inventario["Código:"].insert(0, str(values[1]))
            self.entries_inventario["Nombre:"].insert(0, str(values[2]))
            self.entries_inventario["Descripción:"].insert("1.0", str(values[3]) if values[3] else "")
            self.entries_inventario["Precio:"].insert(0, str(values[4]))
            self.entries_inventario["Stock:"].insert(0, str(values[5]))
            self.tree.focus(selected[0])
        except Exception as e:
            print(f"Error al seleccionar producto: {e}")
            messagebox.showerror("Error", f"Error al cargar datos del producto: {e}")

    def ordenar_por_columna(self, columna):
        try:
            items = [(self.tree.set(item, columna), item) for item in self.tree.get_children('')]
            if columna in ['id', 'stock']:
                items.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
            elif columna == 'precio_venta':
                items.sort(key=lambda x: float(x[0]) if x[0].replace('.', '').replace(',', '').isdigit() else 0)
            else:
                items.sort(key=lambda x: x[0].lower())
            for index, (val, item) in enumerate(items):
                self.tree.move(item, '', index)
        except Exception as e:
            print(f"Error al ordenar por columna {columna}: {e}")

    def limpiar_formulario(self):
        try:
            for label, entry in self.entries_inventario.items():
                if label == "Descripción:":
                    entry.delete("1.0", "end")
                else:
                    entry.delete(0, 'end')
        except Exception as e:
            print(f"Error al limpiar formulario: {e}")

    def cargar_productos(self):
        try:
            self.tree.delete(*self.tree.get_children())
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query = "SELECT id, codigo, nombre, descripcion, precio, stock FROM productos WHERE activo = 1 ORDER BY id ASC"
                self.cursor.execute(query)
            else:
                query = "SELECT id, codigo, nombre, descripcion, precio, stock FROM productos WHERE activo = 1 ORDER BY id ASC"
                self.cursor.execute(query)
            productos = self.cursor.fetchall()
            for prod in productos:
                self.tree.insert('', 'end', values=prod)
            self.verificar_stock_bajo()
        except Exception as err:
            messagebox.showerror("Error", f"Error al cargar productos: {err}")

    def verificar_stock_bajo(self):
        try:
            alerta_stock_minimo = self.alerta_stock_minimo
            if os.path.exists('configuracion.json'):
                with open('configuracion.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    alerta_stock_minimo = int(config.get('alerta_stock_config', alerta_stock_minimo))
            query = f"SELECT COUNT(*) FROM productos WHERE stock <= {alerta_stock_minimo} AND activo = TRUE"
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
            if count > 0:
                self.alerta_stock.config(text=f"⚠️ ALERTA: {count} productos con stock bajo (≤ {alerta_stock_minimo})")
            else:
                self.alerta_stock.config(text="✅ Stock en niveles normales")
        except Exception as err:
            self.alerta_stock.config(text="❌ Error al verificar stock")

    def refrescar_automatico(self):
        self.parent.after(60000, self.cargar_productos)

    def sincronizar_todo(self):
        if not self.get_online_state():
            messagebox.showwarning("Sin conexión", "No hay conexión online para sincronizar.")
            return
        try:
            import mysql.connector
            conn_mysql = mysql.connector.connect(**self.db_config)
            cursor_mysql = conn_mysql.cursor()
            # Sincronizar productos
            cursor_mysql.execute("SELECT id, codigo, nombre, descripcion, precio, stock, activo, fecha_creacion, sincronizado FROM productos")
            productos = cursor_mysql.fetchall()
            for prod in productos:
                self.cursor.execute("INSERT OR REPLACE INTO productos (id, codigo, nombre, descripcion, precio, stock, activo, fecha_creacion, sincronizado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", prod)
            # Sincronizar clientes
            cursor_mysql.execute("SELECT id, nombre, sincronizado FROM clientes")
            clientes = cursor_mysql.fetchall()
            for cli in clientes:
                self.cursor.execute("INSERT OR REPLACE INTO clientes (id, nombre, sincronizado) VALUES (?, ?, ?)", cli)
            # Sincronizar usuarios
            cursor_mysql.execute("SELECT id, username, password, nombre, rol, activo, sincronizado FROM usuarios")
            usuarios = cursor_mysql.fetchall()
            for usr in usuarios:
                self.cursor.execute("INSERT OR REPLACE INTO usuarios (id, username, password, nombre, rol, activo, sincronizado) VALUES (?, ?, ?, ?, ?, ?, ?)", usr)
            # Sincronizar ventas
            cursor_mysql.execute("SELECT id, fecha, cliente_id, usuario_id, subtotal, descuento, total, estado, sincronizado FROM ventas")
            ventas = cursor_mysql.fetchall()
            for venta in ventas:
                self.cursor.execute("INSERT OR REPLACE INTO ventas (id, fecha, cliente_id, usuario_id, subtotal, descuento, total, estado, sincronizado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", venta)
            # Sincronizar detalle_ventas
            cursor_mysql.execute("SELECT id, venta_id, producto_id, cantidad, precio_unitario, subtotal, sincronizado FROM detalle_ventas")
            detalles = cursor_mysql.fetchall()
            for det in detalles:
                self.cursor.execute("INSERT OR REPLACE INTO detalle_ventas (id, venta_id, producto_id, cantidad, precio_unitario, subtotal, sincronizado) VALUES (?, ?, ?, ?, ?, ?, ?)", det)
            self.conn.commit()
            cursor_mysql.close()
            conn_mysql.close()
            self.cargar_productos()
            # Refrescar ventas si existe el método en el módulo de ventas
            try:
                ventas_mod = self.parent.winfo_toplevel().master.tabs.get('ventas')
                if ventas_mod and hasattr(ventas_mod, 'cargar_ventas'):
                    ventas_mod.cargar_ventas()
            except Exception:
                pass
            messagebox.showinfo("Sincronización exitosa", "¡Base de datos local sincronizada con la nube!")
        except Exception as e:
            messagebox.showerror("Error de sincronización", f"No se pudo sincronizar: {e}")

    def descargar_productos(self):
        if not self.get_online_state():
            messagebox.showwarning("Sin conexión", "No hay conexión online para descargar productos.")
            return
        try:
            import mysql.connector
            conn_mysql = mysql.connector.connect(**self.db_config)
            cursor_mysql = conn_mysql.cursor()
            cursor_mysql.execute("SELECT id, codigo, nombre, descripcion, precio, stock, activo, fecha_creacion, sincronizado FROM productos")
            productos = cursor_mysql.fetchall()
            for prod in productos:
                self.cursor.execute("INSERT OR REPLACE INTO productos (id, codigo, nombre, descripcion, precio, stock, activo, fecha_creacion, sincronizado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", prod)
            self.conn.commit()
            cursor_mysql.close()
            conn_mysql.close()
            self.cargar_productos()
            messagebox.showinfo("Descarga exitosa", "¡Base de productos descargada y actualizada!")
        except Exception as e:
            messagebox.showerror("Error de descarga", f"No se pudo descargar la base de productos: {e}")

    # Llamar verificar_stock_bajo tras agregar, actualizar, eliminar producto y tras guardar configuración

    def buscar_productos(self, event=None):
        """Buscar productos con filtros avanzados"""
        try:
            texto_busqueda = self.busqueda_entry.get().strip()
            categoria = self.filtro_categoria.get()
            filtro_stock = self.filtro_stock.get()

            # Intentar con columnas extendidas; si falla, usar fallback mínimo
            query_base = "SELECT id, codigo, nombre, descripcion, precio, stock, stock_minimo, categoria_id FROM productos WHERE activo = 1"
            params = []

            if texto_busqueda:
                query_base += " AND (codigo LIKE ? OR nombre LIKE ? OR descripcion LIKE ?)"
                texto_like = f"%{texto_busqueda}%"
                params.extend([texto_like, texto_like, texto_like])

            if categoria and categoria != "Todas":
                query_base += " AND categoria_id = ?"
                params.append(categoria.split(' - ')[0] if ' - ' in categoria else categoria)

            if filtro_stock == "Stock Bajo":
                query_base += " AND stock_minimo IS NOT NULL AND stock <= stock_minimo"
            elif filtro_stock == "Sin Stock":
                query_base += " AND stock = 0"
            elif filtro_stock == "Stock Normal":
                query_base += " AND (stock_minimo IS NULL OR stock > stock_minimo)"

            query_base += " ORDER BY nombre"

            try:
                self.cursor.execute(query_base, params)
                productos = self.cursor.fetchall()
                usa_extendido = True
            except Exception:
                # Fallback: columnas básicas (sin stock_minimo ni categoria_id)
                query_fb = "SELECT id, codigo, nombre, descripcion, precio, stock FROM productos WHERE activo = 1"
                params_fb = []
                if texto_busqueda:
                    query_fb += " AND (codigo LIKE ? OR nombre LIKE ? OR descripcion LIKE ?)"
                    texto_like = f"%{texto_busqueda}%"
                    params_fb.extend([texto_like, texto_like, texto_like])
                if filtro_stock == "Sin Stock":
                    query_fb += " AND stock = 0"
                query_fb += " ORDER BY nombre"
                self.cursor.execute(query_fb, params_fb)
                productos = self.cursor.fetchall()
                usa_extendido = False

            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Mostrar resultados
            for producto in productos:
                if usa_extendido:
                    id_prod, codigo, nombre, descripcion, precio, stock, stock_minimo, categoria_id = producto
                    stock_min = stock_minimo if stock_minimo is not None else 0
                    categoria_val = categoria_id if categoria_id is not None else ''
                else:
                    id_prod, codigo, nombre, descripcion, precio, stock = producto
                    stock_min = 0
                    categoria_val = ''

                tags = []
                if stock <= stock_min and stock_min > 0:
                    tags.append("stock_bajo")
                elif stock == 0:
                    tags.append("sin_stock")

                self.tree.insert('', 'end', values=(
                    id_prod, codigo, nombre, descripcion, f"${precio:.2f}",
                    f"{stock} (min: {stock_min})", categoria_val
                ), tags=tags)

            self.tree.tag_configure("stock_bajo", background="#fff3cd", foreground="#856404")
            self.tree.tag_configure("sin_stock", background="#f8d7da", foreground="#721c24")

            total_resultados = len(productos)
            self.alerta_stock.config(text=f"📊 Mostrando {total_resultados} productos")

        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {e}")

    def aplicar_filtros(self, event=None):
        """Aplicar filtros de búsqueda"""
        self.buscar_productos()

    def limpiar_busqueda(self):
        """Limpiar filtros de búsqueda"""
        self.busqueda_entry.delete(0, tk.END)
        self.filtro_categoria.set("")
        self.filtro_stock.set("Todos")
        self.cargar_productos()

    def cargar_categorias(self):
        """Cargar categorías disponibles"""
        try:
            # Intentar cargar desde tabla categorias si existe
            self.cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
            categorias_db = self.cursor.fetchall()
            if categorias_db:
                categorias = ["Todas"] + [f"{cat[0]} - {cat[1]}" for cat in categorias_db]
            else:
                # Si no hay tabla categorias, usar valores por defecto
                categorias = ["Todas", "General", "Electrónicos", "Ropa", "Hogar", "Deportes"]
            self.filtro_categoria['values'] = categorias
            self.filtro_categoria.set("Todas")
        except Exception as e:
            print(f"Error cargando categorías: {e}")
            # Valores por defecto en caso de error
            categorias = ["Todas", "General", "Electrónicos", "Ropa", "Hogar", "Deportes"]
            self.filtro_categoria['values'] = categorias
            self.filtro_categoria.set("Todas")

    def exportar_inventario(self):
        """Exportar inventario a archivo"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if archivo:
                self.cursor.execute("SELECT codigo, nombre, descripcion, precio, stock, stock_minimo, categoria FROM productos WHERE activo = 1")
                productos = self.cursor.fetchall()
                
                if archivo.endswith('.csv'):
                    import csv
                    with open(archivo, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Código', 'Nombre', 'Descripción', 'Precio', 'Stock', 'Stock Mínimo', 'Categoría'])
                        writer.writerows(productos)
                elif archivo.endswith('.json'):
                    import json
                    datos = {
                        'fecha_exportacion': str(datetime.now()),
                        'productos': [
                            {
                                'codigo': p[0], 'nombre': p[1], 'descripcion': p[2],
                                'precio': p[3], 'stock': p[4], 'stock_minimo': p[5], 'categoria': p[6]
                            } for p in productos
                        ]
                    }
                    with open(archivo, 'w', encoding='utf-8') as f:
                        json.dump(datos, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Exportación", f"✅ Inventario exportado a: {archivo}")
                
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al exportar: {e}") 