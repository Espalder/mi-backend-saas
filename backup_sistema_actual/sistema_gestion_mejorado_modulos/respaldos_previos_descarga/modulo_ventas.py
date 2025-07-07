import tkinter as tk
from tkinter import ttk, messagebox
from estilos import configurar_estilos, get_colores_tema

class VentasUI:
    def __init__(self, parent, conn, cursor, rol, tema='claro'):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.rol = rol
        self.tema = tema
        self.colores = get_colores_tema(self.tema)
        self.crear_interfaz()
        self.cargar_ventas()
        self.refrescar_automatico()

    def crear_interfaz(self):
        configurar_estilos(self.tema)
        c = self.colores
        main_frame = tk.Frame(self.parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        frame_venta = tk.LabelFrame(main_frame, text="🛒 Nueva Venta", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_venta.pack(fill='x', padx=10, pady=10)
        frame_campos_venta = tk.Frame(frame_venta, bg=c['frame_bg'])
        frame_campos_venta.pack(fill='x', padx=20, pady=20)
        tk.Label(frame_campos_venta, text="👤 Cliente:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        self.cliente_entry = tk.Entry(frame_campos_venta, font=('Segoe UI', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.cliente_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        tk.Label(frame_campos_venta, text="📦 Producto:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=1, column=0, sticky='e', padx=(0, 10), pady=5)
        self.producto_combobox = ttk.Combobox(frame_campos_venta, state="readonly", font=('Segoe UI', 10))
        self.producto_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.producto_combobox.bind('<<ComboboxSelected>>', self.actualizar_precio_producto)
        tk.Label(frame_campos_venta, text="💰 Precio:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=1, column=2, sticky='e', padx=(20, 10), pady=5)
        self.precio_venta_entry = tk.Entry(frame_campos_venta, state='readonly', font=('Segoe UI', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.precio_venta_entry.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(frame_campos_venta, text="🔢 Cantidad:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=1, column=4, sticky='e', padx=(20, 10), pady=5)
        self.cantidad_spinbox = ttk.Spinbox(frame_campos_venta, from_=1, to=100, font=('Segoe UI', 10))
        self.cantidad_spinbox.grid(row=1, column=5, padx=5, pady=5)
        frame_campos_venta.columnconfigure(1, weight=1)
        btn_agregar = tk.Button(frame_campos_venta, text="➕ Agregar Producto", command=self.agregar_producto_venta, font=('Segoe UI', 10, 'bold'), bg=c['button_bg'], fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
        btn_agregar.grid(row=2, column=0, columnspan=6, pady=15)
        frame_detalle = tk.LabelFrame(main_frame, text="📋 Detalle de Venta", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_detalle.pack(fill='both', expand=True, padx=10, pady=10)
        frame_tabla_detalle = tk.Frame(frame_detalle, bg=c['frame_bg'])
        frame_tabla_detalle.pack(fill='both', expand=True, padx=10, pady=10)
        columns = ("producto", "precio", "cantidad", "subtotal")
        self.tree_detalle = ttk.Treeview(frame_tabla_detalle, columns=columns, show='headings', height=8)
        headers = {"producto": ("Producto", 300), "precio": ("Precio Unitario", 150), "cantidad": ("Cantidad", 100), "subtotal": ("Subtotal", 150)}
        for col, (header, width) in headers.items():
            self.tree_detalle.heading(col, text=header)
            self.tree_detalle.column(col, width=width, anchor='center')
        scrollbar_detalle = ttk.Scrollbar(frame_tabla_detalle, orient="vertical", command=self.tree_detalle.yview)
        self.tree_detalle.configure(yscrollcommand=scrollbar_detalle.set)
        self.tree_detalle.pack(side='left', fill='both', expand=True)
        scrollbar_detalle.pack(side='right', fill='y')
        btn_eliminar_producto = tk.Button(frame_tabla_detalle, text="❌ Eliminar Producto", command=self.eliminar_producto_venta, font=('Segoe UI', 9, 'bold'), bg=c['error_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=10, pady=5)
        btn_eliminar_producto.pack(side='bottom', pady=5)
        self.tree_detalle.bind('<Double-1>', self.eliminar_producto_venta_doble_clic)
        frame_total = tk.Frame(main_frame, bg=c['bg'])
        frame_total.pack(fill='x', padx=10, pady=10)
        tk.Label(frame_total, text="💵 Total:", font=('Segoe UI', 14, 'bold'), bg=c['bg'], fg=c['fg']).pack(side='left')
        self.total_venta = tk.Label(frame_total, text="S/0.00", font=('Segoe UI', 16, 'bold'), bg=c['bg'], fg=c['ok_fg'])
        self.total_venta.pack(side='left', padx=10)
        btn_limpiar_venta = tk.Button(frame_total, text="🗑️ Limpiar Venta", command=self.limpiar_venta_actual, font=('Segoe UI', 10, 'bold'), bg=c['error_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=15, pady=8)
        btn_limpiar_venta.pack(side='right', padx=5)
        btn_finalizar = tk.Button(frame_total, text="✅ Finalizar Venta", command=self.finalizar_venta, font=('Segoe UI', 12, 'bold'), bg=c['ok_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=30, pady=10)
        btn_finalizar.pack(side='right', padx=5)
        frame_lista_ventas = tk.LabelFrame(main_frame, text="📊 Ventas Recientes", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_lista_ventas.pack(fill='both', expand=True, padx=10, pady=10)
        frame_tabla_ventas = tk.Frame(frame_lista_ventas, bg=c['frame_bg'])
        frame_tabla_ventas.pack(fill='both', expand=True, padx=10, pady=10)
        columns = ("id", "fecha", "cliente", "total")
        self.tree_ventas = ttk.Treeview(frame_tabla_ventas, columns=columns, show='headings', height=8)
        headers = {"id": ("ID", 50), "fecha": ("Fecha", 150), "cliente": ("Cliente", 200), "total": ("Total", 100)}
        for col, (header, width) in headers.items():
            self.tree_ventas.heading(col, text=header)
            self.tree_ventas.column(col, width=width, anchor='center')
        scrollbar_ventas = ttk.Scrollbar(frame_tabla_ventas, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar_ventas.set)
        self.tree_ventas.pack(side='left', fill='both', expand=True)
        scrollbar_ventas.pack(side='right', fill='y')
        self.tree_ventas.bind('<<TreeviewSelect>>', self.seleccionar_venta)
        self.cargar_productos_ventas()
        # Mostrar el precio si ya hay un producto seleccionado al cargar
        if self.producto_combobox.get():
            self.actualizar_precio_producto()
        # Habilitar ordenamiento por columnas en ventas recientes
        for col in ("id", "fecha", "cliente", "total"):
            self.tree_ventas.heading(col, text=headers[col][0], command=lambda c=col: self.ordenar_ventas_por_columna(c))

    def cargar_ventas(self):
        try:
            self.tree_ventas.delete(*self.tree_ventas.get_children())
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query = "SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total FROM ventas v LEFT JOIN clientes c ON v.cliente_id = c.id WHERE v.estado = 'completada' ORDER BY v.id ASC LIMIT 50"
                self.cursor.execute(query)
            else:
                query = "SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total FROM ventas v LEFT JOIN clientes c ON v.cliente_id = c.id WHERE v.estado = 'completada' ORDER BY v.id ASC LIMIT 50"
                self.cursor.execute(query)
            ventas = self.cursor.fetchall()
            for venta in ventas:
                fecha_formateada = venta[1][:16] if isinstance(venta[1], str) else str(venta[1])
                total_float = float(venta[3])
                self.tree_ventas.insert('', 'end', values=(venta[0], fecha_formateada, venta[2], f"S/{total_float:.2f}"))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas: {e}")

    def actualizar_precio_producto(self, event=None):
        selected = self.producto_combobox.get()
        if not selected:
            self.precio_venta_entry.config(state='normal')
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.config(state='readonly')
            self.precio_venta_entry.configure(fg=self.colores['entry_fg'])
            return
        try:
            codigo = selected.split(' - ')[0]
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
                self.precio_venta_entry.configure(fg=self.colores['entry_fg'])
                if stock < 5:
                    messagebox.showwarning("Stock bajo", f"Stock disponible: {stock} unidades")
            else:
                self.precio_venta_entry.config(state='normal')
                self.precio_venta_entry.delete(0, 'end')
                self.precio_venta_entry.config(state='readonly')
                self.precio_venta_entry.configure(fg=self.colores['entry_fg'])
                messagebox.showerror("Error", "Producto no encontrado")
        except Exception as e:
            self.precio_venta_entry.config(state='normal')
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.config(state='readonly')
            self.precio_venta_entry.configure(fg=self.colores['entry_fg'])
            messagebox.showerror("Error", f"Error al obtener precio: {e}")

    def agregar_producto_venta(self):
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
                messagebox.showwarning("Stock insuficiente", f"No hay suficiente stock de '{nombre_producto}'.\nDisponible: {stock} unidades")
                return
            for item in self.tree_detalle.get_children():
                valores = self.tree_detalle.item(item)['values']
                if valores[0] == producto:
                    messagebox.showwarning("Producto duplicado", f"El producto '{nombre_producto}' ya está en la venta")
                    return
            self.tree_detalle.insert('', 'end', values=(producto, f"{precio:.2f}", cantidad, f"{subtotal:.2f}"))
            self.actualizar_total_venta()
            self.producto_combobox.set('')
            self.precio_venta_entry.config(state='normal')
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.config(state='readonly')
            self.cantidad_spinbox.delete(0, 'end')
            self.cantidad_spinbox.insert(0, '1')
            messagebox.showinfo("Producto agregado", f"'{nombre_producto}' agregado a la venta")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def eliminar_producto_venta(self):
        selected = self.tree_detalle.selection()
        if not selected:
            return
        item = self.tree_detalle.item(selected[0])
        producto = item['values'][0]
        if not messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el producto '{producto}' de la venta?"):
            return
        try:
            self.tree_detalle.delete(selected[0])
            self.actualizar_total_venta()
            messagebox.showinfo("Éxito", f"Producto '{producto}' eliminado de la venta")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")

    def eliminar_producto_venta_doble_clic(self, event):
        self.eliminar_producto_venta()

    def limpiar_venta_actual(self):
        items = self.tree_detalle.get_children()
        if not items:
            messagebox.showinfo("Venta vacía", "La venta ya está vacía")
            return
        if not messagebox.askyesno("Confirmar limpieza", f"¿Está seguro de limpiar la venta actual?\n\nSe eliminarán {len(items)} producto(s)"):
            return
        try:
            self.tree_detalle.delete(*self.tree_detalle.get_children())
            self.cliente_entry.delete(0, 'end')
            self.producto_combobox.set('')
            self.precio_venta_entry.config(state='normal')
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.config(state='readonly')
            self.cantidad_spinbox.delete(0, 'end')
            self.cantidad_spinbox.insert(0, '1')
            self.total_venta.config(text="S/0.00")
            self.cargar_ventas()
            messagebox.showinfo("Éxito", "Venta limpiada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar venta: {e}")

    def finalizar_venta(self):
        cliente = self.cliente_entry.get().strip()
        items = self.tree_detalle.get_children()
        if not items:
            messagebox.showwarning("Venta vacía", "No hay productos en la venta")
            return
        if not cliente:
            cliente = "Consumidor Final"
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
        if not messagebox.askyesno("Confirmar venta", f"¿Desea finalizar la venta?\n\nCliente: {cliente}\nTotal: S/{total:.2f}"):
            return
        try:
            if self.conn.in_transaction:
                self.conn.rollback()
            self.conn.start_transaction()
            cliente_id = None
            if cliente and cliente != "Consumidor Final":
                query_cliente = "SELECT id FROM clientes WHERE nombre = %s"
                self.cursor.execute(query_cliente, (cliente,))
                resultado_cliente = self.cursor.fetchone()
                if resultado_cliente:
                    cliente_id = resultado_cliente[0]
                else:
                    query_crear_cliente = "INSERT INTO clientes (nombre) VALUES (%s)"
                    self.cursor.execute(query_crear_cliente, (cliente,))
                    cliente_id = self.cursor.lastrowid
            usuario_id = 1
            from datetime import datetime
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO ventas (fecha, cliente_id, usuario_id, subtotal, descuento, total, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (fecha, cliente_id, usuario_id, total, 0, total, 'completada'))
            venta_id = self.cursor.lastrowid
            for item in items:
                valores = self.tree_detalle.item(item)['values']
                if len(valores) >= 4:
                    producto = valores[0]
                    codigo = producto.split(' - ')[0]
                    cantidad = int(valores[2])
                    precio = float(valores[1])
                    subtotal = float(valores[3])
                    query_producto = "SELECT id FROM productos WHERE codigo = %s"
                    self.cursor.execute(query_producto, (codigo,))
                    producto_id = self.cursor.fetchone()[0]
                    query_stock = "SELECT stock FROM productos WHERE id = %s"
                    self.cursor.execute(query_stock, (producto_id,))
                    stock_actual = self.cursor.fetchone()[0]
                    if cantidad > stock_actual:
                        self.conn.rollback()
                        messagebox.showerror("Error", f"Stock insuficiente para el producto {codigo}")
                        return
                    query = "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"
                    self.cursor.execute(query, (venta_id, producto_id, cantidad, precio, subtotal))
                    query = "UPDATE productos SET stock = stock - %s WHERE id = %s"
                    self.cursor.execute(query, (cantidad, producto_id))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Venta registrada correctamente.\n\nID de Venta: {venta_id}\nCliente: {cliente}\nTotal: S/{total:.2f}")
            self.cliente_entry.delete(0, 'end')
            self.tree_detalle.delete(*self.tree_detalle.get_children())
            self.total_venta.config(text="S/0.00")
            self.cargar_ventas()
        except Exception as e:
            try:
                if self.conn.in_transaction:
                    self.conn.rollback()
            except:
                pass
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def actualizar_total_venta(self):
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
            self.total_venta.config(text=f"S/{total:.2f}")
        except Exception as e:
            self.total_venta.config(text="S/0.00")

    def seleccionar_venta(self, event=None):
        selected = self.tree_ventas.selection()
        if not selected:
            return
        item = self.tree_ventas.item(selected[0])
        venta_id = item['values'][0]
        try:
            query = """SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
                      FROM detalle_ventas dv
                      JOIN productos p ON dv.producto_id = p.id
                      WHERE dv.venta_id = %s"""
            self.cursor.execute(query, (venta_id,))
            detalles = self.cursor.fetchall()
            texto = f"Detalle de Venta #{venta_id}\n\n"
            total = 0.0
            for detalle in detalles:
                texto += f"Producto: {detalle[0]}\nCantidad: {detalle[1]}\nPrecio: S/{detalle[2]:.2f}\nSubtotal: S/{detalle[3]:.2f}\n---\n"
                total += float(detalle[3])
            texto += f"\nTotal: S/{total:.2f}"
            messagebox.showinfo(f"Detalle de Venta #{venta_id}", texto)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener detalle: {e}")

    def cargar_productos_ventas(self):
        try:
            self.producto_combobox['values'] = []
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query = "SELECT codigo, nombre FROM productos WHERE activo = 1 AND stock > 0"
                self.cursor.execute(query)
            else:
                query = "SELECT codigo, nombre FROM productos WHERE activo = 1 AND stock > 0"
                self.cursor.execute(query)
            productos = self.cursor.fetchall()
            self.productos_venta = {f"{codigo} - {nombre}": codigo for codigo, nombre in productos}
            self.producto_combobox['values'] = list(self.productos_venta.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")

    def ordenar_ventas_por_columna(self, columna):
        try:
            items = [(self.tree_ventas.set(item, columna), item) for item in self.tree_ventas.get_children('')]
            if columna == 'id':
                items.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0)
            elif columna == 'total':
                items.sort(key=lambda x: float(x[0].replace('S/', '').replace(',', '').strip()) if x[0] else 0)
            else:
                items.sort(key=lambda x: x[0].lower())
            for index, (val, item) in enumerate(items):
                self.tree_ventas.move(item, '', index)
        except Exception as e:
            print(f"Error al ordenar ventas por columna {columna}: {e}")

    def refrescar_automatico(self):
        pass  # Deshabilitado, solo actualización manual

    def sincronizar_todo(self):
        # Llama al método del módulo de inventario si existe
        try:
            inv = self.parent.winfo_toplevel().master.tabs.get('inventario')
            if inv and hasattr(inv, 'sincronizar_todo'):
                inv.sincronizar_todo()
            else:
                messagebox.showwarning("Sincronización", "La sincronización completa solo está disponible desde el módulo de Inventario.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo sincronizar: {e}")

    def descargar_productos(self):
        # Llama al método del módulo de inventario si existe
        try:
            inv = self.parent.winfo_toplevel().master.tabs.get('inventario')
            if inv and hasattr(inv, 'descargar_productos'):
                inv.descargar_productos()
            else:
                messagebox.showwarning("Descarga", "La descarga de productos solo está disponible desde el módulo de Inventario.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar: {e}")

    # ... Métodos para seleccionar venta, etc ... 