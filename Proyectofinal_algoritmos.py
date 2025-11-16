"""
Este programa es un editor de texto con interfaz gráfica (GUI)

FUNCIONALIDADES:
- Abrir archivos de texto o código (.txt, .py, .cpp, etc.)
- Guardar y guardar como
- Buscar texto dentro del documento
- Deshacer y rehacer cambios
- Mostrar información del programa y de los integrantes
"""

import tkinter as tk #sirve para crear toda la interfaz gráfica (ventanas, botones, menús, etc.)
from tkinter import filedialog, messagebox, scrolledtext, simpledialog #Estas sirven para abrir/guardar archivos, mostrar mensajes, área de texto con scroll, pedir una palabra al usuario

class Editor:
    """Clase principal del editor de texto."""

    def __init__(self, root): # Método que se ejecuta al crear el editor.
        """Inicializa la ventana principal y sus elementos."""
        self.root = root # Guarda la ventana principal dentro de la clase.
        self.root.title("Editor de Texto") # Inidca el nombre de la ventana 
        self.root.geometry("800x600") # El tamaño de la ventana
        self.filename = None  # Guarda la ruta del archivo actual.

        # Área de texto con barra de desplazamiento y opción de deshacer/rehacer
        self.text = scrolledtext.ScrolledText(root, undo=True)# Crea un cuadro de texto grande con barra de desplazamiento. donde permite deshacer y rehacer.
        self.text.pack(fill="both", expand=True)# Hace que el área de texto ocupe todo el espacio disponible.

        # Crear la barra de menús
        self.crear_menu()

    # CREACIÓN DEL MENÚ PRINCIPAL
    def crear_menu(self): # Define la función encargada de armar los menús.
        """Crea los menús Archivo, Editar y Ayuda."""
        menubar = tk.Menu(self.root)# Crea la barra de menú
        self.root.config(menu=menubar)# asigna a la ventana.

        # Menú Archivo: abrir, guardar, guardar como y salir
        archivo_menu = tk.Menu(menubar, tearoff=0)#Crea el submenú Archivo tearoff=0 evita que se pueda “arrancar” el menú.
        archivo_menu.add_command(label="Abrir", command=self.abrir)# Agrega opción "Abrir" que llama a la función abrir().
        archivo_menu.add_command(label="Guardar", command=self.guardar)# guardan archivos
        archivo_menu.add_command(label="Guardar como", command=self.guardar_como)# guardan archivos
        archivo_menu.add_separator() #Inserta una línea separadora.
        archivo_menu.add_command(label="Salir", command=self.root.quit)#Cierra la aplicación.
        menubar.add_cascade(label="Archivo", menu=archivo_menu)# Agrega el submenú completo a la barra.

        # Menú Editar: deshacer, rehacer y buscar
        editar_menu = tk.Menu(menubar, tearoff=0)
        editar_menu.add_command(label="Deshacer", command=self.text.edit_undo)
        editar_menu.add_command(label="Rehacer", command=self.text.edit_redo)
        editar_menu.add_separator()# Añade separador.
        editar_menu.add_command(label="Buscar", command=self.buscar_texto)# Llama a la función que busca una palabra.
        menubar.add_cascade(label="Editar", menu=editar_menu)

        # Menú Ayuda: información e integrantes
        ayuda_menu = tk.Menu(menubar, tearoff=0)# Crea menú de ayuda.
        ayuda_menu.add_command(label="Información", command=self.mostrar_info)
        ayuda_menu.add_command(label="Integrantes", command=self.mostrar_integrantes)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)

    # FUNCIONES DEL MENÚ ARCHIVO
    
    def abrir(self):
        """Permite seleccionar y abrir un archivo de texto."""
        ruta = filedialog.askopenfilename( #Muestra una ventana para seleccionar un archivo.
            filetypes=[("Archivos de texto", "*.txt *.py *.cpp *.cs"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as archivo:# Abre el archivo y lee todo su contenido.
                    contenido = archivo.read()
                # Mostrar contenido en el área de texto
                self.text.delete(1.0, tk.END)# Limpia el área de texto.
                self.text.insert(tk.END, contenido)# Muestra el contenido del archivo.
                self.filename = ruta # Guarda la ruta del archivo.
                self.root.title(f"Editor de Texto - {ruta}")# Cambia el título de la ventana para mostrar el nombre del archivo.
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar(self):
        """Guarda los cambios en el archivo actual."""
        if not self.filename:
            self.guardar_como()# Si no hay archivo abierto, usa “Guardar como”.
            return
        try:
            contenido = self.text.get(1.0, tk.END)# Obtiene todo el texto escrito
            with open(self.filename, "w", encoding="utf-8") as archivo:# Lectura de archivos
                archivo.write(contenido)# Escribe el contenido en el archivo.
            messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def guardar_como(self):
        """Guarda el contenido del área de texto en un nuevo archivo."""
        ruta = filedialog.asksaveasfilename(# Permite escoger nombre y ubicación del archivo.
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
        palabra = simpledialog.askstring("Buscar", "Ingrese la palabra a buscar:")# Pide la palabra a buscar
        if palabra:
            contenido = self.text.get(1.0, tk.END)
            inicio = contenido.find(palabra)# Busca la palabra dentro del texto.
            if inicio == -1:
                messagebox.showinfo("Buscar", "No se encontró la palabra.")
            else:
                # Resalta la primera ocurrencia encontrada
                pos_inicio = f"1.0 + {inicio} chars"
                pos_final = f"1.0 + {inicio + len(palabra)} chars"# Calcula la posición exacta donde está.
                self.text.tag_remove("highlight", "1.0", tk.END) # Sirve para resaltar el texto seleccionado
                self.text.tag_add("highlight", pos_inicio, pos_final)
                self.text.tag_config("highlight", background="yellow")# Pone de color amarillo el texto
                self.text.see(pos_inicio)


    # MENÚ AYUDA: INFORMACIÓN E INTEGRANTES

    def mostrar_info(self):
        """Muestra información general del programa."""
        info = (
            "Editor de Texto - Proyecto Final de algoritmos\n"
            "Funciones:\n"
            "- Abrir / Guardar / Guardar como\n"
            "- Buscar texto\n"
            "- Deshacer / Rehacer\n"
            "Licencia: Premium\n"
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

if __name__ == "__main__": #Se ejecutara solo se abre el archivo directamente (no importado).
    # Crear la ventana principal
    root = tk.Tk()# Crea la ventana
    app = Editor(root)# Crea el editor dentro de esa ventana 
    root.mainloop()# Mantiene la ventana abierta 
