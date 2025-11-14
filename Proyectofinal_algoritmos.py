"""
Este programa es un editor de texto con interfaz gráfica (GUI)

FUNCIONALIDADES:
- Abrir archivos de texto o código (.txt, .py, .cpp, etc.)
- Guardar y guardar como
- Buscar texto dentro del documento
- Deshacer y rehacer cambios
- Mostrar información del programa y de los integrantes
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog

class Editor:
    """Clase principal del editor de texto."""

    def __init__(self, root):
        """Inicializa la ventana principal y sus elementos."""
        self.root = root
        self.root.title("Editor de Texto") #Inidca el nombre de la ventana 
        self.root.geometry("800x600") #El tamaño de la ventana
        self.filename = None  # Almacena la ruta del archivo abierto o guardado

        # Área de texto con barra de desplazamiento y opción de deshacer/rehacer
        self.text = scrolledtext.ScrolledText(root, undo=True)
        self.text.pack(fill="both", expand=True)

        # Crear la barra de menús
        self.crear_menu()

    # CREACIÓN DEL MENÚ PRINCIPAL
    def crear_menu(self):
        """Crea los menús Archivo, Editar y Ayuda."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú Archivo: abrir, guardar, guardar como y salir
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Abrir", command=self.abrir)
        archivo_menu.add_command(label="Guardar", command=self.guardar)
        archivo_menu.add_command(label="Guardar como", command=self.guardar_como)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        # Menú Editar: deshacer, rehacer y buscar
        editar_menu = tk.Menu(menubar, tearoff=0)
        editar_menu.add_command(label="Deshacer", command=self.text.edit_undo)
        editar_menu.add_command(label="Rehacer", command=self.text.edit_redo)
        editar_menu.add_separator()
        editar_menu.add_command(label="Buscar", command=self.buscar_texto)
        menubar.add_cascade(label="Editar", menu=editar_menu)

        # Menú Ayuda: información e integrantes
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        ayuda_menu.add_command(label="Información", command=self.mostrar_info)
        ayuda_menu.add_command(label="Integrantes", command=self.mostrar_integrantes)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)

    # FUNCIONES DEL MENÚ ARCHIVO
    
    def abrir(self):
        """Permite seleccionar y abrir un archivo de texto."""
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt *.py *.cpp *.cs"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                # Mostrar contenido en el área de texto
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, contenido)
                self.filename = ruta
                self.root.title(f"Editor de Texto - {ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar(self):
        """Guarda los cambios en el archivo actual."""
        if not self.filename:
            self.guardar_como()
            return
        try:
            contenido = self.text.get(1.0, tk.END)
            with open(self.filename, "w", encoding="utf-8") as archivo:
                archivo.write(contenido)
            messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def guardar_como(self):
        """Guarda el contenido del área de texto en un nuevo archivo."""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                contenido = self.text.get(1.0, tk.END)
                with open(ruta, "w", encoding="utf-8") as archivo:
                    archivo.write(contenido)
                self.filename = ruta
                self.root.title(f"Editor de Texto - {ruta}")
                messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    # FUNCIÓN DE BÚSQUEDA DE TEXTO

    def buscar_texto(self):
        """Busca una palabra dentro del texto y la resalta si se encuentra."""
        palabra = simpledialog.askstring("Buscar", "Ingrese la palabra a buscar:")
        if palabra:
            contenido = self.text.get(1.0, tk.END)
            inicio = contenido.find(palabra)
            if inicio == -1:
                messagebox.showinfo("Buscar", "No se encontró la palabra.")
            else:
                # Resalta la primera ocurrencia encontrada
                pos_inicio = f"1.0 + {inicio} chars"
                pos_final = f"1.0 + {inicio + len(palabra)} chars"
                self.text.tag_remove("highlight", "1.0", tk.END)
                self.text.tag_add("highlight", pos_inicio, pos_final)
                self.text.tag_config("highlight", background="yellow")
                self.text.see(pos_inicio)


    # MENÚ AYUDA: INFORMACIÓN E INTEGRANTES

    def mostrar_info(self):
        """Muestra información general del programa."""
        info = (
            "Editor de Texto - Proyecto IV (Versión Simple)\n"
            "Funciones:\n"
            "- Abrir / Guardar / Guardar como\n"
            "- Buscar texto\n"
            "- Deshacer / Rehacer\n"
            "Licencia: Uso educativo\n"
            "- Vension 2.0 \n"
            "Autor: Keneth Rodas"
        )
        messagebox.showinfo("Información", info)

    def mostrar_integrantes(self):
        """Muestra la información de los integrantes del grupo."""
        integrantes = (
            "Integrantes:\n"
            "- Keneth Rodas - Carné: 7690-25-4173\n"
        )
        messagebox.showinfo("Integrantes", integrantes)

# BLOQUE PRINCIPAL DEL PROGRAMA

if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    app = Editor(root)
    root.mainloop()
