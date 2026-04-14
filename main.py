import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip

# ==========================================
# LÓGICA DE LA PESTAÑA 1: GENERADOR
# ==========================================

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
        generar_hex()
        return # Evita ejecutar la generación normal

def evaluar_seguridad_gen(password):
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

def generar_y_mostrar():
    longitud = int(scale_longitud.get())
    chars = ""
    if var_min.get(): chars += string.ascii_lowercase
    if var_mayus.get(): chars += string.ascii_uppercase
    if var_num.get(): chars += string.digits
    if var_sym.get(): chars += string.punctuation
    
    if not chars:
        messagebox.showwarning("Atención", "Selecciona al menos un tipo de carácter.")
        return
        
    pwd = ''.join(secrets.choice(chars) for _ in range(longitud))
    entry_gen.delete(0, tk.END)
    entry_gen.insert(0, pwd)
    
    color, texto = evaluar_seguridad_gen(pwd)
    canvas_gen.config(bg=color)
    label_status_gen.config(text=f"Seguridad: {texto}", fg=color)

def generar_hex():
    longitud = int(scale_longitud.get())
    llave = secrets.token_hex(longitud // 2)
    entry_gen.delete(0, tk.END)
    entry_gen.insert(0, llave)
    canvas_gen.config(bg="#2196F3")
    label_status_gen.config(text="MODO: HEXADECIMAL", fg="#2196F3")

def copiar_clave():
    clave = entry_gen.get()
    if clave:
        pyperclip.copy(clave)
        messagebox.showinfo("KeyForge", "¡Copiado al portapapeles!")

# ==========================================
# LÓGICA DE LA PESTAÑA 2: ANALIZADOR
# ==========================================

def analizar_password(password):
    if not password:
        return "#DDD", "Escribe algo...", []
    
    longitud = len(password)
    fallos = []
    score = 0
    
    if longitud < 8: fallos.append("- Muy corta (mín. 8)")
    elif longitud >= 12: score += 1
    
    if any(c in string.ascii_uppercase for c in password): score += 1
    else: fallos.append("- Falta Mayúscula")
    
    if any(c in string.ascii_lowercase for c in password): score += 1
    else: fallos.append("- Falta Minúscula")
    
    if any(c in string.digits for c in password): score += 1
    else: fallos.append("- Falta Número")
    
    if any(c in string.punctuation for c in password): score += 1
    else: fallos.append("- Falta Símbolo")

    if score <= 2: return "#FF4C4C", "CRÍTICA", fallos
    if score <= 4: return "#FFD700", "ACEPTABLE", fallos
    return "#4CAF50", "EXCELENTE", ["¡Contraseña muy robusta!"]

def evento_analizar(event):
    pwd = entry_analizar.get()
    color, texto, sugerencias = analizar_password(pwd)
    canvas_ana.config(bg=color)
    label_status_ana.config(text=f"Estado: {texto}", fg=color)
    
    text_sugerencias.config(state='normal')
    text_sugerencias.delete('1.0', tk.END)
    text_sugerencias.insert(tk.END, "\n".join(sugerencias))
    text_sugerencias.config(state='disabled')

# ==========================================
# INTERFAZ GRÁFICA PRINCIPAL
# ==========================================
root = tk.Tk()
root.title("KeyForge Suite v2.1")
root.geometry("450x700") # Ventana ligeramente más alta para acomodar todo

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --- PESTAÑA 1: GENERADOR ---
tab_gen = tk.Frame(notebook, bg="#F5F5F5")
notebook.add(tab_gen, text=" ⚒️ Generador ")

tk.Label(tab_gen, text="🛡️ KeyForge", font=("Arial", 20, "bold"), bg="#F5F5F5").pack(pady=10)

# Presets
frame_presets = tk.LabelFrame(tab_gen, text=" Ajustes Predefinidos ", padx=10, pady=5, bg="#F5F5F5")
frame_presets.pack(padx=20, fill="x")

opciones_presets = [
    "PIN (4 dígitos)", 
    "Código Temporal (6 caps)", 
    "Estándar Web (8 chars)", 
    "Seguridad Máxima (16 chars)",
    "Llave Cripto (Hex)"
]
var_preset = tk.StringVar(tab_gen)
var_preset.set("Seleccionar estándar...")
drop_presets = tk.OptionMenu(frame_presets, var_preset, *opciones_presets, command=aplicar_preset)
drop_presets.pack(fill="x")

# Configuración Manual
frame_config = tk.LabelFrame(tab_gen, text=" Configuración Manual ", padx=20, pady=5, bg="#F5F5F5")
frame_config.pack(padx=20, fill="x", pady=10)

scale_longitud = tk.Scale(frame_config, from_=4, to_=64, orient=tk.HORIZONTAL, label="Longitud", bg="#F5F5F5")
scale_longitud.set(16)
scale_longitud.pack(fill="x")

var_min = tk.BooleanVar(value=True); var_mayus = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True); var_sym = tk.BooleanVar(value=True)

