import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from pdfGenerator import crear_documento_apa_reportlab

#---------------------------LOGICA PARA NAVEGAR ENTRE PANTALLAS----------------------------
def mostrar_pantalla(pantalla_a_mostrar):
    
    for pantalla in contenedor_principal.winfo_children():
        pantalla.pack_forget() # Oculta la pantalla
    
    # Muestra la pantalla deseada
    pantalla_a_mostrar.pack(fill="both", expand=True)

# ---Funciones de la Pantalla del Editor---
# Para convertir una linea en titulo
def make_line_title():
    try:
        line_start = texto_usuario.index("insert linestart")
        line_end = texto_usuario.index("insert lineend")
        texto_usuario.tag_add("title1", line_start, line_end)
    except tk.TclError:
        pass
    
# Para convertir una linea en Referencia
def make_line_reference():
    try:
        line_start = texto_usuario.index("insert linestart")
        line_end = texto_usuario.index("insert lineend")
        texto_usuario.tag_add("referencia1", line_start, line_end)
    except tk.TclError:
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
            
        tags_en_linea = texto_usuario.tag_names(line_start)
        
        if "title1" in tags_en_linea:
            contenido_estructurado.append(('title', texto_linea))
            
        elif "referencia1" in tags_en_linea:
            contenido_estructurado.append(('referencia', texto_linea))
        else:
            contenido_estructurado.append(('paragraph', texto_linea))

    if not contenido_estructurado:
        messagebox.showwarning("Advertencia", "El campo de texto está vacío.")
        return
        
    crear_documento_apa_reportlab(contenido_estructurado)

# -----------------------------------VENTANA PRINCIPAL---------------------------------------
ventana = tk.Tk()
ventana.title("MagicText")
ventana.geometry("800x600")

# --- Contenedor Principal ---   .pack() muestra la pantalla _pack() la oculta
contenedor_principal = tk.Frame(ventana)
contenedor_principal.pack(fill="both", expand=True)

#-----------------------------------MENÚ PRINCIPAL--------------------------------------------
pantalla_menu = tk.Frame(contenedor_principal)

fuente_titulo = font.Font(family="Helvetica", size=36, weight="bold")

titulo_label = tk.Label(pantalla_menu, text="MagicText", font=fuente_titulo)
titulo_label.pack(pady=(80, 40))

# El comando del botón ahora llama a la función de navegación
boton_ir_a_apa = tk.Button(pantalla_menu, text="Documento APA", 
                           command=lambda: mostrar_pantalla(pantalla_editor),
                           font=("Arial", 14), 
                           width=20, 
                           height=2
                           )
boton_ir_a_apa.pack(pady=10)

boton_salir = tk.Button(
                pantalla_menu, 
                text="Salir", 
                command=ventana.quit,
                font=("Arial", 14), 
                width=20, height=2
                )
boton_salir.pack(pady=10)

#---------------------PANTALLA DE DOCUMENTO APA-------------------------------
pantalla_editor = tk.Frame(contenedor_principal)
instrucciones = tk.Label(pantalla_editor, text="Escribe y formatea tu documento:", font=("Arial", 14))
instrucciones.pack(pady=10)

panel_botones = tk.Frame(pantalla_editor)
panel_botones.pack(fill='x', padx=20)

# Boton para volver al menu principal
boton_volver = tk.Button(panel_botones, text="<-- Volver al Menú", 
                         command=lambda: mostrar_pantalla(pantalla_menu))
boton_volver.pack(side='left', padx=(0, 10))

# Boton para convertir en titulo
boton_titulo = tk.Button(panel_botones, text="Convertir Línea en Título", command=make_line_title)
boton_titulo.pack(side='left')

# Boton para convertir en referencia --- PENDIENTE
boton_referencia = tk.Button(panel_botones, text="Convertir Línea en Referencia", command=make_line_title)
boton_referencia.pack(side='left')

texto_usuario = scrolledtext.ScrolledText(pantalla_editor, wrap=tk.WORD, width=80, height=25, font=("Times New Roman", 12))
texto_usuario.pack(pady=10, padx=20, expand=True, fill='both')
texto_usuario.tag_configure("title1", font=("Times New Roman", 12, "bold"))

boton_generar = tk.Button(pantalla_editor, text="Generar PDF", command=iniciar_generacion, font=("Arial", 12, "bold"), bg="#00529B", fg="white")
boton_generar.pack(pady=20)


#----------------------------INICIO DE LA APLICACION--------------------------
# Pantalla del Menu
mostrar_pantalla(pantalla_menu)

if __name__ == "__main__":
    ventana.mainloop()