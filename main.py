import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pyperclip
import threading
import time
import security
import os
from PIL import Image
import ctypes

# --- CONFIGURACIÓN ESTÉTICA ---
ctk.set_appearance_mode("Dark")

class KeyForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KeyForge")
        self.geometry("450x400")
        self.minsize(450, 400)

        try:
            if os.name == 'nt':
                myappid = 'portafolio.keyforge.final'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

            ruta_png = os.path.join(os.path.dirname(__file__), "KeyGen.png")
            ruta_ico = os.path.join(os.path.dirname(__file__), "KeyGen.ico")

            if not os.path.exists(ruta_ico):
                imagen_pil = Image.open(ruta_png)
                imagen_pil.save(ruta_ico, format='ICO', sizes=[(64, 64)])

            self.iconbitmap(ruta_ico)
            
        except Exception as e:
            print(f"Aviso: No se pudo configurar el icono nativo - {e}")

        self.withdraw()
        self.actualizando_preset = False
        self.mostrar_pantalla_carga()

    # PANTALLA DE CARGA
    def mostrar_pantalla_carga(self):
        self.splash = ctk.CTkToplevel(self)
        self.splash.geometry("400x260")
        self.splash.overrideredirect(True)
        self.splash.attributes("-topmost", True)
        self.splash.configure(fg_color="#1a1a1a")
        
        # Centrar splash
        x = (self.splash.winfo_screenwidth() // 2) - 200
        y = (self.splash.winfo_screenheight() // 2) - 130
        self.splash.geometry(f"+{x}+{y}")

        try:
            ruta_img = os.path.join(os.path.dirname(__file__), "KeyGen.png")
            logo = ctk.CTkImage(light_image=Image.open(ruta_img), size=(90, 90))
            ctk.CTkLabel(self.splash, text="", image=logo).pack(pady=(30, 5))
        except:
            ctk.CTkLabel(self.splash, text="KEYFORGE", font=("Consolas", 30)).pack(pady=(30, 5))

        ctk.CTkLabel(self.splash, text="KeyForge", font=ctk.CTkFont(size=22, weight="bold")).pack()
        self.lbl_p = ctk.CTkLabel(self.splash, text="Cargando protocolos...", text_color="gray60")
        self.lbl_p.pack(pady=(15, 5))
        
        self.bar_c = ctk.CTkProgressBar(self.splash, width=280, progress_color="#888888", fg_color="#333333")
        self.bar_c.set(0)
        self.bar_c.pack(pady=10)

        threading.Thread(target=self.hilo_carga, daemon=True).start()

    def hilo_carga(self):
        def upd(p):
            self.after(0, self.bar_c.set, p)
            txt = "Sincronizando base de datos..." if p < 0.6 else "Cargando diccionarios..."
            self.after(0, lambda: self.lbl_p.configure(text=txt))

        security.actualizar_diccionario_online(upd)
        security.descargar_diccionario_frases(upd)
        time.sleep(0.5)
        self.after(0, self.splash.destroy)
        self.after(0, self.construir_ui)
        self.after(0, self.deiconify)

    # LÓGICA DE INTERFAZ
    def habilitar_controles(self, activo):
        st = "normal" if activo else "disabled"
        color = "white" if activo else "gray40"
        for chk in [self.chk_min, self.chk_may, self.chk_num, self.chk_sym]:
            chk.configure(state=st, text_color=color)
        if activo: self.slider_long.configure(state="normal")
        else: self.slider_long.configure(state="disabled")

    def cambio_slider(self, val):
        modo = self.var_preset.get()
        txt = "palabras" if modo == "Frase de Seguridad" else "chars"
        self.lbl_long_txt.configure(text=f"{int(val)} {txt}")
        if not self.actualizando_preset:
            self.var_preset.set("Personalizado")
            self.habilitar_controles(True)

    def aplicar_preset(self, sel):
        if "──" in sel:
            self.var_preset.set("Personalizado")
            return

        self.actualizando_preset = True
        
        # 1. Vaciar el contenedor estático
        self.seg_hex.pack_forget()
        self.lbl_long_txt.pack_forget()
        self.slider_long.pack_forget()
        
        # 2. Resetear variables generales
        self.habilitar_controles(True)
        self.var_min.set(False); self.var_may.set(False); self.var_num.set(False); self.var_sym.set(False)

        # 3. Aplicar configuraciones
        if sel == "PIN (4 dígitos)":
            self.slider_long.set(4)
            self.var_num.set(True)
        elif sel == "Código Temporal (6 caps)":
            self.slider_long.set(6)
            self.var_may.set(True)
            self.var_num.set(True)
        elif sel == "Estándar Web (8 chars)":
            self.slider_long.set(8)
            [v.set(True) for v in [self.var_min, self.var_may, self.var_num, self.var_sym]]
        elif sel == "Seguridad Máxima (16 chars)":
            self.slider_long.set(16)
            [v.set(True) for v in [self.var_min, self.var_may, self.var_num, self.var_sym]]
        elif sel == "Frase de Seguridad":
            self.habilitar_controles(False)
            self.slider_long.set(4)
        
        # 4. Rellenar el contenedor estático
        if sel == "Llave Cripto (Hex)":
            self.seg_hex.pack(fill="both", expand=True)
            self.seg_hex.set("64")
            self.habilitar_controles(False)
        else:
            self.lbl_long_txt.pack(side="right")
            self.slider_long.pack(side="right", padx=(0, 10))

        self.cambio_slider(self.slider_long.get())
        self.actualizando_preset = False

    def generar(self):
        modo = self.var_preset.get()
        if modo == "Frase de Seguridad":
            res = security.generar_frase(4)
        elif modo == "Llave Cripto (Hex)":
            res = security.generar_hexadecimal(int(self.seg_hex.get()))
        else:
            res = security.generar_clave(int(self.slider_long.get()), self.var_min.get(), self.var_may.get(), self.var_num.get(), self.var_sym.get())

        if not res: return
        self.ent_res.delete(0, 'end'); self.ent_res.insert(0, res)
        col, txt, _ = security.auditar_clave(res)
        self.bar_res.configure(progress_color=col); self.bar_res.set(1)
        self.lbl_status.configure(text=f"SEGURIDAD: {txt}", text_color=col)

    # CONSTRUCCIÓN DE UI
    def construir_ui(self):
        tabs = ctk.CTkTabview(self, segmented_button_selected_color="#444444", segmented_button_selected_hover_color="#555555")
        tabs.pack(padx=20, pady=10, fill="both", expand=True)
        t_gen = tabs.add("Generador"); t_ana = tabs.add("Analizador")

        # --- Fila Superior: Menú y Selectores ---
        f_top = ctk.CTkFrame(t_gen, fg_color="transparent")
        f_top.pack(fill="x", pady=10)

        self.var_preset = ctk.StringVar(value="Estándar Web (8 chars)")
        opts = ["Personalizado", "PIN (4 dígitos)", "Código Temporal (6 caps)", "Estándar Web (8 chars)", "Seguridad Máxima (16 chars)", "────────────────────", "Frase de Seguridad", "Llave Cripto (Hex)"]
        self.menu = ctk.CTkOptionMenu(f_top, variable=self.var_preset, values=opts, command=self.aplicar_preset, fg_color="#333333", button_color="#444444")
        self.menu.pack(side="left", fill="x", expand=True)

        # Contenedor estático
        self.cont_longitud = ctk.CTkFrame(f_top, fg_color="transparent", width=220, height=30)
        self.cont_longitud.pack_propagate(False)
        self.cont_longitud.pack(side="right", padx=(10, 0))

        self.lbl_long_txt = ctk.CTkLabel(self.cont_longitud, text="8 chars", font=("Arial", 12, "bold"), width=70)
        self.slider_long = ctk.CTkSlider(self.cont_longitud, from_=4, to=64, command=self.cambio_slider, width=130, progress_color="#666666", button_color="#888888")
        self.seg_hex = ctk.CTkSegmentedButton(self.cont_longitud, values=["32", "64", "128"], selected_color="#555555", unselected_color="#222222")

        # Estado inicial
        self.lbl_long_txt.pack(side="right")
        self.slider_long.pack(side="right", padx=(0, 10))

        # --- Checkboxes ---
        f_ch = ctk.CTkFrame(t_gen, fg_color="#222222")
        f_ch.pack(fill="x", pady=10); f_ch.grid_columnconfigure((0,1), weight=1)
        
        self.var_min = ctk.BooleanVar(value=True); self.var_may = ctk.BooleanVar(value=True)
        self.var_num = ctk.BooleanVar(value=True); self.var_sym = ctk.BooleanVar(value=True)

        self.chk_min = ctk.CTkCheckBox(f_ch, text="Minúsculas (a-z)", variable=self.var_min, fg_color="#555555", command=lambda: self.var_preset.set("Personalizado"))
        self.chk_min.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.chk_may = ctk.CTkCheckBox(f_ch, text="Mayúsculas (A-Z)", variable=self.var_may, fg_color="#555555", command=lambda: self.var_preset.set("Personalizado"))
        self.chk_may.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        self.chk_num = ctk.CTkCheckBox(f_ch, text="Números (0-9)", variable=self.var_num, fg_color="#555555", command=lambda: self.var_preset.set("Personalizado"))
        self.chk_num.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        self.chk_sym = ctk.CTkCheckBox(f_ch, text="Símbolos (!@#$)", variable=self.var_sym, fg_color="#555555", command=lambda: self.var_preset.set("Personalizado"))
        self.chk_sym.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        ctk.CTkButton(t_gen, text="FORJAR CLAVE", font=("Arial", 14, "bold"), fg_color="#333333", border_width=1, border_color="#555555", command=self.generar).pack(fill="x", pady=10)

        # --- Resultados ---
        f_res = ctk.CTkFrame(t_gen, fg_color="transparent")
        f_res.pack(fill="x", pady=5)
        self.ent_res = ctk.CTkEntry(f_res, font=("Consolas", 18), justify="center", height=45)
        self.ent_res.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(f_res, text="Copiar", width=70, height=45, fg_color="#333333", command=lambda: pyperclip.copy(self.ent_res.get())).pack(side="right")

        self.bar_res = ctk.CTkProgressBar(t_gen, height=8, progress_color="#444444")
        self.bar_res.set(0); self.bar_res.pack(fill="x", pady=10)
        self.lbl_status = ctk.CTkLabel(t_gen, text="SISTEMA LISTO", font=("Arial", 12, "bold"), text_color="gray60")
        self.lbl_status.pack()

        # --- Analizador ---
        ctk.CTkLabel(t_ana, text="Auditoría de Seguridad", font=("Arial", 16, "bold")).pack(pady=10)
        self.ent_ana = ctk.CTkEntry(t_ana, font=("Consolas", 18), justify="center", height=45, show="*")
        self.ent_ana.pack(fill="x", padx=20, pady=10)
        self.ent_ana.bind("<KeyRelease>", self.ejecutar_auditoria)
        
        self.bar_ana = ctk.CTkProgressBar(t_ana, height=10); self.bar_ana.set(0); self.bar_ana.pack(fill="x", padx=20, pady=10)
        self.txt_sug = ctk.CTkTextbox(t_ana, height=180, fg_color="#1a1a1a", state="disabled", font=("Consolas", 13))
        self.txt_sug.pack(fill="both", expand=True, padx=20, pady=10)

    def ejecutar_auditoria(self, event=None):
        pwd = self.ent_ana.get()
        col, txt, sug = security.auditar_clave(pwd)
        self.bar_ana.configure(progress_color=col); self.bar_ana.set(1 if pwd else 0)
        self.txt_sug.configure(state="normal"); self.txt_sug.delete("1.0", "end")
        self.txt_sug.insert("1.0", "\n".join(sug)); self.txt_sug.configure(state="disabled")

if __name__ == "__main__":
    app = KeyForgeApp()
    app.mainloop()

# -- Hecho por Fernando Perez S. --