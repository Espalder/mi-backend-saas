import tkinter as tk
from tkinter import ttk, messagebox
from estilos import configurar_estilos, get_colores_tema
try:
    from graficos_estadisticas import GraficosEstadisticas
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False
    print("Módulo de gráficos no disponible")

try:
    from generador_pdf import GeneradorPDF
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False
    print("Módulo de PDF no disponible")

class ReportesUI:
    def __init__(self, parent, conn, cursor, rol, tema='claro'):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.rol = rol
        self.tema = tema
        self.colores = get_colores_tema(self.tema)
        self.graficos_widget = None
        self.generador_pdf = None
        if PDF_DISPONIBLE:
            self.generador_pdf = GeneradorPDF(conn, cursor)
        self.crear_interfaz()
        self.refrescar_automatico()

    def crear_interfaz(self):
        configurar_estilos(self.tema)
        c = self.colores
        main_frame = tk.Frame(self.parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Crear notebook para organizar en pestañas
        self.notebook_reportes = ttk.Notebook(main_frame)
        self.notebook_reportes.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pestaña 1: Dashboard
        self.tab_dashboard = tk.Frame(self.notebook_reportes, bg=c['bg'])
        self.notebook_reportes.add(self.tab_dashboard, text="📊 Dashboard")
        
        # Pestaña 2: Reportes Detallados
        self.tab_reportes = tk.Frame(self.notebook_reportes, bg=c['bg'])
        self.notebook_reportes.add(self.tab_reportes, text="📋 Reportes")
        
        # Pestaña 3: Gráficos (si está disponible)
        if GRAFICOS_DISPONIBLES:
            self.tab_graficos = tk.Frame(self.notebook_reportes, bg=c['bg'])
            self.notebook_reportes.add(self.tab_graficos, text="📈 Gráficos")
            self.graficos_widget = GraficosEstadisticas(self.tab_graficos, self.conn, self.cursor, self.tema)
        
        # Crear contenido del dashboard
        self.crear_dashboard()
        
        # Crear contenido de reportes
        self.crear_reportes_detallados()

    def crear_dashboard(self):
        """Crear el dashboard con métricas"""
        c = self.colores
        frame_dashboard = tk.LabelFrame(self.tab_dashboard, text="📈 Dashboard", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_dashboard.pack(fill='x', padx=10, pady=10)
        frame_metricas = tk.Frame(frame_dashboard, bg=c['frame_bg'])
        frame_metricas.pack(fill='x', padx=20, pady=20)
        metricas = [
            ("💰 Ventas Hoy:", "ventas_hoy", c['ok_fg']),
            ("📅 Ventas Mes:", "ventas_mes", c['accent']),
            ("⚠️ Bajo Stock:", "productos_bajo_stock", c['error_fg']),
            ("🏆 Más Vendidos:", "productos_populares", c['ok_fg'])
        ]
        self.labels_metricas = {}
        for i, (texto, key, color) in enumerate(metricas):
            frame_metrica = tk.Frame(frame_metricas, bg=c['frame_bg'], relief='solid', bd=1)
            frame_metrica.grid(row=0, column=i, padx=10, pady=10, sticky='ew')
            tk.Label(frame_metrica, text=texto, font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=color).pack(pady=5)
            label_valor = tk.Label(frame_metrica, text="Cargando...", font=('Segoe UI', 14, 'bold'), bg=c['frame_bg'], fg=color)
            label_valor.pack(pady=5)
            self.labels_metricas[key] = label_valor
        for i in range(4):
            frame_metricas.columnconfigure(i, weight=1)
        
        # Actualizar dashboard inicial
        self.actualizar_dashboard()

    def crear_reportes_detallados(self):
        """Crear la sección de reportes detallados"""
        c = self.colores
        frame_filtros = tk.LabelFrame(self.tab_reportes, text="🔍 Filtros", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_filtros.pack(fill='x', padx=10, pady=10)
        frame_campos_filtros = tk.Frame(frame_filtros, bg=c['frame_bg'])
        frame_campos_filtros.pack(fill='x', padx=20, pady=20)
        tk.Label(frame_campos_filtros, text="📅 Fecha Inicio:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        self.fecha_inicio = tk.Entry(frame_campos_filtros, font=('Segoe UI', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.fecha_inicio.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_campos_filtros, text="📅 Fecha Fin:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=2, sticky='e', padx=(20, 10), pady=5)
        self.fecha_fin = tk.Entry(frame_campos_filtros, font=('Segoe UI', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.fecha_fin.grid(row=0, column=3, padx=5, pady=5)
        frame_fechas_rapidas = tk.Frame(frame_campos_filtros, bg=c['frame_bg'])
        frame_fechas_rapidas.grid(row=1, column=0, columnspan=4, pady=10)
        tk.Label(frame_fechas_rapidas, text="📋 Fechas Rápidas:", font=('Segoe UI', 10, 'bold'), bg=c['frame_bg'], fg=c['fg']).pack(side='left', padx=(0, 10))
        botones_fecha = [
            ("Hoy", self.fecha_hoy),
            ("Ayer", self.fecha_ayer),
            ("Esta Semana", self.fecha_esta_semana),
            ("Este Mes", self.fecha_este_mes),
            ("Último Mes", self.fecha_ultimo_mes)
        ]
        for texto, comando in botones_fecha:
            btn = tk.Button(frame_fechas_rapidas, text=texto, command=comando, font=('Segoe UI', 9, 'bold'), bg=c['accent'], fg=c['button_fg'], relief='flat', bd=0, padx=10, pady=5)
            btn.pack(side='left', padx=2)
        btn_reporte = tk.Button(frame_campos_filtros, text="📊 Generar Reporte", command=self.generar_reporte, font=('Segoe UI', 10, 'bold'), bg=c['ok_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
        btn_reporte.grid(row=2, column=0, columnspan=2, pady=15, padx=(0, 5))
        
        # Botones de PDF
        if PDF_DISPONIBLE:
            btn_pdf_ventas = tk.Button(frame_campos_filtros, text="📄 PDF Ventas", command=self.generar_pdf_ventas, font=('Segoe UI', 10, 'bold'), bg=c['accent'], fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
            btn_pdf_ventas.grid(row=2, column=2, pady=15, padx=5)
            
            btn_pdf_inventario = tk.Button(frame_campos_filtros, text="📦 PDF Inventario", command=self.generar_pdf_inventario, font=('Segoe UI', 10, 'bold'), bg=c['error_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
            btn_pdf_inventario.grid(row=2, column=3, pady=15, padx=(5, 0))
        
        frame_campos_filtros.columnconfigure(1, weight=1)
        frame_campos_filtros.columnconfigure(3, weight=1)
        frame_reporte = tk.LabelFrame(self.tab_reportes, text="📋 Reporte", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        frame_texto_reporte = tk.Frame(frame_reporte, bg=c['frame_bg'])
        frame_texto_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        self.texto_reporte = tk.Text(frame_texto_reporte, wrap='word', font=('Consolas', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        scrollbar_reporte = ttk.Scrollbar(frame_texto_reporte, orient="vertical", command=self.texto_reporte.yview)
        self.texto_reporte.configure(yscrollcommand=scrollbar_reporte.set)
        self.texto_reporte.pack(side='left', fill='both', expand=True)
        scrollbar_reporte.pack(side='right', fill='y')

    def fecha_hoy(self):
        from datetime import datetime
        fecha = datetime.now().strftime("%Y-%m-%d")
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, fecha)
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fecha)

    def fecha_ayer(self):
        from datetime import datetime, timedelta
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, fecha)
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fecha)

    def fecha_esta_semana(self):
        from datetime import datetime, timedelta
        hoy = datetime.now()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        self.fecha_inicio.delete(0, 'end')
        self.fecha_inicio.insert(0, inicio_semana.strftime("%Y-%m-%d"))
        self.fecha_fin.delete(0, 'end')
        self.fecha_fin.insert(0, fin_semana.strftime("%Y-%m-%d"))

    def fecha_este_mes(self):
        from datetime import datetime, timedelta
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
        from datetime import datetime, timedelta
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

    def generar_reporte(self):
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Fechas requeridas", "Ingrese ambas fechas para generar el reporte")
            return
        try:
            from datetime import datetime
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato inválido", "Ingrese fechas en formato AAAA-MM-DD")
            return
        try:
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query = "SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total FROM ventas v LEFT JOIN clientes c ON v.cliente_id = c.id WHERE date(v.fecha) BETWEEN ? AND ? AND v.estado = 'completada' ORDER BY v.fecha"
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
                ventas = self.cursor.fetchall()
                query = "SELECT p.nombre, SUM(dv.cantidad) as cantidad, SUM(dv.subtotal) as total FROM detalle_ventas dv JOIN productos p ON dv.producto_id = p.id JOIN ventas v ON dv.venta_id = v.id WHERE date(v.fecha) BETWEEN ? AND ? AND v.estado = 'completada' GROUP BY p.nombre ORDER BY total DESC"
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
                productos = self.cursor.fetchall()
            else:
                query = "SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total FROM ventas v LEFT JOIN clientes c ON v.cliente_id = c.id WHERE DATE(v.fecha) BETWEEN %s AND %s AND v.estado = 'completada' ORDER BY v.fecha"
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
                ventas = self.cursor.fetchall()
                query = "SELECT p.nombre, SUM(dv.cantidad) as cantidad, SUM(dv.subtotal) as total FROM detalle_ventas dv JOIN productos p ON dv.producto_id = p.id JOIN ventas v ON dv.venta_id = v.id WHERE DATE(v.fecha) BETWEEN %s AND %s AND v.estado = 'completada' GROUP BY p.nombre ORDER BY total DESC"
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
                productos = self.cursor.fetchall()
            self.texto_reporte.delete(1.0, 'end')
            self.texto_reporte.insert('end', f"📊 REPORTE DE VENTAS\nDel {fecha_inicio} al {fecha_fin}\n\n")
            self.texto_reporte.insert('end', "="*50 + "\n")
            self.texto_reporte.insert('end', f"VENTAS POR PERIODO ({len(ventas)} ventas):\n\n")
            total_periodo = 0.0
            for venta in ventas:
                fecha_formateada = venta[1][:16] if isinstance(venta[1], str) else str(venta[1])
                self.texto_reporte.insert('end', f"📅 Fecha: {fecha_formateada}\n")
                self.texto_reporte.insert('end', f"👤 Cliente: {venta[2]}\n")
                self.texto_reporte.insert('end', f"💵 Total: S/{venta[3]:.2f}\n")
                self.texto_reporte.insert('end', "-"*50 + "\n")
                total_periodo += float(venta[3])
            self.texto_reporte.insert('end', f"\n💰 TOTAL DEL PERIODO: S/{total_periodo:.2f}\n\n")
            self.texto_reporte.insert('end', "="*50 + "\n")
            self.texto_reporte.insert('end', f"PRODUCTOS MÁS VENDIDOS ({len(productos)} productos):\n\n")
            for producto in productos:
                self.texto_reporte.insert('end', f"📦 Producto: {producto[0]}\n")
                self.texto_reporte.insert('end', f"🔢 Cantidad: {producto[1]}\n")
                self.texto_reporte.insert('end', f"💵 Total: S/{producto[2]:.2f}\n")
                self.texto_reporte.insert('end', "-"*50 + "\n")
            self.texto_reporte.insert('end', "\n✅ FIN DEL REPORTE")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")

    def actualizar_dashboard(self):
        try:
            # Ventas de hoy
            query = "SELECT SUM(total) FROM ventas WHERE DATE(fecha) = CURDATE() AND estado = 'completada'"
            self.cursor.execute(query)
            ventas_hoy = self.cursor.fetchone()[0] or 0
            self.labels_metricas["ventas_hoy"].config(text=f"S/{ventas_hoy:.2f}")
            # Ventas del mes
            query = "SELECT SUM(total) FROM ventas WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE()) AND estado = 'completada'"
            self.cursor.execute(query)
            ventas_mes = self.cursor.fetchone()[0] or 0
            self.labels_metricas["ventas_mes"].config(text=f"S/{ventas_mes:.2f}")
            # Productos bajo stock
            query = f"SELECT COUNT(*) FROM productos WHERE stock <= 5 AND activo = TRUE"
            self.cursor.execute(query)
            bajo_stock = self.cursor.fetchone()[0]
            self.labels_metricas["productos_bajo_stock"].config(text=str(bajo_stock))
            # Productos más vendidos
            try:
                # Verificar si existen tablas necesarias
                self.cursor.execute("SHOW TABLES LIKE 'detalle_ventas'")
                if self.cursor.fetchone():
                    query = """SELECT p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.subtotal) as total_ingresos
                              FROM detalle_ventas dv
                              JOIN productos p ON dv.producto_id = p.id
                              JOIN ventas v ON dv.venta_id = v.id
                              WHERE v.estado = 'completada'
                              AND v.fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                              GROUP BY p.id, p.nombre
                              ORDER BY total_vendido DESC
                              LIMIT 3"""
                    self.cursor.execute(query)
                    populares = self.cursor.fetchall()
                    if populares:
                        texto_productos = []
                        for p in populares:
                            nombre_corto = p[0][:15] + "..." if len(p[0]) > 15 else p[0]
                            texto_productos.append(f"{nombre_corto} ({p[1]})")
                        texto = ", ".join(texto_productos)
                        self.labels_metricas["productos_populares"].config(text=texto)
                    else:
                        self.labels_metricas["productos_populares"].config(text="Sin ventas recientes")
                else:
                    self.labels_metricas["productos_populares"].config(text="N/A - Sin datos")
            except Exception as e_productos:
                # Fallback: mostrar productos con más stock como alternativa
                try:
                    query_fallback = """SELECT nombre, stock 
                                      FROM productos 
                                      WHERE activo = 1 AND stock > 0
                                      ORDER BY stock DESC 
                                      LIMIT 3"""
                    self.cursor.execute(query_fallback)
                    productos_stock = self.cursor.fetchall()
                    if productos_stock:
                        texto = ", ".join([f"{p[0][:12]}... ({p[1]} stock)" for p in productos_stock])
                        self.labels_metricas["productos_populares"].config(text=texto)
                    else:
                        self.labels_metricas["productos_populares"].config(text="Sin productos")
                except Exception:
                    self.labels_metricas["productos_populares"].config(text="Error en consulta")
        except Exception as e:
            for key in self.labels_metricas:
                self.labels_metricas[key].config(text="Error")

    def refrescar_automatico(self):
        # Refrescar dashboard cada minuto
        self.actualizar_dashboard()
        self.parent.after(60000, self.refrescar_automatico)
    
    def actualizar_tema(self, nuevo_tema):
        """Actualizar tema de la interfaz sin reiniciar"""
        self.tema = nuevo_tema
        self.colores = get_colores_tema(self.tema)
        configurar_estilos(self.tema)
        
        # Actualizar todos los widgets con los nuevos colores
        def actualizar_widget(widget):
            try:
                if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                    widget.configure(bg=self.colores['frame_bg'])
                    if isinstance(widget, tk.LabelFrame):
                        widget.configure(fg=self.colores['fg'])
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=self.colores['frame_bg'], fg=self.colores['fg'])
                elif isinstance(widget, tk.Entry):
                    widget.configure(bg=self.colores['entry_bg'], fg=self.colores['entry_fg'])
                elif isinstance(widget, tk.Text):
                    widget.configure(bg=self.colores['entry_bg'], fg=self.colores['entry_fg'])
                elif isinstance(widget, tk.Button):
                    # Mantener colores específicos de botones
                    current_bg = widget.cget('bg')
                    if current_bg in ['#4CAF50', '#2196F3', '#F44336', '#FF9800']:  # colores específicos
                        pass  # mantener color específico
                    else:
                        widget.configure(bg=self.colores['button_bg'], fg=self.colores['button_fg'])
                
                # Recursivamente actualizar hijos
                for child in widget.winfo_children():
                    actualizar_widget(child)
            except tk.TclError:
                pass  # Widget ya no existe
        
        # Actualizar desde el widget principal
        actualizar_widget(self.parent)
        
        # Refrescar dashboard con nuevos colores
        self.actualizar_dashboard()
        
        # Actualizar gráficos si están disponibles
        if self.graficos_widget and hasattr(self.graficos_widget, 'actualizar_tema'):
            self.graficos_widget.actualizar_tema(nuevo_tema)

    def generar_pdf_ventas(self):
        """Generar reporte de ventas en PDF"""
        if not PDF_DISPONIBLE:
            messagebox.showwarning("PDF no disponible", "El módulo de generación de PDF no está instalado")
            return
        
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        
        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Fechas requeridas", "Seleccione las fechas para generar el reporte PDF")
            return
            
        try:
            from datetime import datetime
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato inválido", "Use formato AAAA-MM-DD para las fechas")
            return
        
        if self.generador_pdf:
            self.generador_pdf.generar_reporte_ventas(fecha_inicio, fecha_fin, incluir_graficos=True)

    def generar_pdf_inventario(self):
        """Generar reporte de inventario en PDF"""
        if not PDF_DISPONIBLE:
            messagebox.showwarning("PDF no disponible", "El módulo de generación de PDF no está instalado")
            return
        
        if self.generador_pdf:
            self.generador_pdf.generar_reporte_inventario() 