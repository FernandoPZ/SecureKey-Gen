import customtkinter as ctk
from tkinter import messagebox
import pyperclip
import threading
import time
import security
import os
from PIL import Image

# --- CONFIGURACIÓN DEL TEMA ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class KeyForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KeyForge Suite")
        self.geometry("500x520")
        self.minsize(480, 520)

        self.withdraw()
        self.actualizando_preset = False

        self.mostrar_pantalla_carga()

    # PANTALLA DE CARGA (SPLASH SCREEN)
    def mostrar_pantalla_carga(self):
        self.splash = ctk.CTkToplevel(self)
        self.splash.title("Iniciando KeyForge...")
        self.splash.geometry("400x250")
        self.splash.overrideredirect(True)
        self.splash.attributes("-topmost", True)

        pantalla_ancho = self.splash.winfo_screenwidth()
        pantalla_alto = self.splash.winfo_screenheight()
        x = (pantalla_ancho // 2) - (400 // 2)
        y = (pantalla_alto // 2) - (250 // 2)
        self.splash.geometry(f"400x250+{x}+{y}")

        # Diseño del Splash
        try:
            ruta_imagen = os.path.join(os.path.dirname(__file__), "KeyGen.png")
            logo_img = ctk.CTkImage(light_image=Image.open(ruta_imagen), size=(80, 80))
            ctk.CTkLabel(self.splash, text="", image=logo_img).pack(pady=(20, 5))
        except Exception as e:
            print(f"Aviso: No se pudo cargar KeyGen.png - {e}")
            ctk.CTkLabel(self.splash, text="🛡️", font=ctk.CTkFont(size=60)).pack(pady=(20, 5))

        ctk.CTkLabel(self.splash, text="KeyForge Suite", font=ctk.CTkFont(size=24, weight="bold")).pack()
        
        self.lbl_progreso = ctk.CTkLabel(self.splash, text="Iniciando protocolos de seguridad...")
        self.lbl_progreso.pack(pady=(20, 5))
        
        self.barra_carga = ctk.CTkProgressBar(self.splash, width=300)
        self.barra_carga.set(0)
        self.barra_carga.pack(pady=10)

        threading.Thread(target=self.tarea_descarga_datos, daemon=True).start()

    def tarea_descarga_datos(self):
        def actualizar_ui(progreso):
            self.after(0, self.barra_carga.set, progreso)
            if progreso < 0.6: 
                self.after(0, lambda: self.lbl_progreso.configure(text="Sincronizando base de datos global..."))
            elif progreso < 0.9: 
                self.after(0, lambda: self.lbl_progreso.configure(text="Cargando estándar criptográfico BIP-39..."))
            else: 
                self.after(0, lambda: self.lbl_progreso.configure(text="¡Sistemas listos!"))

        security.actualizar_diccionario_online(actualizar_ui)
        security.descargar_diccionario_frases(actualizar_ui)
        
        time.sleep(0.5)

        self.after(0, self.splash.destroy)
        self.after(0, self.construir_interfaz)
        self.after(0, self.deiconify)

    # FUNCIONES LÓGICAS DE LA INTERFAZ
    def optimizar_contraste(self, color_hex):
        mapa_colores = {"#8B0000": "#FF4444", "#FF4C4C": "#FF6B6B", "#FFD700": "#FFD93D", "#4CAF50": "#28C76F"}
        return mapa_colores.get(color_hex, color_hex)

    def habilitar_controles(self, activo):
        estado = "normal" if activo else "disabled"
        self.chk_min.configure(state=estado)
        self.chk_mayus.configure(state=estado)
        self.chk_num.configure(state=estado)
        self.chk_sym.configure(state=estado)
        self.slider_longitud.configure(state=estado)

    def actualizar_label_slider(self, valor):
        modo = self.var_preset.get()
        
        # Algoritmo de mapeo para Hexadecimal (0=32, 1=64, 2=128)
        if modo == "Llave Cripto (Hex)":
            longitudes_permitidas = [32, 64, 128]
            valor_real = longitudes_permitidas[int(valor)]
            self.label_longitud_val.configure(text=f"{valor_real} chars")
            
            # Generamos la clave en tiempo real al mover el slider
            if not self.actualizando_preset:
                self.generar_y_mostrar()
            # Salimos de la función AQUÍ para evitar que cambie a "Personalizado"
            return 
            
        elif modo == "Frase de Seguridad":
            self.label_longitud_val.configure(text=f"{int(valor)} palabras")
        else:
            self.label_longitud_val.configure(text=f"{int(valor)} chars")

        # Solo cambiamos a Personalizado si NO estamos en Hex ni en Frase
        if not self.actualizando_preset:
            self.var_preset.set("Personalizado")
            self.habilitar_controles(True)

    def clic_checkbox(self):
        if not self.actualizando_preset:
            self.var_preset.set("Personalizado")
            self.habilitar_controles(True)

    def aplicar_preset(self, seleccion):
        if "───" in seleccion:
            self.var_preset.set("Personalizado")
            return

        self.actualizando_preset = True 
        
        # Restaurar slider al rango normal (60 pasos) y habilitar todo
        self.slider_longitud.configure(from_=4, to=64, number_of_steps=60)
        self.habilitar_controles(True)
        self.var_min.set(False); self.var_mayus.set(False)
        self.var_num.set(False); self.var_sym.set(False)
        
        if seleccion == "PIN (4 dígitos)":
            self.slider_longitud.set(4); self.var_num.set(True)
            self.actualizar_label_slider(4)

        elif seleccion == "Código Temporal (6 caps)":
            self.slider_longitud.set(6); self.var_mayus.set(True); self.var_num.set(True)
            self.actualizar_label_slider(6)

        elif seleccion == "Estándar Web (8 chars)":
            self.slider_longitud.set(8)
            self.var_min.set(True); self.var_mayus.set(True); self.var_num.set(True); self.var_sym.set(True)
            self.actualizar_label_slider(8)

        elif seleccion == "Seguridad Máxima (16 chars)":
            self.slider_longitud.set(16)
            self.var_min.set(True); self.var_mayus.set(True); self.var_num.set(True); self.var_sym.set(True)
            self.actualizar_label_slider(16)

        elif seleccion == "Frase de Seguridad":
            self.habilitar_controles(False)
            self.slider_longitud.set(4)
            self.label_longitud_val.configure(text="4 palabras")
            self.generar_y_mostrar()

        elif seleccion == "Llave Cripto (Hex)":
            # Truco: Limitamos el slider a solo 3 posiciones exactas (0, 1 y 2)
            self.slider_longitud.configure(from_=0, to=2, number_of_steps=2)
            self.slider_longitud.set(1) # Iniciamos en la posición 1 (que mapea a 64 chars)
            self.actualizar_label_slider(1)
            
            self.chk_min.configure(state="disabled"); self.chk_mayus.configure(state="disabled")
            self.chk_num.configure(state="disabled"); self.chk_sym.configure(state="disabled")
            self.generar_y_mostrar()

        self.actualizando_preset = False

    def generar_y_mostrar(self):
        modo = self.var_preset.get()
        
        if modo == "Frase de Seguridad":
            resultado = security.generar_frase(4)
        elif modo == "Llave Cripto (Hex)":
            # Leemos el índice (0, 1, 2) y lo traducimos a la longitud real
            longitudes_hex = [32, 64, 128]
            indice = int(self.slider_longitud.get())
            longitud_real = longitudes_hex[indice]
            resultado = security.generar_hexadecimal(longitud_real)
        else:
            resultado = security.generar_clave(
                int(self.slider_longitud.get()), self.var_min.get(), self.var_mayus.get(), 
                self.var_num.get(), self.var_sym.get()
            )

        if resultado is None:
            messagebox.showwarning("Atención", "Selecciona al menos un tipo de carácter.")
            return

        self.entry_gen.delete(0, 'end')
        self.entry_gen.insert(0, resultado)
        
        color, texto, _ = security.auditar_clave(resultado)
        self.barra_gen.configure(progress_color=color)
        self.barra_gen.set(1)
        
        info = " (Alta Entropía)" if modo == "Frase de Seguridad" else ""
        self.lbl_status_gen.configure(text=f"Seguridad: {texto}{info}", text_color=self.optimizar_contraste(color))

    def copiar_clave(self):
        clave = self.entry_gen.get()
        if clave:
            pyperclip.copy(clave)
            self.btn_copiar.configure(text="✔️", fg_color="#28a745")
            self.after(1200, lambda: self.btn_copiar.configure(text="📋", fg_color="#1f6aa5"))

    def evento_analizar(self, event=None):
        pwd = self.entry_ana.get()
        color, texto, sugerencias = security.auditar_clave(pwd)
        
        self.barra_ana.configure(progress_color=color if pwd else "gray")
        self.barra_ana.set(1 if pwd else 0)
        self.lbl_status_ana.configure(text=f"Estado: {texto}", text_color=self.optimizar_contraste(color) if pwd else "gray")
        
        self.txt_sugerencias.configure(state='normal')
        self.txt_sugerencias.delete('1.0', 'end')
        self.txt_sugerencias.insert('end', "\n".join(sugerencias))
        self.txt_sugerencias.configure(state='disabled')

    # ==========================================
    # CONSTRUCCIÓN VISUAL PRINCIPAL
    # ==========================================
    def construir_interfaz(self):
        tabview = ctk.CTkTabview(self)
        tabview.pack(padx=15, pady=10, fill="both", expand=True)
        tab_gen = tabview.add(" ⚒️ Generador ")
        tab_ana = tabview.add(" 🔍 Analizador ")

        # --- PESTAÑA GENERADOR ---
        frame_top = ctk.CTkFrame(tab_gen, fg_color="transparent")
        frame_top.pack(fill="x", pady=(5, 10))

        self.var_preset = ctk.StringVar(value="Estándar Web (8 chars)")
        opciones = [
            "Personalizado", "PIN (4 dígitos)", "Código Temporal (6 caps)", 
            "Estándar Web (8 chars)", "Seguridad Máxima (16 chars)",
            "────────────────────", 
            "Frase de Seguridad", "Llave Cripto (Hex)"
        ]
        ctk.CTkOptionMenu(frame_top, variable=self.var_preset, values=opciones, command=self.aplicar_preset).pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.label_longitud_val = ctk.CTkLabel(frame_top, text="8 chars", font=ctk.CTkFont(weight="bold"), width=75)
        self.label_longitud_val.pack(side="right")
        self.slider_longitud = ctk.CTkSlider(frame_top, from_=4, to=64, command=self.actualizar_label_slider, width=120)
        self.slider_longitud.set(8)
        self.slider_longitud.pack(side="right", padx=10)

        frame_checks = ctk.CTkFrame(tab_gen)
        frame_checks.pack(fill="x", pady=10)
        frame_checks.grid_columnconfigure((0, 1), weight=1)

        self.var_min = ctk.BooleanVar(value=True); self.var_mayus = ctk.BooleanVar(value=True)
        self.var_num = ctk.BooleanVar(value=True); self.var_sym = ctk.BooleanVar(value=True)

        self.chk_min = ctk.CTkCheckBox(frame_checks, text="Minúsculas (a-z)", variable=self.var_min, command=self.clic_checkbox)
        self.chk_min.grid(row=0, column=0, pady=10, padx=15, sticky="w")
        self.chk_mayus = ctk.CTkCheckBox(frame_checks, text="Mayúsculas (A-Z)", variable=self.var_mayus, command=self.clic_checkbox)
        self.chk_mayus.grid(row=0, column=1, pady=10, padx=15, sticky="w")
        self.chk_num = ctk.CTkCheckBox(frame_checks, text="Números (0-9)", variable=self.var_num, command=self.clic_checkbox)
        self.chk_num.grid(row=1, column=0, pady=10, padx=15, sticky="w")
        self.chk_sym = ctk.CTkCheckBox(frame_checks, text="Símbolos (!@#$)", variable=self.var_sym, command=self.clic_checkbox)
        self.chk_sym.grid(row=1, column=1, pady=10, padx=15, sticky="w")

        ctk.CTkButton(tab_gen, text="FORJAR CLAVE", font=ctk.CTkFont(weight="bold", size=14), fg_color="#28a745", hover_color="#218838", command=self.generar_y_mostrar).pack(fill="x", pady=10)

        frame_res = ctk.CTkFrame(tab_gen, fg_color="transparent")
        frame_res.pack(fill="x", pady=5)
        self.entry_gen = ctk.CTkEntry(frame_res, font=ctk.CTkFont(family="Consolas", size=18), justify="center", height=42)
        self.entry_gen.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_copiar = ctk.CTkButton(frame_res, text="📋", width=45, height=42, command=self.copiar_clave, font=ctk.CTkFont(size=18))
        self.btn_copiar.pack(side="right")

        self.barra_gen = ctk.CTkProgressBar(tab_gen, height=6)
        self.barra_gen.set(0)
        self.barra_gen.pack(fill="x", pady=(10, 5))
        self.lbl_status_gen = ctk.CTkLabel(tab_gen, text="Esperando forja...", font=ctk.CTkFont(weight="bold", size=12))
        self.lbl_status_gen.pack()

        # --- PESTAÑA ANALIZADOR ---
        ctk.CTkLabel(tab_ana, text="Auditoría de Seguridad", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        self.entry_ana = ctk.CTkEntry(tab_ana, font=ctk.CTkFont(family="Consolas", size=18), justify="center", height=42, show="*")
        self.entry_ana.pack(pady=10, fill="x")
        self.entry_ana.bind("<KeyRelease>", self.evento_analizar)

        self.barra_ana = ctk.CTkProgressBar(tab_ana, height=8)
        self.barra_ana.set(0)
        self.barra_ana.pack(pady=(5, 10), fill="x")
        self.lbl_status_ana = ctk.CTkLabel(tab_ana, text="Esperando entrada...", font=ctk.CTkFont(weight="bold"))
        self.lbl_status_ana.pack()

        self.txt_sugerencias = ctk.CTkTextbox(tab_ana, height=130, state="disabled", font=ctk.CTkFont(size=12))
        self.txt_sugerencias.pack(pady=10, fill="both", expand=True)

if __name__ == "__main__":
    app = KeyForgeApp()
    app.mainloop()