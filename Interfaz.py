from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from Analizador import Analizador


class Interfaz(Tk):
    def __init__(self):
        super().__init__()
        # VARIABLES
        self.ruta_archivo = None
        self.lista_errores = []
        self.lista_tokens = []
        self.traduccion = ""
        # VENTANA
        self.title("Proyecto 2 - LFP")
        self.resizable(False, False)
        self.geometry("1000x800")
        # CENTRAR VENTANA
        self.update_idletasks()
        x = int((self.winfo_screenwidth() - self.winfo_width()) / 2)
        y = int((self.winfo_screenheight() - self.winfo_height()) / 2)
        self.geometry("+{}+{}".format(x, y))
        # Configuraciones
        self.crear_menu()
        self.crear_frames()
        self.crear_frame_consola()
        self.crear_frame_tokens()
        self.crear_frame_errores()

    def crear_menu(self):
        # FRAME MENU
        frame_menu = Frame(self, height=40)
        frame_menu.pack(fill="x", side=TOP)
        # FRAME CONTENIDO
        archivo = Menubutton(frame_menu, text="Archivo")
        analisis = Menubutton(frame_menu, text="Analisis")
        tokens = Menubutton(frame_menu, text="Tokens")
        errores = Menubutton(frame_menu, text="Errores")
        archivo.pack(side=LEFT)
        analisis.pack(side=LEFT)
        tokens.pack(side=LEFT)
        errores.pack(side=LEFT)
        # MENUS
        menu_archivo = Menu(archivo, tearoff=0)
        archivo.config(menu=menu_archivo)
        menu_analisis = Menu(analisis, tearoff=0)
        analisis.config(menu=menu_analisis)
        menu_tokens = Menu(tokens, tearoff=0)
        tokens.config(menu=menu_tokens)
        menu_errores = Menu(errores, tearoff=0)
        errores.config(menu=menu_errores)
        # OPCIONES ARCHIVO
        menu_archivo.add_command(label="Nuevo", command=self.nuevo_archivo)
        menu_archivo.add_command(label="Abrir", command=self.abrir_archivo)
        menu_archivo.add_command(label="Guardar", command=self.guardar_archivo)
        menu_archivo.add_command(
            label="Guardar como", command=self.guardar_archivo_como
        )
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.destroy)
        # OPCIONES ANALISIS
        menu_analisis.add_command(
            label="Generar sentencias MongoDB", command=self.analizar
        )
        # OPCIONES TOKENS
        menu_tokens.add_command(label="Ver tokens", command=self.ver_tokens)
        # OPCIONES ERRORES
        menu_errores.add_command(label="Ver errores", command=self.ver_errores)

    def ver_tokens(self):
        self.frame_tabs.select(self.tab_tokens)

    def ver_errores(self):
        self.frame_tabs.select(self.tab_errores)

    def crear_frames(self):
        # FRAME RUTA
        frame_ruta = Frame(self)
        frame_ruta.pack(fill="both", padx=25, pady=10)
        # RUTA -> CONTENIDO
        label_ruta = Label(frame_ruta, text="Ruta:")
        label_ruta.pack(side=LEFT, padx=(0, 20))
        self.entry_ruta = Entry(frame_ruta)
        self.entry_ruta.pack(side=LEFT, fill="x", expand=True)
        self.entry_ruta.config(state="readonly")
        # FRAME NOTEBOOK
        self.frame_tabs = ttk.Notebook(self)
        notebook_style = ttk.Style()
        notebook_style.configure("TNotebook.Tab", font=("Arial", 10))
        self.frame_tabs.pack(fill="both", expand=True)
        # PESTAÑAS
        self.tab_consola = Frame(self.frame_tabs)
        self.tab_tokens = Frame(self.frame_tabs)
        self.tab_errores = Frame(self.frame_tabs)
        self.frame_tabs.add(self.tab_consola, text="Consola")
        self.frame_tabs.add(self.tab_tokens, text="Tokens")
        self.frame_tabs.add(self.tab_errores, text="Errores")

    def crear_frame_consola(self):
        # TAB CONSOLA -> CONTENIDO
        frame_entrada = Frame(self.tab_consola)
        frame_salida = Frame(self.tab_consola)
        frame_ubicacion = Frame(self.tab_consola, height=40)
        frame_ubicacion.pack(fill="both", side=BOTTOM)
        frame_entrada.pack(
            side=LEFT, fill="both", expand=True, padx=(20, 10), pady=(10, 15)
        )
        frame_salida.pack(
            side=LEFT, fill="both", expand=True, padx=(10, 20), pady=(10, 15)
        )
        # CONSOLA -> ENTRADA
        titulo = Label(frame_entrada, text="Entrada:", font=("Arial", 11))
        titulo.pack(side=TOP, anchor=W, padx=(0, 20))
        self.textarea_consola = Text(
            frame_entrada, font=("Arial", 11), width=50, wrap="none"
        )
        # TEXTAREA -> SCROLLBAR
        scroll_y = Scrollbar(frame_entrada, command=self.textarea_consola.yview)
        scroll_x = Scrollbar(
            frame_entrada, command=self.textarea_consola.xview, orient="horizontal"
        )
        scroll_y.pack(side=RIGHT, fill="y")
        scroll_x.pack(side=BOTTOM, fill="x")
        self.textarea_consola.config(
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        self.textarea_consola.pack(fill="both", expand=True, side=LEFT)
        # CONSOLA -> BINDS -> TEXTAREA
        self.textarea_consola.bind("<KeyRelease>", self.obtener_ubicacion)
        self.textarea_consola.bind("<ButtonRelease>", self.obtener_ubicacion)
        self.textarea_consola.bind("<FocusIn>", self.obtener_ubicacion)
        self.textarea_consola.bind("<Motion>", self.obtener_ubicacion)
        # CONSOLA -> SALIDA
        titulo = Label(frame_salida, text="Salida:", font=("Arial", 11))
        titulo.pack(side=TOP, anchor=W, padx=(0, 20))
        self.textarea_salida = Text(
            frame_salida,
            font=("Arial", 11),
            width=50,
            wrap="none",
            state="disabled",
            bg="#F0F0F0",
        )
        # TEXTAREA -> SCROLLBAR
        scroll_y = Scrollbar(frame_salida, command=self.textarea_salida.yview)
        scroll_x = Scrollbar(
            frame_salida, command=self.textarea_salida.xview, orient="horizontal"
        )
        scroll_y.pack(side=RIGHT, fill="y")
        scroll_x.pack(side=BOTTOM, fill="x")
        self.textarea_salida.config(
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        self.textarea_salida.pack(fill="both", expand=True, side=LEFT)

        # CONSOLA -> UBICACION
        self.label_ubicacion = Label(
            frame_ubicacion,
            text="Fila: 1\nColumna: 1",
            font=("Arial", 10),
            justify=LEFT,
        )
        self.label_ubicacion.pack(side=LEFT, padx=25, pady=(0, 15))

    def crear_frame_tokens(self):
        # TAB ERRORES -> CONTENIDO
        frame_tabla = Frame(self.tab_tokens)
        frame_tabla.pack(fill="both", expand=True)
        label_titulo = Label(frame_tabla, text="Tabla de Tokens", font=("Arial", 14))
        label_titulo.pack(side=TOP, anchor=W, padx=25, pady=(25, 0))
        # TABLA -> TOKENS
        self.table_tokens = ttk.Treeview(frame_tabla, columns=("c1", "c2", "c3", "c4"))
        # Ajustar el ancho de cada columna
        self.table_tokens.column("#0", width=50)
        self.table_tokens.column("c1", anchor="center")
        self.table_tokens.column("c2", anchor="center")
        self.table_tokens.column("c3", anchor="center")
        self.table_tokens.column("c4", anchor="center")

        # Agregar encabezados de columna
        self.table_tokens.heading("#0", text="No.")
        self.table_tokens.heading("c1", text="Token")
        self.table_tokens.heading("c2", text="Fila")
        self.table_tokens.heading("c3", text="Columna")
        self.table_tokens.heading("c4", text="Lexema")

        # Agregar barras de desplazamiento
        scroll_x = Scrollbar(
            frame_tabla, orient=HORIZONTAL, command=self.table_tokens.xview
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y = Scrollbar(
            frame_tabla, orient=VERTICAL, command=self.table_tokens.yview
        )
        scroll_y.pack(side=RIGHT, fill=Y)
        self.table_tokens.configure(
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )
        # Agregar la tabla
        self.table_tokens.pack(fill="both", expand=True, padx=25, pady=(0, 25))

    def crear_frame_errores(self):
        # TAB ERRORES -> CONTENIDO
        frame_tabla = Frame(self.tab_errores)
        frame_tabla.pack(fill="both", expand=True)
        label_titulo = Label(frame_tabla, text="Tabla de Errores", font=("Arial", 14))
        label_titulo.pack(side=TOP, anchor=W, padx=25, pady=(25, 0))
        # TABLA -> TOKENS
        self.table_errores = ttk.Treeview(
            frame_tabla, columns=("c1", "c2", "c3", "c4", "c5")
        )
        # Ajustar el ancho de cada columna
        self.table_errores.column("#0", width=50)
        self.table_errores.column("c1", width=100, anchor="center")
        self.table_errores.column("c2", width=50, anchor="center")
        self.table_errores.column("c3", width=50, anchor="center")
        self.table_errores.column("c4", anchor="center")
        self.table_errores.column("c5", anchor="center")

        # Agregar encabezados de columna
        self.table_errores.heading("#0", text="No.")
        self.table_errores.heading("c1", text="Tipo de Error")
        self.table_errores.heading("c2", text="Fila")
        self.table_errores.heading("c3", text="Columna")
        self.table_errores.heading("c4", text="Token Esperado")
        self.table_errores.heading("c5", text="Descripcion")

        # Agregar barras de desplazamiento
        scroll_x = Scrollbar(
            frame_tabla, orient=HORIZONTAL, command=self.table_errores.xview
        )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y = Scrollbar(
            frame_tabla, orient=VERTICAL, command=self.table_errores.yview
        )
        scroll_y.pack(side=RIGHT, fill=Y)
        self.table_errores.configure(
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )
        # Agregar la tabla
        self.table_errores.pack(fill="both", expand=True, padx=25, pady=(0, 25))

    def obtener_ubicacion(self, event):
        fila, columna = self.textarea_consola.index(INSERT).split(".")
        self.label_ubicacion.config(text=f"Fila: {fila}\nColumna: {columna}")

    def abrir_archivo(self):
        self.ruta_archivo = askopenfilename(
            filetypes=[
                ("Todos los archivos", "*.*"),
                ("Archivos de texto", "*.txt"),
                ("Archivos JSON", "*.json"),
            ]
        )
        if self.ruta_archivo:
            # CAMBIAR RUTA EN CAMPO RUTA
            self.entry_ruta.config(state="normal")
            self.entry_ruta.delete(0, END)
            self.entry_ruta.insert(0, self.ruta_archivo)
            self.entry_ruta.config(state="readonly")
            # LEER ARCHIVO
            self.leer_archivo(self.ruta_archivo)

    def leer_archivo(self, ruta):
        self.textarea_consola.delete(1.0, END)
        try:
            contenido = ""
            archivo = open(ruta, "r")
            lineas = archivo.readlines()
            for linea in lineas:
                contenido += linea
            archivo.close()
            contenido += "\n"
            self.textarea_consola.insert(END, contenido)
        except:
            showerror("Error", "No se pudo leer el archivo.")

    def analizar(self):
        self.table_tokens.delete(*self.table_tokens.get_children())
        self.table_errores.delete(*self.table_errores.get_children())
        texto = self.textarea_consola.get(1.0, END)
        if texto:
            analizado = Analizador(texto)
            analizado.analizar()
            self.lista_errores = analizado.listaErrores
            self.lista_tokens = analizado.listaTokens
            if self.lista_errores:
                self.textarea_salida.config(state="normal")
                self.textarea_salida.delete(1.0, END)
                self.textarea_salida.config(state="disabled")
                showwarning("Advertencia", "Se encontraron errores en el texto.")
                self.agregar_tokens_en_tabla()
                self.agregar_errores_en_tabla()
                self.frame_tabs.select(self.tab_errores)
            else:
                self.traduccion = analizado.traduccion
                self.traducir()
                self.agregar_tokens_en_tabla()
                self.agregar_errores_en_tabla()
        else:
            showerror("Error", "No hay texto para analizar.")

    def traducir(self):
        self.textarea_salida.config(state="normal")
        self.textarea_salida.delete(1.0, END)
        self.textarea_salida.insert(END, self.traduccion)
        self.textarea_salida.config(state="disabled")

    def agregar_tokens_en_tabla(self):
        no = 0
        for tkn in self.lista_tokens:
            no += 1
            self.table_tokens.insert(
                "",
                no,
                text=no,
                values=(
                    tkn.getToken(),
                    tkn.getFila(),
                    tkn.getColumna(),
                    tkn.getLexema(),
                ),
            )

    def agregar_errores_en_tabla(self):
        no = 0
        for err in self.lista_errores:
            no += 1
            self.table_errores.insert(
                "",
                no,
                text=no,
                values=(
                    err.getTipo(),
                    err.getFila(),
                    err.getColumna(),
                    err.getToken(),
                    err.getDescripcion(),
                ),
            )

    def guardar_archivo(self):
        if self.ruta_archivo:
            archivo = open(self.ruta_archivo, "w")
            archivo.write(self.textarea_consola.get(1.0, END))
            archivo.close()
            showinfo("Exito", "Archivo guardado exitosamente.")
        else:
            self.guardar_archivo_como()

    def guardar_archivo_como(self):
        nueva_ruta = asksaveasfilename(
            filetypes=[
                ("Todos los archivos", "*.*"),
                ("Archivos de texto", "*.txt"),
                ("Archivos JSON", "*.json"),
            ],
            defaultextension=".txt",
        )
        if nueva_ruta:
            # GUARDAR ARCHIVO
            archivo = open(nueva_ruta, "w")
            archivo.write(self.textarea_consola.get("1.0", END))
            archivo.close()
            # CAMBIAR RUTA EN CAMPO RUTA
            self.ruta_archivo = nueva_ruta
            self.entry_ruta.config(state="normal")
            self.entry_ruta.delete(0, END)
            self.entry_ruta.insert(0, self.ruta_archivo)
            self.entry_ruta.config(state="disabled")
            showinfo("Exito", f"El archivo se guardo correctamente en: \n{nueva_ruta}")

    def nuevo_archivo(self):
        self.ruta_archivo = ""

        self.entry_ruta.config(state="normal")
        self.entry_ruta.delete(0, END)
        self.entry_ruta.config(state="disabled")

        self.textarea_consola.delete(1.0, END)

        self.textarea_salida.config(state="normal")
        self.textarea_salida.delete(1.0, END)
        self.textarea_salida.config(state="disabled")

        self.table_tokens.delete(*self.table_tokens.get_children())
        self.table_errores.delete(*self.table_errores.get_children())


if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()
