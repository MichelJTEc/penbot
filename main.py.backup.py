#!/usr/bin/env python3
"""
Bot de Telegram para Panadería con IA
Punto de entrada principal de la aplicación
"""
import sys
import logging
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters
)

# Importar configuración y handlers
from config.settings import TELEGRAM_BOT_TOKEN, DEBUG_MODE, BAKERY_NAME, EMOJI
from bot.handlers import (
    start_command,
    help_command,
    contact_command,
    menu_command,
    cart_command,
    orders_command,
    ai_mode_command,
    exit_ai_mode,
    admin_command,
    handle_message,
    handle_callback,
    error_handler
)

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if DEBUG_MODE else logging.WARNING
)
logger = logging.getLogger(__name__)


def main():
    """Función principal para iniciar el bot"""
    
    # Validar token
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ ERROR: TELEGRAM_BOT_TOKEN no está configurado")
        logger.error("Por favor configura tu .env con las credenciales necesarias")
        sys.exit(1)
    
    logger.info(f"{EMOJI['bread']} Iniciando bot de {BAKERY_NAME}...")
    
    try:
        # Crear la aplicación
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Registrar comandos
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("ayuda", help_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("contacto", contact_command))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("carrito", cart_command))
        application.add_handler(CommandHandler("cart", cart_command))
        application.add_handler(CommandHandler("pedidos", orders_command))
        application.add_handler(CommandHandler("orders", orders_command))
        application.add_handler(CommandHandler("ia", ai_mode_command))
        application.add_handler(CommandHandler("ai", ai_mode_command))
        application.add_handler(CommandHandler("salir", exit_ai_mode))
        application.add_handler(CommandHandler("exit", exit_ai_mode))
        application.add_handler(CommandHandler("admin", admin_command))
        
        # Registrar handler de callbacks (botones)
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Registrar handler de mensajes de texto
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            handle_message
        ))
        
        # Registrar handler de errores
        application.add_error_handler(error_handler)
        
        # Iniciar el bot
        logger.info(f"{EMOJI['check']} Bot iniciado correctamente!")
        logger.info(f"{EMOJI['robot']} Esperando mensajes...")
        
        # Ejecutar el bot
        application.run_polling(allowed_updates=["message", "callback_query"])
        
    except Exception as e:
        logger.error(f"❌ Error crítico al iniciar el bot: {e}")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info(f"\n{EMOJI['warning']} Bot detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        sys.exit(1)
