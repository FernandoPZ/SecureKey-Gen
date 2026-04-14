import secrets
import string

def generar_clave(longitud, usar_min, usar_mayus, usar_num, usar_sym):
    """Genera una contraseña criptográficamente segura basada en los parámetros."""
    chars = ""
    if usar_min: chars += string.ascii_lowercase
    if usar_mayus: chars += string.ascii_uppercase
    if usar_num: chars += string.digits
    if usar_sym: chars += string.punctuation
    
    if not chars:
        return None # Indica que no se seleccionaron caracteres
        
    return ''.join(secrets.choice(chars) for _ in range(longitud))

def generar_hexadecimal(longitud):
    """Genera una llave hexadecimal."""
    return secrets.token_hex(longitud // 2)

def auditar_clave(password):
    """Audita una contraseña y devuelve su color, estado y sugerencias."""
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

    if score <= 2: return "#FF4C4C", "DÉBIL", fallos
    if score <= 4: return "#FFD700", "MEDIA", fallos
    return "#4CAF50", "FUERTE", ["¡Contraseña muy robusta!"]