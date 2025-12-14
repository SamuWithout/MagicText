import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from pdfGenerator import crear_documento_apa_reportlab

# Diccionario y funciones de navegación y portada
datos_documento = {"portada": {}}

def mostrar_pantalla(pantalla_a_mostrar):
    for pantalla in contenedor_principal.winfo_children():
        pantalla.pack_forget()
    pantalla_a_mostrar.pack(fill="both", expand=True)

def guardar_datos_portada():
    """Recoge los datos, ignorando los placeholders si el usuario no escribió nada."""
    placeholders = {
        "titulo": "[Título del Documento, hasta 12 palabras]", "autor": "[Nombre y Apellidos del Autor]",
        "afiliacion": "[Afiliación Institucional, ej: Universidad]", "curso": "[Código y Nombre del Curso]",
        "instructor": "[Nombre del Instructor]", "fecha": "[Fecha de Entrega]"
    }
    def get_value(entry, placeholder):
        text = entry.get()
        return "" if text == placeholder else text
    datos_documento["portada"] = {
        'titulo': get_value(entry_titulo, placeholders["titulo"]), 'autor': get_value(entry_autor, placeholders["autor"]),
        'afiliacion': get_value(entry_afiliacion, placeholders["afiliacion"]), 'curso': get_value(entry_curso, placeholders["curso"]),
        'instructor': get_value(entry_instructor, placeholders["instructor"]), 'fecha': get_value(entry_fecha, placeholders["fecha"])
    }
    messagebox.showinfo("Guardado", "Los datos de la portada han sido guardados.")
    mostrar_pantalla(pantalla_seleccion)

def make_line_title(event=None):
    try:
        texto_usuario.tag_remove("title2", "insert linestart", "insert lineend")
        texto_usuario.tag_add("title1", "insert linestart", "insert lineend")
    except tk.TclError: pass
    return "break"

def make_line_subtitle(event=None):
    try:
        texto_usuario.tag_remove("title1", "insert linestart", "insert lineend")
        texto_usuario.tag_add("title2", "insert linestart", "insert lineend")
    except tk.TclError: pass
    return "break"

def highlight_selection(event=None):
    try: texto_usuario.tag_add("highlight", "sel.first", "sel.last")
    except tk.TclError: pass
    return "break"

def remove_highlight():
    try: texto_usuario.tag_remove("highlight", "sel.first", "sel.last")
    except tk.TclError: pass
    
def undo_action(event=None):
    try:
        if pantalla_editor.winfo_ismapped(): texto_usuario.edit_undo()
        elif pantalla_referencias.winfo_ismapped(): texto_referencias.edit_undo()
    except tk.TclError: pass
    return "break"

def redo_action(event=None):
    try:
        if pantalla_editor.winfo_ismapped(): texto_usuario.edit_redo()
        elif pantalla_referencias.winfo_ismapped(): texto_referencias.edit_redo()
    except tk.TclError: pass
    return "break"

def iniciar_generacion(event=None):
    contenido_cuerpo = []
    num_lines_cuerpo = int(texto_usuario.index('end-1c').split('.')[0])
    
    for i in range(1, num_lines_cuerpo + 1):
        texto_linea = texto_usuario.get(f"{i}.0", f"{i}.end").strip()
        if not texto_linea: continue
        tags = texto_usuario.tag_names(f"{i}.0")
        if "title1" in tags: contenido_cuerpo.append(('title_level_1', texto_linea))
        elif "title2" in tags: contenido_cuerpo.append(('title_level_2', texto_linea))
        else: contenido_cuerpo.append(('paragraph', texto_linea))
        
    lista_referencias = []
    num_lines_refs = int(texto_referencias.index('end-1c').split('.')[0])
    
    for i in range(1, num_lines_refs + 1):
        texto_linea = texto_referencias.get(f"{i}.0", f"{i}.end").strip()
        
        if texto_linea: lista_referencias.append(('referencia', texto_linea))
    contenido_final = []
    contenido_final.extend(contenido_cuerpo)
    
    if lista_referencias:
        contenido_final.append(('pagebreak', ''))
        contenido_final.append(('title_level_1', 'Referencias'))
        contenido_final.extend(lista_referencias)
        
    if not datos_documento["portada"] and not contenido_final:
        messagebox.showwarning("Advertencia", "No hay contenido para generar el PDF.")
        return "break"
    crear_documento_apa_reportlab(datos_documento["portada"], contenido_final)
    return "break"

