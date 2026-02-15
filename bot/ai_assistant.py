"""
Asistente de IA usando Google Gemini para La Viña Dulce
"""
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, BAKERY_NAME, EMOJI, DEBUG_MODE, ADDRESS, PHONE_NUMBER, INSTAGRAM
from bot.menu import PRODUCTS, MASAS, RELLENOS
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO if DEBUG_MODE else logging.WARNING)
logger = logging.getLogger(__name__)

# Configuración global
genai.configure(api_key=GEMINI_API_KEY)

class BakeryAI:
    """Asistente de IA para La Viña Dulce"""
    
    def __init__(self):
        # Modelo actualizado que funciona
        self.model_name = "models/gemini-flash-latest"
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name
        )
        self.chat_sessions = {}
        
    def _get_system_prompt(self):
        """Genera el prompt del sistema con información de La Viña Dulce"""
        
        # Crear lista de productos para el contexto
        products_info = []
        for product in PRODUCTS:
            if product.available:
                products_info.append({
                    "id": product.id,
                    "nombre": product.name,
                    "categoria": product.category,
                    "precio_base": product.price,
                    "porciones": product.portions,
                    "forma": product.shape,
                    "descripcion": product.description,
                })
        
        # Crear info de masas y rellenos
        masas_info = {k: v['nombre'] for k, v in MASAS.items()}
        rellenos_info = {k: v['nombre'] for k, v in RELLENOS.items()}
        
        prompt = f"""Eres un asistente virtual amigable y profesional de {BAKERY_NAME}, una pastelería artesanal especializada en tortas personalizadas ubicada en Loja, Ecuador.

INFORMACIÓN DEL NEGOCIO:
- Nombre: {BAKERY_NAME}
- Ubicación: {ADDRESS}
- Teléfono: {PHONE_NUMBER}
- Instagram: {INSTAGRAM}
- Especialidad: Tortas personalizadas para eventos especiales

NUESTRO CATÁLOGO:
{json.dumps(products_info, indent=2, ensure_ascii=False)}

OPCIONES DE PERSONALIZACIÓN:

Masas disponibles (6 opciones):
{json.dumps(masas_info, indent=2, ensure_ascii=False)}
- Vainilla Especial: La favorita ⭐ (sin costo extra)
- Red Velvet: +$5 USD (la más elegante)
- Dúo Mixto: +$3 USD (vainilla + chocolate)
- Tradicionales: sin costo extra

Rellenos disponibles (8 opciones):
{json.dumps(rellenos_info, indent=2, ensure_ascii=False)}
- Durazno y Gelatina: sin costo extra
- Muss de frutas: +$2 USD
- Crema mosca y Arequipeños: +$3 USD

IMPORTANTE:
- Todos los precios están en dólares americanos (USD)
- Tiempo mínimo de preparación: 48 horas (2 días)
- Cada torta incluye personalización completa de diseño
- Los rellenos vienen en una capa cremosa de maracuyá y crema de leche

TU ROL:
1. Ayuda a los clientes a elegir la torta perfecta según su evento
2. Explica las opciones de personalización de manera clara
3. Calcula precios totales cuando el cliente elija masa y relleno
4. Recomienda productos según número de invitados
5. Sé amigable, profesional y servicial
6. Usa emojis ocasionalmente para hacer la conversación más cálida

EJEMPLO DE CONVERSACIÓN:
Cliente: "Necesito una torta para 15 años"
Tú: "¡Qué emoción! 👑 Tenemos hermosas tortas para quinceañera. ¿Aproximadamente cuántos invitados tendrás? Así te recomiendo el tamaño perfecto."

Cliente: "Como 50 personas"
Tú: "Perfecto, te recomiendo nuestra Torta 15 Años Redonda 2 Pisos para 50 porciones ($55 USD). Es elegante y viene con diseño personalizado con flores, mariposas y los colores que prefieras. ¿Te gustaría saber sobre las masas y rellenos disponibles?"

LIMITACIONES:
- NO procesas pagos (solo tomas pedidos)
- NO puedes cambiar precios del catálogo
- NO inventes productos que no están en la lista
- Si no sabes algo, sé honesto y ofrece contactar a la tienda

Ahora ayuda al cliente de manera natural y profesional."""

        return prompt
    
    def get_or_create_session(self, user_id):
        """Obtiene o crea una sesión de chat para un usuario"""
        if user_id not in self.chat_sessions:
            logger.info(f"Creando nueva sesión para usuario {user_id}")
            self.chat_sessions[user_id] = self.model.start_chat(history=[])
        return self.chat_sessions[user_id]
    
    def reset_session(self, user_id):
        """Reinicia la sesión de un usuario"""
        if user_id in self.chat_sessions:
            logger.info(f"Reiniciando sesión para usuario {user_id}")
            del self.chat_sessions[user_id]
    
    async def process_message(self, user_id, message):
        """Procesa un mensaje del usuario usando IA"""
        try:
            chat = self.get_or_create_session(user_id)
            
            # En el primer mensaje, incluir el system prompt
            if len(chat.history) == 0:
                full_message = f"{self._get_system_prompt()}\n\nCliente: {message}"
            else:
                full_message = message
            
            logger.info(f"Usuario {user_id}: {message}")
            
            # Llamada asíncrona
            response = await chat.send_message_async(full_message)
            
            ai_response = response.text
            logger.info(f"IA responde a {user_id}: {ai_response[:100]}...")
            
            return ai_response
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error en Gemini ({self.model_name}): {error_msg}")
            
            # Manejo de errores específicos
            if "429" in error_msg:
                return "Estoy recibiendo muchas consultas. Intenta en un minuto, por favor. ⏳"
            
            if "404" in error_msg or "not found" in error_msg.lower():
                return "Disculpa, hay un problema con mi configuración. Por favor contacta directamente a la tienda. 🚫"
            
            return f"Disculpa, tuve un problema procesando tu mensaje. ¿Podrías intentar de nuevo? {EMOJI['robot']}"

# Instancia global
bakery_ai = BakeryAI()
