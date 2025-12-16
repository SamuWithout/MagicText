from tkinter import filedialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas

def encabezado_apa(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    page_num = str(canvas.getPageNumber())
    page_height = doc.pagesize[1]
    y_position = page_height - (0.5 * inch)
    x_position = doc.width + doc.leftMargin
    canvas.drawRightString(x_position, y_position, page_num)
    canvas.restoreState()

def crear_documento_apa_reportlab(datos_portada, contenido_cuerpo):
    try:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Guardar documento APA como..."
        )
        if not filepath: return
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la ruta del archivo:\n{e}")
        return

    try:
        doc = SimpleDocTemplate(filepath,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos
        apa_cover_title_style = ParagraphStyle(
            'APA_Cover_Title', 
            parent=styles['h1'], 
            fontName='Times-Bold', 
            fontSize=14, 
            leading=28, 
            alignment=TA_CENTER, 
            spaceAfter=12)
        apa_cover_info_style = ParagraphStyle(
            'APA_Cover_Info', 
            parent=styles['Normal'], 
            fontName='Times-Roman', 
            fontSize=12, 
            leading=26, 
            alignment=TA_CENTER, 
            spaceAfter=6)
        apa_paragraph_style = ParagraphStyle(
            'APA_Paragraph', 
            parent=styles['Normal'], 
            fontName='Times-Roman', 
            fontSize=12, 
            leading=26, 
            firstLineIndent=0.5 * inch, 
            alignment=TA_LEFT)
        
        #Estilos de Titulos
        apa_title_1_style = ParagraphStyle(
            'APA_Title_1', 
            parent=styles['h1'], 
            fontName='Times-Bold', 
            fontSize=12, leading=24, 
            alignment=TA_CENTER, 
            spaceBefore=12, 
            spaceAfter=6)
        apa_title_2_style = ParagraphStyle(
            'APA_Title_2', 
            parent=styles['h2'], 
            fontName='Times-Bold', 
            fontSize=12, 
            leading=26, 
            alignment=TA_LEFT, 
            spaceBefore=12, 
            spaceAfter=6)
        apa_title_3_style = ParagraphStyle(
            'APA_Title_3', 
            parent=styles['h3'], 
            fontName='Times-BoldItalic', 
            fontSize=12, 
            leading=26, 
            alignment=TA_LEFT, 
            spaceBefore=12, 
            spaceAfter=6)
        apa_title_4_style = ParagraphStyle(
            'APA_Title_4', 
            parent=styles['Normal'], 
            fontName='Times-Bold', 
            fontSize=12, 
            leading=26, 
            firstLineIndent=0.5 * inch, 
            alignment=TA_LEFT, 
            spaceBefore=12, 
            spaceAfter=6)
        apa_title_5_style = ParagraphStyle(
            'APA_Title_5', 
            parent=styles['Normal'], 
            fontName='Times-BoldItalic', 
            fontSize=12, 
            leading=26, 
            firstLineIndent=0.5 * inch, 
            alignment=TA_LEFT, 
            spaceBefore=12, 
            spaceAfter=6)
        apa_reference_style = ParagraphStyle(
            'APA_Reference', 
            parent=styles['Normal'], 
            fontName='Times-Roman', 
            fontSize=12, 
            leading=26, 
            leftIndent=0.5 * inch, 
            firstLineIndent=-0.5 * inch, 
            alignment=TA_LEFT)

        # Añadir Portada
        if datos_portada and any(datos_portada.values()):
            story.append(Spacer(1, 2 * inch))
            if datos_portada.get('titulo'):
                story.append(Paragraph(datos_portada['titulo'], apa_cover_title_style))
                story.append(Spacer(1, 0.5 * inch))
            if datos_portada.get('autor'):
                story.append(Paragraph(datos_portada['autor'], apa_cover_info_style))
            info_fields = ['afiliacion', 'curso', 'instructor', 'fecha']
            for field in info_fields:
                if datos_portada.get(field):
                    story.append(Paragraph(datos_portada[field], apa_cover_info_style))
            story.append(PageBreak())

        # --- LÓGICA DE PROCESAMIENTO ---
        for tipo, texto in contenido_cuerpo:
            if tipo == 'title_level_1':
                story.append(Paragraph(texto, apa_title_1_style))
            elif tipo == 'title_level_2':
                story.append(Paragraph(texto, apa_title_2_style))
            elif tipo == 'title_level_3': 
                story.append(Paragraph(texto, apa_title_3_style))
            elif tipo == 'title_level_4': 
                story.append(Paragraph(texto + ".", apa_title_4_style))
            elif tipo == 'title_level_5': 
                story.append(Paragraph(texto + ".", apa_title_5_style))
            elif tipo == 'referencia':
                story.append(Paragraph(texto, apa_reference_style))
            elif tipo == 'paragraph':
                story.append(Paragraph(texto, apa_paragraph_style))
            elif tipo == 'pagebreak':
                story.append(PageBreak())
                
        doc.build(story, onFirstPage=encabezado_apa, onLaterPages=encabezado_apa)
        messagebox.showinfo("Éxito", f"El archivo PDF ha sido guardado en:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")