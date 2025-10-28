import tkinter as tk
from tkinter import scrolledtext, messagebox
from pdfGenerator import crear_documento_apa_reportlab # Modificaremos esta función después

def make_line_title():
    
    try:
        # Posición del cursor, 'linestart' es el inicio de esa línea
        line_start = texto_usuario.index("insert linestart")
        line_end = texto_usuario.index("insert lineend")
        
        # Aplicamos la etiqueta 'title1' a toda la línea para hacerlo titulo
        texto_usuario.tag_add("title1", line_start, line_end)
        
    except tk.TclError:
        # En caso de que no haya texto lo ignoramos de forma segura
        pass

def iniciar_generacion():

    contenido_estructurado = []
    num_lines = int(texto_usuario.index('end-1c').split('.')[0])

    for i in range(1, num_lines + 1):
        line_start = f"{i}.0"
        line_end = f"{i}.end"
        texto_linea = texto_usuario.get(line_start, line_end).strip()
        
        if not texto_linea:
            continue
            
        # Obtenemos las etiquetas aplicadas al primer carácter de la línea
        tags_en_linea = texto_usuario.tag_names(line_start)
        
        if "title1" in tags_en_linea:
            contenido_estructurado.append(('title', texto_linea))
        else:
            contenido_estructurado.append(('paragraph', texto_linea))

    if not contenido_estructurado:
        messagebox.showwarning("Advertencia", "El campo de texto está vacío.")
        return
        
    crear_documento_apa_reportlab(contenido_estructurado)

# --- Creación de la ventana principal ---
ventana = tk.Tk()
ventana.title("MagicText")
ventana.geometry("800x600")

instrucciones = tk.Label(ventana, text="Escribe y formatea tu documento:", font=("Arial", 14))
instrucciones.pack(pady=10)

# --- Panel de botones de formato ---
panel_botones = tk.Frame(ventana)
panel_botones.pack(fill='x', padx=20)

boton_titulo = tk.Button(panel_botones, text="Convertir Línea en Título", command=make_line_title)
boton_titulo.pack(side='left')

# --- Widget de texto y configuración de la etiqueta visual ---
texto_usuario = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=25, font=("Times New Roman", 12))
texto_usuario.pack(pady=10, padx=20, expand=True, fill='both')

# AQUÍ LA MAGIA: Definimos cómo se verá el texto con la etiqueta 'title1'
texto_usuario.tag_configure("title1", font=("Times New Roman", 12, "bold"))

# --- Botón de generar PDF ---
boton_generar = tk.Button(ventana, text="Generar PDF", command=iniciar_generacion, font=("Arial", 12, "bold"), bg="#00529B", fg="white")
boton_generar.pack(pady=20)

if __name__ == "__main__":
    ventana.mainloop()