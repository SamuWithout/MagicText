import tkinter as tk
from tkinter import scrolledtext, messagebox, font, filedialog
import json # Necesario para guardar y cargar proyectos
from pdfGenerator import crear_documento_apa_reportlab

# Diccionario y funciones de navegación
datos_documento = {"portada": {}}

def mostrar_pantalla(pantalla_a_mostrar):
    for pantalla in contenedor_principal.winfo_children():
        pantalla.pack_forget()
    pantalla_a_mostrar.pack(fill="both", expand=True)
    
def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg='black')

def on_focusout(event, entry, placeholder, is_bold=False):
    if entry.get() == '':
        font_config = font_bold if is_bold else font_normal
        entry.config(fg='grey', font=font_config)
        entry.insert(0, placeholder)
def nuevo_documento():
    if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres crear un nuevo documento? Se perderá todo el trabajo no guardado."):
        # Limpiar datos de portada para empezar uno nuevo
        datos_documento["portada"] = {}
        for entry in [entry_titulo, entry_autor, entry_afiliacion, entry_curso, entry_instructor, entry_fecha]:
            entry.delete(0, "end")
        # Restaurar placeholders de la portada
        on_focusout(None, entry_titulo, placeholders["titulo"], is_bold=True)
        on_focusout(None, entry_autor, placeholders["autor"])
        on_focusout(None, entry_afiliacion, placeholders["afiliacion"])
        on_focusout(None, entry_curso, placeholders["curso"])
        on_focusout(None, entry_instructor, placeholders["instructor"])
        on_focusout(None, entry_fecha, placeholders["fecha"])
        # Limpiar editores de texto
        texto_usuario.delete("1.0", "end")
        texto_referencias.delete("1.0", "end")
        messagebox.showinfo("Nuevo Documento", "Se ha limpiado el área de trabajo.")

def guardar_proyecto():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".magic",
        filetypes=[("MagicText Projects", "*.magic"), ("Todos los archivos", "*.*")],
        title="Guardar proyecto como..."
    )
    if not filepath: return

    # Recopilar todos los datos
    proyecto_data = {
        "portada": datos_documento["portada"],
        "contenido": texto_usuario.get("1.0", "end-1c"),
        "referencias": texto_referencias.get("1.0", "end-1c")
    }

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(proyecto_data, f, indent=4)
        messagebox.showinfo("Éxito", f"Proyecto guardado en:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el proyecto:\n{e}")

def abrir_proyecto():
    filepath = filedialog.askopenfilename(
        filetypes=[("MagicText Projects", "*.magic"), ("Todos los archivos", "*.*")],
        title="Abrir proyecto..."
    )
    if not filepath: return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            proyecto_data = json.load(f)
        nuevo_documento() 
        
        # Cargar datos de portada
        datos_documento["portada"] = proyecto_data.get("portada", {})
        entry_titulo.delete(0, "end"); entry_titulo.insert(0, datos_documento["portada"].get("titulo", ""))
        entry_autor.delete(0, "end"); entry_autor.insert(0, datos_documento["portada"].get("autor", ""))
        entry_afiliacion.delete(0, "end"); entry_afiliacion.insert(0, datos_documento["portada"].get("afiliacion", ""))
        entry_curso.delete(0, "end"); entry_curso.insert(0, datos_documento["portada"].get("curso", ""))
        entry_instructor.delete(0, "end"); entry_instructor.insert(0, datos_documento["portada"].get("instructor", ""))
        entry_fecha.delete(0, "end"); entry_fecha.insert(0, datos_documento["portada"].get("fecha", ""))
        
        # Cargar contenido y referencias
        texto_usuario.delete("1.0", "end"); texto_usuario.insert("1.0", proyecto_data.get("contenido", ""))
        texto_referencias.delete("1.0", "end"); texto_referencias.insert("1.0", proyecto_data.get("referencias", ""))

        messagebox.showinfo("Éxito", f"Proyecto '{filepath.split('/')[-1]}' cargado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el proyecto:\n{e}")

