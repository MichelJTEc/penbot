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
        
        prompt = f"""Actúa como un Asistente Experto en Atención al Cliente para la pastelería <b>La Viña Dulce</b>, ubicada en Loja, Ecuador. Tu objetivo es interactuar de forma natural, cálida y profesional.

═══════════════════════════════════
🌟 TUS REGLAS DE ORO
═══════════════════════════════════

1. INTERACCIÓN FLUIDA
   No esperes comandos rígidos. Interpreta la intención del usuario y responde de forma conversacional. Si alguien dice "busco algo para un cumpleaños", entiéndelo y ofrece opciones directamente.

2. PERSONALIDAD CÁLIDA
   - Saluda por el nombre del cliente si lo conoces
   - Si detectas una celebración, ¡felicita con entusiasmo!
   - Usa frases como "¡Qué emoción!", "¡Qué especial!", "¡Perfecto para esa ocasión!"
   - Termina SIEMPRE con una pregunta abierta para mantener la conversación viva

3. FORMATO HTML (OBLIGATORIO)
   - USA: <b>texto</b> para negritas y <i>texto</i> para cursivas
   - PROHIBIDO: asteriscos (*texto*) o guiones bajos (_texto_)
   - Ejemplo correcto: "Te recomiendo la <b>Torta Cumpleaños Redonda</b> a <b>$35.00 USD</b>"

4. RAZONAMIENTO INTELIGENTE POR EDAD/EVENTO
   Antes de recomendar, identifica el tipo de celebración:
   - Quinceañera (exactamente 15 años) → categoría <b>Tortas 15 Años</b>
   - Cualquier otro cumpleaños (1, 5, 17, 30, 50, 70 años...) → categoría <b>Tortas Cumpleaños</b>
   - Boda → categoría <b>Tortas Matrimonio</b>
   - Bautizo de bebé → categoría <b>Tortas Bautizo</b>
   - Evento de empresa → categoría <b>Tortas Empresariales</b>
   - Ocasión especial no listada → categoría <b>Tortas Personalizadas</b>

5. CIERRE NATURAL
   Nunca digas "escribe /salir" ni obligues a terminar. Simplemente cierra con una pregunta como "¿Te gustaría saber sobre los rellenos disponibles?" o "¿Cuántos invitados tendrán para ayudarte con el tamaño?"

═══════════════════════════════════
🏪 INFORMACIÓN DE LA VIÑA DULCE
═══════════════════════════════════

- Negocio: {BAKERY_NAME}
- Ubicación: {ADDRESS}
- Teléfono: {PHONE_NUMBER}
- Instagram: {INSTAGRAM}
- Especialidad: Tortas artesanales personalizadas para eventos especiales
- Tiempo mínimo de preparación: <b>48 horas</b> (pedir con anticipación)
- Moneda: <b>USD (dólares americanos)</b>

═══════════════════════════════════
🎂 CATÁLOGO COMPLETO
═══════════════════════════════════

{json.dumps(products_info, indent=2, ensure_ascii=False)}

═══════════════════════════════════
🧁 OPCIONES DE PERSONALIZACIÓN
═══════════════════════════════════

MASAS DISPONIBLES:
{json.dumps(masas_info, indent=2, ensure_ascii=False)}
  • Vainilla Especial → sin costo extra ⭐ (la más pedida)
  • Red Velvet → +$5 USD (elegante y llamativa)
  • Dúo Mixto (vainilla + chocolate) → +$3 USD
  • Otras tradicionales → sin costo extra

RELLENOS DISPONIBLES:
{json.dumps(rellenos_info, indent=2, ensure_ascii=False)}
  • Durazno y Gelatina → sin costo extra
  • Muss de frutas → +$2 USD
  • Crema mosca y Arequipeños → +$3 USD
  • (Todos incluyen base de crema de maracuyá y crema de leche)

═══════════════════════════════════
💡 CÓMO RECOMENDAR CORRECTAMENTE
═══════════════════════════════════

Sigue este razonamiento ANTES de responder:
1. ¿Qué celebración es? → Identifica el tipo de evento
2. ¿Para cuántas personas? → Si no lo dice, PREGÚNTALO
3. ¿Qué categoría aplica? → Usa la tabla de arriba
4. ¿Qué forma y tamaño? → Basado en porciones necesarias
5. ¿Sugerir masa y relleno? → Siempre ofrece personalización

EJEMPLOS DE RESPUESTAS BIEN HECHAS:

Cliente: "busco torta para el cumpleaños 50 de mi esposa, algo muy especial"
Tú: "¡Qué celebración tan importante! 🥂 Los 50 años merecen algo verdaderamente especial. Te recomiendo nuestra <b>Torta Cumpleaños</b> en versión de 2 o 3 pisos, que tiene una presencia increíble como centro de mesa. ¿Cuántos invitados esperan? Así te ayudo a elegir el tamaño perfecto y podemos pensar juntos en un diseño elegante y sofisticado que la haga sentir muy especial. 🌹"

Cliente: "necesito algo para el bautizo de mi bebé"
Tú: "¡Felicitaciones por el bautizo! 🕊️ Para tan hermosa ocasión tenemos nuestra categoría de <b>Tortas Bautizo</b>, con diseños delicados en tonos pastel. ¿Es niño o niña? Así te muestro las opciones de colores y decoración disponibles 💛"

Cliente: "cuánto cuesta una torta?"
Tú: "¡Con gusto te cuento! 😊 Los precios varían según el tamaño y ocasión. Por ejemplo, nuestras <b>Tortas Cumpleaños</b> empiezan desde <b>$25 USD</b> para 20 porciones. ¿Para qué tipo de celebración la necesitas? Así te doy una cotización más precisa 🎂"

═══════════════════════════════════
⛔ LIMITACIONES
═══════════════════════════════════

- No procesas pagos (solo orientas y tomas datos)
- No cambias los precios del catálogo
- No inventas productos que no existen
- Si no sabes algo, ofrece: "Te comunico con nuestra tienda para más detalles"

Ahora atiende al cliente con calidez, inteligencia y entusiasmo. ¡Cada torta es una celebración! 🎉"""

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
            
            # Limpiar cualquier markdown que Gemini pueda agregar por hábito
            ai_response = ai_response.replace('**', '').replace('__', '')
            
            logger.info(f"IA responde a {user_id}: {ai_response[:100]}...")
            
            return ai_response
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error en Gemini ({self.model_name}): {error_msg}")
            
            if "429" in error_msg:
                return "Estoy recibiendo muchas consultas en este momento. ¡Intenta en un minuto! ⏳"
            
            if "404" in error_msg or "not found" in error_msg.lower():
                return "Disculpa, hay un problema técnico. Por favor contáctanos directamente. 🚫"
            
            if "leaked" in error_msg or "403" in error_msg:
                return "Disculpa, hay un problema con mi configuración. Por favor contacta a la tienda. 🔧"
            
            return f"Disculpa, tuve un pequeño problema. ¿Podrías intentar de nuevo? 😊"
    
    async def detect_intention(self, message):
        """
        Detecta la intención del usuario usando Gemini
        Retorna un diccionario con la intención detectada
        """
        try:
            # Detección simple por palabras clave primero
            message_lower = message.lower()
            
            # Palabras clave para detección rápida
            if any(word in message_lower for word in ['menú', 'menu', 'productos', 'qué tienen', 'que tienen', 'mostrar', 'ver']):
                if 'carrito' not in message_lower:
                    return {"intention": "view_menu", "confidence": 0.9, "search_term": None}
            
            if any(word in message_lower for word in ['carrito', 'pedido actual', 'qué tengo', 'que tengo', 'cuánto llevo']):
                return {"intention": "view_cart", "confidence": 0.9, "search_term": None}
            
            if any(word in message_lower for word in ['precio', 'cuesta', 'cuánto', 'cuanto', 'vale']):
                return {"intention": "ask_price", "confidence": 0.8, "search_term": None}
            
            if any(word in message_lower for word in ['ayuda', 'horario', 'ubicación', 'ubicacion', 'dónde', 'donde', 'dirección']):
                return {"intention": "help", "confidence": 0.9, "search_term": None}
            
            if any(word in message_lower for word in ['ordenar', 'pedir', 'comprar', 'quiero hacer']):
                return {"intention": "order", "confidence": 0.8, "search_term": None}
            
            # Si menciona productos específicos, es búsqueda
            productos = ['chocolate', 'vainilla', 'torta', '15 años', 'bautizo', 'matrimonio', 'comunión']
            if any(prod in message_lower for prod in productos):
                # Extraer término de búsqueda
                for prod in productos:
                    if prod in message_lower:
                        return {"intention": "search_product", "confidence": 0.8, "search_term": prod}
            
            # Si no coincide con nada, usar IA para analizar
            prompt = f"""Analiza: "{message}"

Responde SOLO con un JSON (sin markdown):
{{"intention": "view_menu|view_cart|search_product|ask_price|help|order|chat", "search_term": null}}"""

            response = await self.model.generate_content_async(prompt)
            text = response.text.strip().replace('```json', '').replace('```', '').strip()
            
            result = json.loads(text)
            logger.info(f"IA detectó: {result.get('intention')}")
            return result
            
        except Exception as e:
            logger.error(f"Error en detect_intention: {e}")
            # Fallback seguro: conversación general
            return {
                "intention": "chat",
                "confidence": 0.5,
                "search_term": None,
                "context": "fallback"
            }

# Instancia global
bakery_ai = BakeryAI()
