from tkinter import filedialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def crear_documento_apa_reportlab(contenido_estructurado):
    #ruta de guardado del archivio pdf
    try:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Guardar documento APA como..."
        )
        # En caso de que se presente algún error a la hora del guardado del archivo 
        if not filepath: return
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ob tener la ruta del archivo:\n{e}")
        return

    try:
        doc = SimpleDocTemplate(filepath,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        story = []
        styles = getSampleStyleSheet()
        
#------------------------ESTILOS PARA TITULOS Y PARRAFOS------------------------------------------
        # Estilo para el parrafo
        apa_paragraph_style = ParagraphStyle(
            'APA_Paragraph', 
            parent=styles['Normal'], 
            fontName='Times-Roman',
            fontSize=12, 
            leading=24, 
            firstLineIndent=0.5 * inch, 
            alignment=TA_LEFT #alineacion a la izquierda
            )
        # Estilo para el titulo
        apa_title_style = ParagraphStyle(
            'APA_Title_1', 
            parent=styles['h1'], 
            fontName='Times-Bold', #fuente en negrita para el titulo
            fontSize=12, 
            leading=24, 
            alignment=TA_CENTER, #alineacion al centro
            spaceAfter=12
            )
        # Estilo para la referencia
        apa_reference_style = ParagraphStyle(
            'APA_Reference',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            leading=24,
            leftIndent=0.5 * inch,      # Todo el párrafo se mueve a la derecha
            firstLineIndent=-0.5 * inch, # La primera línea vuelve a la izquierda
            alignment=TA_LEFT,
            )

#-----------------------------LÓGICA DE PROCESAMIENTO--------------------------------------------------------------
        # Diferenciar entre el titulo o parrafo
        for tipo, texto in contenido_estructurado:
            if tipo == 'title':
                p = Paragraph(texto, apa_title_style)
                story.append(p)
                
            elif tipo == 'referencia':
                p = Paragraph(texto, apa_reference_style)
                story.append(p)
                
            elif tipo == 'paragraph':
                p = Paragraph(texto, apa_paragraph_style)
                story.append(p)
                
        # Informar al usuario si el archivo fue guardado correctamente
        doc.build(story)
        messagebox.showinfo("Éxito", f"El archivo PDF ha sido guardado en:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")