from tkinter import filedialog, messagebox

# --- Importaciones de ReportLab ---
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT

# --- Generación de PDF ---

def crear_documento_apa_reportlab(texto):
    """
    Crea un PDF con el formato APA a partir de un texto dado.
    Solicita al usuario la ubicación para guardar el archivo.
    """
    
    # Preguntamos al usuario la ubicación.
    try:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Guardar documento APA como..."
        )
        
        # Si el usuario presiona "Cancelar", el filepath estará vacío.
        if not filepath:
            print("Guardado cancelado por el usuario.")
            return # Salimos de la función si no se eligió archivo
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la ruta del archivo:\n{e}")
        return

    # CREACIÓN DEL DOCUMENTO PDF
    try:
        # Configuración del documento con la ruta elegida por el usuario
        doc = SimpleDocTemplate(filepath,
                                rightMargin=inch,
                                leftMargin=inch,
                                topMargin=inch,
                                bottomMargin=inch)
        
        # Contenedor para los elementos del PDF (párrafos, imágenes, etc.)
        story = []
        styles = getSampleStyleSheet()
                
        # Crear un estilo APA personalizado
        apa_style = ParagraphStyle(
            'APA_Style',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            leading=24,  # Interlineado doble
            firstLineIndent=0.5 * inch, # Sangría de primera línea
            alignment=TA_LEFT,
        )

        # Procesar el texto del usuario
        parrafos = texto.split('\n')
        for p_texto in parrafos:
            if p_texto.strip():
                p = Paragraph(p_texto, apa_style)
                story.append(p)
        
        # Construir (generar) el PDF
        doc.build(story)
        
        # Informar al usuario de que el archivo se guardó con éxito
        messagebox.showinfo("Éxito", f"El archivo PDF ha sido guardado en:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")