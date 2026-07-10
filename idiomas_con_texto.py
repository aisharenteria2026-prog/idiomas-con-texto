import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import json
import os
import threading
import time
from datetime import datetime

from langdetect import detect, DetectorFactory, LangDetectException
from deep_translator import GoogleTranslator
import pyttsx3

DetectorFactory.seed = 0

BLANCO = "#FFFFFF"
AMARILLO = "#FFD700"
AZUL = "#1E3A8A"
AZUL_CLARO = "#3B82F6"
AZUL_FONDO = "#EFF6FF"
GRIS_TEXTO = "#333333"
GRIS_CLARO = "#F0F4F8"
VERDE = "#10B981"
ROJO = "#EF4444"

PAIS_CONTINENTE = {
    "af": {"nombre": "Afrikáans", "pais": "Sudáfrica", "continente": "África"},
    "am": {"nombre": "Amárico", "pais": "Etiopía", "continente": "África"},
    "ar": {"nombre": "Árabe", "pais": "Arabia Saudita", "continente": "Asia"},
    "as": {"nombre": "Asamés", "pais": "India", "continente": "Asia"},
    "az": {"nombre": "Azerbaiyano", "pais": "Azerbaiyán", "continente": "Asia"},
    "be": {"nombre": "Bielorruso", "pais": "Bielorrusia", "continente": "Europa"},
    "bg": {"nombre": "Búlgaro", "pais": "Bulgaria", "continente": "Europa"},
    "bn": {"nombre": "Bengalí", "pais": "Bangladesh", "continente": "Asia"},
    "bo": {"nombre": "Tibetano", "pais": "Tíbet", "continente": "Asia"},
    "br": {"nombre": "Bretón", "pais": "Francia", "continente": "Europa"},
    "bs": {"nombre": "Bosnio", "pais": "Bosnia y Herzegovina", "continente": "Europa"},
    "ca": {"nombre": "Catalán", "pais": "España", "continente": "Europa"},
    "ceb": {"nombre": "Cebuano", "pais": "Filipinas", "continente": "Asia"},
    "co": {"nombre": "Corso", "pais": "Francia", "continente": "Europa"},
    "cs": {"nombre": "Checo", "pais": "República Checa", "continente": "Europa"},
    "cy": {"nombre": "Galés", "pais": "Reino Unido", "continente": "Europa"},
    "da": {"nombre": "Danés", "pais": "Dinamarca", "continente": "Europa"},
    "de": {"nombre": "Alemán", "pais": "Alemania", "continente": "Europa"},
    "el": {"nombre": "Griego", "pais": "Grecia", "continente": "Europa"},
    "en": {"nombre": "Inglés", "pais": "Reino Unido", "continente": "Europa"},
    "eo": {"nombre": "Esperanto", "pais": "Internacional", "continente": "Europa"},
    "es": {"nombre": "Español", "pais": "España", "continente": "Europa"},
    "et": {"nombre": "Estonio", "pais": "Estonia", "continente": "Europa"},
    "eu": {"nombre": "Euskera", "pais": "España", "continente": "Europa"},
    "fa": {"nombre": "Persa", "pais": "Irán", "continente": "Asia"},
    "fi": {"nombre": "Finés", "pais": "Finlandia", "continente": "Europa"},
    "fj": {"nombre": "Fiyiano", "pais": "Fiyi", "continente": "Oceanía"},
    "fo": {"nombre": "Feroés", "pais": "Islas Feroe", "continente": "Europa"},
    "fr": {"nombre": "Francés", "pais": "Francia", "continente": "Europa"},
    "fy": {"nombre": "Frisón", "pais": "Países Bajos", "continente": "Europa"},
    "ga": {"nombre": "Irlandés", "pais": "Irlanda", "continente": "Europa"},
    "gd": {"nombre": "Gaélico Escocés", "pais": "Reino Unido", "continente": "Europa"},
    "gl": {"nombre": "Gallego", "pais": "España", "continente": "Europa"},
    "gu": {"nombre": "Gujarati", "pais": "India", "continente": "Asia"},
    "ha": {"nombre": "Hausa", "pais": "Nigeria", "continente": "África"},
    "haw": {"nombre": "Hawaiano", "pais": "Estados Unidos", "continente": "Oceanía"},
    "he": {"nombre": "Hebreo", "pais": "Israel", "continente": "Asia"},
    "hi": {"nombre": "Hindi", "pais": "India", "continente": "Asia"},
    "hmn": {"nombre": "Hmong", "pais": "China", "continente": "Asia"},
    "hr": {"nombre": "Croata", "pais": "Croacia", "continente": "Europa"},
    "ht": {"nombre": "Criollo Haitiano", "pais": "Haití", "continente": "América"},
    "hu": {"nombre": "Húngaro", "pais": "Hungría", "continente": "Europa"},
    "hy": {"nombre": "Armenio", "pais": "Armenia", "continente": "Asia"},
    "id": {"nombre": "Indonesio", "pais": "Indonesia", "continente": "Asia"},
    "ig": {"nombre": "Igbo", "pais": "Nigeria", "continente": "África"},
    "is": {"nombre": "Islandés", "pais": "Islandia", "continente": "Europa"},
    "it": {"nombre": "Italiano", "pais": "Italia", "continente": "Europa"},
    "ja": {"nombre": "Japonés", "pais": "Japón", "continente": "Asia"},
    "jv": {"nombre": "Javanés", "pais": "Indonesia", "continente": "Asia"},
    "ka": {"nombre": "Georgiano", "pais": "Georgia", "continente": "Asia"},
    "kk": {"nombre": "Kazajo", "pais": "Kazajistán", "continente": "Asia"},
    "km": {"nombre": "Jemer", "pais": "Camboya", "continente": "Asia"},
    "kn": {"nombre": "Canarés", "pais": "India", "continente": "Asia"},
    "ko": {"nombre": "Coreano", "pais": "Corea del Sur", "continente": "Asia"},
    "ku": {"nombre": "Kurdo", "pais": "Turquía", "continente": "Asia"},
    "ky": {"nombre": "Kirguís", "pais": "Kirguistán", "continente": "Asia"},
    "la": {"nombre": "Latín", "pais": "Vaticano", "continente": "Europa"},
    "lb": {"nombre": "Luxemburgués", "pais": "Luxemburgo", "continente": "Europa"},
    "lo": {"nombre": "Lao", "pais": "Laos", "continente": "Asia"},
    "lt": {"nombre": "Lituano", "pais": "Lituania", "continente": "Europa"},
    "lv": {"nombre": "Letón", "pais": "Letonia", "continente": "Europa"},
    "mg": {"nombre": "Malgache", "pais": "Madagascar", "continente": "África"},
    "mi": {"nombre": "Maorí", "pais": "Nueva Zelanda", "continente": "Oceanía"},
    "mk": {"nombre": "Macedonio", "pais": "Macedonia del Norte", "continente": "Europa"},
    "ml": {"nombre": "Malayalam", "pais": "India", "continente": "Asia"},
    "mn": {"nombre": "Mongol", "pais": "Mongolia", "continente": "Asia"},
    "mr": {"nombre": "Maratí", "pais": "India", "continente": "Asia"},
    "ms": {"nombre": "Malayo", "pais": "Malasia", "continente": "Asia"},
    "mt": {"nombre": "Maltés", "pais": "Malta", "continente": "Europa"},
    "my": {"nombre": "Birmano", "pais": "Myanmar", "continente": "Asia"},
    "ne": {"nombre": "Nepalí", "pais": "Nepal", "continente": "Asia"},
    "nl": {"nombre": "Neerlandés", "pais": "Países Bajos", "continente": "Europa"},
    "no": {"nombre": "Noruego", "pais": "Noruega", "continente": "Europa"},
    "ny": {"nombre": "Chichewa", "pais": "Malawi", "continente": "África"},
    "or": {"nombre": "Odia", "pais": "India", "continente": "Asia"},
    "pa": {"nombre": "Punyabí", "pais": "India", "continente": "Asia"},
    "pl": {"nombre": "Polaco", "pais": "Polonia", "continente": "Europa"},
    "ps": {"nombre": "Pastún", "pais": "Afganistán", "continente": "Asia"},
    "pt": {"nombre": "Portugués", "pais": "Portugal", "continente": "Europa"},
    "ro": {"nombre": "Rumano", "pais": "Rumania", "continente": "Europa"},
    "ru": {"nombre": "Ruso", "pais": "Rusia", "continente": "Europa"},
    "rw": {"nombre": "Kinyarwanda", "pais": "Ruanda", "continente": "África"},
    "sd": {"nombre": "Sindhi", "pais": "Pakistán", "continente": "Asia"},
    "si": {"nombre": "Cingalés", "pais": "Sri Lanka", "continente": "Asia"},
    "sk": {"nombre": "Eslovaco", "pais": "Eslovaquia", "continente": "Europa"},
    "sl": {"nombre": "Esloveno", "pais": "Eslovenia", "continente": "Europa"},
    "sm": {"nombre": "Samoano", "pais": "Samoa", "continente": "Oceanía"},
    "sn": {"nombre": "Shona", "pais": "Zimbabue", "continente": "África"},
    "so": {"nombre": "Somalí", "pais": "Somalia", "continente": "África"},
    "sq": {"nombre": "Albanés", "pais": "Albania", "continente": "Europa"},
    "sr": {"nombre": "Serbio", "pais": "Serbia", "continente": "Europa"},
    "st": {"nombre": "Sesotho", "pais": "Lesoto", "continente": "África"},
    "su": {"nombre": "Sundanés", "pais": "Indonesia", "continente": "Asia"},
    "sv": {"nombre": "Sueco", "pais": "Suecia", "continente": "Europa"},
    "sw": {"nombre": "Suajili", "pais": "Tanzania", "continente": "África"},
    "ta": {"nombre": "Tamil", "pais": "India", "continente": "Asia"},
    "te": {"nombre": "Telugu", "pais": "India", "continente": "Asia"},
    "tg": {"nombre": "Tayiko", "pais": "Tayikistán", "continente": "Asia"},
    "th": {"nombre": "Tailandés", "pais": "Tailandia", "continente": "Asia"},
    "tk": {"nombre": "Turcomano", "pais": "Turkmenistán", "continente": "Asia"},
    "tl": {"nombre": "Tagalo", "pais": "Filipinas", "continente": "Asia"},
    "tr": {"nombre": "Turco", "pais": "Turquía", "continente": "Asia"},
    "tt": {"nombre": "Tártaro", "pais": "Rusia", "continente": "Europa"},
    "ug": {"nombre": "Uigur", "pais": "China", "continente": "Asia"},
    "uk": {"nombre": "Ucraniano", "pais": "Ucrania", "continente": "Europa"},
    "ur": {"nombre": "Urdu", "pais": "Pakistán", "continente": "Asia"},
    "uz": {"nombre": "Uzbeko", "pais": "Uzbekistán", "continente": "Asia"},
    "vi": {"nombre": "Vietnamita", "pais": "Vietnam", "continente": "Asia"},
    "xh": {"nombre": "Xhosa", "pais": "Sudáfrica", "continente": "África"},
    "yi": {"nombre": "Yidis", "pais": "Alemania", "continente": "Europa"},
    "yo": {"nombre": "Yoruba", "pais": "Nigeria", "continente": "África"},
    "zh-cn": {"nombre": "Chino Simplificado", "pais": "China", "continente": "Asia"},
    "zh-tw": {"nombre": "Chino Tradicional", "pais": "Taiwán", "continente": "Asia"},
    "zu": {"nombre": "Zulú", "pais": "Sudáfrica", "continente": "África"},
}

