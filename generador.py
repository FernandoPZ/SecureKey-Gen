import tkinter as tk
from tkinter import messagebox
import secrets
import string

def generar_password():
    # Obtener parámetros de la interfaz
    longitud = int(scale_longitud.get())
    caracteres = string.ascii_lowercase # Minúsculas por defecto
    
    if var_mayus.get():
        caracteres += string.ascii_uppercase
    if var_num.get():
        caracteres += string.digits
    if var_sym.get():
        caracteres += string.punctuation

    # Generar de forma segura
    password = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    
    # Mostrar en la pantalla
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, password)

def generar_hex():
    longitud = int(scale_longitud.get())
    # Genera una llave hexadecimal (2 caracteres por cada byte)
    llave = secrets.token_hex(longitud // 2)
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, llave)

# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Asistente de Seguridad - Generador")
root.geometry("400x450")
root.resizable(False, False)

# Título
label_titulo = tk.Label(root, text="Generador de Credenciales", font=("Arial", 14, "bold"))
label_titulo.pack(pady=10)

# Control de Longitud
label_lon = tk.Label(root, text="Longitud del código:")
label_lon.pack()
scale_longitud = tk.Scale(root, from_=8, to_=32, orient=tk.HORIZONTAL, length=200)
scale_longitud.set(12)
scale_longitud.pack(pady=5)

# Opciones (Checkbuttons)
var_mayus = tk.BooleanVar(value=True)
var_num = tk.BooleanVar(value=True)
var_sym = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Incluir Mayúsculas", variable=var_mayus).pack()
tk.Checkbutton(root, text="Incluir Números", variable=var_num).pack()
tk.Checkbutton(root, text="Incluir Símbolos", variable=var_sym).pack()

# Botones de Acción
btn_pass = tk.Button(root, text="Generar Contraseña", command=generar_password, bg="#4CAF50", fg="white")
btn_pass.pack(pady=10, fill='x', padx=50)

btn_hex = tk.Button(root, text="Generar Llave Hexadecimal", command=generar_hex, bg="#2196F3", fg="white")
btn_hex.pack(pady=5, fill='x', padx=50)

# Resultado
entry_resultado = tk.Entry(root, font=("Courier", 12), justify='center')
entry_resultado.pack(pady=20, fill='x', padx=20)

root.mainloop()