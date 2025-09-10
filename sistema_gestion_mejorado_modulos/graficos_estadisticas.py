import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from collections import Counter

# Configurar matplotlib para mejor apariencia
plt.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

class GraficosEstadisticas:
    def __init__(self):
        self.colores_personalizados = [
            '#1976D2', '#2196F3', '#4CAF50', '#FF9800', '#F44336',
            '#9C27B0', '#607D8B', '#795548', '#E91E63', '#3F51B5'
        ]
        
    def crear_grafico_barras_ventas(self, parent, datos_ventas, titulo="Ventas por Período"):
        """Crea un gráfico de barras para las ventas"""
        
        # Limpiar el frame padre
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Preparar datos
        if not datos_ventas:
            label_no_datos = tk.Label(parent, text="No hay datos disponibles para mostrar", 
                                    font=('Segoe UI', 12), fg='gray')
            label_no_datos.pack(expand=True)
            return
        
        # Agrupar ventas por fecha
        ventas_por_fecha = {}
        for venta in datos_ventas:
            fecha = venta[1][:10] if isinstance(venta[1], str) else str(venta[1])[:10]  # Solo fecha, sin hora
            if fecha in ventas_por_fecha:
                ventas_por_fecha[fecha] += float(venta[3])
            else:
                ventas_por_fecha[fecha] = float(venta[3])
        
        # Preparar datos para el gráfico
        fechas = list(ventas_por_fecha.keys())
        valores = list(ventas_por_fecha.values())
        
        # Crear figura
        fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Crear gráfico de barras
        bars = ax.bar(fechas, valores, color=self.colores_personalizados[0], alpha=0.8)
        
        # Configurar el gráfico
        ax.set_title(titulo, fontsize=14, fontweight='bold', color='#1976D2')
        ax.set_xlabel('Fecha', fontsize=12, color='#333')
        ax.set_ylabel('Ventas (S/)', fontsize=12, color='#333')
        
        # Rotar etiquetas del eje x para mejor legibilidad
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Añadir valores en las barras
        for bar, valor in zip(bars, valores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(valores)*0.01,
                   f'S/ {valor:.0f}', ha='center', va='bottom', fontsize=9, color='#333')
        
        # Mejorar el diseño
        ax.grid(axis='y', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#ccc')
        ax.spines['bottom'].set_color('#ccc')
        
        # Ajustar layout
        fig.tight_layout()
        
        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        return canvas
    
    def crear_grafico_torta_productos(self, parent, productos_vendidos, titulo="Productos Más Vendidos"):
        """Crea un gráfico de torta para los productos más vendidos"""
        
        # Limpiar el frame padre
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Preparar datos
        if not productos_vendidos:
            label_no_datos = tk.Label(parent, text="No hay datos disponibles para mostrar", 
                                    font=('Segoe UI', 12), fg='gray')
            label_no_datos.pack(expand=True)
            return
        
        # Tomar solo los primeros 8 productos para mejor visualización
        productos_top = productos_vendidos[:8]
        nombres = [prod[0][:15] + "..." if len(prod[0]) > 15 else prod[0] for prod in productos_top]
        valores = [float(prod[2]) for prod in productos_top]
        
        # Crear figura
        fig = Figure(figsize=(10, 8), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Crear gráfico de torta
        wedges, texts, autotexts = ax.pie(valores, labels=nombres, autopct='%1.1f%%',
                                         colors=self.colores_personalizados[:len(nombres)],
                                         startangle=90, explode=[0.05]*len(nombres))
        
        # Configurar el gráfico
        ax.set_title(titulo, fontsize=14, fontweight='bold', color='#1976D2', pad=20)
        
        # Mejorar la apariencia del texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        for text in texts:
            text.set_fontsize(10)
            text.set_color('#333')
        
        # Añadir leyenda con valores
        leyenda_labels = [f"{nombres[i]}: S/ {valores[i]:.0f}" for i in range(len(nombres))]
        ax.legend(wedges, leyenda_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), 
                 fontsize=9)
        
        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        return canvas
    
    def crear_grafico_barras_inventario(self, parent, productos, titulo="Estado del Inventario"):
        """Crea un gráfico de barras para el estado del inventario"""
        
        # Limpiar el frame padre
        for widget in parent.winfo_children():
            widget.destroy()
        
        if not productos:
            label_no_datos = tk.Label(parent, text="No hay productos en el inventario", 
                                    font=('Segoe UI', 12), fg='gray')
            label_no_datos.pack(expand=True)
            return
        
        # Preparar datos
        nombres = [prod[2][:15] + "..." if len(prod[2]) > 15 else prod[2] for prod in productos[:10]]
        stock = [prod[5] for prod in productos[:10]]
        
        # Crear figura
        fig = Figure(figsize=(12, 6), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Crear colores basados en el stock (rojo para bajo stock)
        colores = []
        for s in stock:
            if s <= 5:
                colores.append('#F44336')  # Rojo para bajo stock
            elif s <= 15:
                colores.append('#FF9800')  # Naranja para stock medio
            else:
                colores.append('#4CAF50')  # Verde para stock alto
        
        # Crear gráfico de barras
        bars = ax.bar(nombres, stock, color=colores, alpha=0.8)
        
        # Configurar el gráfico
        ax.set_title(titulo, fontsize=14, fontweight='bold', color='#1976D2')
        ax.set_xlabel('Productos', fontsize=12, color='#333')
        ax.set_ylabel('Cantidad en Stock', fontsize=12, color='#333')
        
        # Rotar etiquetas del eje x
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Añadir valores en las barras
        for bar, valor in zip(bars, stock):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(stock)*0.01,
                   str(valor), ha='center', va='bottom', fontsize=9, color='#333')
        
        # Añadir línea de referencia para stock bajo
        ax.axhline(y=5, color='red', linestyle='--', alpha=0.7, label='Nivel de Alerta (5)')
        ax.legend()
        
        # Mejorar el diseño
        ax.grid(axis='y', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#ccc')
        ax.spines['bottom'].set_color('#ccc')
        
        # Ajustar layout
        fig.tight_layout()
        
        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        return canvas
    
    def crear_grafico_torta_categorias_ventas(self, parent, datos_ventas, titulo="Distribución de Ventas"):
        """Crea un gráfico de torta para categorías de ventas"""
        
        # Limpiar el frame padre
        for widget in parent.winfo_children():
            widget.destroy()
        
        if not datos_ventas:
            label_no_datos = tk.Label(parent, text="No hay datos disponibles para mostrar", 
                                    font=('Segoe UI', 12), fg='gray')
            label_no_datos.pack(expand=True)
            return
        
        # Categorizar las ventas por rangos de monto
        categorias = {"Ventas Pequeñas (< S/50)": 0, "Ventas Medianas (S/50-200)": 0, 
                     "Ventas Grandes (> S/200)": 0}
        
        for venta in datos_ventas:
            total = float(venta[3])
            if total < 50:
                categorias["Ventas Pequeñas (< S/50)"] += total
            elif total <= 200:
                categorias["Ventas Medianas (S/50-200)"] += total
            else:
                categorias["Ventas Grandes (> S/200)"] += total
        
        # Filtrar categorías con valores > 0
        categorias_filtradas = {k: v for k, v in categorias.items() if v > 0}
        
        if not categorias_filtradas:
            label_no_datos = tk.Label(parent, text="No hay datos suficientes para categorizar", 
                                    font=('Segoe UI', 12), fg='gray')
            label_no_datos.pack(expand=True)
            return
        
        nombres = list(categorias_filtradas.keys())
        valores = list(categorias_filtradas.values())
        
        # Crear figura
        fig = Figure(figsize=(10, 8), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Crear gráfico de torta
        wedges, texts, autotexts = ax.pie(valores, labels=nombres, autopct='%1.1f%%',
                                         colors=['#4CAF50', '#FF9800', '#F44336'][:len(nombres)],
                                         startangle=90, explode=[0.05]*len(nombres))
        
        # Configurar el gráfico
        ax.set_title(titulo, fontsize=14, fontweight='bold', color='#1976D2', pad=20)
        
        # Mejorar la apariencia del texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        for text in texts:
            text.set_fontsize(10)
            text.set_color('#333')
        
        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        return canvas