IDIOMAS_TRADUCCION = {
    "af": "Afrikáans", "sq": "Albanés", "de": "Alemán", "am": "Amárico",
    "ar": "Árabe", "hy": "Armenio", "az": "Azerbaiyano", "bn": "Bengalí",
    "be": "Bielorruso", "my": "Birmano", "bs": "Bosnio", "bg": "Búlgaro",
    "kn": "Canarés", "ca": "Catalán", "ceb": "Cebuano", "cs": "Checo",
    "ny": "Chichewa", "zh-cn": "Chino Simplificado", "zh-tw": "Chino Tradicional",
    "si": "Cingalés", "ko": "Coreano", "co": "Corso", "ht": "Criollo Haitiano",
    "hr": "Croata", "da": "Danés", "sk": "Eslovaco", "sl": "Esloveno",
    "es": "Español", "eo": "Esperanto", "et": "Estonio", "eu": "Euskera",
    "fi": "Finés", "fr": "Francés", "fy": "Frisón", "gd": "Gaélico Escocés",
    "cy": "Galés", "gl": "Gallego", "ka": "Georgiano", "el": "Griego",
    "gu": "Gujarati", "ha": "Hausa", "haw": "Hawaiano", "he": "Hebreo",
    "hi": "Hindi", "hmn": "Hmong", "nl": "Neerlandés", "hu": "Húngaro",
    "ig": "Igbo", "id": "Indonesio", "en": "Inglés", "ga": "Irlandés",
    "is": "Islandés", "it": "Italiano", "ja": "Japonés", "jv": "Javanés",
    "kk": "Kazajo", "km": "Jemer", "ky": "Kirguís", "ku": "Kurdo",
    "lo": "Lao", "la": "Latín", "lv": "Letón", "lt": "Lituano",
    "lb": "Luxemburgués", "mk": "Macedonio", "mg": "Malgache", "ms": "Malayo",
    "ml": "Malayalam", "mt": "Maltés", "mi": "Maorí", "mr": "Maratí",
    "mn": "Mongol", "ne": "Nepalí", "no": "Noruego", "or": "Odia",
    "ps": "Pastún", "fa": "Persa", "pl": "Polaco", "pt": "Portugués",
    "pa": "Punyabí", "ro": "Rumano", "ru": "Ruso", "sm": "Samoano",
    "sr": "Serbio", "st": "Sesotho", "sn": "Shona", "sd": "Sindhi",
    "so": "Somalí", "su": "Sundanés", "sw": "Suajili", "sv": "Sueco",
    "tl": "Tagalo", "th": "Tailandés", "ta": "Tamil", "tt": "Tártaro",
    "te": "Telugu", "bo": "Tibetano", "tr": "Turco", "tk": "Turcomano",
    "uk": "Ucraniano", "ug": "Uigur", "ur": "Urdu", "uz": "Uzbeko",
    "vi": "Vietnamita", "yi": "Yidis", "yo": "Yoruba", "zu": "Zulú",
}

