import os
import json
from datetime import datetime
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import tempfile

class GeneradorPDF:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.configuracion = self.cargar_configuracion()
        
    def cargar_configuracion(self):
        """Cargar configuración de la empresa"""
        config_default = {
            'nombre_empresa': 'Sistema de Gestión Empresarial',
            'direccion_empresa': 'Dirección no especificada',
            'telefono_empresa': 'Teléfono no especificado'
        }
        
        try:
            if os.path.exists('configuracion.json'):
                with open('configuracion.json', 'r', encoding='utf-8') as f:
                    config_guardada = json.load(f)
                    config_default.update(config_guardada)
        except Exception:
            pass
            
        return config_default

    def crear_estilos(self):
        """Crear estilos personalizados para el PDF"""
        styles = getSampleStyleSheet()
        
        # Estilo para el título principal
        titulo_style = ParagraphStyle(
            'TituloEmpresa',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1976D2')
        )
        
        # Estilo para subtítulos
        subtitulo_style = ParagraphStyle(
            'Subtitulo',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#2196F3')
        )
        
        # Estilo para información de empresa
        info_empresa_style = ParagraphStyle(
            'InfoEmpresa',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        # Estilo para texto normal
        normal_style = ParagraphStyle(
            'NormalCustom',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        return {
            'titulo': titulo_style,
            'subtitulo': subtitulo_style,
            'info_empresa': info_empresa_style,
            'normal': normal_style,
            'heading': styles['Heading2']
        }

    def generar_reporte_ventas(self, fecha_inicio, fecha_fin, incluir_graficos=True):
        """Generar reporte de ventas en PDF"""
        try:
            # Solicitar ubicación de guardado
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Guardar reporte de ventas",
                initialname=f"reporte_ventas_{fecha_inicio}_{fecha_fin}.pdf"
            )
            
            if not filename:
                return False
            
            # Crear documento PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            styles = self.crear_estilos()
            
            # Encabezado de empresa
            story.append(Paragraph(self.configuracion['nombre_empresa'], styles['titulo']))
            story.append(Paragraph(self.configuracion['direccion_empresa'], styles['info_empresa']))
            story.append(Paragraph(f"Tel: {self.configuracion['telefono_empresa']}", styles['info_empresa']))
            story.append(Spacer(1, 20))
            
            # Título del reporte
            story.append(Paragraph("REPORTE DE VENTAS", styles['heading']))
            story.append(Paragraph(f"Período: {fecha_inicio} al {fecha_fin}", styles['normal']))
            story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['normal']))
            story.append(Spacer(1, 20))
            
            # Obtener datos de ventas
            ventas_data = self.obtener_datos_ventas(fecha_inicio, fecha_fin)
            productos_data = self.obtener_productos_vendidos(fecha_inicio, fecha_fin)
            
            # Resumen ejecutivo
            total_ventas = sum([float(v[3]) for v in ventas_data])
            story.append(Paragraph("RESUMEN EJECUTIVO", styles['subtitulo']))
            
            resumen_data = [
                ['Concepto', 'Valor'],
                ['Total de ventas', f'{len(ventas_data)} ventas'],
                ['Monto total facturado', f'S/ {total_ventas:,.2f}'],
                ['Promedio por venta', f'S/ {(total_ventas/len(ventas_data) if len(ventas_data) > 0 else 0):,.2f}'],
                ['Productos únicos vendidos', f'{len(productos_data)} productos']
            ]
            
            resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
            resumen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(resumen_table)
            story.append(Spacer(1, 20))
            
            # Detalle de ventas
            if ventas_data:
                story.append(Paragraph("DETALLE DE VENTAS", styles['subtitulo']))
                
                # Preparar datos de tabla
                ventas_table_data = [['Fecha', 'Cliente', 'Total']]
                for venta in ventas_data[:20]:  # Mostrar máximo 20 ventas
                    fecha_formateada = str(venta[1])[:16] if isinstance(venta[1], str) else str(venta[1])
                    cliente = venta[2] if len(venta[2]) <= 30 else venta[2][:30] + "..."
                    ventas_table_data.append([fecha_formateada, cliente, f'S/ {float(venta[3]):,.2f}'])
                
                ventas_table = Table(ventas_table_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
                ventas_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('ALTERNATE', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                story.append(ventas_table)
                story.append(Spacer(1, 20))
            
            # Productos más vendidos
            if productos_data:
                story.append(Paragraph("PRODUCTOS MÁS VENDIDOS", styles['subtitulo']))
                
                productos_table_data = [['Producto', 'Cantidad', 'Total']]
                for producto in productos_data[:15]:  # Top 15 productos
                    nombre = producto[0] if len(producto[0]) <= 35 else producto[0][:35] + "..."
                    productos_table_data.append([
                        nombre, 
                        str(producto[1]), 
                        f'S/ {float(producto[2]):,.2f}'
                    ])
                
                productos_table = Table(productos_table_data, colWidths=[3*inch, 1*inch, 1.5*inch])
                productos_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('ALTERNATE', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                story.append(productos_table)
                story.append(Spacer(1, 20))
            
            # Agregar gráficos si se solicita
            if incluir_graficos and productos_data:
                grafico_path = self.crear_grafico_para_pdf(productos_data)
                if grafico_path:
                    story.append(Paragraph("GRÁFICO DE PRODUCTOS MÁS VENDIDOS", styles['subtitulo']))
                    img = Image(grafico_path, width=5*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 20))
                    # Limpiar archivo temporal
                    try:
                        os.remove(grafico_path)
                    except:
                        pass
            
            # Pie de página
            story.append(Spacer(1, 30))
            story.append(Paragraph("Este reporte ha sido generado automáticamente por el Sistema de Gestión Empresarial", 
                                 styles['info_empresa']))
            
            # Construir PDF
            doc.build(story)
            
            messagebox.showinfo("PDF Generado", f"Reporte guardado exitosamente en:\n{filename}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
            return False

    def generar_reporte_inventario(self):
        """Generar reporte de inventario en PDF"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Guardar reporte de inventario",
                initialname=f"reporte_inventario_{datetime.now().strftime('%Y%m%d')}.pdf"
            )
            
            if not filename:
                return False
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            styles = self.crear_estilos()
            
            # Encabezado
            story.append(Paragraph(self.configuracion['nombre_empresa'], styles['titulo']))
            story.append(Paragraph(self.configuracion['direccion_empresa'], styles['info_empresa']))
            story.append(Paragraph(f"Tel: {self.configuracion['telefono_empresa']}", styles['info_empresa']))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("REPORTE DE INVENTARIO", styles['heading']))
            story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['normal']))
            story.append(Spacer(1, 20))
            
            # Obtener datos de inventario
            inventario_data = self.obtener_datos_inventario()
            
            # Estadísticas generales
            total_productos = len(inventario_data)
            valor_total = sum([float(p[4]) * int(p[5]) for p in inventario_data])
            productos_bajo_stock = len([p for p in inventario_data if int(p[5]) <= 5])
            
            story.append(Paragraph("ESTADÍSTICAS GENERALES", styles['subtitulo']))
            
            stats_data = [
                ['Concepto', 'Valor'],
                ['Total de productos', f'{total_productos} productos'],
                ['Valor total del inventario', f'S/ {valor_total:,.2f}'],
                ['Productos con stock bajo (≤5)', f'{productos_bajo_stock} productos'],
                ['Valor promedio por producto', f'S/ {(valor_total/total_productos if total_productos > 0 else 0):,.2f}']
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Lista de productos
            if inventario_data:
                story.append(Paragraph("DETALLE DE PRODUCTOS", styles['subtitulo']))
                
                productos_table_data = [['Código', 'Nombre', 'Precio', 'Stock', 'Valor Total']]
                for producto in inventario_data:
                    codigo = producto[1][:10] if len(producto[1]) > 10 else producto[1]
                    nombre = producto[2][:25] if len(producto[2]) > 25 else producto[2]
                    precio = float(producto[4])
                    stock = int(producto[5])
                    valor_total_prod = precio * stock
                    
                    productos_table_data.append([
                        codigo,
                        nombre,
                        f'S/ {precio:.2f}',
                        str(stock),
                        f'S/ {valor_total_prod:.2f}'
                    ])
                
                productos_table = Table(productos_table_data, colWidths=[1*inch, 2*inch, 1*inch, 0.8*inch, 1.2*inch])
                productos_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('ALTERNATE', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),
                ]))
                story.append(productos_table)
            
            # Construir PDF
            doc.build(story)
            messagebox.showinfo("PDF Generado", f"Reporte de inventario guardado en:\n{filename}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF de inventario: {str(e)}")
            return False

    def crear_grafico_para_pdf(self, datos_productos, limite=10):
        """Crear gráfico temporal para incluir en PDF"""
        try:
            # Tomar los top productos
            top_productos = datos_productos[:limite]
            
            nombres = [p[0][:15] + '...' if len(p[0]) > 15 else p[0] for p in top_productos]
            cantidades = [int(p[1]) for p in top_productos]
            
            # Crear gráfico
            plt.figure(figsize=(10, 6))
            colores = plt.cm.Set3(np.linspace(0, 1, len(nombres)))
            
            wedges, texts, autotexts = plt.pie(cantidades, labels=nombres, autopct='%1.1f%%', 
                                             colors=colores, startangle=90)
            
            plt.title('Top Productos Más Vendidos', fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            # Guardar en archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            plt.savefig(temp_file.name, dpi=150, bbox_inches='tight')
            plt.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"Error al crear gráfico: {e}")
            return None

    def obtener_datos_ventas(self, fecha_inicio, fecha_fin):
        """Obtener datos de ventas para el reporte"""
        try:
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query = """
                SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total 
                FROM ventas v 
                LEFT JOIN clientes c ON v.cliente_id = c.id 
                WHERE date(v.fecha) BETWEEN ? AND ? AND v.estado = 'completada' 
                ORDER BY v.fecha DESC
                """
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
            else:
                query = """
                SELECT v.id, v.fecha, COALESCE(c.nombre, 'Consumidor Final') as cliente, v.total 
                FROM ventas v 
                LEFT JOIN clientes c ON v.cliente_id = c.id 
                WHERE DATE(v.fecha) BETWEEN %s AND %s AND v.estado = 'completada' 
                ORDER BY v.fecha DESC
                """
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
            
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener datos de ventas: {e}")
            return []

    def obtener_productos_vendidos(self, fecha_inicio, fecha_fin):
        """Obtener productos más vendidos para el reporte"""
        try:
            if self.conn.__class__.__module__.startswith('sqlite3'):
                query = """
                SELECT p.nombre, SUM(dv.cantidad) as cantidad, SUM(dv.subtotal) as total 
                FROM detalle_ventas dv 
                JOIN productos p ON dv.producto_id = p.id 
                JOIN ventas v ON dv.venta_id = v.id 
                WHERE date(v.fecha) BETWEEN ? AND ? AND v.estado = 'completada' 
                GROUP BY p.nombre 
                ORDER BY total DESC
                """
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
            else:
                query = """
                SELECT p.nombre, SUM(dv.cantidad) as cantidad, SUM(dv.subtotal) as total 
                FROM detalle_ventas dv 
                JOIN productos p ON dv.producto_id = p.id 
                JOIN ventas v ON dv.venta_id = v.id 
                WHERE DATE(v.fecha) BETWEEN %s AND %s AND v.estado = 'completada' 
                GROUP BY p.nombre 
                ORDER BY total DESC
                """
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
            
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos vendidos: {e}")
            return []

    def obtener_datos_inventario(self):
        """Obtener datos del inventario"""
        try:
            query = """
            SELECT id, codigo, nombre, descripcion, precio, stock 
            FROM productos 
            WHERE activo = 1 
            ORDER BY stock DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener datos de inventario: {e}")
            return []