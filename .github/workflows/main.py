import os
import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer
)


# ============================================================
# COLORES
# ============================================================

AZUL = "#0D47A1"
AZUL_CLARO = "#1976D2"
VERDE = "#2E7D32"
ROJO = "#C62828"
NARANJA = "#EF6C00"
BLANCO = "#FFFFFF"
NEGRO = "#212121"
GRIS = "#ECEFF1"
GRIS_OSCURO = "#455A64"
GRIS_CLARO = "#F5F7F9"


# ============================================================
# APLICACIÓN
# ============================================================

class ControlAcceso(App):

    def build(self):

        self.title = "Control de Acceso"
        self.registro_id = None
        self.foto_bytes = None

        self.crear_base_datos()

        principal = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        encabezado = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(85),
            padding=[dp(10), dp(8)]
        )

        titulo = Label(
            text="CONTROL DE ACCESO",
            font_size="23sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)
        )

        subtitulo = Label(
            text="Registro y control de personas",
            font_size="14sp",
            color=(1, 1, 1, 1)
        )

        encabezado.add_widget(titulo)
        encabezado.add_widget(subtitulo)

        principal.add_widget(
            self.color_layout(encabezado, AZUL)
        )

        # ----------------------------------------------------
        # HORA
        # ----------------------------------------------------

        hora_box = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        hora_box.add_widget(
            Label(
                text="HORA",
                size_hint_x=None,
                width=dp(90),
                bold=True,
                color=self.rgb(NEGRO)
            )
        )

        self.hora = TextInput(
            readonly=True,
            multiline=False,
            font_size="16sp"
        )

        hora_box.add_widget(self.hora)
        principal.add_widget(hora_box)

        Clock.schedule_interval(self.actualizar_hora, 1)
        self.actualizar_hora()

        # ----------------------------------------------------
        # CAMPOS
        # ----------------------------------------------------

        campos = GridLayout(
            cols=2,
            spacing=dp(7),
            size_hint_y=None,
            padding=[dp(3), dp(3)]
        )

        campos.bind(minimum_height=campos.setter("height"))

        # Persona
        campos.add_widget(self.etiqueta("PERSONA"))
        self.persona = TextInput(
            multiline=False,
            font_size="16sp"
        )
        campos.add_widget(self.persona)

        # RUT
        campos.add_widget(self.etiqueta("RUT"))
        self.rut = TextInput(
            multiline=False,
            font_size="16sp"
        )
        campos.add_widget(self.rut)

        # Vehículo
        campos.add_widget(self.etiqueta("VEHÍCULO"))

        self.vehiculo = Spinner(
            text="Automovil",
            values=(
                "Automovil",
                "Camioneta",
                "SUV",
                "Moto",
                "Furgon",
                "Camion",
                "Otro"
            ),
            font_size="16sp"
        )

        campos.add_widget(self.vehiculo)

        # Marca
        campos.add_widget(self.etiqueta("MARCA"))
        self.marca = TextInput(
            multiline=False,
            font_size="16sp"
        )
        campos.add_widget(self.marca)

        # Modelo
        campos.add_widget(self.etiqueta("MODELO"))
        self.modelo = TextInput(
            multiline=False,
            font_size="16sp"
        )
        campos.add_widget(self.modelo)

        # Patente
        campos.add_widget(self.etiqueta("PATENTE"))
        self.patente = TextInput(
            multiline=False,
            font_size="16sp"
        )
        campos.add_widget(self.patente)

        # Color
        campos.add_widget(self.etiqueta("COLOR"))
        self.color = TextInput(
            multiline=False,
            font_size="16sp"
        )
        campos.add_widget(self.color)

        # Departamento
        campos.add_widget(self.etiqueta("DEPARTAMENTO"))
        self.departamento = TextInput(
            multiline=False,
            font_size="16sp"
        )
        campos.add_widget(self.departamento)

        scroll_campos = ScrollView(
            size_hint_y=0.43
        )

        scroll_campos.add_widget(campos)
        principal.add_widget(scroll_campos)

        # ----------------------------------------------------
        # FOTO DE PATENTE
        # ----------------------------------------------------

        self.foto_label = Label(
            text="FOTO DE PATENTE: No capturada",
            size_hint_y=None,
            height=dp(35),
            font_size="14sp",
            color=self.rgb(GRIS_OSCURO)
        )

        principal.add_widget(self.foto_label)

        botones_foto = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(6)
        )

        boton_foto = Button(
            text="📷 TOMAR FOTO PATENTE",
            background_color=self.rgb(AZUL_CLARO),
            bold=True
        )

        boton_foto.bind(on_press=self.abrir_camara)

        botones_foto.add_widget(boton_foto)

        principal.add_widget(botones_foto)

        # ----------------------------------------------------
        # BOTONES PRINCIPALES
        # ----------------------------------------------------

        botones = GridLayout(
            cols=4,
            spacing=dp(5),
            size_hint_y=None,
            height=dp(52)
        )

        b_ingresar = Button(
            text="I\nINGRESAR",
            background_color=self.rgb(VERDE),
            bold=True
        )
        b_ingresar.bind(on_press=self.ingresar)

        b_buscar = Button(
            text="B\nBUSCAR",
            background_color=self.rgb(AZUL_CLARO),
            bold=True
        )
        b_buscar.bind(on_press=self.abrir_busqueda)

        b_eliminar = Button(
            text="E\nELIMINAR",
            background_color=self.rgb(ROJO),
            bold=True
        )
        b_eliminar.bind(on_press=self.eliminar)

        b_modificar = Button(
            text="M\nMODIFICAR",
            background_color=self.rgb(NARANJA),
            bold=True
        )
        b_modificar.bind(on_press=self.modificar)

        botones.add_widget(b_ingresar)
        botones.add_widget(b_buscar)
        botones.add_widget(b_eliminar)
        botones.add_widget(b_modificar)

        principal.add_widget(botones)

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        botones_pdf = GridLayout(
            cols=2,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(50)
        )

        b_pdf = Button(
            text="IMPRIMIR REGISTRO",
            background_color=self.rgb(GRIS_OSCURO),
            bold=True
        )
        b_pdf.bind(on_press=self.pdf_individual)

        b_pdf_todos = Button(
            text="IMPRIMIR TODOS",
            background_color=self.rgb(GRIS_OSCURO),
            bold=True
        )
        b_pdf_todos.bind(on_press=self.pdf_general)

        botones_pdf.add_widget(b_pdf)
        botones_pdf.add_widget(b_pdf_todos)

        principal.add_widget(botones_pdf)

        # ----------------------------------------------------
        # BOTONES INFERIORES
        # ----------------------------------------------------

        inferiores = GridLayout(
            cols=2,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(48)
        )

        limpiar = Button(
            text="LIMPIAR CAMPOS",
            background_color=self.rgb(GRIS_OSCURO),
            bold=True
        )
        limpiar.bind(on_press=self.limpiar)

        salir = Button(
            text="SALIR",
            background_color=self.rgb(ROJO),
            bold=True
        )
        salir.bind(on_press=self.salir)

        inferiores.add_widget(limpiar)
        inferiores.add_widget(salir)

        principal.add_widget(inferiores)

        return principal

    # ========================================================
    # UTILIDADES DE INTERFAZ
    # ========================================================

    def rgb(self, hexadecimal):

        hexadecimal = hexadecimal.replace("#", "")

        return (
            int(hexadecimal[0:2], 16) / 255,
            int(hexadecimal[2:4], 16) / 255,
            int(hexadecimal[4:6], 16) / 255,
            1
        )

    def color_layout(self, widget, color):

        from kivy.graphics import Color, Rectangle

        with widget.canvas.before:
            Color(*self.rgb(color))
            rect = Rectangle(
                pos=widget.pos,
                size=widget.size
            )

        widget.bind(
            pos=lambda instance, value: setattr(
                rect, "pos", value
            )
        )

        widget.bind(
            size=lambda instance, value: setattr(
                rect, "size", value
            )
        )

        return widget

    def etiqueta(self, texto):

        return Label(
            text=texto,
            bold=True,
            color=self.rgb(NEGRO),
            size_hint_y=None,
            height=dp(42),
            halign="left",
            valign="middle"
        )

    # ========================================================
    # BASE DE DATOS
    # ========================================================

    def ruta_db(self):

        return os.path.join(
            self.user_data_dir,
            "control_acceso.db"
        )

    def conectar(self):

        return sqlite3.connect(self.ruta_db())

    def crear_base_datos(self):

        con = self.conectar()
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hora TEXT NOT NULL,
                persona TEXT NOT NULL,
                rut TEXT,
                vehiculo TEXT,
                marca TEXT,
                modelo TEXT,
                patente TEXT,
                color TEXT,
                departamento TEXT,
                foto_patente BLOB
            )
        """)

        con.commit()
        con.close()

    # ========================================================
    # HORA
    # ========================================================

    def actualizar_hora(self, *args):

        if hasattr(self, "hora"):
            self.hora.text = datetime.now().strftime(
                "%d/%m/%Y  %H:%M:%S"
            )

    # ========================================================
    # INGRESAR
    # ========================================================

    def ingresar(self, *args):

        persona = self.persona.text.strip()

        if not persona:
            self.mensaje(
                "Falta información",
                "Debe ingresar el nombre de la persona."
            )
            return

        con = self.conectar()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO registros
            (
                hora,
                persona,
                rut,
                vehiculo,
                marca,
                modelo,
                patente,
                color,
                departamento,
                foto_patente
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%d/%m/%Y  %H:%M:%S"),
            persona,
            self.rut.text.strip(),
            self.vehiculo.text,
            self.marca.text.strip(),
            self.modelo.text.strip(),
            self.patente.text.strip().upper(),
            self.color.text.strip(),
            self.departamento.text.strip(),
            self.foto_bytes
        ))

        con.commit()
        con.close()

        self.mensaje(
            "Registro ingresado",
            "El registro fue guardado correctamente."
        )

        self.limpiar()

    # ========================================================
    # BÚSQUEDA
    # ========================================================

    def abrir_busqueda(self, *args):

        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        entrada = TextInput(
            hint_text="ID, nombre, RUT, patente, departamento...",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size="16sp"
        )

        contenido.add_widget(entrada)

        resultados = GridLayout(
            cols=1,
            spacing=dp(5),
            size_hint_y=None
        )
        resultados.bind(
            minimum_height=resultados.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(resultados)

        contenido.add_widget(scroll)

        botones = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(5)
        )

        buscar = Button(
            text="BUSCAR",
            background_color=self.rgb(AZUL_CLARO)
        )

        cerrar = Button(
            text="CERRAR",
            background_color=self.rgb(ROJO)
        )

        botones.add_widget(buscar)
        botones.add_widget(cerrar)

        contenido.add_widget(botones)

        popup = Popup(
            title="BUSCAR REGISTRO",
            content=contenido,
            size_hint=(0.95, 0.85)
        )

        cerrar.bind(on_press=popup.dismiss)

        def ejecutar_busqueda(instance):

            texto = entrada.text.strip()

            if not texto:
                return

            con = self.conectar()
            cur = con.cursor()

            patron = "%" + texto + "%"

            cur.execute("""
                SELECT
                    id,
                    hora,
                    persona,
                    rut,
                    vehiculo,
                    marca,
                    modelo,
                    patente,
                    color,
                    departamento
                FROM registros
                WHERE
                    CAST(id AS TEXT) LIKE ?
                    OR hora LIKE ?
                    OR persona LIKE ?
                    OR rut LIKE ?
                    OR vehiculo LIKE ?
                    OR marca LIKE ?
                    OR modelo LIKE ?
                    OR patente LIKE ?
                    OR color LIKE ?
                    OR departamento LIKE ?
                ORDER BY id DESC
            """, (
                patron,
                patron,
                patron,
                patron,
                patron,
                patron,
                patron,
                patron,
                patron,
                patron
            ))

            registros = cur.fetchall()
            con.close()

            resultados.clear_widgets()

            if not registros:

                resultados.add_widget(
                    Label(
                        text="No se encontraron registros.",
                        size_hint_y=None,
                        height=dp(50)
                    )
                )
                return

            for registro in registros:

                rid = registro[0]
                hora = registro[1]
                persona = registro[2]
                patente = registro[7] or ""
                departamento = registro[9] or ""

                texto_boton = (
                    f"ID {rid}  |  "
                    f"{persona}  |  "
                    f"{patente}  |  "
                    f"{departamento}\n"
                    f"{hora}"
                )

                boton = Button(
                    text=texto_boton,
                    size_hint_y=None,
                    height=dp(65),
                    halign="left",
                    valign="middle"
                )

                boton.bind(
                    on_press=lambda x, r=rid:
                    self.seleccionar_busqueda(r, popup)
                )

                resultados.add_widget(boton)

        buscar.bind(on_press=ejecutar_busqueda)

        popup.open()

    def seleccionar_busqueda(self, registro_id, popup):

        self.cargar_registro(registro_id)

        popup.dismiss()

    # ========================================================
    # CARGAR REGISTRO
    # ========================================================

    def cargar_registro(self, registro_id):

        con = self.conectar()
        cur = con.cursor()

        cur.execute("""
            SELECT
                id,
                hora,
                persona,
                rut,
                vehiculo,
                marca,
                modelo,
                patente,
                color,
                departamento,
                foto_patente
            FROM registros
            WHERE id = ?
        """, (registro_id,))

        registro = cur.fetchone()
        con.close()

        if not registro:
            self.mensaje(
                "Error",
                "No se encontró el registro."
            )
            return

        self.registro_id = registro[0]

        self.hora.text = registro[1] or ""
        self.persona.text = registro[2] or ""
        self.rut.text = registro[3] or ""

        vehiculos = [
            "Automovil",
            "Camioneta",
            "SUV",
            "Moto",
            "Furgon",
            "Camion",
            "Otro"
        ]

        if registro[4] in vehiculos:
            self.vehiculo.text = registro[4]
        else:
            self.vehiculo.text = "Automovil"

        self.marca.text = registro[5] or ""
        self.modelo.text = registro[6] or ""
        self.patente.text = registro[7] or ""
        self.color.text = registro[8] or ""
        self.departamento.text = registro[9] or ""

        self.foto_bytes = registro[10]

        if self.foto_bytes:
            self.foto_label.text = "FOTO DE PATENTE: Capturada"
        else:
            self.foto_label.text = "FOTO DE PATENTE: No capturada"

    # ========================================================
    # MODIFICAR
    # ========================================================

    def modificar(self, *args):

        if not self.registro_id:
            self.mensaje(
                "Modificar",
                "Primero debe buscar y seleccionar un registro."
            )
            return

        if not self.persona.text.strip():
            self.mensaje(
                "Modificar",
                "El campo PERSONA es obligatorio."
            )
            return

        con = self.conectar()
        cur = con.cursor()

        cur.execute("""
            UPDATE registros
            SET
                persona = ?,
                rut = ?,
                vehiculo = ?,
                marca = ?,
                modelo = ?,
                patente = ?,
                color = ?,
                departamento = ?,
                foto_patente = ?
            WHERE id = ?
        """, (
            self.persona.text.strip(),
            self.rut.text.strip(),
            self.vehiculo.text,
            self.marca.text.strip(),
            self.modelo.text.strip(),
            self.patente.text.strip().upper(),
            self.color.text.strip(),
            self.departamento.text.strip(),
            self.foto_bytes,
            self.registro_id
        ))

        con.commit()
        con.close()

        self.mensaje(
            "Registro modificado",
            "Los datos fueron actualizados correctamente."
        )

    # ========================================================
    # ELIMINAR
    # ========================================================

    def eliminar(self, *args):

        if not self.registro_id:
            self.mensaje(
                "Eliminar",
                "Primero debe buscar y seleccionar un registro."
            )
            return

        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        contenido.add_widget(
            Label(
                text="¿Está seguro de eliminar este registro?",
                font_size="17sp"
            )
        )

        botones = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        si = Button(
            text="ELIMINAR",
            background_color=self.rgb(ROJO)
        )

        no = Button(
            text="CANCELAR"
        )

        botones.add_widget(si)
        botones.add_widget(no)

        contenido.add_widget(botones)

        popup = Popup(
            title="Confirmar eliminación",
            content=contenido,
            size_hint=(0.85, 0.35)
        )

        no.bind(on_press=popup.dismiss)

        def confirmar(instance):

            con = self.conectar()
            cur = con.cursor()

            cur.execute(
                "DELETE FROM registros WHERE id = ?",
                (self.registro_id,)
            )

            con.commit()
            con.close()

            popup.dismiss()

            self.mensaje(
                "Registro eliminado",
                "El registro fue eliminado correctamente."
            )

            self.limpiar()

        si.bind(on_press=confirmar)

        popup.open()

    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar(self, *args):

        self.registro_id = None
        self.foto_bytes = None

        self.actualizar_hora()

        self.persona.text = ""
        self.rut.text = ""
        self.vehiculo.text = "Automovil"
        self.marca.text = ""
        self.modelo.text = ""
        self.patente.text = ""
        self.color.text = ""
        self.departamento.text = ""

        self.foto_label.text = (
            "FOTO DE PATENTE: No capturada"
        )

    # ========================================================
    # CÁMARA
    # ========================================================

    def abrir_camara(self, *args):

        contenido = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=dp(5)
        )

        camara = Camera(
            resolution=(1280, 720),
            play=True
        )

        contenido.add_widget(camara)

        botones = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(5)
        )

        tomar = Button(
            text="CAPTURAR",
            background_color=self.rgb(VERDE)
        )

        cancelar = Button(
            text="CANCELAR",
            background_color=self.rgb(ROJO)
        )

        botones.add_widget(tomar)
        botones.add_widget(cancelar)

        contenido.add_widget(botones)

        popup = Popup(
            title="FOTOGRAFÍA DE PATENTE",
            content=contenido,
            size_hint=(0.98, 0.90)
        )

        cancelar.bind(
            on_press=lambda x: self.cerrar_camara(
                camara,
                popup
            )
        )

        tomar.bind(
            on_press=lambda x: self.capturar_foto(
                camara,
                popup
            )
        )

        popup.open()

    def cerrar_camara(self, camara, popup):

        camara.play = False
        popup.dismiss()

    def capturar_foto(self, camara, popup):

        carpeta = self.user_data_dir

        archivo = os.path.join(
            carpeta,
            "patente_temp.png"
        )

        try:

            camara.export_to_png(archivo)

            with open(archivo, "rb") as f:
                self.foto_bytes = f.read()

            self.foto_label.text = (
                "FOTO DE PATENTE: Capturada"
            )

            camara.play = False
            popup.dismiss()

            self.mensaje(
                "Fotografía",
                "La foto de la patente fue capturada."
            )

        except Exception as e:

            self.mensaje(
                "Error de cámara",
                str(e)
            )

    # ========================================================
    # PDF INDIVIDUAL
    # ========================================================

    def pdf_individual(self, *args):

        if not self.registro_id:

            self.mensaje(
                "PDF",
                "Primero debe buscar y seleccionar un registro."
            )
            return

        con = self.conectar()
        cur = con.cursor()

        cur.execute("""
            SELECT
                id,
                hora,
                persona,
                rut,
                vehiculo,
                marca,
                modelo,
                patente,
                color,
                departamento
            FROM registros
            WHERE id = ?
        """, (self.registro_id,))

        r = cur.fetchone()
        con.close()

        if not r:
            return

        carpeta = self.user_data_dir

        archivo = os.path.join(
            carpeta,
            f"registro_{r[0]}.pdf"
        )

        doc = SimpleDocTemplate(
            archivo,
            pagesize=A4,
            rightMargin=35,
            leftMargin=35,
            topMargin=35,
            bottomMargin=35
        )

        estilos = getSampleStyleSheet()

        titulo = ParagraphStyle(
            "Titulo",
            parent=estilos["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22,
            spaceAfter=8
        )

        subtitulo = ParagraphStyle(
            "Subtitulo",
            parent=estilos["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=14,
            spaceAfter=15
        )

        elementos = []

        elementos.append(
            Paragraph(
                "CONTROL DE ACCESO",
                titulo
            )
        )

        elementos.append(
            Paragraph(
                f"Registro de ingreso N° {r[0]}",
                subtitulo
            )
        )

        partes = r[1].split("  ")

        fecha = partes[0] if partes else r[1]
        hora = partes[1] if len(partes) > 1 else ""

        datos = [
            ["ID", str(r[0])],
            ["FECHA DE INGRESO", fecha],
            ["HORA DE INGRESO", hora],
            ["NOMBRE", r[2] or ""],
            ["RUT", r[3] or ""],
            ["VEHÍCULO", r[4] or ""],
            ["MARCA", r[5] or ""],
            ["MODELO", r[6] or ""],
            ["PATENTE", r[7] or ""],
            ["COLOR", r[8] or ""],
            ["DEPARTAMENTO", r[9] or ""]
        ]

        tabla = Table(
            datos,
            colWidths=[120, 325]
        )

        tabla.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor(AZUL)
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ])
        )

        elementos.append(tabla)

        doc.build(elementos)

        self.mensaje(
            "PDF generado",
            f"Archivo creado:\n{archivo}"
        )

    # ========================================================
    # PDF GENERAL
    # ========================================================

    def pdf_general(self, *args):

        con = self.conectar()
        cur = con.cursor()

        cur.execute("""
            SELECT
                id,
                hora,
                persona,
                rut,
                vehiculo,
                marca,
                modelo,
                patente,
                color,
                departamento
            FROM registros
            ORDER BY
                substr(hora, 7, 4),
                substr(hora, 4, 2),
                substr(hora, 1, 2),
                id
        """)

        registros = cur.fetchall()
        con.close()

        if not registros:

            self.mensaje(
                "PDF",
                "No existen registros para imprimir."
            )
            return

        archivo = os.path.join(
            self.user_data_dir,
            "registros_generales.pdf"
        )

        doc = SimpleDocTemplate(
            archivo,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=25,
            bottomMargin=25
        )

        estilos = getSampleStyleSheet()

        titulo = ParagraphStyle(
            "TituloGeneral",
            parent=estilos["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22,
            spaceAfter=12
        )

        elementos = []

        elementos.append(
            Paragraph(
                "CONTROL DE ACCESO",
                titulo
            )
        )

        elementos.append(
            Paragraph(
                "REGISTROS GENERALES",
                ParagraphStyle(
                    "Sub",
                    parent=estilos["Normal"],
                    alignment=TA_CENTER,
                    fontSize=11,
                    spaceAfter=12
                )
            )
        )

        encabezados = [
            "ID",
            "FECHA DE INGRESO",
            "HORA DE INGRESO",
            "PERSONA",
            "RUT",
            "VEHÍCULO",
            "MARCA",
            "MODELO",
            "PATENTE",
            "COLOR",
            "DEPARTAMENTO"
        ]

        datos = [encabezados]

        for r in registros:

            partes = r[1].split("  ")

            fecha = partes[0] if partes else r[1]
            hora = partes[1] if len(partes) > 1 else ""

            datos.append([
                str(r[0]),
                fecha,
                hora,
                r[2] or "",
                r[3] or "",
                r[4] or "",
                r[5] or "",
                r[6] or "",
                r[7] or "",
                r[8] or "",
                r[9] or ""
            ])

        tabla = Table(
            datos,
            repeatRows=1,
            colWidths=[
                27,
                68,
                62,
                118,
                60,
                63,
                65,
                70,
                63,
                58,
                102
            ]
        )

        tabla.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(AZUL)
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F5F7F9")
                    ]
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    3
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    3
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                )
            ])
        )

        elementos.append(tabla)

        doc.build(elementos)

        self.mensaje(
            "PDF generado",
            f"Se generó el informe general con "
            f"{len(registros)} registros."
        )

    # ========================================================
    # MENSAJES
    # ========================================================

    def mensaje(self, titulo, texto):

        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        contenido.add_widget(
            Label(
                text=texto,
                font_size="15sp"
            )
        )

        aceptar = Button(
            text="ACEPTAR",
            size_hint_y=None,
            height=dp(48)
        )

        contenido.add_widget(aceptar)

        popup = Popup(
            title=titulo,
            content=contenido,
            size_hint=(0.88, 0.38)
        )

        aceptar.bind(on_press=popup.dismiss)

        popup.open()

    # ========================================================
    # SALIR
    # ========================================================

    def salir(self, *args):

        self.stop()


# ============================================================
# INICIO
# ============================================================

if __name__ == "__main__":
    ControlAcceso().run()
