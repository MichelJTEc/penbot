"""
Configuración centralizada del bot de La Viña Dulce
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

# Configuración de La Viña Dulce
BAKERY_NAME = os.getenv('BAKERY_NAME', 'La Viña Dulce')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '+593 9 9563-9050')
EMAIL = os.getenv('EMAIL', 'lavinadulce16@gmail.com')
ADDRESS = os.getenv('ADDRESS', 'Loja, 18 de Noviembre 211-11 y Mercadillo')
INSTAGRAM = os.getenv('INSTAGRAM', '@lavinadulce')
TIKTOK = os.getenv('TIKTOK', '@lavinadulce')

# Moneda
CURRENCY = os.getenv('CURRENCY', 'USD')
CURRENCY_SYMBOL = os.getenv('CURRENCY_SYMBOL', '$')

# Horarios
TIMEZONE = pytz.timezone(os.getenv('TIMEZONE', 'America/Guayaquil'))
OPENING_HOUR = int(os.getenv('OPENING_HOUR', '9'))
CLOSING_HOUR = int(os.getenv('CLOSING_HOUR', '18'))
MIN_PREPARATION_TIME = int(os.getenv('MIN_PREPARATION_TIME', '48'))

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
👑 ¡Bienvenido a {BAKERY_NAME}!

Soy tu asistente virtual con inteligencia artificial. 

🎂 *Somos especialistas en:*
• Tortas personalizadas para 15 años
• Tortas de matrimonio elegantes
• Tortas de bautizo y primera comunión
• Cumpleaños (niños, jóvenes y adultos)
• Graduaciones
• Baby shower y revelación de género

✨ *Personalizamos cada torta según tu evento:*
✅ 6 tipos de masas (incluyendo Red Velvet)
✅ 8 opciones de rellenos gourmet
✅ Diseños únicos y creativos
✅ Colores y decoración a tu gusto

📍 {ADDRESS}
📞 {PHONE_NUMBER}

¿En qué puedo ayudarte hoy?
    """,
    
    'help': f"""
{EMOJI['info']} *Comandos disponibles:*

/start - Iniciar conversación
/menu - Ver todas nuestras tortas
/carrito - Ver tu carrito actual
/pedidos - Ver tus pedidos anteriores
/ayuda - Mostrar esta ayuda
/contacto - Información de contacto
/cancelar - Cancelar operación actual

💬 *También puedes escribirme naturalmente:*
• "Quiero una torta de 15 años"
• "¿Tienen tortas de graduación?"
• "Necesito una torta para 50 personas"
• "Quiero ver diseños de matrimonio"

⏰ *Importante:*
Necesitamos mínimo {MIN_PREPARATION_TIME} horas de anticipación para preparar tu torta perfecta.
    """,
    
    'contact': f"""
{EMOJI['phone']} *Información de Contacto*

🏪 *{BAKERY_NAME}*
📱 Teléfono: {PHONE_NUMBER}
📧 Email: {EMAIL}
{EMOJI['location']} Dirección: {ADDRESS}

📱 *Redes Sociales:*
Instagram: {INSTAGRAM}
TikTok: {TIKTOK}

{EMOJI['clock']} *Horarios de Atención:*
Lunes a Domingo: {OPENING_HOUR}:00 - {CLOSING_HOUR}:00

💡 *Tips:*
• Pedidos con {MIN_PREPARATION_TIME}h de anticipación mínimo
• Envíanos fotos de referencia por WhatsApp
• Consulta por nuestros diseños en redes sociales
    """,
}
