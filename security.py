import secrets
import string
import requests

# BASE DE DATOS DE VULNERABILIDADES
CONTRASENAS_VULNERABLES = {
    "123456", "password", "admin", "12345678", "12345", "qwerty"
}

def actualizar_diccionario_online():
    """Se conecta a internet para descargar las contraseñas más vulnerables."""
    global CONTRASENAS_VULNERABLES

    url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/Language-Specific/Spanish_common-usernames-and-passwords.txt"

    headers = {
        "User-Agent": "KeyForgeApp/1.0 (Python Security Tool)"
    }
    
    try:
        respuesta = requests.get(url, headers=headers, timeout=5)
        if respuesta.status_code == 200:
            claves_descargadas = respuesta.text.lower().splitlines()
            CONTRASENAS_VULNERABLES.update(claves_descargadas)
            return True, len(claves_descargadas)
        else:
            print(f"⚠️ Error del servidor: El código de estado fue {respuesta.status_code}")
            
    except requests.RequestException as e:
        print(f"⚠️ Error de red detallado: {e}")
        
    return False, len(CONTRASENAS_VULNERABLES)

# LÓGICA DE GENERACIÓN
def generar_clave(longitud, usar_min, usar_mayus, usar_num, usar_sym):
    chars = ""
    if usar_min: chars += string.ascii_lowercase
    if usar_mayus: chars += string.ascii_uppercase
    if usar_num: chars += string.digits
    if usar_sym: chars += string.punctuation
    
    if not chars: return None 
    return ''.join(secrets.choice(chars) for _ in range(longitud))

def generar_hexadecimal(longitud):
    return secrets.token_hex(longitud // 2)

# LÓGICA DE AUDITORÍA
def auditar_clave(password):
    if not password:
        return "#DDD", "Escribe algo...", []
    
    if password.lower() in CONTRASENAS_VULNERABLES:
        return "#8B0000", "VULNERABLE", [
            "¡PELIGRO EXTREMO!",
            "- Esta clave está en listas públicas de hackers.",
            "- Nunca la utilices en cuentas reales."
        ]
    
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

    if score <= 2: return "#FF4C4C", "DÉBIL", fallos
    if score <= 4: return "#FFD700", "MEDIA", fallos
    return "#4CAF50", "FUERTE", ["¡Contraseña muy robusta!"]