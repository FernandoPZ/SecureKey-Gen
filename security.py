import secrets
import string
import requests
import math

# BASES DE DATOS Y DICCIONARIOS LOCALES
CONTRASENAS_VULNERABLES = {
    "123456", "123456789", "12345678", "12345", "1234567", "111111", "1234", "123123", 
    "qwerty", "qwertyuiop", "asdfgh", "zxcvbnm", "1q2w3e", "000000",
    "password", "password123", "admin", "admin123", "iloveyou", "letmein", "monkey", 
    "dragon", "sunshine", "welcome", "hello", "shadow", "football", "baseball", "ninja",
    "contraseña", "tequiero", "teamo", "madrid", "barcelona", "futbol", "america", 
    "chivas", "cruzazul", "hola", "hola123", "princesa", "estrella", "corazon", 
    "sistemas", "usuario", "invitado", "secreto", "dios",
    "carlos", "daniel", "alejandro", "andrea", "maria", "juan", "david", "jorge", "pedro"
}
PINS_PROHIBIDOS = {
    "0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999", 
    "1234", "2345", "3456", "4567", "5678", "6789", "9876", "8765", "7654", "6543", 
    "5432", "4321", "2580", "0852", "1379", "9731", "1212", "6969"
}
PALABRAS_RESPALDO = [
    "sol", "luna", "nube", "rio", "monte", "verde", "azul", "rojo", "claro", "oscuro",
    "perro", "gato", "lobo", "halcon", "veloz", "fuerte", "libre", "salto", "correr",
    "llave", "puerta", "casa", "camino", "viento", "fuego", "tierra", "mar", "arena"
]

DICCIONARIO_FRASES = set(PALABRAS_RESPALDO)

# FUNCIONES DE DESCARGA EN SEGUNDO PLANO
def actualizar_diccionario_online(callback_progreso=None):
    """Descarga listas y reporta progreso a la UI (Avanza hasta el 60%)."""
    global CONTRASENAS_VULNERABLES
    urls = [
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt",
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/Language-Specific/Spanish_common-usernames-and-passwords.txt"
    ]
    
    for i, url in enumerate(urls):
        try:
            if callback_progreso: callback_progreso((i + 1) * 0.3)
            
            respuesta = requests.get(url, headers={"User-Agent": "KeyForgeApp/1.0"}, timeout=5)
            if respuesta.status_code == 200:
                lineas = respuesta.text.lower().splitlines()
                for linea in lineas:
                    if ":" in linea:
                        CONTRASENAS_VULNERABLES.update([p.strip() for p in linea.split(":") if p.strip()])
                    else:
                        CONTRASENAS_VULNERABLES.add(linea.strip())
        except:
            pass
    return True

def descargar_diccionario_frases(callback_progreso=None):
    """Descarga estándar criptográfico BIP-39 (Avanza hasta el 100%)."""
    global DICCIONARIO_FRASES
    if callback_progreso: callback_progreso(0.8)
    
    url = "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/spanish.txt"
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            DICCIONARIO_FRASES.update(respuesta.text.splitlines())
            if callback_progreso: callback_progreso(1.0)
            return True
    except:
        pass
    
    if callback_progreso: callback_progreso(1.0)
    return False

# LÓGICA DE GENERACIÓN
def generar_clave(longitud, usar_min, usar_mayus, usar_num, usar_sym):
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
    
    if not chars_permitidos: return None 
        
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

        es_solo_numeros = usar_num and not (usar_min or usar_mayus or usar_sym)
        if es_solo_numeros and clave_final in PINS_PROHIBIDOS:
            continue
            
        return clave_final

def generar_hexadecimal(longitud):
    return secrets.token_hex(longitud // 2).upper()

def generar_frase(num_palabras=4):
    lista_palabras = list(DICCIONARIO_FRASES)
    seleccion = [secrets.choice(lista_palabras) for _ in range(num_palabras)]
    return "-".join(seleccion)

# LÓGICA DE AUDITORÍA
def formatear_tiempo(segundos):
    """Convierte segundos en una escala de tiempo comprensible."""
    if segundos < 1: return "Instántaneo [!!!]"
    if segundos < 60: return "Unos Segundos [!!!]"
    if segundos < 3600: return f"{int(segundos // 60)} Minutos [!!]"
    if segundos < 86400: return f"{int(segundos // 3600)} Horas [!]"
    if segundos < 31536000: return f"{int(segundos // 86400)} Días"
    if segundos < 3153600000: return f"{int(segundos // 31536000)} Años"
    return "Siglos [Inquebrantable]"

def auditar_clave(password):
    if not password: 
        return "#444444", "Esperando entrada...", []
    
    if password.lower() in CONTRASENAS_VULNERABLES:
        return "#FF4444", "VULNERABLE", [
            "¡PELIGRO EXTREMO: CLAVE FILTRADA!",
            "Esta contraseña se encuentra en listas",
            "Tiempo de hackeo: 0.00 milisegundos."
        ]
    
    longitud = len(password)
    
    # Comprobación de características
    has_min = any(c in string.ascii_lowercase for c in password)
    has_may = any(c in string.ascii_uppercase for c in password)
    has_num = any(c in string.digits for c in password)
    has_sym = any(c in string.punctuation for c in password)
    
    # Cálculo del tamaño del bloque (R)
    R = 0
    if has_min: R += 26
    if has_may: R += 26
    if has_num: R += 10
    if has_sym: R += 32
    
    # Entropía E = L * log2(R)
    entropia = longitud * math.log2(R) if R > 0 else 0
    
    # Combinaciones totales y Tiempo estimado (10 mil millones de intentos por seg)
    combinaciones = R ** longitud
    segundos_hackeo = combinaciones / 10_000_000_000
    
    tiempo_str = formatear_tiempo(segundos_hackeo)
    
    # Construcción del reporte profesional
    reporte = [
        "───    ANÁLISIS CRIPTOGRÁFICO  ───",
        f"Entropía:    {entropia:.1f} bits",
        f"Descifrado : {tiempo_str}",
        "",
        "───         PARAMETROS         ───",
        f"[{'OK' if longitud >= 8 else 'NO'}] Longitud mínima (8+)",
        f"[{'OK' if has_min else 'NO'}] Minúsculas (a-z)",
        f"[{'OK' if has_may else 'NO'}] Mayúsculas (A-Z)",
        f"[{'OK' if has_num else 'NO'}] Números (0-9)",
        f"[{'OK' if has_sym else 'NO'}] Símbolos especiales"
    ]
    
    # Asignación de colores basada en la Entropía real
    if entropia < 40: return "#FF6B6B", "DÉBIL", reporte
    if entropia < 65: return "#FFD93D", "MEDIA", reporte
    return "#28C76F", "FUERTE", reporte