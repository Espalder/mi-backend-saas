import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from estilos import get_colores_tema, configurar_estilos
import numpy as np
from datetime import datetime, timedelta
import mysql.connector

class GraficosEstadisticas:
    def __init__(self, parent, conn, cursor, tema='claro'):
        self.parent = parent
        self.conn = conn
        self.cursor = cursor
        self.tema = tema
        self.colores = get_colores_tema(self.tema)
        self.figuras = {}
        self.canvas_widgets = {}
        self.auto_refresh_job = None
        self.setup_matplotlib_style()
        self.crear_interfaz()
        self.actualizar_todos_graficos()
        self.iniciar_auto_refresh()
    
    def setup_matplotlib_style(self):
        """Configurar el estilo de matplotlib según el tema"""
        plt.style.use('default')
        if self.tema == 'oscuro':
            plt.rcParams.update({
                'figure.facecolor': '#23272e',
                'axes.facecolor': '#2c313a',
                'axes.edgecolor': '#e6e6e6',
                'axes.labelcolor': '#e6e6e6',
                'text.color': '#e6e6e6',
                'xtick.color': '#e6e6e6',
                'ytick.color': '#e6e6e6',
                'grid.color': '#404040'
            })
        else:
            plt.rcParams.update({
                'figure.facecolor': '#e6f3ff',
                'axes.facecolor': '#f8f9fa',
                'axes.edgecolor': '#1976D2',
                'axes.labelcolor': '#1976D2',
                'text.color': '#1976D2',
                'xtick.color': '#1976D2',
                'ytick.color': '#1976D2',
                'grid.color': '#cccccc'
            })

    def crear_interfaz(self):
        """Crear la interfaz de gráficos"""
        configurar_estilos(self.tema)
        c = self.colores
        
        # Frame principal
        main_frame = tk.Frame(self.parent, bg=c['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Frame de controles
        frame_controles = tk.LabelFrame(main_frame, text="📊 Controles de Gráficos", 
                                      font=('Segoe UI', 12, 'bold'), fg=c['fg'],
                                      bg=c['frame_bg'], relief='raised', bd=2, labelanchor='n')
        frame_controles.pack(fill='x', padx=10, pady=5)
        
        controles_inner = tk.Frame(frame_controles, bg=c['frame_bg'])
        controles_inner.pack(fill='x', padx=20, pady=10)
        
        # Botones de control
        btn_refresh = tk.Button(controles_inner, text="🔄 Actualizar Gráficos", 
                               command=self.actualizar_todos_graficos,
                               font=('Segoe UI', 10, 'bold'), bg=c['accent'], 
                               fg=c['button_fg'], relief='flat', bd=0, padx=20, pady=8)
        btn_refresh.pack(side='left', padx=5)
        
        # Toggle para auto-refresh
        self.auto_refresh_var = tk.BooleanVar(value=True)
        cb_auto = tk.Checkbutton(controles_inner, text="🔄 Actualización automática (30s)",
                                variable=self.auto_refresh_var, command=self.toggle_auto_refresh,
                                font=('Segoe UI', 10), bg=c['frame_bg'], fg=c['fg'],
                                selectcolor=c['entry_bg'])
        cb_auto.pack(side='left', padx=20)
        
        # Notebook para diferentes tipos de gráficos
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tab 1: Gráficos de Stock
        self.tab_stock = tk.Frame(self.notebook, bg=c['bg'])
        self.notebook.add(self.tab_stock, text="📦 Stock")
        
        # Tab 2: Gráficos de Ventas
        self.tab_ventas = tk.Frame(self.notebook, bg=c['bg'])
        self.notebook.add(self.tab_ventas, text="💰 Ventas")
        
        # Tab 3: Gráficos de Productos Más Vendidos
        self.tab_productos = tk.Frame(self.notebook, bg=c['bg'])
        self.notebook.add(self.tab_productos, text="🏆 Top Productos")
        
        # Tab 4: Gráficos de Categorías
        self.tab_categorias = tk.Frame(self.notebook, bg=c['bg'])
        self.notebook.add(self.tab_categorias, text="📊 Categorías")

    def crear_grafico_stock(self):
        """Crear gráfico de torta para productos por stock"""
        try:
            # Obtener datos de stock
            query = """
            SELECT nombre, stock 
            FROM productos 
            WHERE activo = 1 AND stock > 0
            ORDER BY stock DESC 
            LIMIT 10
            """
            self.cursor.execute(query)
            datos = self.cursor.fetchall()
            
            if not datos:
                self.mostrar_mensaje_vacio(self.tab_stock, "No hay datos de stock disponibles")
                return
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(8, 6))
            
            productos = [item[0][:15] + '...' if len(item[0]) > 15 else item[0] for item in datos]
            stocks = [item[1] for item in datos]
            
            # Colores para el gráfico
            colores_grafico = plt.cm.Set3(np.linspace(0, 1, len(productos)))
            
            # Crear gráfico de torta
            wedges, texts, autotexts = ax.pie(stocks, labels=productos, autopct='%1.1f%%',
                                            colors=colores_grafico, startangle=90)
            
            ax.set_title('Distribución de Stock por Producto', 
                        fontsize=14, fontweight='bold', pad=20)
            
            # Ajustar el diseño
            plt.tight_layout()
            
            # Guardar y mostrar
            self.mostrar_grafico(fig, self.tab_stock, 'stock')
            
        except Exception as e:
            self.mostrar_mensaje_error(self.tab_stock, f"Error al crear gráfico de stock: {str(e)}")

    def crear_grafico_ventas(self):
        """Crear gráfico de ventas por período"""
        try:
            # Obtener ventas de los últimos 7 días
            query = """
            SELECT DATE(fecha) as dia, SUM(total) as total_dia
            FROM ventas 
            WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) 
            AND estado = 'completada'
            GROUP BY DATE(fecha)
            ORDER BY dia DESC
            """
            self.cursor.execute(query)
            datos = self.cursor.fetchall()
            
            if not datos:
                self.mostrar_mensaje_vacio(self.tab_ventas, "No hay datos de ventas disponibles")
                return
            
            # Crear figura con dos subgráficos
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Gráfico 1: Ventas por día (barras)
            fechas = [str(item[0]) for item in datos]
            totales = [float(item[1]) for item in datos]
            
            ax1.bar(range(len(fechas)), totales, color='skyblue', alpha=0.7)
            ax1.set_title('Ventas por Día (Últimos 7 días)', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Fechas')
            ax1.set_ylabel('Total Ventas (S/)')
            ax1.set_xticks(range(len(fechas)))
            ax1.set_xticklabels(fechas, rotation=45, ha='right')
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Distribución de ventas (torta)
            if len(datos) > 1:
                colores_grafico = plt.cm.Pastel1(np.linspace(0, 1, len(fechas)))
                ax2.pie(totales, labels=fechas, autopct='%1.1f%%', 
                       colors=colores_grafico, startangle=90)
                ax2.set_title('Distribución de Ventas por Día', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            self.mostrar_grafico(fig, self.tab_ventas, 'ventas')
            
        except Exception as e:
            self.mostrar_mensaje_error(self.tab_ventas, f"Error al crear gráfico de ventas: {str(e)}")

    def crear_grafico_productos_vendidos(self):
        """Crear gráfico de productos más vendidos"""
        try:
            query = """
            SELECT p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.subtotal) as total_ingresos
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            JOIN ventas v ON dv.venta_id = v.id
            WHERE v.estado = 'completada'
            AND v.fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY p.id, p.nombre
            ORDER BY total_vendido DESC
            LIMIT 10
            """
            self.cursor.execute(query)
            datos = self.cursor.fetchall()
            
            if not datos:
                self.mostrar_mensaje_vacio(self.tab_productos, "No hay datos de productos vendidos")
                return
            
            # Crear figura con dos subgráficos
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            productos = [item[0][:12] + '...' if len(item[0]) > 12 else item[0] for item in datos]
            cantidades = [int(item[1]) for item in datos]
            ingresos = [float(item[2]) for item in datos]
            
            # Gráfico 1: Cantidades vendidas (torta)
            colores1 = plt.cm.Set2(np.linspace(0, 1, len(productos)))
            ax1.pie(cantidades, labels=productos, autopct='%1.0f', colors=colores1, startangle=90)
            ax1.set_title('Productos Más Vendidos (Cantidad)\nÚltimos 30 días', 
                         fontsize=12, fontweight='bold')
            
            # Gráfico 2: Ingresos por producto (torta)
            colores2 = plt.cm.Set1(np.linspace(0, 1, len(productos)))
            ax2.pie(ingresos, labels=productos, autopct='S/%.0f', colors=colores2, startangle=90)
            ax2.set_title('Ingresos por Producto\nÚltimos 30 días', 
                         fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            self.mostrar_grafico(fig, self.tab_productos, 'productos')
            
        except Exception as e:
            self.mostrar_mensaje_error(self.tab_productos, f"Error al crear gráfico de productos: {str(e)}")

    def crear_grafico_categorias(self):
        """Crear gráfico de ventas por categorías"""
        try:
            # Primero verificar si existe la columna categoria
            try:
                query_test = "SELECT categoria FROM productos LIMIT 1"
                self.cursor.execute(query_test)
                self.cursor.fetchall()
                
                # Si existe, usar la consulta con categorías
                query = """
                SELECT COALESCE(p.categoria, 'Sin Categoría') as categoria, 
                       COUNT(DISTINCT p.id) as productos_categoria,
                       SUM(dv.cantidad) as total_vendido,
                       SUM(dv.subtotal) as total_ingresos
                FROM productos p
                LEFT JOIN detalle_ventas dv ON p.id = dv.producto_id
                LEFT JOIN ventas v ON dv.venta_id = v.id AND v.estado = 'completada'
                WHERE p.activo = 1
                GROUP BY p.categoria
                ORDER BY total_ingresos DESC
                """
            except:
                # Si no existe la columna categoría, crear categorías básicas por precio
                query = """
                SELECT 
                    CASE 
                        WHEN p.precio <= 10 THEN 'Económico'
                        WHEN p.precio <= 50 THEN 'Medio'
                        ELSE 'Premium'
                    END as categoria,
                    COUNT(DISTINCT p.id) as productos_categoria,
                    COALESCE(SUM(dv.cantidad), 0) as total_vendido,
                    COALESCE(SUM(dv.subtotal), 0) as total_ingresos
                FROM productos p
                LEFT JOIN detalle_ventas dv ON p.id = dv.producto_id
                LEFT JOIN ventas v ON dv.venta_id = v.id AND v.estado = 'completada'
                WHERE p.activo = 1
                GROUP BY categoria
                ORDER BY total_ingresos DESC
                """
            
            self.cursor.execute(query)
            datos = self.cursor.fetchall()
            
            if not datos:
                self.mostrar_mensaje_vacio(self.tab_categorias, "No hay datos de categorías disponibles")
                return
            
            # Crear figura con dos subgráficos
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            categorias = [item[0] for item in datos]
            productos_count = [int(item[1]) for item in datos]
            ingresos = [float(item[3]) if item[3] else 0 for item in datos]
            
            # Gráfico 1: Cantidad de productos por categoría
            colores1 = plt.cm.Paired(np.linspace(0, 1, len(categorias)))
            wedges1, texts1, autotexts1 = ax1.pie(productos_count, labels=categorias, 
                                                 autopct='%1.0f', colors=colores1, startangle=90)
            ax1.set_title('Productos por Categoría', fontsize=12, fontweight='bold')
            
            # Gráfico 2: Ingresos por categoría
            if sum(ingresos) > 0:
                colores2 = plt.cm.Dark2(np.linspace(0, 1, len(categorias)))
                wedges2, texts2, autotexts2 = ax2.pie(ingresos, labels=categorias, 
                                                     autopct='S/%.0f', colors=colores2, startangle=90)
                ax2.set_title('Ingresos por Categoría', fontsize=12, fontweight='bold')
            else:
                ax2.text(0.5, 0.5, 'Sin datos de ingresos', ha='center', va='center', 
                        fontsize=14, transform=ax2.transAxes)
                ax2.set_title('Ingresos por Categoría', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            self.mostrar_grafico(fig, self.tab_categorias, 'categorias')
            
        except Exception as e:
            self.mostrar_mensaje_error(self.tab_categorias, f"Error al crear gráfico de categorías: {str(e)}")

    def mostrar_grafico(self, fig, parent, nombre):
        """Mostrar gráfico en el widget padre"""
        try:
            # Limpiar widget anterior si existe
            if nombre in self.canvas_widgets:
                self.canvas_widgets[nombre].destroy()
            
            # Crear canvas para matplotlib
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
            # Guardar referencias
            self.figuras[nombre] = fig
            self.canvas_widgets[nombre] = canvas.get_tk_widget()
            
        except Exception as e:
            self.mostrar_mensaje_error(parent, f"Error al mostrar gráfico: {str(e)}")

    def mostrar_mensaje_vacio(self, parent, mensaje):
        """Mostrar mensaje cuando no hay datos"""
        # Limpiar widgets anteriores
        for widget in parent.winfo_children():
            widget.destroy()
        
        label = tk.Label(parent, text=mensaje, font=('Segoe UI', 12), 
                        bg=self.colores['bg'], fg=self.colores['fg'])
        label.pack(expand=True)

    def mostrar_mensaje_error(self, parent, mensaje):
        """Mostrar mensaje de error"""
        # Limpiar widgets anteriores
        for widget in parent.winfo_children():
            widget.destroy()
        
        label = tk.Label(parent, text=mensaje, font=('Segoe UI', 12), 
                        bg=self.colores['bg'], fg=self.colores['error_fg'])
        label.pack(expand=True)

    def actualizar_todos_graficos(self):
        """Actualizar todos los gráficos"""
        try:
            self.crear_grafico_stock()
            self.crear_grafico_ventas()
            self.crear_grafico_productos_vendidos()
            self.crear_grafico_categorias()
            
            print("Gráficos actualizados correctamente")
            
        except Exception as e:
            print(f"Error al actualizar gráficos: {e}")

    def toggle_auto_refresh(self):
        """Activar/desactivar actualización automática"""
        if self.auto_refresh_var.get():
            self.iniciar_auto_refresh()
        else:
            self.detener_auto_refresh()

    def iniciar_auto_refresh(self):
        """Iniciar actualización automática cada 30 segundos"""
        self.detener_auto_refresh()  # Cancelar trabajo anterior si existe
        if self.auto_refresh_var.get():
            self.auto_refresh_job = self.parent.after(30000, self.auto_refresh_callback)

    def auto_refresh_callback(self):
        """Callback para actualización automática"""
        self.actualizar_todos_graficos()
        self.iniciar_auto_refresh()  # Programar próxima actualización

    def detener_auto_refresh(self):
        """Detener actualización automática"""
        if self.auto_refresh_job:
            self.parent.after_cancel(self.auto_refresh_job)
            self.auto_refresh_job = None

    def actualizar_tema(self, nuevo_tema):
        """Actualizar tema de los gráficos"""
        self.tema = nuevo_tema
        self.colores = get_colores_tema(self.tema)
        self.setup_matplotlib_style()
        
        # Actualizar widgets de la interfaz
        def actualizar_widget(widget):
            try:
                if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                    widget.configure(bg=self.colores['frame_bg'])
                    if isinstance(widget, tk.LabelFrame):
                        widget.configure(fg=self.colores['fg'])
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=self.colores['bg'], fg=self.colores['fg'])
                elif isinstance(widget, tk.Button):
                    widget.configure(bg=self.colores['accent'], fg=self.colores['button_fg'])
                elif isinstance(widget, tk.Checkbutton):
                    widget.configure(bg=self.colores['frame_bg'], fg=self.colores['fg'], 
                                   selectcolor=self.colores['entry_bg'])
                
                for child in widget.winfo_children():
                    actualizar_widget(child)
            except tk.TclError:
                pass
        
        actualizar_widget(self.parent)
        
        # Recrear gráficos con nuevo tema
        self.actualizar_todos_graficos()

    def destruir(self):
        """Limpiar recursos al cerrar"""
        self.detener_auto_refresh()
        for fig in self.figuras.values():
            plt.close(fig)
        self.figuras.clear()
        self.canvas_widgets.clear()