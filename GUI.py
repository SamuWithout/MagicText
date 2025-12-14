import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from pdfGenerator import crear_documento_apa_reportlab

# --- DICCIONARIO PARA ALMACENAR LOS DATOS ---
datos_documento = {
    "portada": {},
    "cuerpo": []
}

#---------------------------LOGICA PARA NAVEGAR ENTRE PANTALLAS----------------------------
def mostrar_pantalla(pantalla_a_mostrar):
    for pantalla in contenedor_principal.winfo_children():
        pantalla.pack_forget()
    pantalla_a_mostrar.pack(fill="both", expand=True)

# ---Funciones de la Pantalla de Portada---
def guardar_datos_portada():
    datos_documento["portada"] = {
        'titulo': entry_titulo.get(),
        'autor': entry_autor.get(),
        'afiliacion': entry_afiliacion.get(),
        'curso': entry_curso.get(),
        'instructor': entry_instructor.get(),
        'fecha': entry_fecha.get()
    }
    messagebox.showinfo("Guardado", "Los datos de la portada han sido guardados.")
    mostrar_pantalla(pantalla_seleccion)

# ---Funciones de la Pantalla para el cuerpo del documento---
def make_line_title():
    try:
        line_start = texto_usuario.index("insert linestart")
        line_end = texto_usuario.index("insert lineend")
        texto_usuario.tag_remove("title2", line_start, line_end)
        texto_usuario.tag_add("title1", line_start, line_end)
    except tk.TclError:
        pass

def make_line_subtitle():
    try:
        line_start = texto_usuario.index("insert linestart")
        line_end = texto_usuario.index("insert lineend")
        texto_usuario.tag_remove("title1", line_start, line_end)
        texto_usuario.tag_add("title2", line_start, line_end)
    except tk.TclError:
        pass

def make_line_reference():
    try:
        line_start = texto_usuario.index("insert linestart")
        line_end = texto_usuario.index("insert lineend")
        texto_usuario.tag_add("referencia1", line_start, line_end)
    except tk.TclError:
        pass
    
def iniciar_generacion():
    contenido_estructurado = []
    num_lines_str = texto_usuario.index('end-1c').split('.')[0]
    if not num_lines_str: return
    num_lines = int(num_lines_str)

    for i in range(1, num_lines + 1):
        line_start = f"{i}.0"
        line_end = f"{i}.end"
        texto_linea = texto_usuario.get(line_start, line_end).strip()
        
        if not texto_linea:
            continue
            
        tags_en_linea = texto_usuario.tag_names(line_start)

        if "title1" in tags_en_linea:
            contenido_estructurado.append(('title_level_1', texto_linea))
        elif "title2" in tags_en_linea:
            contenido_estructurado.append(('title_level_2', texto_linea))
        elif "referencia1" in tags_en_linea:
            contenido_estructurado.append(('referencia', texto_linea))
        else:
            contenido_estructurado.append(('paragraph', texto_linea))

    # Verifica si hay contenido en la portada o en el cuerpo
    if not datos_documento["portada"] and not contenido_estructurado:
        messagebox.showwarning("Advertencia", "No hay contenido para generar el PDF.")
        return
        
    # Llama a la función de generación con ambos conjuntos de datos
    crear_documento_apa_reportlab(datos_documento["portada"], contenido_estructurado)

# ... (El resto del código de la ventana principal, menú, selección y portada no cambia) ...

# -----------------------------------VENTANA PRINCIPAL---------------------------------------
ventana = tk.Tk()
ventana.title("MagicText")
ventana.geometry("900x700") 

contenedor_principal = tk.Frame(ventana)
contenedor_principal.pack(fill="both", expand=True)

#-----------------------------------MENÚ PRINCIPAL--------------------------------------------
pantalla_menu = tk.Frame(contenedor_principal)
#Titulo del menu
fuente_titulo = font.Font(family="Helvetica", size=36, weight="bold")
titulo_label = tk.Label(pantalla_menu, text="MagicText", font=fuente_titulo)
titulo_label.pack(pady=(80, 40))
#Botones de Documento Apa y Salir--
#APA
boton_ir_a_apa = tk.Button(pantalla_menu, text="Documento APA", command=lambda: mostrar_pantalla(pantalla_seleccion),
                           font=("Arial", 14), width=20, height=2)
boton_ir_a_apa.pack(pady=10)
#Salir
boton_salir = tk.Button(pantalla_menu, text="Salir", command=ventana.quit, font=("Arial", 14), width=20, height=2)
boton_salir.pack(pady=10)

#---------------------PANTALLA DE DOCUMENTO APA-------------------------------
pantalla_seleccion = tk.Frame(contenedor_principal)
label_seleccion = tk.Label(pantalla_seleccion, text="¿Qué deseas hacer?", font=("Arial", 20))
label_seleccion.pack(pady=(50, 30))
frame_botones_seleccion = tk.Frame(pantalla_seleccion)
frame_botones_seleccion.pack(pady=20)

#Boton para la portada--
boton_portada = tk.Button(frame_botones_seleccion, text="Portada", command=lambda: mostrar_pantalla(pantalla_portada),
                          font=("Arial", 14), width=20, height=3)
boton_portada.pack(side="left", padx=15)

