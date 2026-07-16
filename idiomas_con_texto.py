import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import json
import os
import threading
import tempfile
from datetime import datetime

from langdetect import detect, DetectorFactory, LangDetectException
from deep_translator import GoogleTranslator
from gtts import gTTS

DetectorFactory.seed = 0

NEGRO = "#000000"
BLANCO = "#FFFFFF"
AMARILLO = "#FFD700"
AZUL = "#1E3A8A"
AZUL_CLARO = "#3B82F6"
GRIS_CLARO = "#F0F4F8"
GRIS_FONDO = "#E8EDF2"
ROJO = "#EF4444"
VERDE = "#10B981"

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
        self.root.geometry("950x780")
        self.root.minsize(850, 680)

        self.textos_guardados = cargar_guardados()
        self.ultimo_texto = ""
        self.traduciendo = False
        self.traduccion_actual = ""
        self.idioma_detectado_actual = ""
        self.codigo_traduccion_destino = "es"

        self.build_ui()
        self.cargar_lista_guardados()

    def build_ui(self):
        header = tk.Frame(self.root, bg=AZUL, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="Idiomas con Texto",
            font=("Segoe UI", 20, "bold"), bg=AZUL, fg=BLANCO
        ).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            header, text="Detecta, traduce y escucha cualquier idioma",
            font=("Segoe UI", 9), bg=AZUL, fg=AMARILLO
        ).place(relx=0.5, rely=0.78, anchor="center")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_traductor = tk.Frame(notebook, bg=BLANCO)
        self.tab_idiomas = tk.Frame(notebook, bg=BLANCO)
        self.tab_guardados = tk.Frame(notebook, bg=BLANCO)

        notebook.add(self.tab_traductor, text="  Traductor  ")
        notebook.add(self.tab_idiomas, text="  Idiomas por Continente  ")
        notebook.add(self.tab_guardados, text="  Textos Guardados  ")

        self.build_traductor_tab()
        self.build_idiomas_tab()
        self.build_guardados_tab()

    def build_traductor_tab(self):
        parent = self.tab_traductor

        input_frame = tk.Frame(parent, bg=BLANCO)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 5))

        tk.Label(
            input_frame, text="Escribe o pega tu texto:",
            font=("Segoe UI", 11, "bold"), bg=BLANCO, fg=NEGRO, anchor="w"
        ).pack(fill=tk.X)

        text_container = tk.Frame(input_frame, bg=AZUL, padx=2, pady=2)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        self.texto_entrada = scrolledtext.ScrolledText(
            text_container, height=5, wrap=tk.WORD,
            font=("Segoe UI", 11), bg=BLANCO, fg=NEGRO,
            relief=tk.FLAT, bd=0, padx=10, pady=10,
            highlightthickness=0
        )
        self.texto_entrada.pack(fill=tk.BOTH, expand=True)
        self.texto_entrada.config(insertbackground=NEGRO)

        lang_row = tk.Frame(parent, bg=BLANCO)
        lang_row.pack(fill=tk.X, padx=15, pady=(8, 5))

        tk.Label(
            lang_row, text="Traducir a:",
            font=("Segoe UI", 10, "bold"), bg=BLANCO, fg=NEGRO
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.idioma_destino = tk.StringVar(value="es")
        self.combo_idiomas = ttk.Combobox(
            lang_row, textvariable=self.idioma_destino,
            font=("Segoe UI", 10), state="readonly", width=35
        )
        items = sorted(IDIOMAS_TRADUCCION.items(), key=lambda x: x[1])
        self.combo_idiomas["values"] = [f"{cod} - {nom}" for cod, nom in items]
        self.combo_idiomas.set("es - Español")
        self.combo_idiomas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.combo_idiomas.bind("<<ComboboxSelected>>", self.on_idioma_cambiado)

        btn_row = tk.Frame(parent, bg=BLANCO)
        btn_row.pack(fill=tk.X, padx=15, pady=(5, 8))

        self.btn_traducir = tk.Button(
            btn_row, text="Detectar y Traducir",
            font=("Segoe UI", 10, "bold"), bg=AZUL, fg=BLANCO,
            activebackground=AZUL_CLARO, activeforeground=BLANCO,
            relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
            command=self.detectar_y_traducir
        )
        self.btn_traducir.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_escuchar = tk.Button(
            btn_row, text="Escuchar",
            font=("Segoe UI", 10, "bold"), bg=AMARILLO, fg=NEGRO,
            activebackground="#FFC000", activeforeground=NEGRO,
            relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
            command=self.escuchar_texto
        )
        self.btn_escuchar.pack(side=tk.LEFT, padx=(0, 8))

        btn_guardar = tk.Button(
            btn_row, text="Guardar Texto",
            font=("Segoe UI", 10, "bold"), bg=VERDE, fg=BLANCO,
            activebackground="#059669", activeforeground=BLANCO,
            relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
            command=self.guardar_texto_actual
        )
        btn_guardar.pack(side=tk.LEFT)

        result_frame = tk.Frame(parent, bg=GRIS_FONDO, padx=15, pady=12)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        tk.Label(
            result_frame, text="Resultado:",
            font=("Segoe UI", 11, "bold"), bg=GRIS_FONDO, fg=NEGRO, anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))

        self.resultado_text = tk.Text(
            result_frame, height=6, wrap=tk.WORD,
            font=("Segoe UI", 10), bg=BLANCO, fg=NEGRO,
            relief=tk.SOLID, bd=1, padx=10, pady=10,
            highlightthickness=0, state=tk.DISABLED
        )
        self.resultado_text.pack(fill=tk.BOTH, expand=True)

        audio_trad_row = tk.Frame(result_frame, bg=GRIS_FONDO)
        audio_trad_row.pack(fill=tk.X, pady=(8, 0))

        self.btn_escuchar_traduccion = tk.Button(
            audio_trad_row, text="Escuchar Traduccion",
            font=("Segoe UI", 10, "bold"), bg=AZUL_CLARO, fg=BLANCO,
            activebackground=AZUL, activeforeground=BLANCO,
            relief=tk.FLAT, padx=20, pady=7, cursor="hand2",
            command=self.escuchar_traduccion
        )
        self.btn_escuchar_traduccion.pack(side=tk.LEFT)

    def build_idiomas_tab(self):
        parent = self.tab_idiomas

        tk.Label(
            parent, text="Selecciona un continente para ver sus idiomas:",
            font=("Segoe UI", 11, "bold"), bg=BLANCO, fg=NEGRO, pady=10
        ).pack()

        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        continentes = {
            "Europa": lambda: self._filtrar_por_continente("Europa"),
            "America": lambda: self._filtrar_por_continente("América"),
            "Africa": lambda: self._filtrar_por_continente("África"),
        }

        self.idiomas_canvas = {}

        for nombre, _ in continentes.items():
            frame = tk.Frame(notebook, bg=BLANCO)
            notebook.add(frame, text=f"  {nombre}  ")

            search_frame = tk.Frame(frame, bg=BLANCO)
            search_frame.pack(fill=tk.X, padx=10, pady=8)

            tk.Label(search_frame, text="Buscar:", bg=BLANCO, fg=NEGRO,
                     font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 5))

            var = tk.StringVar()
            entry = tk.Entry(search_frame, textvariable=var,
                             font=("Segoe UI", 10), relief=tk.SOLID, bd=1)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

            list_container = tk.Frame(frame, bg=BLANCO)
            list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

            canvas = tk.Canvas(list_container, bg=BLANCO, highlightthickness=0)
            scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL, command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=BLANCO)

            scroll_frame.bind("<Configure>",
                              lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            def make_scroll(c=canvas):
                def scroll_handler(event):
                    c.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return scroll_handler

            canvas.bind("<Enter>", lambda e, c=canvas: c.bind_all("<MouseWheel>", make_scroll(c)))
            canvas.bind("<Leave>", lambda e, c=canvas: c.unbind_all("<MouseWheel>"))

            self.idiomas_canvas[nombre] = {
                "canvas": canvas,
                "scroll_frame": scroll_frame,
                "search_var": var,
                "search_entry": entry,
                "continente_nombre": {"Europa": "Europa", "America": "América", "Africa": "África"}[nombre]
            }

            var.trace_add("write", lambda *a, n=nombre: self._filtrar_idiomas(n))

        self._filtrar_idiomas("Europa")

    def _filtrar_por_continente(self, continente):
        datos = {}
        for k, v in PAIS_CONTINENTE.items():
            if v["continente"] == continente:
                datos[k] = v
        return datos

    def _filtrar_idiomas(self, nombre_tab):
        info = self.idiomas_canvas[nombre_tab]
        canvas = info["canvas"]
        scroll_frame = info["scroll_frame"]
        busqueda = info["search_var"].get().lower().strip()
        continente = info["continente_nombre"]

        for w in scroll_frame.winfo_children():
            w.destroy()

        datos = self._filtrar_por_continente(continente)
        items = sorted(datos.items(), key=lambda x: x[1]["nombre"])

        if busqueda:
            items = [(k, v) for k, v in items
                     if busqueda in v["nombre"].lower()
                     or busqueda in v["pais"].lower()
                     or busqueda in k.lower()]

        if not items:
            tk.Label(scroll_frame, text="No se encontraron idiomas.",
                     font=("Segoe UI", 10), bg=BLANCO, fg=NEGRO, pady=20).pack()
            return

        for i, (codigo, info_idioma) in enumerate(items):
            bg = BLANCO if i % 2 == 0 else GRIS_CLARO
            row = tk.Frame(scroll_frame, bg=bg, padx=10, pady=3)
            row.pack(fill=tk.X)

            tk.Label(row, text=info_idioma["nombre"],
                     font=("Segoe UI", 10, "bold"), bg=bg, fg=NEGRO,
                     width=28, anchor="w").pack(side=tk.LEFT)

            tk.Label(row, text=f"({codigo})",
                     font=("Segoe UI", 9), bg=bg, fg=NEGRO,
                     width=10, anchor="w").pack(side=tk.LEFT)

            tk.Label(row, text=f"{info_idioma['pais']}",
                     font=("Segoe UI", 9), bg=bg, fg=NEGRO,
                     anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

        canvas.configure(scrollregion=canvas.bbox("all"))

    def build_guardados_tab(self):
        parent = self.tab_guardados

        header = tk.Frame(parent, bg=BLANCO)
        header.pack(fill=tk.X, padx=15, pady=(15, 5))

        tk.Label(header, text="Textos Guardados",
                 font=("Segoe UI", 13, "bold"), bg=BLANCO, fg=NEGRO).pack(side=tk.LEFT)

        btn_limpiar = tk.Button(
            header, text="Limpiar Todo",
            font=("Segoe UI", 9), bg=ROJO, fg=BLANCO,
            activebackground="#DC2626", activeforeground=BLANCO,
            relief=tk.FLAT, padx=12, pady=4, cursor="hand2",
            command=self.limpiar_guardados
        )
        btn_limpiar.pack(side=tk.RIGHT)

        list_container = tk.Frame(parent, bg=AZUL, padx=2, pady=2)
        list_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 8))

        self.lista_guardados = tk.Listbox(
            list_container, font=("Segoe UI", 10), bg=BLANCO, fg=NEGRO,
            relief=tk.FLAT, bd=0,
            selectbackground=AZUL_CLARO, selectforeground=BLANCO
        )
        scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL,
                                 command=self.lista_guardados.yview)
        self.lista_guardados.config(yscrollcommand=scrollbar.set)
        self.lista_guardados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_guardados.bind("<Double-Button-1>", self.cargar_guardado_seleccionado)

        btn_frame = tk.Frame(parent, bg=BLANCO)
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        btn_cargar = tk.Button(
            btn_frame, text="Cargar en Editor",
            font=("Segoe UI", 10, "bold"), bg=AZUL, fg=BLANCO,
            activebackground=AZUL_CLARO, activeforeground=BLANCO,
            relief=tk.FLAT, padx=16, pady=6, cursor="hand2",
            command=lambda: self.cargar_guardado_seleccionado()
        )
        btn_cargar.pack(side=tk.LEFT, padx=(0, 8))

        btn_eliminar = tk.Button(
            btn_frame, text="Eliminar Seleccionado",
            font=("Segoe UI", 10, "bold"), bg=ROJO, fg=BLANCO,
            activebackground="#DC2626", activeforeground=BLANCO,
            relief=tk.FLAT, padx=16, pady=6, cursor="hand2",
            command=self.eliminar_guardado
        )
        btn_eliminar.pack(side=tk.LEFT)

        status_frame = tk.Frame(parent, bg=GRIS_FONDO)
        status_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.status_guardados = tk.Label(
            status_frame, text="", font=("Segoe UI", 9),
            bg=GRIS_FONDO, fg=NEGRO, anchor="w", padx=10, pady=6
        )
        self.status_guardados.pack(fill=tk.X)

    def obtener_codigo_idioma(self):
        seleccion = self.combo_idiomas.get()
        if " - " in seleccion:
            return seleccion.split(" - ")[0].strip()
        return "es"

    def on_idioma_cambiado(self, event=None):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if texto:
            self.detectar_y_traducir()

    def detectar_y_traducir(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Texto vacio", "Escribe o pega un texto primero.")
            return

        if self.traduciendo:
            return

        self.traduciendo = True
        self.btn_traducir.config(state=tk.DISABLED, text="Traduciendo...")

        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert("1.0", "Procesando...")
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

            traduccion = ""
            try:
                traductor = GoogleTranslator(source="auto", target=codigo_destino)
                traduccion = traductor.translate(texto)
            except Exception as e:
                try:
                    traductor = GoogleTranslator(source=codigo_detectado, target=codigo_destino)
                    traduccion = traductor.translate(texto)
                except Exception as e2:
                    traduccion = f"[Error al traducir]"

            self.traduccion_actual = traduccion
            self.idioma_detectado_actual = codigo_detectado
            self.codigo_traduccion_destino = codigo_destino

            resultado = (
                f"Idioma detectado: {nombre_idioma} ({codigo_detectado})\n"
                f"Pais: {pais}\n"
                f"Continente: {continente}\n"
                f"----------------------------------------\n"
                f"Traduccion al {nombre_destino}:\n"
                f"{traduccion}"
            )

            self.root.after(0, self._mostrar_resultado, resultado)

        except LangDetectException:
            self.root.after(0, self._mostrar_error,
                          "No se pudo detectar el idioma. El texto es muy corto o contiene caracteres no reconocidos.")
        except Exception as e:
            self.root.after(0, self._mostrar_error, f"Error: {str(e)}")
        finally:
            self.root.after(0, self._habilitar_boton)

    def _habilitar_boton(self):
        self.traduciendo = False
        self.btn_traducir.config(state=tk.NORMAL, text="Detectar y Traducir")

    def _mostrar_resultado(self, texto):
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert("1.0", texto)
        self.resultado_text.config(state=tk.DISABLED)

    def _mostrar_error(self, mensaje):
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert("1.0", mensaje)
        self.resultado_text.config(state=tk.DISABLED)

    def _lang_to_gtts(self, code):
        mapa = {
            "zh-cn": "zh-CN", "zh-tw": "zh-TW",
            "jv": "jw", "he": "iw",
            "fr-ca": "fr-CA", "pt-pt": "pt-PT",
            "nb": "no", "jw": "jw",
        }
        return mapa.get(code, code)

    def escuchar_texto(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Texto vacio", "No hay texto para escuchar.")
            return

        try:
            lang_code = self._lang_to_gtts(detect(texto))
        except:
            lang_code = "en"

        self.btn_escuchar.original_text = "Escuchar"
        self.btn_escuchar.config(state=tk.DISABLED, text="Reproduciendo...")
        self.root.update()
        threading.Thread(
            target=self._reproducir_audio,
            args=(texto, lang_code, self.btn_escuchar),
            daemon=True
        ).start()

    def _reproducir_audio(self, texto, lang_code, btn_restore=None):
        try:
            tts = gTTS(text=texto, lang=lang_code, slow=False, tld="com")
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
            tts.save(temp_path)
            os.system(f"afplay {temp_path} &>/dev/null")
            os.unlink(temp_path)
        except Exception:
            try:
                tts = gTTS(text=texto, lang="en", slow=False)
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    temp_path = f.name
                tts.save(temp_path)
                os.system(f"afplay {temp_path} &>/dev/null")
                os.unlink(temp_path)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"No se pudo reproducir audio: {str(e)}"))
        finally:
            if btn_restore:
                self.root.after(0, lambda b=btn_restore: b.config(state=tk.NORMAL, text=b.original_text))

    def escuchar_traduccion(self):
        texto = getattr(self, 'traduccion_actual', '')
        if not texto or texto.startswith("[Error"):
            messagebox.showwarning("Sin traduccion", "Primero traduce un texto.")
            return

        lang_code = self._lang_to_gtts(getattr(self, 'codigo_traduccion_destino', 'en'))

        self.btn_escuchar_traduccion.original_text = "Escuchar Traduccion"
        self.btn_escuchar_traduccion.config(state=tk.DISABLED, text="Reproduciendo...")
        self.root.update()
        threading.Thread(
            target=self._reproducir_audio,
            args=(texto, lang_code, self.btn_escuchar_traduccion),
            daemon=True
        ).start()

    def guardar_texto_actual(self):
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Texto vacio", "No hay texto para guardar.")
            return

        idioma_info = "Desconocido"
        traduccion_info = ""

        contenido = self.resultado_text.get("1.0", tk.END).strip()
        if contenido and "Idioma detectado" in contenido:
            lineas = contenido.split("\n")
            if lineas:
                primera = lineas[0]
                if ":" in primera:
                    idioma_info = primera.split(":", 1)[1].strip()

            idx_trad = -1
            for i, linea in enumerate(lineas):
                if linea.startswith("Traduccion al"):
                    idx_trad = i + 1
                    break
            if idx_trad > 0 and idx_trad < len(lineas):
                traduccion_info = "\n".join(lineas[idx_trad:])

        self.textos_guardados = guardar_texto_json(texto, idioma_info, traduccion_info)
        self.cargar_lista_guardados()

        tab_guardados = self.root.nametowidget(self.root.winfo_children()[1]).tabs()
        self.root.nametowidget(self.root.winfo_children()[1]).select(len(tab_guardados) - 1)

        messagebox.showinfo("Guardado", "Texto guardado exitosamente.")

    def cargar_lista_guardados(self):
        self.lista_guardados.delete(0, tk.END)
        self.textos_guardados = cargar_guardados()
        for item in self.textos_guardados:
            preview = item["texto"][:65] + "..." if len(item["texto"]) > 65 else item["texto"]
            self.lista_guardados.insert(
                tk.END,
                f"[{item.get('fecha', '')}] {item.get('idioma', '?')}: {preview}"
            )

        if self.textos_guardados:
            self.status_guardados.config(text=f"Total: {len(self.textos_guardados)} texto(s) guardado(s)")
        else:
            self.status_guardados.config(text="No hay textos guardados todavia.")

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
                    f"Idioma detectado: {item.get('idioma', 'Desconocido')}\n"
                    f"Traduccion:\n{item['traduccion']}"
                )
                self.resultado_text.config(state=tk.DISABLED)

            notebook = self.root.nametowidget(self.root.winfo_children()[1])
            notebook.select(0)

            messagebox.showinfo("Cargado", "Texto cargado en el editor.")

    def eliminar_guardado(self):
        seleccion = self.lista_guardados.curselection()
        if not seleccion:
            messagebox.showinfo("Seleccionar", "Selecciona un texto para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "Eliminar este texto guardado?"):
            self.textos_guardados = eliminar_guardado_json(seleccion[0])
            self.cargar_lista_guardados()

    def limpiar_guardados(self):
        if not self.textos_guardados:
            return
        if messagebox.askyesno("Confirmar", "Eliminar todos los textos guardados?"):
            with open(RUTA_GUARDADOS, "w", encoding="utf-8") as f:
                json.dump([], f)
            self.textos_guardados = []
            self.cargar_lista_guardados()


if __name__ == "__main__":
    root = tk.Tk()
    app = IdiomasConTextoApp(root)
    root.mainloop()
