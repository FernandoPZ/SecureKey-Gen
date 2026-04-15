import customtkinter as ctk
from tkinter import messagebox
import pyperclip
import security

# --- CONFIGURACIÓN DEL TEMA MODERNO ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# FUNCIONES DE AYUDA Y UI
def optimizar_contraste(color_hex):
    """Convierte colores oscuros del backend en colores brillantes para el texto en modo oscuro."""
    mapa_colores = {
        "#8B0000": "#FF4444",  # Rojo oscuro -> Rojo brillante neón
        "#FF4C4C": "#FF6B6B",  # Rojo estándar -> Rojo pastel
        "#FFD700": "#FFD93D",  # Amarillo -> Amarillo brillante
        "#4CAF50": "#28C76F"   # Verde -> Verde esmeralda claro
    }
    return mapa_colores.get(color_hex, color_hex)

def actualizar_label_slider(valor):
    label_longitud_val.configure(text=f"{int(valor)} chars")

def aplicar_preset(seleccion):
    var_min.set(False); var_mayus.set(False); var_num.set(False); var_sym.set(False)
    
    if seleccion == "PIN (4 dígitos)":
        slider_longitud.set(4); var_num.set(True)
    elif seleccion == "Código Temporal (6 caps)":
        slider_longitud.set(6); var_mayus.set(True); var_num.set(True)
    elif seleccion == "Estándar Web (8 chars)":
        slider_longitud.set(8); var_min.set(True); var_mayus.set(True); var_num.set(True); var_sym.set(True)
    elif seleccion == "Seguridad Máxima (16 chars)":
        slider_longitud.set(16); var_min.set(True); var_mayus.set(True); var_num.set(True); var_sym.set(True)
    elif seleccion == "Llave Cripto (Hex)":
        generar_hex_ui()
    elif seleccion == "Frase de Seguridad":
        frase = security.generar_frase(4)
        entry_gen.delete(0, 'end')
        entry_gen.insert(0, frase)

        color, texto, _ = security.auditar_clave(frase)
        barra_seguridad_gen.configure(progress_color=color)
        barra_seguridad_gen.set(1)
        label_status_gen.configure(text=f"Seguridad: {texto}", text_color=optimizar_contraste(color))
        return
        
    actualizar_label_slider(slider_longitud.get())

def generar_y_mostrar_ui():
    longitud = int(slider_longitud.get())
    pwd = security.generar_clave(longitud, var_min.get(), var_mayus.get(), var_num.get(), var_sym.get())
    
    if pwd is None:
        messagebox.showwarning("Atención", "Selecciona al menos un tipo de carácter.")
        return
        
    entry_gen.delete(0, 'end')
    entry_gen.insert(0, pwd)
    
    color, texto, _ = security.auditar_clave(pwd)
    barra_seguridad_gen.configure(progress_color=color)
    barra_seguridad_gen.set(1)

    color_texto = optimizar_contraste(color)
    label_status_gen.configure(text=f"Seguridad: {texto}", text_color=color_texto)

def generar_hex_ui():
    longitud = int(slider_longitud.get())
    llave = security.generar_hexadecimal(longitud)
    
    entry_gen.delete(0, 'end')
    entry_gen.insert(0, llave)
    barra_seguridad_gen.configure(progress_color="#1f6aa5")
    barra_seguridad_gen.set(1)
    label_status_gen.configure(text="MODO: HEXADECIMAL", text_color="#5DA8FF")
    actualizar_label_slider(longitud)

def copiar_clave():
    clave = entry_gen.get()
    if clave:
        pyperclip.copy(clave)
        btn_copiar.configure(text="✔️", fg_color="#28a745")
        app.after(1500, lambda: btn_copiar.configure(text="📋", fg_color="#1f6aa5"))

def evento_analizar_ui(event=None):
    pwd = entry_analizar.get()
    color, texto, sugerencias = security.auditar_clave(pwd)
    
    barra_seguridad_ana.configure(progress_color=color if pwd else "gray")
    barra_seguridad_ana.set(1 if pwd else 0)
    
    color_texto = optimizar_contraste(color) if pwd else "gray"
    label_status_ana.configure(text=f"Estado: {texto}", text_color=color_texto)
    
    text_sugerencias.configure(state='normal')
    text_sugerencias.delete('1.0', 'end')
    text_sugerencias.insert('end', "\n".join(sugerencias))
    text_sugerencias.configure(state='disabled')

# INTERFAZ GRÁFICA PRINCIPAL
app = ctk.CTk()
app.title("KeyForge Suite")
app.geometry("500x500")
app.minsize(450, 500)
app.resizable(True, True)

security.actualizar_diccionario_online()
security.descargar_diccionario_frases()

