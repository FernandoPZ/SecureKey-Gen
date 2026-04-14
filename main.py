import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

def aplicar_preset(seleccion):
    """Ajusta los controles según el estándar seleccionado."""
    # Resetear checkboxes
    var_min.set(False); var_mayus.set(False)
    var_num.set(False); var_sym.set(False)
    
    if seleccion == "PIN (4 dígitos)":
        scale_longitud.set(4)
        var_num.set(True)
    elif seleccion == "Código Temporal (6 caps)":
        scale_longitud.set(6)
        var_mayus.set(True); var_num.set(True)
    elif seleccion == "Estándar Web (8 chars)":
        scale_longitud.set(8)
        var_min.set(True); var_mayus.set(True); var_num.set(True); var_sym.set(True)
    elif seleccion == "Seguridad Máxima (16 chars)":
        scale_longitud.set(16)
        var_min.set(True); var_mayus.set(True); var_num.set(True); var_sym.set(True)
    elif seleccion == "Llave Cripto (Hex)":
        generar_hex() # Llama directo a la función hex

def evaluar_seguridad(password):
    longitud = len(password)
    score = sum([
        longitud >= 12,
        any(c in string.ascii_uppercase for c in password),
        any(c in string.ascii_lowercase for c in password),
        any(c in string.digits for c in password),
        any(c in string.punctuation for c in password)
    ])
    if longitud < 8 or score < 3: return "#FF4C4C", "DÉBIL"
    elif score == 4: return "#FFD700", "MEDIA"
    else: return "#4CAF50", "FUERTE"

def copiar_clave():
    clave = entry_resultado.get()
    if clave:
        pyperclip.copy(clave)
        messagebox.showinfo("KeyForge", "¡Copiado al portapapeles!")

def generar_password():
    longitud = int(scale_longitud.get())
    caracteres = ""
    if var_min.get(): caracteres += string.ascii_lowercase
    if var_mayus.get(): caracteres += string.ascii_uppercase
    if var_num.get(): caracteres += string.digits
    if var_sym.get(): caracteres += string.punctuation

    if not caracteres:
        messagebox.showwarning("Atención", "Selecciona al menos un tipo de carácter.")
        return

    password = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, password)
    
    color, texto = evaluar_seguridad(password)
    canvas_seguridad.config(bg=color)
    label_estado.config(text=f"Seguridad: {texto}", fg=color)

def generar_hex():
    longitud = int(scale_longitud.get())
    llave = secrets.token_hex(longitud // 2)
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, llave)
    canvas_seguridad.config(bg="#2196F3")
    label_estado.config(text="MODO: HEXADECIMAL", fg="#2196F3")

# --- Interfaz ---
root = tk.Tk()
root.title("KeyForge v1.2")
root.geometry("440x650")
root.configure(bg="#F5F5F5")

tk.Label(root, text="🛡️ KeyForge", font=("Arial", 20, "bold"), bg="#F5F5F5").pack(pady=15)

# Sección de Presets
frame_presets = tk.LabelFrame(root, text=" Ajustes Predefinidos ", padx=10, pady=10)
frame_presets.pack(padx=20, fill="x", pady=5)

opciones_presets = [
    "PIN (4 dígitos)", 
    "Código Temporal (6 caps)", 
    "Estándar Web (8 chars)", 
    "Seguridad Máxima (16 chars)",
    "Llave Cripto (Hex)"
]
var_preset = tk.StringVar(root)
var_preset.set("Seleccionar estándar...")
drop_presets = tk.OptionMenu(frame_presets, var_preset, *opciones_presets, command=aplicar_preset)
drop_presets.pack(fill="x")

# Parámetros Manuales
frame_config = tk.LabelFrame(root, text=" Configuración Manual ", padx=20, pady=10)
frame_config.pack(padx=20, fill="x", pady=10)

scale_longitud = tk.Scale(frame_config, from_=4, to_=64, orient=tk.HORIZONTAL, label="Longitud")
scale_longitud.set(12)
scale_longitud.pack(fill="x")

var_min = tk.BooleanVar(value=True); var_mayus = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True); var_sym = tk.BooleanVar(value=True)

tk.Checkbutton(frame_config, text="Minúsculas", variable=var_min).pack(anchor="w")
tk.Checkbutton(frame_config, text="Mayúsculas", variable=var_mayus).pack(anchor="w")
tk.Checkbutton(frame_config, text="Números", variable=var_num).pack(anchor="w")
tk.Checkbutton(frame_config, text="Símbolos", variable=var_sym).pack(anchor="w")

# Botones y Salida
tk.Button(root, text="GENERAR", command=generar_password, bg="#2E7D32", fg="white", font=("Arial", 12, "bold")).pack(pady=10, fill="x", padx=50)
entry_resultado = tk.Entry(root, font=("Consolas", 14), justify='center', bd=2)
entry_resultado.pack(pady=5, padx=20, fill="x")
tk.Button(root, text="📋 Copiar", command=copiar_clave, bg="#1976D2", fg="white").pack(pady=5)

label_estado = tk.Label(root, text="Listo para forjar", font=("Arial", 9), bg="#F5F5F5")
label_estado.pack()
canvas_seguridad = tk.Canvas(root, height=8, bg="#DDD", highlightthickness=0)
canvas_seguridad.pack(fill="x", padx=60, pady=10)

root.mainloop()