# security.py
import secrets
import string

# ==========================================
# BASE DE DATOS DE VULNERABILIDADES
# ==========================================
# Un 'set' en Python {} es más rápido para buscar que una lista []
CONTRASENAS_VULNERABLES = {
    "123456", "password", "123456789", "12345", "12345678", 
    "111111", "1234567", "qwerty", "1234567890", "1234", 
    "admin", "iloveyou", "contraseña", "admin123", "hola123", 
    "password123", "1234567890!", "qwertyuiop", "123123"
}

# ==========================================
# LÓGICA DE GENERACIÓN
# ==========================================
def generar_clave(longitud, usar_min, usar_mayus, usar_num, usar_sym):
    """Genera una contraseña criptográficamente segura."""
    chars = ""
    if usar_min: chars += string.ascii_lowercase
    if usar_mayus: chars += string.ascii_uppercase
    if usar_num: chars += string.digits
    if usar_sym: chars += string.punctuation
    
    if not chars:
        return None 
        
    return ''.join(secrets.choice(chars) for _ in range(longitud))

def generar_hexadecimal(longitud):
    """Genera una llave hexadecimal."""
    return secrets.token_hex(longitud // 2)

# ==========================================
# LÓGICA DE AUDITORÍA
# ==========================================
def auditar_clave(password):
    """Audita una contraseña contra reglas matemáticas y listas negras."""
    if not password:
        return "#DDD", "Escribe algo...", []
    
    # 1. VERIFICACIÓN CRÍTICA: Ataque de Diccionario
    # Convertimos a minúsculas para atrapar variaciones como "Password" o "PASSWORD"
    if password.lower() in CONTRASENAS_VULNERABLES:
        # Rojo oscuro para indicar peligro inminente
        return "#8B0000", "VULNERABLE", [
            "¡PELIGRO EXTREMO!",
            "- Esta clave está en listas de hackers.",
            "- Se puede romper en milisegundos.",
            "- Cámbiala de inmediato."
        ]
    
    # 2. EVALUACIÓN MATEMÁTICA (Si pasa la prueba del diccionario)
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
    return "#4CAF50", "FUERTE", ["¡Contraseña muy robusta y original!"]