# --- ESTRUCTURA PRINCIPAL ---
tabview = ctk.CTkTabview(app)
tabview.pack(padx=15, pady=10, fill="both", expand=True)
tab_gen = tabview.add(" ⚒️ Generador ")
tab_ana = tabview.add(" 🔍 Analizador ")

# PESTAÑA 1: GENERADOR
# Fila 1: Presets y Longitud
frame_top = ctk.CTkFrame(tab_gen, fg_color="transparent")
frame_top.pack(fill="x", pady=(5, 10))

opciones_presets = ["PIN (4 dígitos)", "Código Temporal (6 caps)", "Estándar Web (8 chars)", "Seguridad Máxima (16 chars)", "Frase de Seguridad", "Llave Cripto (Hex)"]
ctk.CTkOptionMenu(frame_top, values=opciones_presets, command=aplicar_preset).pack(side="left", fill="x", expand=True, padx=(0, 10))

label_longitud_val = ctk.CTkLabel(frame_top, text="16 chars", font=ctk.CTkFont(weight="bold"), width=60)
label_longitud_val.pack(side="right")
slider_longitud = ctk.CTkSlider(frame_top, from_=4, to=64, command=actualizar_label_slider, width=120)
slider_longitud.set(16)
slider_longitud.pack(side="right", padx=10)

# Fila 2: Casillas en Cuadrícula 2x2
frame_checks = ctk.CTkFrame(tab_gen)
frame_checks.pack(fill="x", pady=10)
frame_checks.grid_columnconfigure((0, 1), weight=1)

var_min = ctk.BooleanVar(value=True); var_mayus = ctk.BooleanVar(value=True)
var_num = ctk.BooleanVar(value=True); var_sym = ctk.BooleanVar(value=True)

ctk.CTkCheckBox(frame_checks, text="Minúsculas (a-z)", variable=var_min).grid(row=0, column=0, pady=10, padx=15, sticky="w")
ctk.CTkCheckBox(frame_checks, text="Mayúsculas (A-Z)", variable=var_mayus).grid(row=0, column=1, pady=10, padx=15, sticky="w")
ctk.CTkCheckBox(frame_checks, text="Números (0-9)", variable=var_num).grid(row=1, column=0, pady=10, padx=15, sticky="w")
ctk.CTkCheckBox(frame_checks, text="Símbolos (!@#$)", variable=var_sym).grid(row=1, column=1, pady=10, padx=15, sticky="w")

# Fila 3: Botón Generar
ctk.CTkButton(tab_gen, text="FORJAR CLAVE", font=ctk.CTkFont(weight="bold", size=14), fg_color="#28a745", hover_color="#218838", command=generar_y_mostrar_ui).pack(fill="x", pady=10)

# Fila 4: Resultado y Copiar (Lado a lado)
frame_res = ctk.CTkFrame(tab_gen, fg_color="transparent")
frame_res.pack(fill="x", pady=5)

entry_gen = ctk.CTkEntry(frame_res, font=ctk.CTkFont(family="Consolas", size=18), justify="center", height=40)
entry_gen.pack(side="left", fill="x", expand=True, padx=(0, 10))

btn_copiar = ctk.CTkButton(frame_res, text="📋", width=45, height=40, command=copiar_clave, font=ctk.CTkFont(size=18))
btn_copiar.pack(side="right")

# Fila 5: Estado
barra_seguridad_gen = ctk.CTkProgressBar(tab_gen, height=6)
barra_seguridad_gen.set(0)
barra_seguridad_gen.pack(fill="x", pady=(10, 5))
label_status_gen = ctk.CTkLabel(tab_gen, text="Esperando...", font=ctk.CTkFont(weight="bold", size=12))
label_status_gen.pack()

# PESTAÑA 2: ANALIZADOR
ctk.CTkLabel(tab_ana, text="Auditoría en Tiempo Real", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

entry_analizar = ctk.CTkEntry(tab_ana, font=ctk.CTkFont(family="Consolas", size=18), justify="center", height=40, show="*")
entry_analizar.pack(pady=10, fill="x")
entry_analizar.bind("<KeyRelease>", evento_analizar_ui)

barra_seguridad_ana = ctk.CTkProgressBar(tab_ana, height=8)
barra_seguridad_ana.set(0)
barra_seguridad_ana.pack(pady=(5, 10), fill="x")

label_status_ana = ctk.CTkLabel(tab_ana, text="Estado: Esperando entrada...", font=ctk.CTkFont(weight="bold"))
label_status_ana.pack()

text_sugerencias = ctk.CTkTextbox(tab_ana, height=120, state="disabled")
text_sugerencias.pack(pady=10, fill="both", expand=True)

app.mainloop()