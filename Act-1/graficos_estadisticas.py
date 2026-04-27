# graficos_estadisticas.py
"""
Módulo para generar gráficos estadísticos del sistema
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import os

class GraficosEstadisticas:
    def __init__(self, parent, conn, cursor, tema='claro'):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.tema = tema
        self.figuras = {}
        
        # Configurar estilo de matplotlib según el tema
        self.configurar_estilo_matplotlib()
        
    def limpiar_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def crear_grafico_barras_ventas(self, parent_frame, ventas, titulo):
        """Crea gráfico de barras con ventas por fecha a partir de datos ya consultados"""
        try:
            self.limpiar_frame(parent_frame)
            from matplotlib.figure import Figure
            fig = Figure(figsize=(10, 4), facecolor=self.colores['fondo'])
            ax = fig.add_subplot(111)
            if not ventas:
                ax.text(0.5, 0.5, 'No hay datos de ventas para mostrar', ha='center', va='center',
                        transform=ax.transAxes, fontsize=12, color=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
            else:
                # Agrupar ventas por fecha
                from collections import defaultdict
                suma_por_fecha = defaultdict(float)
                for v in ventas:
                    fecha = str(v[1])[:10]
                    suma_por_fecha[fecha] += float(v[3])
                fechas = sorted(suma_por_fecha.keys())
                totales = [suma_por_fecha[f] for f in fechas]
                ax.bar(fechas, totales, color=self.colores['primario'])
                ax.set_title(titulo, fontsize=12, color=self.colores['texto'])
                ax.set_ylabel('Total S/', color=self.colores['texto'])
                ax.tick_params(axis='x', rotation=45, colors=self.colores['texto'])
                ax.tick_params(axis='y', colors=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        except Exception as e:
            print(f"Error en crear_grafico_barras_ventas: {e}")

    def crear_grafico_torta_productos(self, parent_frame, productos, titulo):
        """Crea gráfico de torta de productos más vendidos a partir de datos ya consultados"""
        try:
            self.limpiar_frame(parent_frame)
            from matplotlib.figure import Figure
            fig = Figure(figsize=(8, 4), facecolor=self.colores['fondo'])
            ax = fig.add_subplot(111)
            if not productos:
                ax.text(0.5, 0.5, 'No hay productos vendidos en el periodo', ha='center', va='center',
                        transform=ax.transAxes, fontsize=12, color=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
            else:
                labels = [p[0] for p in productos]
                cantidades = [int(p[1]) for p in productos]
                ax.pie(cantidades, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title(titulo, fontsize=12, color=self.colores['texto'])
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        except Exception as e:
            print(f"Error en crear_grafico_torta_productos: {e}")
    
    def configurar_estilo_matplotlib(self):
        """Configurar el estilo de matplotlib según el tema"""
        if self.tema == 'oscuro':
            plt.style.use('dark_background')
            self.colores = {
                'fondo': '#2c3e50',
                'texto': '#ecf0f1',
                'primario': '#3498db',
                'secundario': '#e74c3c',
                'terciario': '#2ecc71',
                'cuaternario': '#f39c12'
            }
        else:
            plt.style.use('default')
            self.colores = {
                'fondo': '#ffffff',
                'texto': '#2c3e50',
                'primario': '#3498db',
                'secundario': '#e74c3c',
                'terciario': '#2ecc71',
                'cuaternario': '#f39c12'
            }
    
    def crear_grafico_ventas_por_dia(self, parent_frame):
        """Crear gráfico de ventas por día"""
        try:
            # Obtener datos de ventas de los últimos 30 días
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            if self.conn.__class__.__module__.startswith('sqlite3'):
                self.cursor.execute(
                    "SELECT strftime('%Y-%m-%d', fecha) as dia, COUNT(*), SUM(total) "
                    "FROM ventas WHERE date(fecha) >= ? AND estado = 'completada' "
                    "GROUP BY strftime('%Y-%m-%d', fecha) ORDER BY dia",
                    (fecha_inicio,)
                )
            else:
                self.cursor.execute(
                    "SELECT DATE(fecha) as dia, COUNT(*) as cantidad_ventas, SUM(total) as total_ventas "
                    "FROM ventas WHERE DATE(fecha) >= %s AND estado = 'completada' "
                    "GROUP BY DATE(fecha) ORDER BY dia",
                    (fecha_inicio,)
                )
            
            datos = self.cursor.fetchall()
            
            if not datos:
                # Crear gráfico vacío
                fig = Figure(figsize=(8, 4), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, 'No hay datos de ventas\npara mostrar', 
                       ha='center', va='center', transform=ax.transAxes,
                       fontsize=12, color=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
            else:
                # Preparar datos
                from datetime import date
                fechas = [datetime.strptime(d[0], '%Y-%m-%d') if isinstance(d[0], str) else (datetime(d[0].year, d[0].month, d[0].day) if isinstance(d[0], date) else d[0]) for d in datos]
                cantidades = [int(d[1]) for d in datos]
                totales = [float(d[2]) if d[2] is not None else 0.0 for d in datos]
                
                # Crear figura
                fig = Figure(figsize=(10, 6), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                
                # Crear gráfico de barras
                ax.bar(fechas, cantidades, color=self.colores['primario'], alpha=0.7, label='Cantidad de Ventas')
                
                # Configurar el gráfico
                ax.set_title('📊 Ventas por Día (Últimos 30 días)', 
                           fontsize=14, fontweight='bold', color=self.colores['texto'])
                ax.set_xlabel('Fecha', color=self.colores['texto'])
                ax.set_ylabel('Cantidad de Ventas', color=self.colores['texto'])
                ax.tick_params(colors=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
                
                # Formatear fechas en el eje X
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
                
                # Agregar grid
                ax.grid(True, alpha=0.3, color=self.colores['texto'])
                ax.legend()
            
            # Limpiar frame y crear canvas para tkinter
            self.limpiar_frame(parent_frame)
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
            return canvas
            
        except Exception as e:
            print(f"Error creando gráfico de ventas por día: {e}")
            return None
    
    def crear_grafico_productos_mas_vendidos(self, parent_frame):
        """Crear gráfico de productos más vendidos"""
        try:
            # Obtener datos de productos más vendidos
            if self.conn.__class__.__module__.startswith('sqlite3'):
                self.cursor.execute(
                    "SELECT p.nombre, SUM(dv.cantidad) as total_vendido "
                    "FROM detalle_ventas dv JOIN productos p ON dv.producto_id = p.id "
                    "JOIN ventas v ON dv.venta_id = v.id WHERE v.estado = 'completada' "
                    "GROUP BY p.id, p.nombre ORDER BY total_vendido DESC LIMIT 10"
                )
            else:
                self.cursor.execute(
                    "SELECT p.nombre, SUM(dv.cantidad) as total_vendido "
                    "FROM detalle_ventas dv JOIN productos p ON dv.producto_id = p.id "
                    "JOIN ventas v ON dv.venta_id = v.id WHERE v.estado = 'completada' "
                    "GROUP BY p.id, p.nombre ORDER BY total_vendido DESC LIMIT 10"
                )
            
            datos = self.cursor.fetchall()
            
            if not datos:
                # Crear gráfico vacío
                fig = Figure(figsize=(8, 4), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, 'No hay datos de productos\nvendidos para mostrar', 
                       ha='center', va='center', transform=ax.transAxes,
                       fontsize=12, color=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
            else:
                # Preparar datos
                productos = [d[0][:20] + '...' if len(d[0]) > 20 else d[0] for d in datos]
                cantidades = [d[1] for d in datos]
                
                # Crear figura
                fig = Figure(figsize=(10, 6), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                
                # Crear gráfico de barras horizontales
                y_pos = np.arange(len(productos))
                ax.barh(y_pos, cantidades, color=self.colores['terciario'], alpha=0.7)
                
                # Configurar el gráfico
                ax.set_yticks(y_pos)
                ax.set_yticklabels(productos)
                ax.set_title('🏆 Productos Más Vendidos', 
                           fontsize=14, fontweight='bold', color=self.colores['texto'])
                ax.set_xlabel('Cantidad Vendida', color=self.colores['texto'])
                ax.tick_params(colors=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
                
                # Agregar valores en las barras
                for i, v in enumerate(cantidades):
                    vv = float(v)
                    ax.text(vv + 0.1, i, str(v), va='center', color=self.colores['texto'])
                
                # Invertir el eje Y para mostrar el más vendido arriba
                ax.invert_yaxis()
            
            self.limpiar_frame(parent_frame)
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
            return canvas
            
        except Exception as e:
            print(f"Error creando gráfico de productos más vendidos: {e}")
            return None
    
    def crear_grafico_estado_stock(self, parent_frame):
        """Crear gráfico de estado del stock (torta)"""
        try:
            # Obtener datos del estado del stock
            if self.conn.__class__.__module__.startswith('sqlite3'):
                self.cursor.execute(
                    "SELECT CASE WHEN stock = 0 THEN 'Sin Stock' "
                    "WHEN stock_minimo IS NOT NULL AND stock <= stock_minimo THEN 'Stock Bajo' "
                    "ELSE 'Stock Normal' END as estado_stock, COUNT(*) FROM productos WHERE activo = 1 "
                    "GROUP BY estado_stock"
                )
            else:
                self.cursor.execute(
                    "SELECT CASE WHEN stock = 0 THEN 'Sin Stock' "
                    "WHEN stock <= stock_minimo THEN 'Stock Bajo' ELSE 'Stock Normal' END as estado_stock, "
                    "COUNT(*) FROM productos WHERE activo = 1 GROUP BY estado_stock"
                )
            
            datos = self.cursor.fetchall()
            
            if not datos:
                # Crear gráfico vacío
                fig = Figure(figsize=(6, 6), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, 'No hay productos\npara mostrar', 
                       ha='center', va='center', transform=ax.transAxes,
                       fontsize=12, color=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
            else:
                # Preparar datos
                estados = [d[0] for d in datos]
                cantidades = [d[1] for d in datos]
                
                # Colores para cada estado
                colores_estado = []
                for estado in estados:
                    if estado == 'Sin Stock':
                        colores_estado.append(self.colores['secundario'])
                    elif estado == 'Stock Bajo':
                        colores_estado.append(self.colores['cuaternario'])
                    else:
                        colores_estado.append(self.colores['terciario'])
                
                # Crear figura
                fig = Figure(figsize=(8, 6), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                
                # Crear gráfico de torta
                wedges, texts, autotexts = ax.pie(cantidades, labels=estados, colors=colores_estado,
                                                 autopct='%1.1f%%', startangle=90)
                
                # Configurar el gráfico
                ax.set_title('📦 Estado del Stock de Productos', 
                           fontsize=14, fontweight='bold', color=self.colores['texto'])
                
                # Configurar colores del texto
                for text in texts:
                    text.set_color(self.colores['texto'])
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            
            self.limpiar_frame(parent_frame)
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
            return canvas
            
        except Exception as e:
            print(f"Error creando gráfico de estado del stock: {e}")
            return None
    
    def crear_grafico_ingresos_mensuales(self, parent_frame):
        """Crear gráfico de ingresos mensuales"""
        try:
            # Obtener datos de ingresos de los últimos 12 meses
            fecha_inicio = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
            self.cursor.execute("""
                SELECT 
                    DATE_FORMAT(fecha, '%Y-%m') as mes,
                    SUM(total) as ingresos
                FROM ventas 
                WHERE DATE(fecha) >= %s AND estado = 'completada'
                GROUP BY DATE_FORMAT(fecha, '%Y-%m')
                ORDER BY mes
            """, (fecha_inicio,))
            
            datos = self.cursor.fetchall()
            
            if not datos:
                # Crear gráfico vacío
                fig = Figure(figsize=(10, 4), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, 'No hay datos de ingresos\npara mostrar', 
                       ha='center', va='center', transform=ax.transAxes,
                       fontsize=12, color=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
            else:
                # Preparar datos
                meses = [datetime.strptime(d[0], '%Y-%m') for d in datos]
                ingresos = [float(d[1]) for d in datos]
                
                # Crear figura
                fig = Figure(figsize=(10, 6), facecolor=self.colores['fondo'])
                ax = fig.add_subplot(111)
                
                # Crear gráfico de línea
                ax.plot(meses, ingresos, marker='o', linewidth=2, markersize=6,
                       color=self.colores['primario'], label='Ingresos Mensuales')
                
                # Rellenar área bajo la curva
                ax.fill_between(meses, ingresos, alpha=0.3, color=self.colores['primario'])
                
                # Configurar el gráfico
                ax.set_title('💰 Ingresos Mensuales (Últimos 12 meses)', 
                           fontsize=14, fontweight='bold', color=self.colores['texto'])
                ax.set_xlabel('Mes', color=self.colores['texto'])
                ax.set_ylabel('Ingresos (S/)', color=self.colores['texto'])
                ax.tick_params(colors=self.colores['texto'])
                ax.set_facecolor(self.colores['fondo'])
                
                # Formatear fechas en el eje X
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
                ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
                
                # Formatear eje Y como moneda
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'S/{x:,.0f}'))
                
                # Agregar grid
                ax.grid(True, alpha=0.3, color=self.colores['texto'])
                ax.legend()
            
            self.limpiar_frame(parent_frame)
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
            return canvas
            
        except Exception as e:
            print(f"Error creando gráfico de ingresos mensuales: {e}")
            return None
    
    def crear_panel_graficos_completo(self, parent_frame):
        """Crear panel completo con todos los gráficos"""
        try:
            # Limpiar contenedor primero
            for child in parent_frame.winfo_children():
                child.destroy()
            # Frame principal con scroll
            main_frame = tk.Frame(parent_frame)
            main_frame.pack(fill='both', expand=True)
            
            # Crear notebook para organizar los gráficos
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Pestana 1: Ventas por día
            tab_ventas = ttk.Frame(notebook)
            notebook.add(tab_ventas, text="📊 Ventas por Día")
            self.crear_grafico_ventas_por_dia(tab_ventas)
            
            # Pestana 2: Productos más vendidos
            tab_productos = ttk.Frame(notebook)
            notebook.add(tab_productos, text="🏆 Productos Más Vendidos")
            self.crear_grafico_productos_mas_vendidos(tab_productos)
            
            # Pestana 3: Estado del stock
            tab_stock = ttk.Frame(notebook)
            notebook.add(tab_stock, text="📦 Estado del Stock")
            self.crear_grafico_estado_stock(tab_stock)
            
            # Pestana 4: Ingresos mensuales
            tab_ingresos = ttk.Frame(notebook)
            notebook.add(tab_ingresos, text="💰 Ingresos Mensuales")
            self.crear_grafico_ingresos_mensuales(tab_ingresos)
            
            # Actualizar gráficos cuando se cambia de pestaña
            def actualizar_graficos_seleccionado(event):
                selected_tab = event.widget.tab(event.widget.select())["text"]
                if selected_tab == "📊 Ventas por Día":
                    self.crear_grafico_ventas_por_dia(tab_ventas)
                elif selected_tab == "🏆 Productos Más Vendidos":
                    self.crear_grafico_productos_mas_vendidos(tab_productos)
                elif selected_tab == "📦 Estado del Stock":
                    self.crear_grafico_estado_stock(tab_stock)
                elif selected_tab == "💰 Ingresos Mensuales":
                    self.crear_grafico_ingresos_mensuales(tab_ingresos)
            
            notebook.bind("<<NotebookTabChanged>>", actualizar_graficos_seleccionado)
            
            return notebook
            
        except Exception as e:
            print(f"Error creando panel de gráficos: {e}")
            return None