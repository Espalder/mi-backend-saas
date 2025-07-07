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
            ("🧹 Limpiar", self.limpiar_formulario, c['ok_fg'])
        ]
        for texto, comando, color in botones:
            btn = tk.Button(frame_botones, text=texto, command=comando,
                           font=('Segoe UI', 10, 'bold'), bg=color, fg=c['button_fg'],
                           relief='flat', bd=0, padx=20, pady=8)
            btn.pack(side='left', padx=5)
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=color))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=color))
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