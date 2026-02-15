"""
Asistente de IA usando Google Gemini para procesar pedidos y consultas
"""
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, BAKERY_NAME, EMOJI, DEBUG_MODE
from bot.menu import PRODUCTS
import json
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO if DEBUG_MODE else logging.WARNING)
logger = logging.getLogger(__name__)

# Configuración global
genai.configure(api_key=GEMINI_API_KEY)

class BakeryAI:
    """Asistente de IA para la panadería"""
    
    def __init__(self):
        # ESTRATEGIA: Usamos 'models/gemini-flash-latest'
        # Este nombre apareció explícitamente en tu lista de modelos disponibles.
        self.model_name = "models/gemini-flash-latest"
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name
        )
        self.chat_sessions = {}
        
    def _get_system_prompt(self):
        """Genera el prompt del sistema con información de la panadería"""
        products_info = [{"id": p.id, "nombre": p.name, "precio": p.price} for p in PRODUCTS if p.available]
        return f"Eres un asistente de {BAKERY_NAME}. Catálogo: {json.dumps(products_info, ensure_ascii=False)}"
    
    def get_or_create_session(self, user_id):
        if user_id not in self.chat_sessions:
            self.chat_sessions[user_id] = self.model.start_chat(history=[])
        return self.chat_sessions[user_id]
    
    async def process_message(self, user_id, message):
        """Procesa un mensaje del usuario usando IA"""
        try:
            chat = self.get_or_create_session(user_id)
            
            if len(chat.history) == 0:
                prompt = f"{self._get_system_prompt()}\n\nCliente: {message}"
            else:
                prompt = message
            
            # Llamada asíncrona
            response = await chat.send_message_async(prompt)
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error en Gemini ({self.model_name}): {error_msg}")
            
            # Si falla por cuota (429), intentamos un plan B de emergencia
            if "429" in error_msg:
                return "Estoy recibiendo demasiadas consultas. Intenta en un minuto. ⏳"
            
            # Si falla por 404 (No encontrado), es un problema crítico de la cuenta
            if "404" in error_msg:
                return "Error de configuración: El modelo de IA no está disponible en esta cuenta. 🚫"
            
            return f"Disculpa, tuve un problema procesando tu mensaje. 🤖"

# Instancia para importar en handlers.py
bakery_ai = BakeryAI()