import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

# --- Importaciones de ReportLab ---
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Lógica de generación de PDF ---

def crear_documento_apa_reportlab(texto):
    """
    Crea un PDF con el formato APA.
    """
    
    #Preguntar al usuario la ubicación.
    try:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Guardar documento APA como..."
        )
        
        # Si el usuario presiona "Cancelar", filepath estará vacío.
        if not filepath:
            print("Guardado cancelado por el usuario.")
            return # Salimos de la función si no se eligió archivo
        
    #El usuario debe de elegir la ruta  para que se pueda realizar el guardado del archivo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la ruta del archivo:\n{e}")
        return

    #CREACIÓN DEL DOCUMENTO PDF
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
        
        # Definir y registrar la fuente Times New Roman (opcional pero recomendado)
        # Esto asegura que la fuente se use correctamente.
        # pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf')) # Asegúrate de tener el archivo .ttf
        # addMapping('Times-Roman', 0, 0, 'Times-Roman') # normal
        # addMapping('Times-Roman', 1, 0, 'Times-Bold') # bold
        
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
        #Informar al usuario de que el archivo se guardo con exito
        messagebox.showinfo("Éxito", f"El archivo PDF ha sido guardado en:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

# --- Interfaz Gráfica con Tkinter ---

def iniciar_generacion():
    contenido = texto_usuario.get("1.0", tk.END)
    if not contenido.strip():
        messagebox.showwarning("Advertencia", "El campo de texto está vacío.")
        return
    crear_documento_apa_reportlab(contenido)

ventana = tk.Tk()
ventana.title("Generador de Documentos Avanzado")
ventana.geometry("800x600")

instrucciones = tk.Label(ventana, text="Escribe el contenido de tu documento:", font=("Arial", 14))
instrucciones.pack(pady=10)

texto_usuario = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=25, font=("Times New Roman", 12))
texto_usuario.pack(pady=10, padx=20, expand=True, fill='both')

boton_generar = tk.Button(ventana, text="Generar PDF", command=iniciar_generacion, font=("Arial", 12, "bold"), bg="#00529B", fg="white")
boton_generar.pack(pady=20)

ventana.mainloop()