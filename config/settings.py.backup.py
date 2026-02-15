"""
Configuración centralizada del bot de panadería
"""
import os
from dotenv import load_dotenv
import pytz

# Cargar variables de entorno
load_dotenv()

# Configuración del Bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Validar que existan las credenciales
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no está configurado en .env")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY no está configurado en .env")

# Base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bakery.db')

# Administradores
ADMIN_USER_IDS = [
    int(uid.strip()) 
    for uid in os.getenv('ADMIN_USER_IDS', '').split(',') 
    if uid.strip()
]

# Configuración de la panadería
BAKERY_NAME = os.getenv('BAKERY_NAME', 'Panadería Artesanal')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '+52 55 1234 5678')
EMAIL = os.getenv('EMAIL', 'contacto@panaderia.com')
ADDRESS = os.getenv('ADDRESS', 'Calle Principal #123, Colonia Centro')

# Horarios
TIMEZONE = pytz.timezone(os.getenv('TIMEZONE', 'America/Mexico_City'))
OPENING_HOUR = int(os.getenv('OPENING_HOUR', '7'))
CLOSING_HOUR = int(os.getenv('CLOSING_HOUR', '20'))
MIN_PREPARATION_TIME = int(os.getenv('MIN_PREPARATION_TIME', '2'))

# Modo debug
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

# Emojis para el bot
EMOJI = {
    'bread': '🥖',
    'cake': '🍰',
    'croissant': '🥐',
    'cookie': '🍪',
    'cart': '🛒',
    'check': '✅',
    'cross': '❌',
    'clock': '🕐',
    'location': '📍',
    'phone': '📞',
    'money': '💰',
    'robot': '🤖',
    'star': '⭐',
    'info': 'ℹ️',
    'warning': '⚠️',
}

# Mensajes del sistema
MESSAGES = {
    'welcome': f"""
{EMOJI['bread']} ¡Bienvenido a {BAKERY_NAME}!

Soy tu asistente virtual con inteligencia artificial. Puedo ayudarte a:

{EMOJI['check']} Ver nuestro menú completo
{EMOJI['check']} Hacer pedidos de forma fácil y rápida
{EMOJI['check']} Recomendar productos según tus preferencias
{EMOJI['check']} Responder tus preguntas sobre ingredientes y alérgenos

¿En qué puedo ayudarte hoy?
    """,
    
    'help': f"""
{EMOJI['info']} *Comandos disponibles:*

/start - Iniciar conversación
/menu - Ver el menú completo
/carrito - Ver tu carrito actual
/pedidos - Ver tus pedidos anteriores
/ayuda - Mostrar esta ayuda
/contacto - Información de contacto
/cancelar - Cancelar operación actual

También puedes escribirme naturalmente:
• "Quiero un pan integral"
• "¿Tienen pasteles sin azúcar?"
• "Recomiéndame algo para el desayuno"
    """,
    
    'contact': f"""
{EMOJI['phone']} *Información de Contacto*

📱 Teléfono: {PHONE_NUMBER}
📧 Email: {EMAIL}
{EMOJI['location']} Dirección: {ADDRESS}

{EMOJI['clock']} *Horarios de Atención:*
Lunes a Domingo: {OPENING_HOUR}:00 - {CLOSING_HOUR}:00
    """,
}