# Ventana Principal
ventana = tk.Tk()
ventana.title("MagicText")
ventana.geometry("900x700") 
contenedor_principal = tk.Frame(ventana)
contenedor_principal.pack(fill="both", expand=True)
#624
ANCHO_PAGINA_PIXELES = 450

#-----------------------------------MENÚ PRINCIPAL (DISEÑO MODERNO)--------------------------------------------
pantalla_menu = tk.Frame(contenedor_principal, bg="#F2F2F2")

header_frame = tk.Frame(pantalla_menu, bg="white", height=50)
header_frame.pack(fill="x", side="top")

fuente_titulo_pequeno = font.Font(family="Arial", size=14, weight="bold")

titulo_label_pequeno = tk.Label(header_frame, text="MagicText", font=fuente_titulo_pequeno, bg="white", fg="#0D47A1")
titulo_label_pequeno.place(x=20, rely=0.5, anchor="w")

fuente_bienvenida = font.Font(family="Arial", size=28, weight="bold")

bienvenida_label = tk.Label(pantalla_menu, text="¡Te damos la bienvenida!", font=fuente_bienvenida, bg="#F2F2F2", fg="#0D47A1")
bienvenida_label.place(relx=0.5, rely=0.4, anchor="center")

botones_frame_container = tk.Frame(pantalla_menu, bg="white", borderwidth=1, relief="solid", highlightbackground="#E0E0E0", highlightthickness=1)
botones_frame_container.place(relx=0.5, rely=0.55, anchor="center")

boton_ir_a_apa = tk.Button(botones_frame_container, text="⊕ Crear Documento", command=lambda: mostrar_pantalla(pantalla_seleccion), font=("Arial", 12, "bold"), bg="#0D47A1", fg="white", relief="flat", padx=20, pady=10)
boton_ir_a_apa.pack(side="left", padx=15, pady=15)

boton_salir = tk.Button(botones_frame_container, text="↑ Salir de la Aplicación", command=ventana.quit, font=("Arial", 12), bg="white", fg="black", relief="flat", padx=20, pady=10)
boton_salir.pack(side="left", padx=15, pady=15)

#---------------------PANTALLA DE SELECCIÓN (DISEÑO VISUAL)-------------------------------
pantalla_seleccion = tk.Frame(contenedor_principal, bg="#F2F2F2")

label_seleccion = tk.Label(pantalla_seleccion, text="Selecciona la sección a editar:", font=("Arial", 20), bg="#F2F2F2", fg="#333333")
label_seleccion.pack(pady=(40, 30))

opciones_frame = tk.Frame(pantalla_seleccion, bg="#F2F2F2")
opciones_frame.pack(pady=20, expand=True, fill="x", anchor="n")
opciones_frame.columnconfigure((0, 1, 2), weight=1)

def go_to_portada(event): mostrar_pantalla(pantalla_portada)
def go_to_contenido(event): mostrar_pantalla(pantalla_editor)
def go_to_referencias(event): mostrar_pantalla(pantalla_referencias)

#fuentes de los previews
font_preview_titulo = font.Font(family="Times New Roman", size=10, weight="bold")
font_preview_texto = font.Font(family="Times New Roman", size=9)

# Portada
columna_portada = tk.Frame(opciones_frame, bg="#F2F2F2")
columna_portada.grid(row=0, column=0, padx=15, sticky="n")

label_titulo_portada = tk.Label(columna_portada, text="Portada", font=("Arial", 14), bg="#F2F2F2")
label_titulo_portada.pack(pady=(0, 10))

hoja_portada = tk.Frame(columna_portada, width=220, height=311, bg="white", borderwidth=1, relief="solid", highlightbackground="#CCCCCC", highlightthickness=1)
hoja_portada.pack()
hoja_portada.pack_propagate(False)
# Portada preview
preview_titulo_p = tk.Label(hoja_portada, text="Título del Documento", font=font_preview_titulo, bg="white")
preview_titulo_p.pack(pady=(60, 20))
preview_info_p = tk.Label(hoja_portada, text="Nombre del Autor\nUniversidad\nCurso\nFecha de Entrega", font=font_preview_texto, bg="white", justify="center")
preview_info_p.pack()