LENGUA_AFRICA = {k: v for k, v in PAIS_CONTINENTE.items() if v["continente"] == "África"}
LENGUA_AMERICA = {k: v for k, v in PAIS_CONTINENTE.items() if v["continente"] == "América"}
LENGUA_EUROPA = {k: v for k, v in PAIS_CONTINENTE.items() if v["continente"] == "Europa"}

ARCHIVO_GUARDADOS = "textos_guardados.json"

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_GUARDADOS = os.path.join(RUTA_BASE, ARCHIVO_GUARDADOS)


def cargar_guardados():
    if os.path.exists(RUTA_GUARDADOS):
        try:
            with open(RUTA_GUARDADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def guardar_texto_json(texto, idioma, traduccion):
    datos = cargar_guardados()
    datos.append({
        "texto": texto,
        "idioma": idioma,
        "traduccion": traduccion,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    with open(RUTA_GUARDADOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return datos


def eliminar_guardado_json(indice):
    datos = cargar_guardados()
    if 0 <= indice < len(datos):
        datos.pop(indice)
        with open(RUTA_GUARDADOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    return datos


class IdiomasConTextoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Idiomas con Texto")
        self.root.configure(bg=BLANCO)
        self.root.geometry("900x750")
        self.root.minsize(800, 650)

        self.tts_engine = None
        self.textos_guardados = cargar_guardados()

        self.setup_styles()
        self.build_ui()
        self.cargar_lista_guardados()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BLANCO)
        style.configure("TLabel", background=BLANCO, foreground=GRIS_TEXTO, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("TMenubutton", font=("Segoe UI", 10), padding=5)
        style.map("TButton",
                  background=[("active", AZUL_CLARO)],
                  foreground=[("active", BLANCO)])

    def build_ui(self):
        canvas = tk.Canvas(self.root, bg=AZUL, height=8, highlightthickness=0)
        canvas.pack(fill=tk.X)

        header_frame = tk.Frame(self.root, bg=AZUL, padx=20, pady=15)
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame, text="🌍 Idiomas con Texto",
            font=("Segoe UI", 22, "bold"), bg=AZUL, fg=BLANCO
        ).pack()

        tk.Label(
            header_frame, text="Detecta, traduce y escucha cualquier idioma",
            font=("Segoe UI", 11), bg=AZUL, fg=AMARILLO
        ).pack(pady=(2, 0))

        main_container = tk.Frame(self.root, bg=BLANCO, padx=20, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)

        self.build_input_section(main_container)
        self.build_control_section(main_container)
        self.build_result_section(main_container)
        self.build_saved_section(main_container)

    def build_input_section(self, parent):
        input_frame = tk.Frame(parent, bg=BLANCO)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            input_frame, text="✏️ Escribe o pega tu texto aquí:",
            font=("Segoe UI", 11, "bold"), bg=BLANCO, fg=AZUL, anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))

        text_frame = tk.Frame(input_frame, bg=AZUL, padx=2, pady=2)
        text_frame.pack(fill=tk.X)

        self.texto_entrada = scrolledtext.ScrolledText(
            text_frame, height=4, wrap=tk.WORD,
            font=("Segoe UI", 11), bg=BLANCO, fg=GRIS_TEXTO,
            relief=tk.FLAT, bd=0, padx=10, pady=10,
            highlightthickness=0
        )
        self.texto_entrada.pack(fill=tk.X)
        self.texto_entrada.config(insertbackground=AZUL_CLARO)

        self.texto_entrada.bind("<KeyRelease>", self.on_text_change)

    def build_control_section(self, parent):
        control_frame = tk.Frame(parent, bg=BLANCO)
        control_frame.pack(fill=tk.X, pady=(0, 12))

        top_row = tk.Frame(control_frame, bg=BLANCO)
        top_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            top_row, text="Traducir a:",
            font=("Segoe UI", 10, "bold"), bg=BLANCO, fg=AZUL
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.idioma_destino = tk.StringVar(value="es")
        self.combo_idiomas = ttk.Combobox(
            top_row, textvariable=self.idioma_destino,
            font=("Segoe UI", 10), state="readonly", width=30
        )
        idiomas_ordenados = sorted(IDIOMAS_TRADUCCION.items(), key=lambda x: x[1])
        self.combo_idiomas["values"] = [f"{cod} - {nom}" for cod, nom in idiomas_ordenados]
        self.combo_idiomas.set("es - Español")
        self.combo_idiomas.pack(side=tk.LEFT, padx=(0, 10))

        btn_frame = tk.Frame(control_frame, bg=BLANCO)
        btn_frame.pack(fill=tk.X)

        btn_detectar = tk.Button(
            btn_frame, text="🔍 Detectar y Traducir",
            font=("Segoe UI", 10, "bold"), bg=AZUL, fg=BLANCO,
            activebackground=AZUL_CLARO, activeforeground=BLANCO,
            relief=tk.FLAT, padx=16, pady=8, cursor="hand2",
            command=self.detectar_y_traducir
        )
        btn_detectar.pack(side=tk.LEFT, padx=(0, 8))

        btn_escuchar = tk.Button(
            btn_frame, text="🔊 Escuchar",
            font=("Segoe UI", 10, "bold"), bg=AMARILLO, fg=AZUL,
            activebackground="#FFC000", activeforeground=AZUL,
            relief=tk.FLAT, padx=16, pady=8, cursor="hand2",
            command=self.escuchar_texto
        )
        btn_escuchar.pack(side=tk.LEFT, padx=(0, 8))

        btn_idiomas = tk.Button(
            btn_frame, text="🌐 Ver Idiomas",
            font=("Segoe UI", 10, "bold"), bg=AZUL_CLARO, fg=BLANCO,
            activebackground=AZUL, activeforeground=BLANCO,
            relief=tk.FLAT, padx=16, pady=8, cursor="hand2",
            command=self.mostrar_idiomas_continentes
        )
        btn_idiomas.pack(side=tk.LEFT, padx=(0, 8))

        btn_guardar = tk.Button(
            btn_frame, text="💾 Guardar Texto",
            font=("Segoe UI", 10, "bold"), bg=VERDE, fg=BLANCO,
            activebackground="#059669", activeforeground=BLANCO,
            relief=tk.FLAT, padx=16, pady=8, cursor="hand2",
            command=self.guardar_texto_actual
        )
        btn_guardar.pack(side=tk.LEFT)

    def build_result_section(self, parent):
        result_frame = tk.Frame(parent, bg=GRIS_CLARO, padx=15, pady=12, relief=tk.FLAT)
        result_frame.pack(fill=tk.X, pady=(0, 12))

        tk.Label(
            result_frame, text="📋 Resultado:",
            font=("Segoe UI", 11, "bold"), bg=GRIS_CLARO, fg=AZUL, anchor="w"
        ).pack(fill=tk.X, pady=(0, 8))

        self.resultado_text = tk.Text(
            result_frame, height=5, wrap=tk.WORD,
            font=("Segoe UI", 10), bg=BLANCO, fg=GRIS_TEXTO,
            relief=tk.SOLID, bd=1, padx=10, pady=10,
            highlightthickness=0, state=tk.DISABLED
        )
        self.resultado_text.pack(fill=tk.X)

    def build_saved_section(self, parent):
        saved_frame = tk.Frame(parent, bg=BLANCO)
        saved_frame.pack(fill=tk.BOTH, expand=True)

        header_saved = tk.Frame(saved_frame, bg=BLANCO)
        header_saved.pack(fill=tk.X, pady=(0, 5))

        tk.Label(
            header_saved, text="📚 Textos Guardados",
            font=("Segoe UI", 11, "bold"), bg=BLANCO, fg=AZUL
        ).pack(side=tk.LEFT)

        btn_limpiar = tk.Button(
            header_saved, text="🗑️ Limpiar Todo",
            font=("Segoe UI", 9), bg=ROJO, fg=BLANCO,
            activebackground="#DC2626", activeforeground=BLANCO,
            relief=tk.FLAT, padx=10, pady=2, cursor="hand2",
            command=self.limpiar_guardados
        )
        btn_limpiar.pack(side=tk.RIGHT)

        list_frame = tk.Frame(saved_frame, bg=AZUL, padx=2, pady=2)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.lista_guardados = tk.Listbox(
            list_frame, font=("Segoe UI", 9), bg=BLANCO, fg=GRIS_TEXTO,
            relief=tk.FLAT, bd=0,
            selectbackground=AZUL_CLARO, selectforeground=BLANCO,
            height=4
        )
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.lista_guardados.yview)
        self.lista_guardados.config(yscrollcommand=scrollbar.set)
        self.lista_guardados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_guardados.bind("<Double-Button-1>", self.cargar_guardado_seleccionado)

        btn_frame = tk.Frame(saved_frame, bg=BLANCO)
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        btn_eliminar = tk.Button(
            btn_frame, text="❌ Eliminar Seleccionado",
            font=("Segoe UI", 9), bg=ROJO, fg=BLANCO,
            activebackground="#DC2626", activeforeground=BLANCO,
            relief=tk.FLAT, padx=12, pady=4, cursor="hand2",
            command=self.eliminar_guardado
        )
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 8))

        btn_cargar = tk.Button(
            btn_frame, text="📂 Cargar en Editor",
            font=("Segoe UI", 9), bg=AZUL, fg=BLANCO,
            activebackground=AZUL_CLARO, activeforeground=BLANCO,
            relief=tk.FLAT, padx=12, pady=4, cursor="hand2",
            command=self.cargar_guardado_seleccionado
        )
        btn_cargar.pack(side=tk.LEFT)

    def on_text_change(self, event=None):
        pass

    def obtener_codigo_idioma(self):
        seleccion = self.combo_idiomas.get()
        if " - " in seleccion:
            return seleccion.split(" - ")[0].strip()
        return "es"

    def detectar_y_traducir(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Texto vacío", "Por favor, escribe o pega un texto primero.")
            return

        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert("1.0", "⏳ Procesando...\n")
        self.resultado_text.config(state=tk.DISABLED)
        self.root.update()

        threading.Thread(target=self._procesar_texto, args=(texto,), daemon=True).start()

    def _procesar_texto(self, texto):
        try:
            codigo_detectado = detect(texto)

            info_lengua = PAIS_CONTINENTE.get(codigo_detectado, {})
            nombre_idioma = info_lengua.get("nombre", codigo_detectado)
            pais = info_lengua.get("pais", "Desconocido")
            continente = info_lengua.get("continente", "Desconocido")

            codigo_destino = self.obtener_codigo_idioma()
            nombre_destino = IDIOMAS_TRADUCCION.get(codigo_destino, codigo_destino)

            try:
                traductor = GoogleTranslator(source=codigo_detectado, target=codigo_destino)
                traduccion = traductor.translate(texto)
            except Exception:
                try:
                    traductor = GoogleTranslator(source="auto", target=codigo_destino)
                    traduccion = traductor.translate(texto)
                except Exception as e:
                    traduccion = f"[Error al traducir: {str(e)}]"

            self.traduccion_actual = traduccion
            self.idioma_detectado_actual = codigo_detectado

            resultado = (
                f"🌐 Idioma detectado: {nombre_idioma} ({codigo_detectado})\n"
                f"📍 País: {pais}\n"
                f"🗺️ Continente: {continente}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔤 Traducción al {nombre_destino}:\n"
                f"{traduccion}"
            )

            self.root.after(0, self._mostrar_resultado, resultado)

        except LangDetectException:
            self.root.after(0, self._mostrar_error,
                          "No se pudo detectar el idioma. El texto es muy corto o contiene caracteres no reconocidos.")
        except Exception as e:
            self.root.after(0, self._mostrar_error, f"Error: {str(e)}")

    def _mostrar_resultado(self, texto):
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert("1.0", texto)
        self.resultado_text.config(state=tk.DISABLED)

    def _mostrar_error(self, mensaje):
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert("1.0", f"❌ {mensaje}")
        self.resultado_text.config(state=tk.DISABLED)

    def escuchar_texto(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Texto vacío", "No hay texto para escuchar.")
            return

        threading.Thread(target=self._reproducir_audio, args=(texto,), daemon=True).start()

    def _reproducir_audio(self, texto):
        try:
            if self.tts_engine is None:
                self.tts_engine = pyttsx3.init()

            voices = self.tts_engine.getProperty("voices")
            voz_seleccionada = None
            for v in voices:
                if "daniel" in v.id.lower():
                    voz_seleccionada = v.id
                    break
            if voz_seleccionada is None:
                for v in voices:
                    if "male" in v.gender.lower() or "fred" in v.id.lower() or "thomas" in v.id.lower():
                        voz_seleccionada = v.id
                        break
            if voz_seleccionada is None and voices:
                voz_seleccionada = voices[0].id

            if voz_seleccionada:
                self.tts_engine.setProperty("voice", voz_seleccionada)

            self.tts_engine.setProperty("rate", 165)
            self.tts_engine.setProperty("volume", 0.9)

            self.tts_engine.say(texto)
            self.tts_engine.runAndWait()

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"No se pudo reproducir el audio:\n{str(e)}"))

    def mostrar_idiomas_continentes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Idiomas por Continente")
        ventana.configure(bg=BLANCO)
        ventana.geometry("700x550")
        ventana.minsize(600, 400)
        ventana.transient(self.root)

        tk.Label(
            ventana, text="🌐 Idiomas por Continente",
            font=("Segoe UI", 16, "bold"), bg=AZUL, fg=BLANCO, pady=12
        ).pack(fill=tk.X)

        notebook = ttk.Notebook(ventana)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        for continente, datos_continente, color in [
            ("🌍 Europa", LENGUA_EUROPA, AZUL),
            ("🌍 América", LENGUA_AMERICA, VERDE),
            ("🌍 África", LENGUA_AFRICA, AMARILLO),
        ]:
            frame = tk.Frame(notebook, bg=BLANCO)
            notebook.add(frame, text=continente)

            canvas = tk.Canvas(frame, bg=BLANCO, highlightthickness=0)
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=BLANCO)

            scroll_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=650)
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            def on_mousewheel(event, c=canvas):
                c.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind_all("<MouseWheel>", on_mousewheel)

            idiomas_ordenados = sorted(datos_continente.items(), key=lambda x: x[1]["nombre"])

            for i, (codigo, info) in enumerate(idiomas_ordenados):
                bg_item = BLANCO if i % 2 == 0 else GRIS_CLARO
                item_frame = tk.Frame(scroll_frame, bg=bg_item, padx=10, pady=4)
                item_frame.pack(fill=tk.X)

                tk.Label(
                    item_frame, text=f"{info['nombre']}",
                    font=("Segoe UI", 10, "bold"), bg=bg_item, fg=AZUL, width=25, anchor="w"
                ).pack(side=tk.LEFT)

                tk.Label(
                    item_frame, text=f"({codigo})",
                    font=("Segoe UI", 9), bg=bg_item, fg=GRIS_TEXTO, width=10, anchor="w"
                ).pack(side=tk.LEFT)

                tk.Label(
                    item_frame, text=f"📍 {info['pais']}",
                    font=("Segoe UI", 9), bg=bg_item, fg=GRIS_TEXTO, anchor="w"
                ).pack(side=tk.LEFT, fill=tk.X, expand=True)

            if not idiomas_ordenados:
                tk.Label(
                    scroll_frame, text="No hay idiomas registrados para este continente.",
                    font=("Segoe UI", 10), bg=BLANCO, fg=GRIS_TEXTO, pady=30
                ).pack()

            def cleanup(event, c=canvas):
                c.unbind_all("<MouseWheel>")

            ventana.protocol("WM_DELETE_WINDOW", lambda: (cleanup(None, canvas), ventana.destroy()))

    def guardar_texto_actual(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Texto vacío", "No hay texto para guardar.")
            return

        idioma_info = "Desconocido"
        traduccion_info = ""

        contenido_resultado = self.resultado_text.get("1.0", tk.END).strip()
        if contenido_resultado and "Idioma detectado" in contenido_resultado:
            lineas = contenido_resultado.split("\n")
            for linea in lineas:
                if "Idioma detectado" in linea:
                    idioma_info = linea.split(":")[1].strip()
                if "Traducción al" in linea or "━━━━" in lineas:
                    pass

            idx_traduccion = -1
            for i, linea in enumerate(lineas):
                if linea.startswith("🔤"):
                    idx_traduccion = i + 1
                    break
            if idx_traduccion > 0 and idx_traduccion < len(lineas):
                traduccion_info = "\n".join(lineas[idx_traduccion:])

        self.textos_guardados = guardar_texto_json(texto, idioma_info, traduccion_info)
        self.cargar_lista_guardados()
        messagebox.showinfo("Guardado", "Texto guardado exitosamente.")

    def cargar_lista_guardados(self):
        self.lista_guardados.delete(0, tk.END)
        self.textos_guardados = cargar_guardados()
        for item in self.textos_guardados:
            texto_preview = item["texto"][:60] + "..." if len(item["texto"]) > 60 else item["texto"]
            self.lista_guardados.insert(
                tk.END,
                f"[{item.get('fecha', '')}] {item.get('idioma', '?')}: {texto_preview}"
            )

    def cargar_guardado_seleccionado(self, event=None):
        seleccion = self.lista_guardados.curselection()
        if not seleccion:
            messagebox.showinfo("Seleccionar", "Selecciona un texto guardado de la lista.")
            return

        indice = seleccion[0]
        if 0 <= indice < len(self.textos_guardados):
            item = self.textos_guardados[indice]
            self.texto_entrada.delete("1.0", tk.END)
            self.texto_entrada.insert("1.0", item["texto"])

            if item.get("traduccion"):
                self.resultado_text.config(state=tk.NORMAL)
                self.resultado_text.delete("1.0", tk.END)
                self.resultado_text.insert("1.0",
                    f"🌐 Idioma detectado: {item.get('idioma', 'Desconocido')}\n"
                    f"🔤 Traducción:\n{item['traduccion']}"
                )
                self.resultado_text.config(state=tk.DISABLED)

    def eliminar_guardado(self):
        seleccion = self.lista_guardados.curselection()
        if not seleccion:
            messagebox.showinfo("Seleccionar", "Selecciona un texto para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este texto guardado?"):
            self.textos_guardados = eliminar_guardado_json(seleccion[0])
            self.cargar_lista_guardados()

    def limpiar_guardados(self):
        if not self.textos_guardados:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar todos los textos guardados?"):
            with open(RUTA_GUARDADOS, "w", encoding="utf-8") as f:
                json.dump([], f)
            self.textos_guardados = []
            self.cargar_lista_guardados()


if __name__ == "__main__":
    root = tk.Tk()
    app = IdiomasConTextoApp(root)
    root.mainloop()
