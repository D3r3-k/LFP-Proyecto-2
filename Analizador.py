from Clases.Error import Error
from Clases.Token import Token


lexemas_reservados = [
    "---",
    "/*",
    "*/",
    "=",
    "nueva",
    "(",
    '"',
    ",",
    ")",
    ";",
]

funciones = [
    "CrearBD",
    "EliminarBD",
    "CrearColeccion",
    "EliminarColeccion",
    "InsertarUnico",
    "ActualizarUnico",
    "EliminarUnico",
    "BuscarTodo",
    "BuscarUnico",
]


class Analizador:
    def __init__(self, cadena: str):
        self.cadena = cadena
        self.traduccion = ""
        self.fila = 1
        self.columna = 0
        self.listaTokens = []
        self.listaErrores = []

    def analizar(self):
        # Funciones para la traduccion
        funcion_actual = ""
        identificador = ""
        parametro_json = ""
        # VARIABLES DE ESTADO
        estado_actual = "S0"

        # CICLO PRINCIPAL DEL ANALIZADOR
        while self.cadena:
            # |-----[ S0 | Funcion {Comentario Simple, Multiple o Funcion}]-----|
            if estado_actual == "S0":
                lexema = self.obtener_lexema()
                if lexema == "---":
                    self.generar_token("Comentario_Simple", lexema)
                    funcion_actual = lexema
                    estado_actual = "S1"
                elif lexema == "/*":
                    self.generar_token("Abrir_Comentario_Multiple", lexema)
                    funcion_actual = lexema
                    estado_actual = "S1"
                elif lexema in funciones:
                    self.generar_token("Funcion", lexema)
                    funcion_actual = lexema
                    estado_actual = "S1"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente != "=":
                        self.generar_error("Lexico", "Funcion", lexema)
                    else:
                        self.generar_error("Sintactico", "Funcion", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S1 | Identificador {Palabra o ID}]-----|
            elif estado_actual == "S1":
                if funcion_actual == "---":
                    comentario = self.comentario_simple()
                    # print(f"Comentario ignorado: {comentario}")
                    estado_actual = "S0"
                elif funcion_actual == "/*":
                    comentario = self.comentario_multiple()
                    # print(f"Comentario ignorado: {comentario}")
                    estado_actual = "S0"
                elif funcion_actual in funciones:
                    lexema = self.obtener_lexema()
                    if self.validar_identificador(lexema):
                        self.generar_token("Identificador", lexema)
                        identificador = lexema
                        estado_actual = "S2"
                    else:
                        funcion_actual = "Error"
                        self.cadena = f"{lexema} " + self.cadena
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente != "=":
                        self.generar_error("Lexico", "Identificador", lexema)
                    else:
                        self.generar_error("Sintactico", "Identificador", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S2 | Operador Igual {=}]-----|
            elif estado_actual == "S2":
                lexema = self.obtener_lexema()
                if lexema == "=":
                    self.generar_token("Operador_Igual", lexema)
                    estado_actual = "S3"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente == "nueva":
                        self.generar_error("Lexico", "Operador_Igual", lexema)
                    else:
                        self.generar_error("Sintactico", "Operador_Igual", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S3 | Palabra Reservada {nueva}]-----|
            elif estado_actual == "S3":
                lexema = self.obtener_lexema()
                if lexema == "nueva":
                    self.generar_token("Palabra_Reservada", lexema)
                    estado_actual = "S4"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente in funciones:
                        self.generar_error("Lexico", "Palabra_Reservada", lexema)
                    else:
                        self.generar_error("Sintactico", "Palabra_Reservada", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S4 | Funcion {Funcion}]-----|
            elif estado_actual == "S4":
                lexema = self.obtener_lexema()
                if lexema in funciones and lexema == funcion_actual:
                    self.generar_token("Funcion", lexema)
                    estado_actual = "S5"
                else:
                    if lexema != funcion_actual:
                        self.generar_error("Sintactico", "Funcion", lexema)
                    else:
                        lexema_siguiente = self.obtener_lexema()
                        self.cadena = f"{lexema_siguiente} " + self.cadena
                        self.columna -= len(lexema_siguiente)
                        if lexema_siguiente == "(":
                            self.generar_error("Lexico", "Funcion", lexema)
                        else:
                            self.generar_error("Sintactico", "Funcion", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S5 | Abrir Parentesis { ( }]-----|
            elif estado_actual == "S5":
                lexema = self.obtener_lexema()
                if lexema == "(":
                    self.generar_token("Abrir_Parentesis", lexema)
                    estado_actual = "S6"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente == ")" or lexema_siguiente == ",":
                        self.generar_error("Sintactico", "Abrir_Parentesis", lexema)
                    else:
                        self.generar_error("Lexico", "Abrir_Parentesis", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S6 | Parametro_Identificador { "identificador" }]-----|
            elif estado_actual == "S6":
                lexema = self.obtener_lexema()
                if self.validar_identificador(lexema):
                    identificador = lexema
                    self.generar_token("Parametro_Identificador", lexema)
                    estado_actual = "S7"
                elif lexema == ")":
                    self.generar_token("Cerrar_Parentesis", lexema)
                    estado_actual = "SF"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente != ")" or lexema_siguiente != ",":
                        self.generar_error(
                            "Sintactico", "Parametro_Identificador", lexema
                        )
                    else:
                        self.generar_error("Lexico", "Parametro_Identificador", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S7 | Separador Coma { , }]-----|
            elif estado_actual == "S7":
                lexema = self.obtener_lexema()
                if lexema == ")":
                    self.generar_token("Cerrar_Parentesis", lexema)
                    estado_actual = "SF"
                elif lexema == ",":
                    self.generar_token("Separador_Coma", lexema)
                    estado_actual = "S8"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if (
                        lexema_siguiente != ")"
                        or lexema_siguiente != ";"
                        or lexema_siguiente != "\n"
                    ):
                        self.generar_error("Lexico", "Parametro_Json", lexema)
                    else:
                        self.generar_error("Sintactico", "Parametro_Json", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S8 | Parametro Json { "JSON" }]-----|
            elif estado_actual == "S8":
                lexema = self.armar_json()
                if self.validar_json(lexema):
                    parametro_json = lexema
                    self.generar_token("Parametro_Json", lexema)
                    estado_actual = "S9"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente != ")" or lexema_siguiente != ";":
                        self.generar_error("Lexico", "Parametro_Json", lexema)
                    else:
                        self.generar_error("Sintactico", "Parametro_Json", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ S9 | Cerrar Parentesis { ) }]-----|
            elif estado_actual == "S9":
                lexema = self.obtener_lexema()
                if lexema == ")":
                    self.generar_token("Cerrar_Parentesis", lexema)
                    estado_actual = "SF"
                else:
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema_siguiente != ";" or lexema_siguiente != "\n":
                        self.generar_error("Lexico", "Cerrar_Parentesis", lexema)
                    else:
                        self.generar_error("Sintactico", "Cerrar_Parentesis", lexema)
                    self.ignorar_funcion()
                    estado_actual = "S0"

            # |-----[ SF | Punto Coma { ; }]-----|
            elif estado_actual == "SF":
                if self.cadena[0] != "\n":
                    lexema = self.obtener_lexema()
                # Verificar que el lexema sea un punto y coma
                if lexema == ";":
                    self.generar_token("Punto_Coma", lexema)
                    estado_actual = "ST"
                else:
                    lexema = self.cadena[0]
                    lexema_siguiente = self.obtener_lexema()
                    self.cadena = f"{lexema_siguiente} " + self.cadena
                    self.columna -= len(lexema_siguiente)
                    if lexema == "\n" or lexema_siguiente == ";":
                        self.generar_error("Sintactico", "Punto_Coma", lexema)
                    else:
                        self.generar_error("Lexico", "Punto_Coma", lexema)
                    estado_actual = "S0"

            # |-----[ ST | Traduccion { Traudcciones }]-----|
            elif estado_actual == "ST":
                # traduccion
                if funcion_actual == "CrearBD":
                    self.traduccion += f"use.('{identificador}');\n"
                elif funcion_actual == "EliminarBD":
                    self.traduccion += f"db.dropDatabase();\n"
                elif funcion_actual == "CrearColeccion":
                    self.traduccion += f"db.createCollection('{identificador}');\n"
                elif funcion_actual == "EliminarColeccion":
                    self.traduccion += f"db.{identificador}.drop();\n"
                elif funcion_actual == "InsertarUnico":
                    self.traduccion += (
                        f"db.{identificador}.insertOne('{parametro_json}');\n"
                    )
                elif funcion_actual == "ActualizarUnico":
                    self.traduccion += (
                        f"db.{identificador}.updateOne('{parametro_json}');\n"
                    )
                elif funcion_actual == "EliminarUnico":
                    self.traduccion += (
                        f"db.{identificador}.deleteOne('{parametro_json}');\n"
                    )
                elif funcion_actual == "EliminarUnico":
                    self.traduccion += (
                        f"db.{identificador}.deleteOne('{parametro_json}');\n"
                    )
                elif funcion_actual == "BuscarTodo":
                    self.traduccion += f"db.{identificador}.find();\n"
                elif funcion_actual == "BuscarUnico":
                    self.traduccion += f"db.{identificador}.findOne();\n"
                estado_actual = "S0"
                identificador = ""
                funcion_actual = ""
                parametro_json = ""
            else:
                estado_actual = "S0"
                funcion_actual = ""
                identificador = ""
                parametro_json = ""

    def generar_token(self, token, lexema):
        if lexema:
            token = Token(token, lexema, self.fila, self.columna - len(lexema))
            self.listaTokens.append(token)

    def generar_error(self, tipo, token, lexema):
        if lexema:
            col = self.columna - len(lexema)
            if token == "Parametro_Json":
                col = self.columna
            error = None
            if tipo == "Sintactico":
                error = Error(
                    "Sintactico",
                    self.fila,
                    col,
                    token,
                    f"Token esperado: {token}",
                )
            elif tipo == "Lexico":
                error = Error(
                    "Lexico",
                    self.fila,
                    col,
                    token,
                    f"Lexema '{lexema}' no valido.",
                )
            self.listaErrores.append(error)

    def obtener_lexema(self):
        palabra = self.armar_palabra()
        while self.cadena and palabra in ("\n", "\t", " ", "", '"'):
            palabra = self.armar_palabra()
        return palabra

    def ignorar_funcion(self):
        while self.cadena:
            if self.cadena[0] == ";":
                self.cadena = self.cadena[1:]
                self.columna += 1
                break
            elif self.cadena[0] == "\n":
                self.fila += 1
                self.columna = 0
                self.cadena = self.cadena[1:]
            elif self.cadena[0] == "\t":
                self.columna += 4
                self.cadena = self.cadena[1:]
            else:
                self.columna += 1
                self.cadena = self.cadena[1:]

    def armar_json(self):
        json = ""
        while self.cadena:
            if self.cadena[0] == ")":
                break
            elif self.cadena[0] == "\n":
                self.fila += 1
                self.columna = 0
                self.cadena = self.cadena[1:]
            elif self.cadena[0] == "\t":
                self.columna += 4
                self.cadena = self.cadena[1:]
            else:
                json += self.cadena[0]
                self.cadena = self.cadena[1:]
        return json

    def validar_identificador(self, identificador):
        caracteres_validos = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "_",
        ]
        if identificador:
            for char in identificador:
                if char not in caracteres_validos:
                    return False
            return True
        else:
            return False

    def validar_json(self, json):
        json = json[1:-1]
        if not json:
            return False
        if json[0] not in ["{", "["] or json[-1] not in ["}", "]"]:
            return False
        temporal = []
        for char in json:
            if char in ["{", "["]:
                temporal.append(char)
            elif char in ["}", "]"]:
                if not temporal:
                    return False
                if char == "}" and temporal[-1] == "{":
                    temporal.pop()
                elif char == "]" and temporal[-1] == "[":
                    temporal.pop()
        return not temporal

    def comentario_simple(self):
        comentario = ""
        while self.cadena:
            if self.cadena[0] == "\n":
                self.cadena = self.cadena[1:]
                self.fila += 1
                self.columna = 0
                break
            else:
                comentario += self.cadena[0]
                self.cadena = self.cadena[1:]
                self.columna += 1
        return comentario

    def comentario_multiple(self):
        lexema_cierre = ""
        comentario = ""
        while self.cadena:
            if lexema_cierre == "*/":
                tkn = Token(
                    "Cerrar_Comentario_Multiple",
                    lexema_cierre,
                    self.fila,
                    self.columna - len(lexema_cierre),
                )
                self.listaTokens.append(tkn)
                break
            elif self.cadena[0] == "*" or lexema_cierre == "*":
                lexema_cierre += self.cadena[0]
                self.columna += 1
                self.cadena = self.cadena[1:]
            elif self.cadena[0] == "\n":
                comentario += self.cadena[0]
                self.fila += 1
                self.columna = 0
                self.cadena = self.cadena[1:]
            elif self.cadena[0] == "\t":
                comentario += self.cadena[0]
                self.columna += 4
                self.cadena = self.cadena[1:]
            else:
                if len(lexema_cierre) == 2:
                    lexema_cierre = ""
                comentario += self.cadena[0]
                self.columna += 1
                self.cadena = self.cadena[1:]
        return comentario

    def armar_palabra(self):
        palabra_actual = ""
        char_actual = ""
        for char in self.cadena:
            if palabra_actual in lexemas_reservados or palabra_actual in funciones:
                return palabra_actual
            elif char_actual in lexemas_reservados:
                self.cadena = char_actual + self.cadena
                return palabra_actual[:-1]
            elif char == " ":
                self.cadena = self.cadena[1:]
                self.columna += 1
                break
            elif char == "\n":
                self.cadena = self.cadena[1:]
                self.fila += 1
                self.columna = 0
                break
            elif char == "\t":
                self.cadena = self.cadena[1:]
                self.columna += 4
                break
            else:
                palabra_actual += char
                char_actual = char
                self.columna += 1
                self.cadena = self.cadena[1:]
        return palabra_actual

    def imprimir_tokens(self):
        for token in self.listaTokens:
            print(f"-------------[ {token.getToken()} ]-------------")
            print("Lexema:", token.getLexema())
            print("Fila:", token.getFila())
            print("Columna:", token.getColumna())

    def imprimir_errores(self):
        for error in self.listaErrores:
            print(f"-------------[ Error ]-------------")
            print("Tipo:", error.getTipo())
            print("Fila:", error.getFila())
            print("Columna:", error.getColumna())
            print("Token:", error.getToken())
            print("Descripcion:", error.getDescripcion())


# archivo = open("archivo.txt", "r")
# cadena = ""
# for linea in archivo.readlines():
#     cadena += linea
# archivo.close()

# analizador = Analizador(cadena)
# analizador.analizar()