# Contenido
columna_contenido = tk.Frame(opciones_frame, bg="#F2F2F2")
columna_contenido.grid(row=0, column=1, padx=15, sticky="n")

label_titulo_contenido = tk.Label(columna_contenido, text="Contenido", font=("Arial", 14), bg="#F2F2F2")
label_titulo_contenido.pack(pady=(0, 10))

hoja_contenido = tk.Frame(columna_contenido, width=220, height=311, bg="white", borderwidth=1, relief="solid", highlightbackground="#CCCCCC", highlightthickness=1)
hoja_contenido.pack()
hoja_contenido.pack_propagate(False)
# Contenido preview
preview_titulo_c = tk.Label(hoja_contenido, text="Título Principal", font=font_preview_titulo, bg="white", justify="center")
preview_titulo_c.pack(pady=(20, 10))
preview_texto_c = tk.Label(hoja_contenido, text="El primer párrafo comienza aquí...", font=font_preview_texto, bg="white", justify="left")
preview_texto_c.pack(padx=15)

# Referencias
columna_referencias = tk.Frame(opciones_frame, bg="#F2F2F2")
columna_referencias.grid(row=0, column=2, padx=15, sticky="n")

label_titulo_referencias = tk.Label(columna_referencias, text="Referencias", font=("Arial", 14), bg="#F2F2F2")
label_titulo_referencias.pack(pady=(0, 10))

hoja_referencias = tk.Frame(columna_referencias, width=220, height=311, bg="white", borderwidth=1, relief="solid", highlightbackground="#CCCCCC", highlightthickness=1)
hoja_referencias.pack()
hoja_referencias.pack_propagate(False)
# Referencias preview
preview_titulo_r = tk.Label(hoja_referencias, text="Referencias", font=font_preview_titulo, bg="white", justify="center")
preview_titulo_r.pack(pady=(20, 10))
preview_ref1_r = tk.Label(hoja_referencias, text="A. A. (Año).\nLincoln Research.", font=font_preview_texto, bg="white", justify="left")
preview_ref1_r.pack(padx=15, pady=5)

for hoja in [hoja_portada, hoja_contenido, hoja_referencias]:
    hoja.config(cursor="hand2")
    for widget in hoja.winfo_children(): widget.config(cursor="hand2")
# Hojas interactivas
hoja_portada.bind("<Button-1>", go_to_portada)
hoja_contenido.bind("<Button-1>", go_to_contenido)
hoja_referencias.bind("<Button-1>", go_to_referencias)

for widget in hoja_portada.winfo_children(): widget.bind("<Button-1>", go_to_portada)
for widget in hoja_contenido.winfo_children(): widget.bind("<Button-1>", go_to_contenido)
for widget in hoja_referencias.winfo_children(): widget.bind("<Button-1>", go_to_referencias)

boton_volver_menu = tk.Button(pantalla_seleccion, text="Volver al Menú Principal", command=lambda: mostrar_pantalla(pantalla_menu))
boton_volver_menu.pack(pady=40, side="bottom")

#----------------------- PANTALLA DE PORTADA APA (DISEÑO)-------------------------------
def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg='black', font=("Times New Roman", 12))
        
def on_focusout(event, entry, placeholder, is_bold=False):
    if entry.get() == '':
        entry.insert(0, placeholder)
        font_config = ("Times New Roman", 12, "bold") if is_bold else ("Times New Roman", 12)
        entry.config(fg='grey', font=font_config)
        
pantalla_portada = tk.Frame(contenedor_principal, bg="#F2F2F2")

instrucciones_portada = tk.Label(pantalla_portada, text="Completa los datos de la portada:", font=("Arial", 16), bg="#F2F2F2")
instrucciones_portada.pack(pady=20)

page_frame_portada = tk.Frame(pantalla_portada, width=ANCHO_PAGINA_PIXELES, height=500, borderwidth=1, relief="solid", bg="white")
page_frame_portada.pack(pady=10)
page_frame_portada.pack_propagate(False)
# previews de la portada
tk.Frame(page_frame_portada, height=100, bg='white').pack()
placeholders = {
    "titulo": "[Título del Documento, hasta 12 palabras]", "autor": "[Nombre y Apellidos del Autor]",
    "afiliacion": "[Afiliación Institucional, ej: Universidad]", "curso": "[Código y Nombre del Curso]",
    "instructor": "[Nombre del Instructor]", "fecha": "[Fecha de Entrega]"
}

