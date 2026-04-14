import tkinter as tk
from tkinter import messagebox
import secrets
import string

def evaluar_seguridad(password):
    """Calcula la fortaleza de la contraseña y devuelve un color y texto."""
    longitud = len(password)
    score = 0
    if longitud >= 12: score += 1
    if any(c in string.ascii_uppercase for c in password): score += 1
    if any(c in string.digits for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if longitud < 8 or score < 2:
        return "#FF4C4C", "DÉBIL"  # Rojo
    elif score == 3:
        return "#FFD700", "MEDIA"  # Amarillo/Oro
    else:
        return "#4CAF50", "FUERTE" # Verde

def actualizar_interfaz_seguridad(password):
    color, texto = evaluar_seguridad(password)
    canvas_seguridad.config(bg=color)
    label_estado.config(text=f"Seguridad: {texto}", fg=color)

def generar_password():
    longitud = int(scale_longitud.get())
    caracteres = string.ascii_lowercase
    if var_mayus.get(): caracteres += string.ascii_uppercase
    if var_num.get(): caracteres += string.digits
    if var_sym.get(): caracteres += string.punctuation

    password = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, password)
    actualizar_interfaz_seguridad(password)

def generar_hex():
    longitud = int(scale_longitud.get())
    llave = secrets.token_hex(longitud // 2)
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, llave)
    canvas_seguridad.config(bg="#2196F3") # Azul para llaves técnicas
    label_estado.config(text="MODO: HEXADECIMAL", fg="#2196F3")

# --- Interfaz Gráfica ---
root = tk.Tk()
root.title("KeyForge v1.0")
root.geometry("400x500")
root.configure(bg="#F0F0F0")

# Encabezado
tk.Label(root, text="🛡️ KeyForge", font=("Segoe UI", 18, "bold"), bg="#F0F0F0").pack(pady=15)

# Configuración
frame_config = tk.LabelFrame(root, text=" Configuración ", padx=20, pady=10, bg="#F0F0F0")
frame_config.pack(padx=20, fill="x")

scale_longitud = tk.Scale(frame_config, from_=8, to_=64, orient=tk.HORIZONTAL, label="Longitud")
scale_longitud.set(16)
scale_longitud.pack(fill="x")

var_mayus = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True)
var_sym = tk.BooleanVar(value=True)

tk.Checkbutton(frame_config, text="Mayúsculas (A-Z)", variable=var_mayus, bg="#F0F0F0").pack(anchor="w")
tk.Checkbutton(frame_config, text="Números (0-9)", variable=var_num, bg="#F0F0F0").pack(anchor="w")
tk.Checkbutton(frame_config, text="Símbolos (!@#$)", variable=var_sym, bg="#F0F0F0").pack(anchor="w")

# Botones
tk.Button(root, text="FORJAR CONTRASEÑA", command=generar_password, bg="#333", fg="white", font=("Arial", 10, "bold")).pack(pady=10, fill="x", padx=40)
tk.Button(root, text="Generar Llave Hex", command=generar_hex, bg="#555", fg="white").pack(fill="x", padx=40)

# Resultado y Seguridad
entry_resultado = tk.Entry(root, font=("Consolas", 14), justify='center', bd=2)
entry_resultado.pack(pady=15, padx=20, fill="x")

label_estado = tk.Label(root, text="Esperando generación...", font=("Arial", 9, "bold"), bg="#F0F0F0")
label_estado.pack()

canvas_seguridad = tk.Canvas(root, height=10, bg="#DDD", highlightthickness=0)
canvas_seguridad.pack(fill="x", padx=50, pady=5)

root.mainloop()