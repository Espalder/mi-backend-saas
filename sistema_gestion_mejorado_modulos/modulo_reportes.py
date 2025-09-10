import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from estilos import configurar_estilos, get_colores_tema
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import os

class ReportesUI:
    def __init__(self, parent, conn, cursor, rol, tema='claro'):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.rol = rol
        self.tema = tema
        self.colores = get_colores_tema(self.tema)
        self.crear_interfaz()
        self.refrescar_automatico()

    def crear_interfaz(self):
        configurar_estilos(self.tema)
        c = self.colores
        main_frame = tk.Frame(self.parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        frame_dashboard = tk.LabelFrame(main_frame, text="📈 Dashboard", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
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
        frame_filtros = tk.LabelFrame(main_frame, text="🔍 Filtros", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
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
        # Frame para botones
        frame_botones = tk.Frame(frame_campos_filtros, bg=c['frame_bg'])
        frame_botones.grid(row=2, column=0, columnspan=4, pady=15)
        
        btn_reporte = tk.Button(frame_botones, text="📊 Generar Reporte", command=self.generar_reporte, font=('Segoe UI', 10, 'bold'), bg=c['ok_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=15, pady=8)
        btn_reporte.pack(side='left', padx=5)
        
        btn_pdf = tk.Button(frame_botones, text="📄 Exportar PDF", command=self.exportar_pdf, font=('Segoe UI', 10, 'bold'), bg=c['error_fg'], fg=c['button_fg'], relief='flat', bd=0, padx=15, pady=8)
        btn_pdf.pack(side='left', padx=5)
        
        btn_grafico = tk.Button(frame_botones, text="📈 Ver Gráficos", command=self.mostrar_graficos, font=('Segoe UI', 10, 'bold'), bg=c['accent'], fg=c['button_fg'], relief='flat', bd=0, padx=15, pady=8)
        btn_grafico.pack(side='left', padx=5)
        frame_campos_filtros.columnconfigure(1, weight=1)
        frame_campos_filtros.columnconfigure(3, weight=1)
        frame_reporte = tk.LabelFrame(main_frame, text="📋 Reporte", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        frame_texto_reporte = tk.Frame(frame_reporte, bg=c['frame_bg'])
        frame_texto_reporte.pack(fill='both', expand=True, padx=10, pady=10)
        self.texto_reporte = tk.Text(frame_texto_reporte, wrap='word', font=('Consolas', 10), bg=c['entry_bg'], fg=c['entry_fg'], relief='solid', bd=1)
        scrollbar_reporte = ttk.Scrollbar(frame_texto_reporte, orient="vertical", command=self.texto_reporte.yview)
        self.texto_reporte.configure(yscrollcommand=scrollbar_reporte.set)
        self.texto_reporte.pack(side='left', fill='both', expand=True)
        scrollbar_reporte.pack(side='right', fill='y')
        
        # Frame para gráficos
        self.frame_graficos = tk.LabelFrame(main_frame, text="📈 Gráficos", font=('Segoe UI', 12, 'bold'), fg=c['fg'], bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        # No mostrar por defecto
        
        # Almacenar datos del último reporte para PDF y gráficos
        self.ultimo_reporte_datos = None
        
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
            
            # Guardar datos para PDF y gráficos
            self.ultimo_reporte_datos = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'ventas': ventas,
                'productos': productos,
                'total_periodo': total_periodo
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")

    def actualizar_dashboard(self):
        try:
            # Determinar tipo de base de datos para las consultas
            is_sqlite = self.conn.__class__.__module__.startswith('sqlite3')
            
            # Ventas de hoy
            if is_sqlite:
                query = "SELECT SUM(total) FROM ventas WHERE date(fecha) = date('now') AND estado = 'completada'"
            else:
                query = "SELECT SUM(total) FROM ventas WHERE DATE(fecha) = CURDATE() AND estado = 'completada'"
            self.cursor.execute(query)
            ventas_hoy = self.cursor.fetchone()[0] or 0
            self.labels_metricas["ventas_hoy"].config(text=f"S/{ventas_hoy:.2f}")
            
            # Ventas del mes
            if is_sqlite:
                query = "SELECT SUM(total) FROM ventas WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now') AND estado = 'completada'"
            else:
                query = "SELECT SUM(total) FROM ventas WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE()) AND estado = 'completada'"
            self.cursor.execute(query)
            ventas_mes = self.cursor.fetchone()[0] or 0
            self.labels_metricas["ventas_mes"].config(text=f"S/{ventas_mes:.2f}")
            
            # Productos bajo stock
            if is_sqlite:
                query = "SELECT COUNT(*) FROM productos WHERE stock <= 5 AND activo = 1"
            else:
                query = "SELECT COUNT(*) FROM productos WHERE stock <= 5 AND activo = TRUE"
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
        except Exception as e:
            for key in self.labels_metricas:
                self.labels_metricas[key].config(text="Error")

    def refrescar_automatico(self):
        # Aquí solo debe refrescar dashboard, sin lógica de sincronización ni botones extra
        self.parent.after(60000, self.actualizar_dashboard)
    
    def exportar_pdf(self):
        """Exporta el reporte actual a PDF"""
        if not self.ultimo_reporte_datos:
            messagebox.showwarning("Sin datos", "Primero genere un reporte para exportar a PDF")
            return
        
        # Solicitar ubicación para guardar el PDF
        filename = filedialog.asksaveasfilename(
            title="Guardar reporte como PDF",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if not filename:
            return
        
        try:
            self._generar_pdf(filename)
            messagebox.showinfo("Éxito", f"Reporte PDF generado exitosamente: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
    
    def _generar_pdf(self, filename):
        """Genera el archivo PDF del reporte"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=colors.darkblue
        )
        
        datos = self.ultimo_reporte_datos
        story.append(Paragraph(f"REPORTE DE VENTAS", title_style))
        story.append(Paragraph(f"Del {datos['fecha_inicio']} al {datos['fecha_fin']}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Resumen ejecutivo
        story.append(Paragraph("RESUMEN EJECUTIVO", styles['Heading2']))
        story.append(Paragraph(f"Total de ventas: {len(datos['ventas'])}", styles['Normal']))
        story.append(Paragraph(f"Total facturado: S/{datos['total_periodo']:.2f}", styles['Normal']))
        story.append(Paragraph(f"Productos diferentes vendidos: {len(datos['productos'])}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Tabla de ventas
        if datos['ventas']:
            story.append(Paragraph("DETALLE DE VENTAS", styles['Heading2']))
            ventas_data = [['Fecha', 'Cliente', 'Total (S/)']]
            for venta in datos['ventas'][:20]:  # Limitar a 20 para el PDF
                fecha_formateada = venta[1][:16] if isinstance(venta[1], str) else str(venta[1])
                ventas_data.append([fecha_formateada, venta[2], f"S/{venta[3]:.2f}"])
            
            ventas_table = Table(ventas_data)
            ventas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(ventas_table)
            story.append(Spacer(1, 20))
        
        # Tabla de productos más vendidos
        if datos['productos']:
            story.append(Paragraph("PRODUCTOS MÁS VENDIDOS", styles['Heading2']))
            productos_data = [['Producto', 'Cantidad', 'Total (S/)']]
            for producto in datos['productos'][:10]:  # Top 10
                productos_data.append([producto[0], str(producto[1]), f"S/{producto[2]:.2f}"])
            
            productos_table = Table(productos_data)
            productos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(productos_table)
        
        # Pie de página
        story.append(Spacer(1, 30))
        story.append(Paragraph(f"Reporte generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Italic']))
        
        doc.build(story)
    
    def mostrar_graficos(self):
        """Muestra gráficos basados en los datos del reporte"""
        if not self.ultimo_reporte_datos:
            messagebox.showwarning("Sin datos", "Primero genere un reporte para ver gráficos")
            return
        
        # Mostrar frame de gráficos
        self.frame_graficos.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Limpiar gráficos anteriores
        for widget in self.frame_graficos.winfo_children():
            widget.destroy()
        
        # Crear notebook para múltiples gráficos
        notebook_graficos = ttk.Notebook(self.frame_graficos)
        notebook_graficos.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configurar matplotlib para usar tema
        plt.style.use('seaborn-v0_8' if hasattr(plt.style, 'seaborn-v0_8') else 'default')
        
        # Gráfico 1: Ventas por día
        self._crear_grafico_ventas_dia(notebook_graficos)
        
        # Gráfico 2: Productos más vendidos
        self._crear_grafico_productos(notebook_graficos)
        
        # Gráfico 3: Distribución de ventas
        self._crear_grafico_distribucion(notebook_graficos)
    
    def _crear_grafico_ventas_dia(self, parent):
        """Crea gráfico de ventas por día"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="📈 Ventas por Día")
        
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        datos = self.ultimo_reporte_datos
        if not datos['ventas']:
            ax.text(0.5, 0.5, 'Sin datos para mostrar', ha='center', va='center', transform=ax.transAxes)
        else:
            # Procesar datos por día
            ventas_por_dia = {}
            for venta in datos['ventas']:
                fecha = venta[1][:10] if isinstance(venta[1], str) else str(venta[1])[:10]
                if fecha not in ventas_por_dia:
                    ventas_por_dia[fecha] = 0
                ventas_por_dia[fecha] += float(venta[3])
            
            fechas = sorted(ventas_por_dia.keys())
            valores = [ventas_por_dia[fecha] for fecha in fechas]
            
            ax.plot(fechas, valores, marker='o', linewidth=2, markersize=6)
            ax.set_title(f'Ventas por Día ({datos["fecha_inicio"]} - {datos["fecha_fin"]})', fontsize=14, fontweight='bold')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Ventas (S/)')
            ax.grid(True, alpha=0.3)
            
            # Rotar etiquetas de fecha si hay muchas
            if len(fechas) > 7:
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def _crear_grafico_productos(self, parent):
        """Crea gráfico de productos más vendidos"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="📦 Top Productos")
        
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        datos = self.ultimo_reporte_datos
        if not datos['productos']:
            ax.text(0.5, 0.5, 'Sin datos para mostrar', ha='center', va='center', transform=ax.transAxes)
        else:
            # Tomar top 10 productos
            top_productos = datos['productos'][:10]
            nombres = [p[0][:15] + '...' if len(p[0]) > 15 else p[0] for p in top_productos]
            cantidades = [p[1] for p in top_productos]
            
            bars = ax.bar(range(len(nombres)), cantidades, color='skyblue', edgecolor='navy', alpha=0.7)
            
            ax.set_title('Top 10 Productos Más Vendidos', fontsize=14, fontweight='bold')
            ax.set_xlabel('Productos')
            ax.set_ylabel('Cantidad Vendida')
            ax.set_xticks(range(len(nombres)))
            ax.set_xticklabels(nombres, rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Añadir valores en las barras
            for bar, cantidad in zip(bars, cantidades):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{cantidad}', ha='center', va='bottom')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def _crear_grafico_distribucion(self, parent):
        """Crea gráfico de distribución de ventas"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="🥧 Distribución")
        
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        datos = self.ultimo_reporte_datos
        if not datos['productos']:
            ax.text(0.5, 0.5, 'Sin datos para mostrar', ha='center', va='center', transform=ax.transAxes)
        else:
            # Crear gráfico de pastel con top 8 productos
            top_productos = datos['productos'][:8]
            otros_total = sum([p[2] for p in datos['productos'][8:]])
            
            labels = [p[0][:10] + '...' if len(p[0]) > 10 else p[0] for p in top_productos]
            sizes = [p[2] for p in top_productos]
            
            if otros_total > 0:
                labels.append('Otros')
                sizes.append(otros_total)
            
            colors_pie = plt.cm.Set3(np.linspace(0, 1, len(sizes)))
            
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                             startangle=90, colors=colors_pie)
            
            ax.set_title('Distribución de Ventas por Producto', fontsize=14, fontweight='bold')
            
            # Mejorar legibilidad de los textos
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True) 