tk.Checkbutton(frame_config, text="Minúsculas", variable=var_min, bg="#F5F5F5").pack(anchor="w")
tk.Checkbutton(frame_config, text="Mayúsculas", variable=var_mayus, bg="#F5F5F5").pack(anchor="w")
tk.Checkbutton(frame_config, text="Números", variable=var_num, bg="#F5F5F5").pack(anchor="w")
tk.Checkbutton(frame_config, text="Símbolos", variable=var_sym, bg="#F5F5F5").pack(anchor="w")

# Botones y Salida Generador
tk.Button(tab_gen, text="GENERAR", command=generar_y_mostrar, bg="#2E7D32", fg="white", font=("Arial", 12, "bold")).pack(pady=10, fill="x", padx=50)
entry_gen = tk.Entry(tab_gen, font=("Consolas", 14), justify='center', bd=2)
entry_gen.pack(pady=5, padx=20, fill="x")
tk.Button(tab_gen, text="📋 Copiar", command=copiar_clave, bg="#1976D2", fg="white").pack(pady=5)

label_status_gen = tk.Label(tab_gen, text="Listo para forjar", font=("Arial", 9), bg="#F5F5F5")
label_status_gen.pack()
canvas_gen = tk.Canvas(tab_gen, height=8, bg="#DDD", highlightthickness=0)
canvas_gen.pack(fill="x", padx=60, pady=5)


# --- PESTAÑA 2: ANALIZADOR ---
tab_ana = tk.Frame(notebook, bg="#F5F5F5")
notebook.add(tab_ana, text=" 🔍 Analizador ")

tk.Label(tab_ana, text="Auditoría de Seguridad", font=("Arial", 16, "bold"), bg="#F5F5F5").pack(pady=20)
tk.Label(tab_ana, text="Ingresa una contraseña para evaluarla:", bg="#F5F5F5").pack()

entry_analizar = tk.Entry(tab_ana, font=("Consolas", 14), justify='center', show="*")
entry_analizar.pack(pady=10, padx=20, fill='x')
entry_analizar.bind("<KeyRelease>", evento_analizar)

label_status_ana = tk.Label(tab_ana, text="Estado: Esperando...", font=("Arial", 10, "bold"), bg="#F5F5F5")
label_status_ana.pack(pady=5)

canvas_ana = tk.Canvas(tab_ana, height=10, bg="#DDD", highlightthickness=0)
canvas_ana.pack(fill='x', padx=60)

tk.Label(tab_ana, text="Sugerencias de mejora:", bg="#F5F5F5", font=("Arial", 9, "italic")).pack(pady=(20,0))
text_sugerencias = tk.Text(tab_ana, height=8, width=40, state='disabled', bg="#EEE")
text_sugerencias.pack(pady=10, padx=40)

root.mainloop()