import secrets
import string
import requests

# BASE DE DATOS DE VULNERABILIDADES
CONTRASENAS_VULNERABLES = {
    # Clásicos Numéricos y Secuencias de Teclado (Universales)
    "123456", "123456789", "12345678", "12345", "1234567", "111111", "1234", "123123", 
    "qwerty", "qwertyuiop", "asdfgh", "zxcvbnm", "1q2w3e", "000000",

    # Top Anglosajón (Inglés)
    "password", "password123", "admin", "admin123", "iloveyou", "letmein", "monkey", 
    "dragon", "sunshine", "welcome", "hello", "shadow", "football", "baseball", "ninja",

    # Top Hispanohablante (Español)
    "contraseña", "tequiero", "teamo", "madrid", "barcelona", "futbol", "america", 
    "chivas", "cruzazul", "hola", "hola123", "princesa", "estrella", "corazon", 
    "sistemas", "usuario", "invitado", "secreto", "dios",

    # Nombres propios comunes usados como clave
    "carlos", "daniel", "alejandro", "andrea", "maria", "juan", "david", "jorge", "pedro"
}

PINS_PROHIBIDOS = {
    "0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999", # Repeticiones
    "1234", "2345", "3456", "4567", "5678", "6789", # Secuencias ascendentes
    "9876", "8765", "7654", "6543", "5432", "4321", # Secuencias descendentes
    "2580", "0852", "1379", "9731", "1212", "6969"  # Patrones de teclado visuales
}

def actualizar_diccionario_online():
    """Descarga múltiples listas de credenciales y las fusiona."""
    global CONTRASENAS_VULNERABLES
    
    # Lista de diccionarios a descargar
    urls = [
        # Top 10,000 global (Mayormente inglés y patrones numéricos)
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt",
        # Específico en español
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/Language-Specific/Spanish_common-usernames-and-passwords.txt"
    ]
    
    headers = {"User-Agent": "KeyForgeApp/1.0"}
    
    for url in urls:
        try:
            respuesta = requests.get(url, headers=headers, timeout=5)
            if respuesta.status_code == 200:
                lineas = respuesta.text.lower().splitlines()
                nuevas_claves = set()
                
                for linea in lineas:
                    if ":" in linea:
                        partes = linea.split(":")
                        nuevas_claves.update([p.strip() for p in partes if p.strip()])
                    else:
                        nuevas_claves.add(linea.strip())
                
                CONTRASENAS_VULNERABLES.update(nuevas_claves)
                
        except requests.RequestException:
            print(f"⚠️ Error al conectar con: {url}")
            
    return True, len(CONTRASENAS_VULNERABLES)

# LÓGICA DE GENERACIÓN
def generar_clave(longitud, usar_min, usar_mayus, usar_num, usar_sym):
    """Genera una contraseña criptográficamente segura, con filtro de calidad para PINs."""
    chars_permitidos = ""
    caracteres_obligatorios = []
    
    if usar_min:
        chars_permitidos += string.ascii_lowercase
        caracteres_obligatorios.append(secrets.choice(string.ascii_lowercase))
    if usar_mayus:
        chars_permitidos += string.ascii_uppercase
        caracteres_obligatorios.append(secrets.choice(string.ascii_uppercase))
    if usar_num:
        chars_permitidos += string.digits
        caracteres_obligatorios.append(secrets.choice(string.digits))
    if usar_sym:
        chars_permitidos += string.punctuation
        caracteres_obligatorios.append(secrets.choice(string.punctuation))
    
    if not chars_permitidos:
        return None 
        
    # --- BUCLE DE GENERACIÓN Y FILTRADO ---
    while True:
        if longitud < len(caracteres_obligatorios):
            resultado = caracteres_obligatorios[:longitud]
        else:
            faltantes = longitud - len(caracteres_obligatorios)
            resto_caracteres = [secrets.choice(chars_permitidos) for _ in range(faltantes)]
            resultado = caracteres_obligatorios + resto_caracteres
            
        generador_seguro = secrets.SystemRandom()
        generador_seguro.shuffle(resultado)
        clave_final = ''.join(resultado)
        
        # Filtro Inteligente: Si es solo números y está en nuestra lista negra, RECHÁZALO y vuelve a intentar
        es_solo_numeros = usar_num and not (usar_min or usar_mayus or usar_sym)
        if es_solo_numeros and clave_final in PINS_PROHIBIDOS:
            continue # El 'continue' hace que el bucle 'while' vuelva a empezar mágicamente
            
        return clave_final # Si pasa el filtro (o no es un PIN), lo entregamos

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