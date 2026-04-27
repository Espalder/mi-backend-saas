# generador_pdf.py
"""
Generador de PDFs para reportes del sistema
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class GeneradorPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.configurar_estilos()
    
    def configurar_estilos(self):
        """Configurar estilos personalizados para los PDFs"""
        # Estilo para títulos
        self.styles.add(ParagraphStyle(
            name='TituloReporte',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkgreen
        ))
        
        # Estilo para texto normal
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        ))
        
        # Estilo para encabezados de tabla
        self.styles.add(ParagraphStyle(
            name='EncabezadoTabla',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.white,
            backColor=colors.darkblue
        ))

    def generar_reporte_inventario(self, datos_productos, nombre_archivo=None):
        """Generar reporte de inventario en PDF"""
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_inventario_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Título del reporte
        titulo = Paragraph("📦 REPORTE DE INVENTARIO", self.styles['TituloReporte'])
        story.append(titulo)
        story.append(Spacer(1, 12))
        
        # Información del reporte
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        info_reporte = Paragraph(f"<b>Fecha de generación:</b> {fecha}", self.styles['TextoNormal'])
        story.append(info_reporte)
        story.append(Spacer(1, 20))
        
        # Resumen estadístico
        total_productos = len(datos_productos)
        productos_activos = len([p for p in datos_productos if p.get('activo', 1) == 1])
        stock_bajo = len([p for p in datos_productos if p.get('stock', 0) <= p.get('stock_minimo', 5)])
        
        resumen_data = [
            ['Total de Productos', str(total_productos)],
            ['Productos Activos', str(productos_activos)],
            ['Productos con Stock Bajo', str(stock_bajo)]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ]))
        
        story.append(Paragraph("📊 RESUMEN ESTADÍSTICO", self.styles['Subtitulo']))
        story.append(resumen_table)
        story.append(Spacer(1, 20))
        
        # Tabla de productos
        if datos_productos:
            story.append(Paragraph("📋 DETALLE DE PRODUCTOS", self.styles['Subtitulo']))
            
            # Preparar datos para la tabla
            tabla_data = [['Código', 'Nombre', 'Precio', 'Stock', 'Stock Mín.', 'Estado']]
            
            for producto in datos_productos:
                estado = "Activo" if producto.get('activo', 1) == 1 else "Inactivo"
                stock = producto.get('stock', 0)
                stock_min = producto.get('stock_minimo', 5)
                
                # Color de fila según stock
                if stock <= stock_min:
                    estado_stock = "⚠️ Bajo"
                elif stock == 0:
                    estado_stock = "❌ Sin Stock"
                else:
                    estado_stock = "✅ Normal"
                
                fila = [
                    producto.get('codigo', ''),
                    producto.get('nombre', ''),
                    f"${producto.get('precio_venta', 0):.2f}",
                    str(stock),
                    str(stock_min),
                    estado_stock
                ]
                tabla_data.append(fila)
            
            # Crear tabla
            tabla = Table(tabla_data, colWidths=[1*inch, 2.5*inch, 1*inch, 0.8*inch, 0.8*inch, 1*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(tabla)
        else:
            story.append(Paragraph("No hay productos para mostrar.", self.styles['TextoNormal']))
        
        # Pie de página
        story.append(Spacer(1, 30))
        pie_pagina = Paragraph("Sistema de Gestión Empresarial - Reporte generado automáticamente", 
                              self.styles['TextoNormal'])
        story.append(pie_pagina)
        
        # Generar PDF
        doc.build(story)
        return nombre_archivo

    def generar_reporte_ventas(self, datos_ventas, nombre_archivo=None):
        """Generar reporte de ventas en PDF"""
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_ventas_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Título del reporte
        titulo = Paragraph("💰 REPORTE DE VENTAS", self.styles['TituloReporte'])
        story.append(titulo)
        story.append(Spacer(1, 12))
        
        # Información del reporte
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        info_reporte = Paragraph(f"<b>Fecha de generación:</b> {fecha}", self.styles['TextoNormal'])
        story.append(info_reporte)
        story.append(Spacer(1, 20))
        
        # Resumen estadístico
        total_ventas = len(datos_ventas)
        ventas_completadas = len([v for v in datos_ventas if v.get('estado') == 'completada'])
        total_ingresos = sum([v.get('total', 0) for v in datos_ventas if v.get('estado') == 'completada'])
        
        resumen_data = [
            ['Total de Ventas', str(total_ventas)],
            ['Ventas Completadas', str(ventas_completadas)],
            ['Total de Ingresos', f"${total_ingresos:.2f}"]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ]))
        
        story.append(Paragraph("📊 RESUMEN ESTADÍSTICO", self.styles['Subtitulo']))
        story.append(resumen_table)
        story.append(Spacer(1, 20))
        
        # Tabla de ventas
        if datos_ventas:
            story.append(Paragraph("📋 DETALLE DE VENTAS", self.styles['Subtitulo']))
            
            # Preparar datos para la tabla
            tabla_data = [['ID', 'Fecha', 'Cliente', 'Total', 'Estado']]
            
            for venta in datos_ventas:
                fecha_venta = venta.get('fecha', '')
                if fecha_venta:
                    try:
                        fecha_obj = datetime.strptime(fecha_venta, '%Y-%m-%d %H:%M:%S')
                        fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
                    except:
                        fecha_formateada = fecha_venta
                else:
                    fecha_formateada = 'N/A'
                
                estado = venta.get('estado', 'completada')
                estado_icono = "✅" if estado == 'completada' else "⏳" if estado == 'pendiente' else "❌"
                
                fila = [
                    str(venta.get('id', '')),
                    fecha_formateada,
                    venta.get('cliente_nombre', 'Cliente General'),
                    f"S/{venta.get('total', 0):.2f}",
                    f"{estado_icono} {estado.title()}"
                ]
                tabla_data.append(fila)
            
            # Crear tabla
            tabla = Table(tabla_data, colWidths=[0.8*inch, 1.2*inch, 2*inch, 1*inch, 1.5*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(tabla)
        else:
            story.append(Paragraph("No hay ventas para mostrar.", self.styles['TextoNormal']))
        
        # Pie de página
        story.append(Spacer(1, 30))
        pie_pagina = Paragraph("Sistema de Gestión Empresarial - Reporte generado automáticamente", 
                              self.styles['TextoNormal'])
        story.append(pie_pagina)
        
        # Generar PDF
        doc.build(story)
        return nombre_archivo

    def generar_reporte_completo(self, datos_inventario, datos_ventas, nombre_archivo=None):
        """Generar reporte completo del sistema"""
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_completo_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Título del reporte
        titulo = Paragraph("📊 REPORTE COMPLETO DEL SISTEMA", self.styles['TituloReporte'])
        story.append(titulo)
        story.append(Spacer(1, 12))
        
        # Información del reporte
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        info_reporte = Paragraph(f"<b>Fecha de generación:</b> {fecha}", self.styles['TextoNormal'])
        story.append(info_reporte)
        story.append(Spacer(1, 20))
        
        # Resumen general
        total_productos = len(datos_inventario)
        total_ventas = len(datos_ventas)
        ingresos_totales = sum([v.get('total', 0) for v in datos_ventas if v.get('estado') == 'completada'])
        
        resumen_general = [
            ['MÉTRICA', 'VALOR'],
            ['Total de Productos', str(total_productos)],
            ['Total de Ventas', str(total_ventas)],
            ['Ingresos Totales', f"${ingresos_totales:.2f}"]
        ]
        
        resumen_table = Table(resumen_general, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(Paragraph("📈 RESUMEN GENERAL", self.styles['Subtitulo']))
        story.append(resumen_table)
        story.append(PageBreak())
        
        # Agregar reporte de inventario
        story.append(Paragraph("📦 INVENTARIO", self.styles['Subtitulo']))
        if datos_inventario:
            tabla_inv_data = [['Código', 'Nombre', 'Precio', 'Stock']]
            for producto in datos_inventario[:10]:  # Mostrar solo los primeros 10
                tabla_inv_data.append([
                    producto.get('codigo', ''),
                    producto.get('nombre', ''),
                    f"${producto.get('precio_venta', 0):.2f}",
                    str(producto.get('stock', 0))
                ])
            
            tabla_inv = Table(tabla_inv_data, colWidths=[1.5*inch, 3*inch, 1*inch, 1*inch])
            tabla_inv.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(tabla_inv)
        
        story.append(PageBreak())
        
        # Agregar reporte de ventas
        story.append(Paragraph("💰 VENTAS", self.styles['Subtitulo']))
        if datos_ventas:
            tabla_ventas_data = [['ID', 'Fecha', 'Total', 'Estado']]
            for venta in datos_ventas[:10]:  # Mostrar solo las primeras 10
                fecha_venta = venta.get('fecha', '')
                if fecha_venta:
                    try:
                        fecha_obj = datetime.strptime(fecha_venta, '%Y-%m-%d %H:%M:%S')
                        fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
                    except:
                        fecha_formateada = fecha_venta
                else:
                    fecha_formateada = 'N/A'
                
                tabla_ventas_data.append([
                    str(venta.get('id', '')),
                    fecha_formateada,
                    f"S/{venta.get('total', 0):.2f}",
                    venta.get('estado', 'completada').title()
                ])
            
            tabla_ventas = Table(tabla_ventas_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            tabla_ventas.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(tabla_ventas)
        
        # Pie de página
        story.append(Spacer(1, 30))
        pie_pagina = Paragraph("Sistema de Gestión Empresarial - Reporte completo generado automáticamente", 
                              self.styles['TextoNormal'])
        story.append(pie_pagina)
        
        # Generar PDF
        doc.build(story)
        return nombre_archivo