#Boton para el cuerpo del documento--
boton_contenido = tk.Button(frame_botones_seleccion, text="Escribir Contenido", command=lambda: mostrar_pantalla(pantalla_editor),
                            font=("Arial", 14), width=20, height=3)
boton_contenido.pack(side="left", padx=15)

#Boton de volver al menu--
boton_volver_menu = tk.Button(pantalla_seleccion, text="Volver al Menú Principal",
                             command=lambda: mostrar_pantalla(pantalla_menu))
boton_volver_menu.pack(pady=40)

#-----------------------PANTALLA DE PORTADA APA-------------------------------
pantalla_portada = tk.Frame(contenedor_principal)
label_portada = tk.Label(pantalla_portada, text="Completa los datos de la Portada (APA 7ma Ed.)", font=("Arial", 16))
label_portada.pack(pady=20)
frame_formulario = tk.Frame(pantalla_portada)
frame_formulario.pack(pady=10, padx=40, fill="x")

# Campos de la portada
campos_portada = {
    "Título del Documento:": tk.Entry(frame_formulario, font=("Arial", 12), width=50),
    "Autor (Tu Nombre Completo):": tk.Entry(frame_formulario, font=("Arial", 12), width=50),
    "Afiliación (Nombre de la Universidad):": tk.Entry(frame_formulario, font=("Arial", 12), width=50),
    "Curso (Ej: PSYC 101):": tk.Entry(frame_formulario, font=("Arial", 12), width=50),
    "Nombre del Instructor:": tk.Entry(frame_formulario, font=("Arial", 12), width=50),
    "Fecha de Entrega:": tk.Entry(frame_formulario, font=("Arial", 12), width=50),
}

#Guardar referencias a los Entry widgets para la función de guardado--
entry_titulo = campos_portada["Título del Documento:"]
entry_autor = campos_portada["Autor (Tu Nombre Completo):"]
entry_afiliacion = campos_portada["Afiliación (Nombre de la Universidad):"]
entry_curso = campos_portada["Curso (Ej: PSYC 101):"]
entry_instructor = campos_portada["Nombre del Instructor:"]
entry_fecha = campos_portada["Fecha de Entrega:"]
for label_text, entry_widget in campos_portada.items():
    label = tk.Label(frame_formulario, text=label_text, font=("Arial", 12))
    label.pack(fill="x", padx=10, pady=(10, 0))
    entry_widget.pack(fill="x", padx=10, pady=5)
boton_guardar_portada = tk.Button(pantalla_portada, text="Guardar Datos de Portada", command=guardar_datos_portada, font=("Arial", 12, "bold"))
boton_guardar_portada.pack(pady=20)
boton_volver_seleccion = tk.Button(pantalla_portada, text="<-- Volver", command=lambda: mostrar_pantalla(pantalla_seleccion))
boton_volver_seleccion.pack()

#---------------------PANTALLA DEl CUERPO para el DOCUMENTO APA-------------------------------
pantalla_editor = tk.Frame(contenedor_principal)
instrucciones = tk.Label(pantalla_editor, text="Escribe y formatea tu documento:", font=("Arial", 14))
instrucciones.pack(pady=10)

panel_botones = tk.Frame(pantalla_editor)
panel_botones.pack(fill='x', padx=20)

boton_volver = tk.Button(panel_botones, text="<-- Volver", 
                         command=lambda: mostrar_pantalla(pantalla_seleccion))
boton_volver.pack(side='left', padx=(0, 10))

boton_titulo = tk.Button(panel_botones, text="Título (Nivel 1)", command=make_line_title)
boton_titulo.pack(side='left')

boton_subtitulo = tk.Button(panel_botones, text="Subtítulo (Nivel 2)", command=make_line_subtitle)
boton_subtitulo.pack(side='left', padx=5)

boton_referencia = tk.Button(panel_botones, text="Convertir Línea en Referencia", command=make_line_reference)
boton_referencia.pack(side='left')

boton_generar = tk.Button(panel_botones, text="Generar PDF", command=iniciar_generacion, font=("Arial", 12, "bold"), bg="#00529B", fg="white")
boton_generar.pack(side='right')

# ---Hoja para completar (cuerpo)---
#Contenedor que simulará la hoja de papel para escribir
ANCHO_PAGINA_PIXELES = 624
page_frame = tk.Frame(pantalla_editor, width=ANCHO_PAGINA_PIXELES, height=600,
                      borderwidth=1, relief="solid", bg="white")
page_frame.pack(pady=10, expand=True)
page_frame.pack_propagate(False)

texto_usuario = scrolledtext.ScrolledText(page_frame,
                                          wrap=tk.WORD, 
                                          font=("Times New Roman", 12),
                                          borderwidth=0,
                                          highlightthickness=0,
                                          undo=True) # Habilitamos el Undo/Redo
texto_usuario.pack(expand=True, fill='both', padx=10, pady=10)

texto_usuario.tag_configure("title1", font=("Times New Roman", 12, "bold"), justify='center')
texto_usuario.tag_configure("title2", font=("Times New Roman", 12, "bold")) # Solo negrita
texto_usuario.tag_configure("referencia1", font=("Times New Roman", 12, "italic"))

#----------------------------INICIO DE LA APLICACION--------------------------
mostrar_pantalla(pantalla_menu)

if __name__ == "__main__":
    ventana.mainloop()