from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class GeneradorPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1976D2')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#2196F3')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            alignment=TA_LEFT
        ))

    def crear_header_footer(self, canvas_obj, doc):
        """Crea encabezado y pie de página"""
        canvas_obj.saveState()
        
        # Header
        canvas_obj.setFont('Helvetica-Bold', 12)
        canvas_obj.setFillColor(colors.HexColor('#1976D2'))
        canvas_obj.drawString(50, A4[1] - 50, "Sistema de Gestión Empresarial")
        
        # Footer
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.black)
        canvas_obj.drawRightString(A4[0] - 50, 30, 
                                   f"Página {doc.page} - Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        canvas_obj.restoreState()

    def generar_reporte_ventas(self, datos_ventas, productos_vendidos, fecha_inicio, fecha_fin, 
                              nombre_archivo=None, mostrar_graficos=False, datos_graficos=None):
        """Genera un reporte de ventas en PDF"""
        
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_ventas_{timestamp}.pdf"
        
        # Crear el documento
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Título principal
        titulo = f"REPORTE DE VENTAS<br/>Del {fecha_inicio} al {fecha_fin}"
        story.append(Paragraph(titulo, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Resumen ejecutivo
        total_ventas = sum([float(venta[3]) for venta in datos_ventas])
        story.append(Paragraph("RESUMEN EJECUTIVO", self.styles['CustomSubtitle']))
        
        resumen_data = [
            ['Métrica', 'Valor'],
            ['Total de Ventas', f'{len(datos_ventas)} ventas'],
            ['Ingresos Totales', f'S/ {total_ventas:.2f}'],
            ['Promedio por Venta', f'S/ {total_ventas/len(datos_ventas):.2f}' if datos_ventas else 'S/ 0.00'],
            ['Período', f'{fecha_inicio} a {fecha_fin}']
        ]
        
        resumen_table = Table(resumen_data)
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(resumen_table)
        story.append(Spacer(1, 30))
        
        # Detalle de ventas
        story.append(Paragraph("DETALLE DE VENTAS", self.styles['CustomSubtitle']))
        
        if datos_ventas:
            ventas_data = [['ID', 'Fecha', 'Cliente', 'Total']]
            for venta in datos_ventas:
                fecha_formateada = venta[1][:16] if isinstance(venta[1], str) else str(venta[1])
                ventas_data.append([
                    str(venta[0]),
                    fecha_formateada,
                    venta[2] if len(venta[2]) < 25 else venta[2][:22] + "...",
                    f'S/ {float(venta[3]):.2f}'
                ])
            
            ventas_table = Table(ventas_data)
            ventas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (3, 1), (3, -1), 'RIGHT')  # Alinear totales a la derecha
            ]))
            
            story.append(ventas_table)
        else:
            story.append(Paragraph("No se encontraron ventas en el período especificado.", self.styles['CustomBody']))
        
        story.append(Spacer(1, 30))
        
        # Productos más vendidos
        story.append(Paragraph("PRODUCTOS MÁS VENDIDOS", self.styles['CustomSubtitle']))
        
        if productos_vendidos:
            productos_data = [['Producto', 'Cantidad', 'Total Vendido']]
            for producto in productos_vendidos:
                productos_data.append([
                    producto[0] if len(producto[0]) < 30 else producto[0][:27] + "...",
                    str(producto[1]),
                    f'S/ {float(producto[2]):.2f}'
                ])
            
            productos_table = Table(productos_data)
            productos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (2, 1), (2, -1), 'RIGHT')  # Alinear totales a la derecha
            ]))
            
            story.append(productos_table)
        else:
            story.append(Paragraph("No se encontraron productos vendidos en el período.", self.styles['CustomBody']))
        
        # Generar el PDF
        doc.build(story, onFirstPage=self.crear_header_footer, onLaterPages=self.crear_header_footer)
        
        return os.path.abspath(nombre_archivo)

    def generar_reporte_inventario(self, productos, nombre_archivo=None):
        """Genera un reporte de inventario en PDF"""
        
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_inventario_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Título
        titulo = "REPORTE DE INVENTARIO"
        story.append(Paragraph(titulo, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Estadísticas generales
        total_productos = len(productos)
        productos_activos = len([p for p in productos if p[6] == 1])  # Asumiendo que activo es columna 6
        bajo_stock = len([p for p in productos if p[5] <= 5])  # Stock <= 5
        
        stats_data = [
            ['Estadística', 'Valor'],
            ['Total de Productos', str(total_productos)],
            ['Productos Activos', str(productos_activos)],
            ['Productos Bajo Stock', str(bajo_stock)],
            ['Fecha de Reporte', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ]
        
        stats_table = Table(stats_data)
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 30))
        
        # Detalle de productos
        story.append(Paragraph("DETALLE DE PRODUCTOS", self.styles['CustomSubtitle']))
        
        if productos:
            productos_data = [['Código', 'Nombre', 'Precio', 'Stock', 'Estado']]
            for producto in productos:
                productos_data.append([
                    producto[1],  # código
                    producto[2] if len(producto[2]) < 25 else producto[2][:22] + "...",  # nombre
                    f'S/ {float(producto[4]):.2f}',  # precio
                    str(producto[5]),  # stock
                    'Activo' if producto[6] == 1 else 'Inactivo'  # estado
                ])
            
            productos_table = Table(productos_data)
            productos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(productos_table)
        
        doc.build(story, onFirstPage=self.crear_header_footer, onLaterPages=self.crear_header_footer)
        
        return os.path.abspath(nombre_archivo)