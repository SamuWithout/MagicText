from tkinter import filedialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas

#Funcion para el encabezado de la pagina
def encabezado_apa(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    # Posiciona el número de página en la esquina superior derecha
    page_num = str(canvas.getPageNumber())
    canvas.drawRightString(doc.width + doc.leftMargin, doc.height + 0.75 * inch, page_num)
    canvas.restoreState()

#--------------------------Guardado del archivo-----------------------------------
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
        
#------------------------ESTILOS------------------------------------------
#Estilos de la portada--------------------------
        apa_cover_title_style = ParagraphStyle(
            'APA_Cover_Title', parent=styles['h1'], fontName='Times-Bold',
            fontSize=14, leading=28, alignment=TA_CENTER, spaceAfter=12
        )
        apa_cover_info_style = ParagraphStyle(
            'APA_Cover_Info', parent=styles['Normal'], fontName='Times-Roman',
            fontSize=12, leading=24, alignment=TA_CENTER, spaceAfter=6
        )
        
#Estilos para el cuerpo del documento (Parrafos y Portada)--------
        apa_paragraph_style = ParagraphStyle(
            'APA_Paragraph', parent=styles['Normal'], fontName='Times-Roman',
            fontSize=12, leading=24, firstLineIndent=0.5 * inch, alignment=TA_LEFT
        )
        apa_title_style = ParagraphStyle(
            'APA_Title_1', parent=styles['h1'], fontName='Times-Bold',
            fontSize=12, leading=24, alignment=TA_CENTER, spaceAfter=12
        )
        apa_reference_style = ParagraphStyle(
            'APA_Reference', parent=styles['Normal'], fontName='Times-Roman',
            fontSize=12, leading=24, leftIndent=0.5 * inch,
            firstLineIndent=-0.5 * inch, alignment=TA_LEFT
        )

#-----------------------------LÓGICA DE PROCESAMIENTO--------------------------------
#-------------------------------AÑADIR LA PORTADA-------------------------------------
        if datos_portada and any(datos_portada.values()):
            # Agrega espacios para bajar el contenido en la página
            story.append(Spacer(1, 2 * inch))
    
            # Título
            if datos_portada.get('titulo'):
                story.append(Paragraph(datos_portada['titulo'], apa_cover_title_style))
                story.append(Spacer(1, 0.5 * inch)) # Espacio extra después del título
            
            # Autor
            if datos_portada.get('autor'):
                story.append(Paragraph(datos_portada['autor'], apa_cover_info_style))
            
            # Afiliación, Curso, Instructor, Fecha
            info_fields = ['afiliacion', 'curso', 'instructor', 'fecha']
            for field in info_fields:
                if datos_portada.get(field):
                    story.append(Paragraph(datos_portada[field], apa_cover_info_style))

            story.append(PageBreak()) # Termina la portada y pasa a la siguiente página

#-----------------------AÑADIR EL CUERPO DEL DOCUMENTO------------------------------------------
        for tipo, texto in contenido_cuerpo:
            if tipo == 'title':
                story.append(Paragraph(texto, apa_title_style))
            elif tipo == 'referencia':
                story.append(Paragraph(texto, apa_reference_style))
            elif tipo == 'paragraph':
                story.append(Paragraph(texto, apa_paragraph_style))
                
#----------------------------------Construir el PDF--------------------------------------------
        doc.build(story, onFirstPage=encabezado_apa, onLaterPages=encabezado_apa)
        messagebox.showinfo("Éxito", f"El archivo PDF ha sido guardado en:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")