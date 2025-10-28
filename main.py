# --- Importaciones para la Interfaz Gráfica ---
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- Importación de la lógica de negocio (nuestro otro archivo) ---
from pdfGenerator import crear_documento_apa_reportlab

# --- Definición de funciones de la Interfaz ---

def iniciar_generacion():
    """
    Obtiene el texto de la interfaz y llama a la función
    de generación de PDF.
    """
    contenido = texto_usuario.get("1.0", tk.END)
    if not contenido.strip():
        messagebox.showwarning("Advertencia", "El campo de texto está vacío.")
        return
    
    # Llama a la función importada desde pdf_generator.py
    crear_documento_apa_reportlab(contenido)

# --- Ventana principal y widgets ---

# Creamos la ventana raíz
ventana = tk.Tk()
ventana.title("Generador de Documentos Avanzado")
ventana.geometry("800x600")

# Creacion y posicionamiento de los widgets
instrucciones = tk.Label(ventana, text="Escribe el contenido de tu documento:", font=("Arial", 14))
instrucciones.pack(pady=10)

texto_usuario = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=25, font=("Times New Roman", 12))
texto_usuario.pack(pady=10, padx=20, expand=True, fill='both')

boton_generar = tk.Button(ventana, text="Generar PDF", command=iniciar_generacion, font=("Arial", 12, "bold"), bg="#00529B", fg="white")
boton_generar.pack(pady=20)

# --- Iniciar el bucle principal de la aplicación ---
if __name__ == "__main__":
    ventana.mainloop()