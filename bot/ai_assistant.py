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

Ahora atiende al cliente con calidez, inteligencia y entusiasmo. ¡Cada torta es una celebración! 🎉

═══════════════════════════════════
⚡ SISTEMA DE ACCIONES (MUY IMPORTANTE)
═══════════════════════════════════

Al final de tu respuesta, incluye UNA etiqueta de acción cuando aplique:

- Si el cliente quiere ver el menú/productos → agrega: [ACCION:ver_menu]
- Si el cliente quiere ver su carrito → agrega: [ACCION:ver_carrito]
- Si el cliente necesita ayuda/contacto → agrega: [ACCION:ver_ayuda]
- Si es conversación normal → NO agregues etiqueta

Ejemplos:
Cliente: "quiero ver el menú"
Tú: "¡Con gusto! Aquí están todas nuestras opciones 🎂 [ACCION:ver_menu]"

Cliente: "qué tengo en mi carrito?"
Tú: "¡Claro! Te muestro lo que tienes 🛒 [ACCION:ver_carrito]"

Cliente: "tienen tortas de chocolate?"
Tú: "¡Sí! Tenemos opciones deliciosas con chocolate... [ACCION:ver_menu]"

Cliente: "hola buenas noches"
Tú: "¡Buenas noches! Bienvenido a La Viña Dulce 🎂 ¿En qué te puedo ayudar?"
(sin etiqueta porque es saludo)

La etiqueta va siempre AL FINAL, pegada al texto, sin espacio extra."""

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
        """
        UNA SOLA LLAMADA a Gemini que responde Y decide la acción.
        La IA incluye etiquetas especiales en su respuesta:
        [ACCION:ver_menu], [ACCION:ver_carrito], [ACCION:ver_ayuda]
        """
        try:
            chat = self.get_or_create_session(user_id)
            
            # En el primer mensaje, incluir el system prompt
            if len(chat.history) == 0:
                full_message = f"{self._get_system_prompt()}\n\nCliente: {message}"
            else:
                full_message = message
            
            logger.info(f"Usuario {user_id}: {message}")
            
            # UNA SOLA llamada asíncrona
            response = await chat.send_message_async(full_message)
            ai_response = response.text
            
            # Limpiar markdown que Gemini pueda agregar por hábito
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
            
            return "Disculpa, tuve un pequeño problema. ¿Podrías intentar de nuevo? 😊"
    
    def extract_action(self, ai_response):
        """
        Extrae la etiqueta de acción del texto de la IA (si existe)
        y devuelve (texto_limpio, accion)
        """
        import re
        
        action = None
        clean_text = ai_response
        
        match = re.search(r'\[ACCION:(\w+)\]', ai_response)
        if match:
            action = match.group(1)
            clean_text = re.sub(r'\[ACCION:\w+\]\s*', '', ai_response).strip()
        
        return clean_text, action

# Instancia global
bakery_ai = BakeryAI()