def guardar_datos_portada():
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
#-------------------------------------------------------
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
#-----------------------------------------
# --- Panel de Navegación Lateral ---
def crear_panel_navegacion(parent):
    nav_panel = tk.Frame(parent, bg="#EAECEE", width=180)
    nav_panel.pack(side="left", fill="y", padx=(5,0), pady=5)
    nav_panel.pack_propagate(False)
    font_nav_titulo = font.Font(family="Arial", size=9, weight="bold")
    font_nav_texto = font.Font(family="Times New Roman", size=7)
    def crear_mini_hoja(p, texto_titulo, preview_factory):
        tk.Label(p, text=texto_titulo, font=("Arial", 10), bg="#EAECEE").pack(pady=(15, 5))
        hoja = tk.Frame(p, width=150, height=212, bg="white", borderwidth=1, relief="solid")
        hoja.pack(); hoja.pack_propagate(False)
        preview_factory(hoja)
        return hoja
    
    def prev_portada(h): tk.Label(h, text="Título del Documento", font=font_nav_titulo, bg="white").pack(pady=(40, 15)); tk.Label(h, text="Nombre del Autor\nUniversidad...", font=font_nav_texto, bg="white").pack()
    
    def prev_contenido(h): tk.Label(h, text="Título Principal", font=font_nav_titulo, bg="white").pack(pady=(15, 10)); tk.Label(h, text="El primer párrafo...", font=font_nav_texto, bg="white", justify="left").pack(padx=10)
    
    def prev_referencias(h): tk.Label(h, text="Referencias", font=font_nav_titulo, bg="white").pack(pady=(15, 10)); tk.Label(h, text="Apellido, A. (Año)...", font=font_nav_texto, bg="white", justify="left").pack(padx=10)
    hojas = [(crear_mini_hoja(nav_panel, "Portada", prev_portada), lambda e: mostrar_pantalla(pantalla_portada)),
             (crear_mini_hoja(nav_panel, "Contenido", prev_contenido), lambda e: mostrar_pantalla(pantalla_editor)),
             (crear_mini_hoja(nav_panel, "Referencias", prev_referencias), lambda e: mostrar_pantalla(pantalla_referencias))]
    for hoja, func in hojas:
        hoja.config(cursor="hand2"); hoja.bind("<Button-1>", func)
        for child in hoja.winfo_children(): child.config(cursor="hand2"); child.bind("<Button-1>", func)

# --- FUNCIÓN PARA LA CINTA RIBBON
def crear_ribbon(parent, es_editor_principal=True):
    ribbon_frame = tk.Frame(parent, bg="#F2F2F2")
    # Barra de pestañas
    tab_bar = tk.Frame(ribbon_frame, bg="#F2F2F2")
    tab_bar.pack(fill='x', padx=5, pady=(5,0))
    # Contenedor para el contenido de las pestañas
    content_bar = tk.Frame(ribbon_frame, bg="#E0E0E0", height=60)
    content_bar.pack(fill='x', padx=5, pady=(0,5))
    content_bar.pack_propagate(False)
    # Contenido de cada pestaña
    inicio_content = tk.Frame(content_bar, bg="#E0E0E0")
    archivo_content = tk.Frame(content_bar, bg="#E0E0E0")
    edicion_content = tk.Frame(content_bar, bg="#E0E0E0")
    tabs = {"archivo": archivo_content, "inicio": inicio_content, "edicion": edicion_content}
    
    def mostrar_tab(tab_name):
        for tab in tabs.values():
            tab.pack_forget()
        tabs[tab_name].pack(fill='both', expand=True, padx=10)

    # Crear pestañas
    tk.Button(tab_bar, text="Inicio", relief='flat', command=lambda: mostrar_pantalla(pantalla_seleccion)).pack(side='left')
    tk.Button(tab_bar, text="Archivo", relief='flat', command=lambda: mostrar_tab("archivo")).pack(side='left')
    tk.Button(tab_bar, text="Edicion", relief='flat', command=lambda: mostrar_tab("edicion")).pack(side='left')

    # Poblar pestaña Archivo
    tk.Button(archivo_content, text="+ Nuevo", relief='flat', command=nuevo_documento).pack(side='left', pady=10, padx=5)
    tk.Button(archivo_content, text="♳ Abrir", relief='flat', command=abrir_proyecto).pack(side='left', pady=10, padx=5)
    tk.Button(archivo_content, text="☑ Guardar", relief='flat', command=guardar_proyecto).pack(side='left', pady=10, padx=5)
    tk.Button(archivo_content, text="<-- Volver", relief='flat', command= lambda: mostrar_pantalla(pantalla_seleccion)).pack(side='left', pady=10, padx=5)
    
    # Poblar pestaña Edicion
    tk.Button(edicion_content, text="↶ Deshacer", relief='flat', command=undo_action).pack(side='left', pady=10, padx=5)
    tk.Button(edicion_content, text="↷ Rehacer", relief='flat', command=redo_action).pack(side='left', pady=10, padx=5)
    
    if es_editor_principal: # Solo aparece en la pantalla contenido
        tk.Button(edicion_content, text="Ⓣ", relief='flat', command=make_line_title).pack(side='left', pady=10, padx=5)
        tk.Button(edicion_content, text="Ⓢ", relief='flat', command=make_line_subtitle).pack(side='left', pady=10, padx=5)

    tk.Button(edicion_content, text="▶ Generar PDF", bg="#00529B", fg="white", relief='flat', command=iniciar_generacion).pack(side='right', pady=10, padx=10)
    
    mostrar_tab("inicio")
    return ribbon_frame

