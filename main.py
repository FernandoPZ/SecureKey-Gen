import customtkinter as ctk
from tkinter import messagebox
import pyperclip
import security

# --- CONFIGURACIÓN DEL TEMA MODERNO ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# FUNCIONES PUENTE
def actualizar_label_slider(valor):
    """Actualiza el texto del número al mover el slider."""
    label_longitud_val.configure(text=f"{int(valor)} caracteres")

def aplicar_preset(seleccion):
    var_min.set(False); var_mayus.set(False)
    var_num.set(False); var_sym.set(False)
    
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
    label_status_gen.configure(text=f"Seguridad: {texto}", text_color=color)

def generar_hex_ui():
    longitud = int(slider_longitud.get())
    llave = security.generar_hexadecimal(longitud)
    
    entry_gen.delete(0, 'end')
    entry_gen.insert(0, llave)
    barra_seguridad_gen.configure(progress_color="#1f6aa5")
    barra_seguridad_gen.set(1)
    label_status_gen.configure(text="MODO: HEXADECIMAL", text_color="#1f6aa5")
    actualizar_label_slider(longitud)

def copiar_clave():
    clave = entry_gen.get()
    if clave:
        pyperclip.copy(clave)
        btn_copiar.configure(text="¡Copiado!", fg_color="#28a745")
        app.after(2000, lambda: btn_copiar.configure(text="📋 Copiar al Portapapeles", fg_color="#1f6aa5"))

def evento_analizar_ui(event=None):
    pwd = entry_analizar.get()
    color, texto, sugerencias = security.auditar_clave(pwd)
    
    barra_seguridad_ana.configure(progress_color=color if pwd else "gray")
    barra_seguridad_ana.set(1 if pwd else 0)
    label_status_ana.configure(text=f"Estado: {texto}", text_color=color if pwd else "gray")
    
    text_sugerencias.configure(state='normal')
    text_sugerencias.delete('1.0', 'end')
    text_sugerencias.insert('end', "\n".join(sugerencias))
    text_sugerencias.configure(state='disabled')

# INTERFAZ GRÁFICA PRINCIPAL
app = ctk.CTk()
app.title("KeyForge Suite v3.0")
app.geometry("450x750")
app.resizable(False, False)

# --- INICIALIZAR BASE DE DATOS EN SEGUNDO PLANO ---
exito, cantidad = security.actualizar_diccionario_online()

# --- TÍTULO Y PESTAÑAS ---
lbl_titulo = ctk.CTkLabel(app, text="🛡️ KeyForge", font=ctk.CTkFont(size=24, weight="bold"))
lbl_titulo.pack(pady=(20, 10))

tabview = ctk.CTkTabview(app, width=400, height=650)
tabview.pack(padx=20, pady=10, fill="both", expand=True)

tab_gen = tabview.add("Generador")
tab_ana = tabview.add("Analizador")

# PESTAÑA 1: GENERADOR

# Presets
ctk.CTkLabel(tab_gen, text="Ajustes Rápidos", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5), anchor="w", padx=20)
opciones_presets = ["PIN (4 dígitos)", "Código Temporal (6 caps)", "Estándar Web (8 chars)", "Seguridad Máxima (16 chars)", "Llave Cripto (Hex)"]
ctk.CTkOptionMenu(tab_gen, values=opciones_presets, command=aplicar_preset).pack(padx=20, fill="x")

# Longitud
frame_longitud = ctk.CTkFrame(tab_gen, fg_color="transparent")
frame_longitud.pack(fill="x", padx=20, pady=(20, 5))
ctk.CTkLabel(frame_longitud, text="Longitud:").pack(side="left")
label_longitud_val = ctk.CTkLabel(frame_longitud, text="16 caracteres", font=ctk.CTkFont(weight="bold"))
label_longitud_val.pack(side="right")

slider_longitud = ctk.CTkSlider(tab_gen, from_=4, to=64, command=actualizar_label_slider)
slider_longitud.set(16)
slider_longitud.pack(padx=20, fill="x", pady=5)

# Checkboxes
frame_checks = ctk.CTkFrame(tab_gen)
frame_checks.pack(padx=20, pady=20, fill="x")

var_min = ctk.BooleanVar(value=True)
var_mayus = ctk.BooleanVar(value=True)
var_num = ctk.BooleanVar(value=True)
var_sym = ctk.BooleanVar(value=True)

ctk.CTkCheckBox(frame_checks, text="Minúsculas (a-z)", variable=var_min).pack(pady=10, padx=20, anchor="w")
ctk.CTkCheckBox(frame_checks, text="Mayúsculas (A-Z)", variable=var_mayus).pack(pady=10, padx=20, anchor="w")
ctk.CTkCheckBox(frame_checks, text="Números (0-9)", variable=var_num).pack(pady=10, padx=20, anchor="w")
ctk.CTkCheckBox(frame_checks, text="Símbolos (!@#$)", variable=var_sym).pack(pady=10, padx=20, anchor="w")

# Generar y Resultados
btn_generar = ctk.CTkButton(tab_gen, text="FORJAR CLAVE", font=ctk.CTkFont(weight="bold"), fg_color="#28a745", hover_color="#218838", command=generar_y_mostrar_ui)
btn_generar.pack(pady=(10, 20), fill="x", padx=40)

entry_gen = ctk.CTkEntry(tab_gen, font=ctk.CTkFont(family="Consolas", size=18), justify="center", height=40)
entry_gen.pack(padx=20, fill="x")

barra_seguridad_gen = ctk.CTkProgressBar(tab_gen, height=8)
barra_seguridad_gen.set(0)
barra_seguridad_gen.pack(padx=20, pady=10, fill="x")

label_status_gen = ctk.CTkLabel(tab_gen, text="Ajusta los parámetros para comenzar", font=ctk.CTkFont(size=12))
label_status_gen.pack()

btn_copiar = ctk.CTkButton(tab_gen, text="📋 Copiar al Portapapeles", command=copiar_clave)
btn_copiar.pack(pady=10, fill="x", padx=60)

# PESTAÑA 2: ANALIZADOR
ctk.CTkLabel(tab_ana, text="Auditoría en Tiempo Real", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))
ctk.CTkLabel(tab_ana, text="Ingresa una clave para evaluar su resistencia frente\na reglas matemáticas y diccionarios de hackers.").pack(pady=5)

entry_analizar = ctk.CTkEntry(tab_ana, font=ctk.CTkFont(family="Consolas", size=18), justify="center", height=40, show="*")
entry_analizar.pack(padx=20, pady=20, fill="x")
entry_analizar.bind("<KeyRelease>", evento_analizar_ui)

label_status_ana = ctk.CTkLabel(tab_ana, text="Estado: Esperando entrada...", font=ctk.CTkFont(weight="bold"))
label_status_ana.pack(pady=5)

barra_seguridad_ana = ctk.CTkProgressBar(tab_ana, height=10)
barra_seguridad_ana.set(0)
barra_seguridad_ana.pack(padx=40, pady=10, fill="x")

ctk.CTkLabel(tab_ana, text="Reporte de Vulnerabilidades:", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5), anchor="w", padx=20)
text_sugerencias = ctk.CTkTextbox(tab_ana, height=150, state="disabled")
text_sugerencias.pack(padx=20, pady=5, fill="x")

app.mainloop()