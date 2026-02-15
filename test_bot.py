import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Cargar token manualmente para asegurar que se lee
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

print("--- INICIANDO DIAGNÓSTICO ---")

if not TOKEN:
    print("❌ ERROR CRÍTICO: No se encontró el TELEGRAM_BOT_TOKEN en el archivo .env")
    exit()
else:
    print(f"✅ Token encontrado: {TOKEN[:5]}... (oculto)")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"📩 ¡Mensaje recibido de {update.effective_user.first_name}!")
    await update.message.reply_text("¡Estoy vivo! La conexión funciona. 🤖")

async def main():
    print("🔄 Intentando conectar con los servidores de Telegram...")
    try:
        # Construir la aplicación mínima
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        
        print("✅ Conexión exitosa. El bot está escuchando.")
        print("👉 Ve a Telegram y escribe /start")
        
        # Ejecutar polling
        await app.run_polling()
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido.")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")