def crear_ribbon_portada(parent):
    ribbon_frame = tk.Frame(parent, bg="#F2F2F2")
    
    # Barra de pestañas
    tab_bar = tk.Frame(ribbon_frame, bg="#F2F2F2")
    tab_bar.pack(fill='x', padx=5, pady=(5,0))
    
    # Contenedor para el contenido de las pestañas
    content_bar = tk.Frame(ribbon_frame, bg="#E0E0E0", height=60)
    content_bar.pack(fill='x', padx=5, pady=(0,5))
    content_bar.pack_propagate(False)

    # Contenido de cada pestaña (solo necesitamos "Inicio" aquí)
    inicio_content = tk.Frame(content_bar, bg="#E0E0E0")
    inicio_content.pack(fill='both', expand=True, padx=10)

    # Pestaña "Inicio"
    tk.Button(tab_bar, text="Inicio", relief='flat', command=lambda: mostrar_pantalla(pantalla_seleccion)).pack(side='left')
    
    # Poblar la pestaña "Inicio" con los botones de la portada
    tk.Button(inicio_content, text="Guardar Datos", relief='flat', 
              command=guardar_datos_portada).pack(side='left', pady=10, padx=5)

    tk.Button(inicio_content, text="Generar PDF", bg="#00529B", fg="white", relief='flat', 
              command=iniciar_generacion).pack(side='right', pady=10, padx=10)
    
    return ribbon_frame

# Ventana Principal
ventana = tk.Tk()
ventana.title("MagicText")
ventana.geometry("1100x750") 
contenedor_principal = tk.Frame(ventana)
contenedor_principal.pack(fill="both", expand=True)
ANCHO_PAGINA_PIXELES = 624

#-----------------------------------MENÚ PRINCIPAL (DISEÑO MODERNO)--------------------------------------------
pantalla_menu = tk.Frame(contenedor_principal, bg="#F2F2F2")
header_frame = tk.Frame(pantalla_menu, bg="white", height=50); header_frame.pack(fill="x", side="top")
fuente_titulo_pequeno = font.Font(family="Arial", size=14, weight="bold")
tk.Label(header_frame, text="MagicText", font=fuente_titulo_pequeno, bg="white", fg="#0D47A1").place(x=20, rely=0.5, anchor="w")
fuente_bienvenida = font.Font(family="Arial", size=28, weight="bold")
tk.Label(pantalla_menu, text="¡Te damos la bienvenida!", font=fuente_bienvenida, bg="#F2F2F2", fg="#0D47A1").place(relx=0.5, rely=0.4, anchor="center")
botones_frame_container = tk.Frame(pantalla_menu, bg="white", borderwidth=1, relief="solid", highlightbackground="#E0E0E0", highlightthickness=1)
botones_frame_container.place(relx=0.5, rely=0.55, anchor="center")
tk.Button(botones_frame_container, text="⊕ Crear Documento", command=lambda: mostrar_pantalla(pantalla_seleccion), font=("Arial", 12, "bold"), bg="#0D47A1", fg="white", relief="flat", padx=20, pady=10).pack(side="left", padx=15, pady=15)
tk.Button(botones_frame_container, text="↑ Salir de la Aplicación", command=ventana.quit, font=("Arial", 12), bg="white", fg="black", relief="flat", padx=20, pady=10).pack(side="left", padx=15, pady=15)