font_bold = ("Times New Roman", 12, "bold")
font_normal = ("Times New Roman", 12)
# campo de entrada para el titulo
entry_titulo = tk.Entry(page_frame_portada, font=font_bold, fg='grey', justify='center', relief='flat', bg='white')
entry_titulo.pack(pady=5, fill='x', padx=20)
entry_titulo.insert(0, placeholders["titulo"])
entry_titulo.bind('<FocusIn>', lambda e: on_entry_click(e, entry_titulo, placeholders["titulo"]))
entry_titulo.bind('<FocusOut>', lambda e: on_focusout(e, entry_titulo, placeholders["titulo"], is_bold=True))
# campo de entrada para el autor
entry_autor = tk.Entry(page_frame_portada, font=font_normal, fg='grey', justify='center', relief='flat', bg='white')
entry_autor.pack(pady=(10, 5), fill='x', padx=20)
entry_autor.insert(0, placeholders["autor"])
entry_autor.bind('<FocusIn>', lambda e: on_entry_click(e, entry_autor, placeholders["autor"]))
entry_autor.bind('<FocusOut>', lambda e: on_focusout(e, entry_autor, placeholders["autor"]))
# campo de entrada para la afiliacion
entry_afiliacion = tk.Entry(page_frame_portada, font=font_normal, fg='grey', justify='center', relief='flat', bg='white')
entry_afiliacion.pack(pady=5, fill='x', padx=20)
entry_afiliacion.insert(0, placeholders["afiliacion"])
entry_afiliacion.bind('<FocusIn>', lambda e: on_entry_click(e, entry_afiliacion, placeholders["afiliacion"]))
entry_afiliacion.bind('<FocusOut>', lambda e: on_focusout(e, entry_afiliacion, placeholders["afiliacion"]))
#campo de entrada para el curso
entry_curso = tk.Entry(page_frame_portada, font=font_normal, fg='grey', justify='center', relief='flat', bg='white')
entry_curso.pack(pady=5, fill='x', padx=20)
entry_curso.insert(0, placeholders["curso"])
entry_curso.bind('<FocusIn>', lambda e: on_entry_click(e, entry_curso, placeholders["curso"]))
entry_curso.bind('<FocusOut>', lambda e: on_focusout(e, entry_curso, placeholders["curso"]))
#campo de entrada para el instructor/maestro
entry_instructor = tk.Entry(page_frame_portada, font=font_normal, fg='grey', justify='center', relief='flat', bg='white')
entry_instructor.pack(pady=5, fill='x', padx=20)
entry_instructor.insert(0, placeholders["instructor"])
entry_instructor.bind('<FocusIn>', lambda e: on_entry_click(e, entry_instructor, placeholders["instructor"]))
entry_instructor.bind('<FocusOut>', lambda e: on_focusout(e, entry_instructor, placeholders["instructor"]))
#campo de entrada para la fecha
entry_fecha = tk.Entry(page_frame_portada, font=font_normal, fg='grey', justify='center', relief='flat', bg='white')
entry_fecha.pack(pady=5, fill='x', padx=20)
entry_fecha.insert(0, placeholders["fecha"])
entry_fecha.bind('<FocusIn>', lambda e: on_entry_click(e, entry_fecha, placeholders["fecha"]))
entry_fecha.bind('<FocusOut>', lambda e: on_focusout(e, entry_fecha, placeholders["fecha"]))
# botones de la portada
panel_botones_portada = tk.Frame(pantalla_portada, bg="#F2F2F2")
panel_botones_portada.pack(pady=20)

boton_guardar_portada = tk.Button(panel_botones_portada, text="Guardar Datos", command=guardar_datos_portada, font=("Arial", 12, "bold"))
boton_guardar_portada.pack(side="left", padx=10)

boton_volver_seleccion = tk.Button(panel_botones_portada, text="<-- Volver a Secciones", command=lambda: mostrar_pantalla(pantalla_seleccion))
boton_volver_seleccion.pack(side="left", padx=10)

#---------------------PANTALLA DEL CUERPO del DOCUMENTO APA-------------------------------
pantalla_editor = tk.Frame(contenedor_principal)

