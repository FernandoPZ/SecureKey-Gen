import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip # Librería opcional para copiar al portapapeles

def evaluar_seguridad(password):
    longitud = len(password)
    score = 0
    if longitud >= 12: score += 1
    if any(c in string.ascii_uppercase for c in password): score += 1
    if any(c in string.ascii_lowercase for c in password): score += 1
    if any(c in string.digits for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if longitud < 8 or score < 3:
        return "#FF4C4C", "DÉBIL"
    elif score == 4:
        return "#FFD700", "MEDIA"
    else:
        return "#4CAF50", "FUERTE"

def copiar_clave():
    clave = entry_resultado.get()
    if clave:
        pyperclip.copy(clave)
        messagebox.showinfo("KeyForge", "¡Copiado al portapapeles!")

def generar_password():
    longitud = int(scale_longitud.get())
    caracteres = ""
    
    # Construcción dinámica de la "bolsa" de caracteres
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

# --- Configuración Interfaz ---
root = tk.Tk()
root.title("KeyForge v1.1")
root.geometry("420x550")
root.configure(bg="#F5F5F5")

tk.Label(root, text="🛡️ KeyForge", font=("Arial", 20, "bold"), bg="#F5F5F5").pack(pady=15)

frame_config = tk.LabelFrame(root, text=" Parámetros de Generación ", padx=20, pady=10)
frame_config.pack(padx=20, fill="x")

scale_longitud = tk.Scale(frame_config, from_=4, to_=64, orient=tk.HORIZONTAL, label="Longitud de clave")
scale_longitud.set(16)
scale_longitud.pack(fill="x")

# Variables de control
var_min = tk.BooleanVar(value=True)
var_mayus = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True)
var_sym = tk.BooleanVar(value=True)

# Checkboxes actualizados
tk.Checkbutton(frame_config, text="Minúsculas (a-z)", variable=var_min).pack(anchor="w")
tk.Checkbutton(frame_config, text="Mayúsculas (A-Z)", variable=var_mayus).pack(anchor="w")
tk.Checkbutton(frame_config, text="Números (0-9)", variable=var_num).pack(anchor="w")
tk.Checkbutton(frame_config, text="Símbolos (!#$%)", variable=var_sym).pack(anchor="w")

# Botones
tk.Button(root, text="GENERAR CLAVE", command=generar_password, bg="#2E7D32", fg="white", font=("Arial", 10, "bold")).pack(pady=10, fill="x", padx=50)

# Resultado y Copiar
entry_resultado = tk.Entry(root, font=("Consolas", 14), justify='center')
entry_resultado.pack(pady=10, padx=20, fill="x")

tk.Button(root, text="📋 Copiar Clave", command=copiar_clave, bg="#1976D2", fg="white").pack(pady=5)

label_estado = tk.Label(root, text="Ajusta los parámetros y genera", font=("Arial", 9), bg="#F5F5F5")
label_estado.pack(pady=5)

canvas_seguridad = tk.Canvas(root, height=8, bg="#DDD", highlightthickness=0)
canvas_seguridad.pack(fill="x", padx=60)

root.mainloop()