#---------------------PANTALLA DE SELECCIÓN APA (DISEÑO VISUAL)-------------------------------
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

# Portada Preview
columna_portada = tk.Frame(opciones_frame, bg="#F2F2F2")
columna_portada.grid(row=0, column=0, padx=15, sticky="n")

label_titulo_portada = tk.Label(columna_portada, text="Portada", font=("Arial", 14), bg="#F2F2F2")
label_titulo_portada.pack(pady=(0, 10))

hoja_portada = tk.Frame(columna_portada, width=220, height=311, bg="white", borderwidth=1, relief="solid", highlightbackground="#CCCCCC", highlightthickness=1)
hoja_portada.pack()
hoja_portada.pack_propagate(False)

preview_titulo_p = tk.Label(hoja_portada, text="Título del Documento", font=font_preview_titulo, bg="white")
preview_titulo_p.pack(pady=(60, 20))
preview_info_p = tk.Label(hoja_portada, text="Nombre del Autor\nUniversidad\nCurso\nFecha de Entrega", font=font_preview_texto, bg="white", justify="center")
preview_info_p.pack()

# Contenido preview
columna_contenido = tk.Frame(opciones_frame, bg="#F2F2F2")
columna_contenido.grid(row=0, column=1, padx=15, sticky="n")

label_titulo_contenido = tk.Label(columna_contenido, text="Contenido", font=("Arial", 14), bg="#F2F2F2")
label_titulo_contenido.pack(pady=(0, 10))

hoja_contenido = tk.Frame(columna_contenido, width=220, height=311, bg="white", borderwidth=1, relief="solid", highlightbackground="#CCCCCC", highlightthickness=1)
hoja_contenido.pack()
hoja_contenido.pack_propagate(False)

preview_titulo_c = tk.Label(hoja_contenido, text="Título Principal", font=font_preview_titulo, bg="white", justify="center")
preview_titulo_c.pack(pady=(20, 10))
preview_texto_c = tk.Label(hoja_contenido, text="El primer párrafo comienza aquí...", font=font_preview_texto, bg="white", justify="left")
preview_texto_c.pack(padx=15)

# Referencias preview
columna_referencias = tk.Frame(opciones_frame, bg="#F2F2F2")
columna_referencias.grid(row=0, column=2, padx=15, sticky="n")

label_titulo_referencias = tk.Label(columna_referencias, text="Referencias", font=("Arial", 14), bg="#F2F2F2")
label_titulo_referencias.pack(pady=(0, 10))

hoja_referencias = tk.Frame(columna_referencias, width=220, height=311, bg="white", borderwidth=1, relief="solid", highlightbackground="#CCCCCC", highlightthickness=1)
hoja_referencias.pack()
hoja_referencias.pack_propagate(False)

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


