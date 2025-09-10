import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from estilos import configurar_estilos, get_colores_tema
from generador_pdf import GeneradorPDF
from graficos_estadisticas import GraficosEstadisticas
import os

class ReportesUI:
    def __init__(self, parent, conn, cursor, rol, tema='claro'):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.rol = rol
        self.tema = tema
        self.colores = get_colores_tema(self.tema)
        self.generador_pdf = GeneradorPDF()
        self.graficos = GraficosEstadisticas()
        self.datos_actuales = {'ventas': [], 'productos': []}
        self.crear_interfaz()
        self.refrescar_automatico()

    def crear_interfaz(self):
        configurar_estilos(self.tema)
        c = self.colores
        
        # Frame principal
        main_frame = tk.Frame(self.parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Dashboard superior
        frame_dashboard = tk.LabelFrame(main_frame, text="📈 Dashboard", font=('Segoe UI', 12, 'bold'), 
                                      fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
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
            tk.Label(frame_metrica, text=texto, font=('Segoe UI', 10, 'bold'), 
                    bg=c['frame_bg'], fg=color).pack(pady=5)
            label_valor = tk.Label(frame_metrica, text="Cargando...", font=('Segoe UI', 14, 'bold'), 
                                 bg=c['frame_bg'], fg=color)
            label_valor.pack(pady=5)
            self.labels_metricas[key] = label_valor
        
        for i in range(4):
            frame_metricas.columnconfigure(i, weight=1)
        
        # Filtros
        frame_filtros = tk.LabelFrame(main_frame, text="🔍 Filtros", font=('Segoe UI', 12, 'bold'), 
                                    fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_filtros.pack(fill='x', padx=10, pady=10)
        
        frame_campos_filtros = tk.Frame(frame_filtros, bg=c['frame_bg'])
        frame_campos_filtros.pack(fill='x', padx=20, pady=20)
        
        # Campos de fecha
        tk.Label(frame_campos_filtros, text="📅 Fecha Inicio:", font=('Segoe UI', 10, 'bold'), 
                bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=0, sticky='e', padx=(0, 10), pady=5)
        self.fecha_inicio = tk.Entry(frame_campos_filtros, font=('Segoe UI', 10), 
                                   bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.fecha_inicio.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_campos_filtros, text="📅 Fecha Fin:", font=('Segoe UI', 10, 'bold'), 
                bg=c['frame_bg'], fg=c['fg']).grid(row=0, column=2, sticky='e', padx=(20, 10), pady=5)
        self.fecha_fin = tk.Entry(frame_campos_filtros, font=('Segoe UI', 10), 
                                bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        self.fecha_fin.grid(row=0, column=3, padx=5, pady=5)
        
        # Botones de fechas rápidas
        frame_fechas_rapidas = tk.Frame(frame_campos_filtros, bg=c['frame_bg'])
        frame_fechas_rapidas.grid(row=1, column=0, columnspan=4, pady=10)
        
        tk.Label(frame_fechas_rapidas, text="📋 Fechas Rápidas:", font=('Segoe UI', 10, 'bold'), 
                bg=c['frame_bg'], fg=c['fg']).pack(side='left', padx=(0, 10))
        
        botones_fecha = [
            ("Hoy", self.fecha_hoy),
            ("Ayer", self.fecha_ayer),
            ("Esta Semana", self.fecha_esta_semana),
            ("Este Mes", self.fecha_este_mes),
            ("Último Mes", self.fecha_ultimo_mes)
        ]
        
        for texto, comando in botones_fecha:
            btn = tk.Button(frame_fechas_rapidas, text=texto, command=comando, 
                          font=('Segoe UI', 9, 'bold'), bg=c['accent'], fg=c['button_fg'], 
                          relief='flat', bd=0, padx=10, pady=5)
            btn.pack(side='left', padx=2)
        
        # Botones de acción
        frame_botones = tk.Frame(frame_campos_filtros, bg=c['frame_bg'])
        frame_botones.grid(row=2, column=0, columnspan=4, pady=15)
        
        btn_reporte = tk.Button(frame_botones, text="📊 Generar Reporte", command=self.generar_reporte, 
                              font=('Segoe UI', 10, 'bold'), bg=c['ok_fg'], fg=c['button_fg'], 
                              relief='flat', bd=0, padx=20, pady=8)
        btn_reporte.pack(side='left', padx=5)
        
        btn_pdf = tk.Button(frame_botones, text="📄 Generar PDF", command=self.generar_pdf, 
                          font=('Segoe UI', 10, 'bold'), bg=c['error_fg'], fg=c['button_fg'], 
                          relief='flat', bd=0, padx=20, pady=8)
        btn_pdf.pack(side='left', padx=5)
        
        frame_campos_filtros.columnconfigure(1, weight=1)
        frame_campos_filtros.columnconfigure(3, weight=1)
        
        # Notebook para pestañas de visualización
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de Reporte de Texto
        tab_texto = tk.Frame(self.notebook, bg=c['bg'])
        self.notebook.add(tab_texto, text="📋 Reporte")
        
        frame_texto_reporte = tk.Frame(tab_texto, bg=c['frame_bg'])
        frame_texto_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.texto_reporte = tk.Text(frame_texto_reporte, wrap='word', font=('Consolas', 10), 
                                   bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        scrollbar_reporte = ttk.Scrollbar(frame_texto_reporte, orient="vertical", 
                                        command=self.texto_reporte.yview)
        self.texto_reporte.configure(yscrollcommand=scrollbar_reporte.set)
        self.texto_reporte.pack(side='left', fill='both', expand=True)
        scrollbar_reporte.pack(side='right', fill='y')
        
        # Pestaña de Gráfico de Barras
        tab_barras = tk.Frame(self.notebook, bg=c['bg'])
        self.notebook.add(tab_barras, text="📊 Gráfico Barras")
        
        self.frame_grafico_barras = tk.Frame(tab_barras, bg=c['bg'])
        self.frame_grafico_barras.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de Gráfico de Torta
        tab_torta = tk.Frame(self.notebook, bg=c['bg'])
        self.notebook.add(tab_torta, text="🥧 Gráfico Torta")
        
        self.frame_grafico_torta = tk.Frame(tab_torta, bg=c['bg'])
        self.frame_grafico_torta.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.actualizar_dashboard()

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
            
            # Guardar datos para uso posterior y generar gráficos
            self.datos_actuales['ventas'] = ventas
            self.datos_actuales['productos'] = productos
            
            # Generar gráficos
            self.generar_graficos_reporte(ventas, productos)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")
    
    def generar_graficos_reporte(self, ventas, productos):
        """Genera los gráficos basados en los datos del reporte"""
        try:
            # Gráfico de barras de ventas
            self.graficos.crear_grafico_barras_ventas(
                self.frame_grafico_barras, 
                ventas, 
                f"Ventas del {self.fecha_inicio.get()} al {self.fecha_fin.get()}"
            )
            
            # Gráfico de torta de productos
            self.graficos.crear_grafico_torta_productos(
                self.frame_grafico_torta, 
                productos, 
                f"Productos Más Vendidos ({self.fecha_inicio.get()} - {self.fecha_fin.get()})"
            )
            
        except Exception as e:
            print(f"Error al generar gráficos: {e}")
    
    def generar_pdf(self):
        """Genera un archivo PDF del reporte actual"""
        if not self.datos_actuales['ventas']:
            messagebox.showwarning("Sin datos", "Primero genera un reporte para poder exportar a PDF")
            return
        
        try:
            # Pedir ubicación del archivo
            archivo_pdf = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar reporte como PDF"
            )
            
            if not archivo_pdf:
                return
            
            # Generar el PDF
            ruta_pdf = self.generador_pdf.generar_reporte_ventas(
                self.datos_actuales['ventas'],
                self.datos_actuales['productos'],
                self.fecha_inicio.get(),
                self.fecha_fin.get(),
                archivo_pdf
            )
            
            messagebox.showinfo("PDF Generado", f"El reporte PDF se ha guardado exitosamente en:\n{ruta_pdf}")
            
            # Abrir el PDF automáticamente
            try:
                os.startfile(ruta_pdf)  # Windows
            except AttributeError:
                try:
                    os.system(f"open '{ruta_pdf}'")  # macOS
                except:
                    os.system(f"xdg-open '{ruta_pdf}'")  # Linux
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {e}")

    def actualizar_dashboard(self):
        """Actualiza el dashboard con mejor manejo de errores y compatibilidad SQLite/MySQL"""
        try:
            # Detectar tipo de base de datos
            is_sqlite = self.conn.__class__.__module__.startswith('sqlite3')
            
            # Ventas de hoy
            if is_sqlite:
                query = "SELECT SUM(total) FROM ventas WHERE date(fecha) = date('now') AND estado = 'completada'"
            else:
                query = "SELECT SUM(total) FROM ventas WHERE DATE(fecha) = CURDATE() AND estado = 'completada'"
            
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            ventas_hoy = result[0] if result and result[0] else 0
            
            # Ventas del mes
            if is_sqlite:
                query = "SELECT SUM(total) FROM ventas WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now') AND estado = 'completada'"
            else:
                query = "SELECT SUM(total) FROM ventas WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE()) AND estado = 'completada'"
            
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            ventas_mes = result[0] if result and result[0] else 0
            
            # Productos bajo stock
            if is_sqlite:
                query = "SELECT COUNT(*) FROM productos WHERE stock <= 5 AND activo = 1"
            else:
                query = "SELECT COUNT(*) FROM productos WHERE stock <= 5 AND activo = TRUE"
            
            self.cursor.execute(query)
            bajo_stock = self.cursor.fetchone()[0] or 0
            
            # Productos más vendidos (optimizado)
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
            
            # Actualizar interfaz de forma asíncrona para mejor fluidez
            self.parent.after_idle(lambda: self.actualizar_metricas_ui(ventas_hoy, ventas_mes, bajo_stock, populares))
            
        except Exception as e:
            print(f"Error al actualizar dashboard: {e}")
            # Usar after_idle para evitar bloqueos
            self.parent.after_idle(lambda: self.mostrar_error_dashboard())
    
    def actualizar_metricas_ui(self, ventas_hoy, ventas_mes, bajo_stock, populares):
        """Actualiza la UI con las métricas calculadas"""
        try:
            self.labels_metricas["ventas_hoy"].config(text=f"S/ {ventas_hoy:.2f}")
            self.labels_metricas["ventas_mes"].config(text=f"S/ {ventas_mes:.2f}")
            self.labels_metricas["productos_bajo_stock"].config(text=str(bajo_stock))
            
            if populares:
                # Truncar nombres largos para mejor presentación
                texto = ", ".join([f"{p[0][:15]}... ({p[1]})" if len(p[0]) > 15 else f"{p[0]} ({p[1]})" for p in populares])
                self.labels_metricas["productos_populares"].config(text=texto)
            else:
                self.labels_metricas["productos_populares"].config(text="Ninguno")
        except Exception as e:
            print(f"Error al actualizar UI del dashboard: {e}")
            self.mostrar_error_dashboard()
    
    def mostrar_error_dashboard(self):
        """Muestra error en las métricas del dashboard"""
        try:
            for key in self.labels_metricas:
                self.labels_metricas[key].config(text="Error")
        except Exception as e:
            print(f"Error crítico en dashboard: {e}")

    def refrescar_automatico(self):
        """Refrescar dashboard de forma optimizada para evitar bloqueos"""
        def refrescar():
            try:
                # Solo actualizar si el widget sigue existiendo
                if self.parent.winfo_exists():
                    self.actualizar_dashboard()
                    # Programar siguiente actualización
                    self.parent.after(60000, refrescar)
            except Exception as e:
                print(f"Error en refrescar automático: {e}")
        
        # Iniciar el ciclo de actualización
        self.parent.after(5000, refrescar)  # Primera actualización en 5 segundos
    
    def actualizar_tema(self, nuevo_tema):
        """Actualiza el tema del módulo sin recrear toda la interfaz"""
        try:
            from estilos import get_colores_tema
            
            self.tema = nuevo_tema
            self.colores = get_colores_tema(nuevo_tema)
            
            # Recrear la interfaz con el nuevo tema
            self.recrear_interfaz()
            
        except Exception as e:
            print(f"Error al actualizar tema en reportes: {e}")
    
    def recrear_interfaz(self):
        """Recrea la interfaz con el nuevo tema"""
        try:
            # Limpiar la interfaz actual
            for widget in self.parent.winfo_children():
                widget.destroy()
            
            # Recrear con el nuevo tema
            self.crear_interfaz()
            
            # Si hay datos actuales, regenerar los gráficos
            if self.datos_actuales['ventas']:
                self.generar_graficos_reporte(
                    self.datos_actuales['ventas'], 
                    self.datos_actuales['productos']
                )
            
        except Exception as e:
            print(f"Error al recrear interfaz de reportes: {e}")

    # ... Métodos para generar reportes, mostrar dashboard, etc ... 