instrucciones = tk.Label(pantalla_editor, text="Escribe el contenido de tu documento:", font=("Arial", 14))
instrucciones.pack(pady=10)
#Botones del cuerpo del documento
panel_botones_editor = tk.Frame(pantalla_editor)
panel_botones_editor.pack(fill='x', padx=20)

boton_volver_editor = tk.Button(panel_botones_editor, text="<-- Volver", command=lambda: mostrar_pantalla(pantalla_seleccion))
boton_volver_editor.pack(side='left', padx=(0, 5))

boton_deshacer_editor = tk.Button(panel_botones_editor, text="Deshacer", command=undo_action)
boton_deshacer_editor.pack(side='left')

boton_rehacer_editor = tk.Button(panel_botones_editor, text="Rehacer", command=redo_action)
boton_rehacer_editor.pack(side='left', padx=5)

boton_titulo = tk.Button(panel_botones_editor, text="Título", command=make_line_title)
boton_titulo.pack(side='left')

boton_subtitulo = tk.Button(panel_botones_editor, text="Subtítulo", command=make_line_subtitle)
boton_subtitulo.pack(side='left', padx=5)

boton_generar = tk.Button(panel_botones_editor, text="Generar PDF", command=iniciar_generacion, font=("Arial", 12, "bold"), bg="#00529B", fg="white")
boton_generar.pack(side='right')

page_frame_editor = tk.Frame(pantalla_editor, width=ANCHO_PAGINA_PIXELES, height=600, borderwidth=1, relief="solid", bg="white")
page_frame_editor.pack(pady=10, expand=True)
page_frame_editor.pack_propagate(False)

texto_usuario = scrolledtext.ScrolledText(page_frame_editor, wrap=tk.WORD, font=("Times New Roman", 12), borderwidth=0, highlightthickness=0, undo=True)
texto_usuario.pack(expand=True, fill='both', padx=10, pady=10)

texto_usuario.tag_configure("title1", font=("Times New Roman", 12, "bold"), justify='center')
texto_usuario.tag_configure("title2", font=("Times New Roman", 12, "bold"))
texto_usuario.tag_configure("highlight", background="yellow")

# Referencias
pantalla_referencias = tk.Frame(contenedor_principal)

instrucciones_ref = tk.Label(pantalla_referencias, text="Escribe tus referencias (una por línea):", font=("Arial", 14))
instrucciones_ref.pack(pady=10)
# Botones de la pantalla referencias
panel_botones_ref = tk.Frame(pantalla_referencias)
panel_botones_ref.pack(fill='x', padx=20)

boton_volver_ref = tk.Button(panel_botones_ref, text="<-- Volver", command=lambda: mostrar_pantalla(pantalla_seleccion))
boton_volver_ref.pack(side='left')

boton_deshacer_ref = tk.Button(panel_botones_ref, text="Deshacer", command=undo_action)
boton_deshacer_ref.pack(side='left', padx=5)

boton_rehacer_ref = tk.Button(panel_botones_ref, text="Rehacer", command=redo_action)
boton_rehacer_ref.pack(side='left')

boton_generar_ref = tk.Button(panel_botones_ref, text="Generar PDF", command=iniciar_generacion, font=("Arial", 12, "bold"), bg="#00529B", fg="white")
boton_generar_ref.pack(side='right')

page_frame_ref = tk.Frame(pantalla_referencias, width=ANCHO_PAGINA_PIXELES, height=600, borderwidth=1, relief="solid", bg="white")

page_frame_ref.pack(pady=10, expand=True)
page_frame_ref.pack_propagate(False)

texto_referencias = scrolledtext.ScrolledText(page_frame_ref, wrap=tk.WORD, font=("Times New Roman", 12), borderwidth=0, highlightthickness=0, undo=True)
texto_referencias.pack(expand=True, fill='both', padx=10, pady=10)

#----------------------------INICIO DE LA APLICACION--------------------------
ventana.bind('<Control-t>', make_line_title)
ventana.bind('<Control-d>', make_line_subtitle)
ventana.bind('<Control-g>', iniciar_generacion)
ventana.bind('<Control-z>', undo_action)
ventana.bind('<Control-y>', redo_action)
mostrar_pantalla(pantalla_menu)
if __name__ == "__main__":
    ventana.mainloop()