#-----------------------PANTALLA DE PORTADA APA (DISEÑO INTEGRADO)-------------------------------
pantalla_portada = tk.Frame(contenedor_principal, bg="#DDEBF7")
panel_navegacion_portada = crear_panel_navegacion(pantalla_portada)
contenido_portada = tk.Frame(pantalla_portada, bg="#DDEBF7"); contenido_portada.pack(side="right", fill="both", expand=True)
ribbon_portada = crear_ribbon_portada(contenido_portada); ribbon_portada.pack(fill='x')
page_frame_portada = tk.Frame(contenido_portada, width=ANCHO_PAGINA_PIXELES, height=550, borderwidth=1, relief="solid", bg="white")
page_frame_portada.pack(pady=10, expand=True); page_frame_portada.pack_propagate(False)
tk.Frame(page_frame_portada, height=100, bg='white').pack()
placeholders = {"titulo": "[Título del Documento]", "autor": "[Nombre del Autor]", "afiliacion": "[Afiliación]", "curso": "[Curso]", "instructor": "[Instructor]", "fecha": "[Fecha]"}
font_bold = ("Times New Roman", 12, "bold"); font_normal = ("Times New Roman", 12)
entries_portada = {key: tk.Entry(page_frame_portada, font=(font_bold if key=='titulo' else font_normal), fg='grey', justify='center', relief='flat', bg='white') for key in placeholders}
entry_titulo=entries_portada["titulo"]; entry_autor=entries_portada["autor"]; entry_afiliacion=entries_portada["afiliacion"]; entry_curso=entries_portada["curso"]; entry_instructor=entries_portada["instructor"]; entry_fecha=entries_portada["fecha"]
for entry in entries_portada.values(): entry.pack(pady=5, fill='x', padx=20)
for key, entry in entries_portada.items():
    entry.insert(0, placeholders[key]); entry.bind('<FocusIn>', lambda e, en=entry, ph=placeholders[key]: on_entry_click(e, en, ph)); entry.bind('<FocusOut>', lambda e, en=entry, ph=placeholders[key], b=(key == "titulo"): on_focusout(e, en, ph, b))

#---------------------PANTALLA DEL CUERPO del DOCUMENTO APA-------------------------------
pantalla_editor = tk.Frame(contenedor_principal, bg="#DDEBF7")
panel_navegacion_editor = crear_panel_navegacion(pantalla_editor)
contenido_editor = tk.Frame(pantalla_editor, bg="#DDEBF7"); contenido_editor.pack(side="right", fill="both", expand=True)
ribbon_editor = crear_ribbon(contenido_editor, es_editor_principal=True); ribbon_editor.pack(fill='x')
page_frame_editor = tk.Frame(contenido_editor, width=ANCHO_PAGINA_PIXELES, height=550, borderwidth=1, relief="solid", bg="white")
page_frame_editor.pack(pady=10, expand=True); page_frame_editor.pack_propagate(False)
texto_usuario = scrolledtext.ScrolledText(page_frame_editor, wrap=tk.WORD, font=("Times New Roman", 12), borderwidth=0, highlightthickness=0, undo=True)
texto_usuario.pack(expand=True, fill='both', padx=10, pady=10)
texto_usuario.tag_configure("title1", font=("Times New Roman", 12, "bold"), justify='center')
texto_usuario.tag_configure("title2", font=("Times New Roman", 12, "bold"))

#---------------------PANTALLA DE REFERENCIAS-------------------------------
pantalla_referencias = tk.Frame(contenedor_principal, bg="#DDEBF7")
panel_navegacion_referencias = crear_panel_navegacion(pantalla_referencias)
contenido_referencias = tk.Frame(pantalla_referencias, bg="#DDEBF7"); contenido_referencias.pack(side="right", fill="both", expand=True)
ribbon_referencias = crear_ribbon(contenido_referencias, es_editor_principal=False); ribbon_referencias.pack(fill='x')
page_frame_ref = tk.Frame(contenido_referencias, width=ANCHO_PAGINA_PIXELES, height=550, borderwidth=1, relief="solid", bg="white")
page_frame_ref.pack(pady=10, expand=True); page_frame_ref.pack_propagate(False)
texto_referencias = scrolledtext.ScrolledText(page_frame_ref, wrap=tk.WORD, font=("Times New Roman", 12), borderwidth=0, highlightthickness=0, undo=True)
texto_referencias.pack(expand=True, fill='both', padx=10, pady=10)

#----------------------------INICIO DE LA APLICACION--------------------------
# Atajos de teclado
ventana.bind('<Control-z>', undo_action)
ventana.bind('<Control-y>', redo_action)
ventana.bind('<Control-g>', iniciar_generacion)
ventana.bind('<Control-t>', make_line_title)
ventana.bind('<Control-d>', make_line_subtitle)

mostrar_pantalla(pantalla_menu)

if __name__ == "__main__":
    ventana.mainloop()