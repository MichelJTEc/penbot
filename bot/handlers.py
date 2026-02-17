"""
Manejadores de comandos y callbacks del bot de Telegram
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
import os
from pathlib import Path

from config.settings import EMOJI, MESSAGES, ADMIN_USER_IDS, BAKERY_NAME
from bot.menu import (
    CATEGORIES, get_product_by_id, get_products_by_category, 
    get_category_emoji, search_products
)
from bot.ai_assistant import bakery_ai
from bot.order_manager import order_manager
from utils.keyboards import (
    get_main_menu_keyboard, get_categories_keyboard, 
    get_products_keyboard, get_product_detail_keyboard,
    get_cart_keyboard, get_delivery_type_keyboard,
    get_time_slots_keyboard, get_confirm_order_keyboard,
    get_quantity_keyboard, get_admin_keyboard
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estados de conversación
AWAITING_ADDRESS = 'awaiting_address'
AWAITING_PHONE = 'awaiting_phone'
AWAITING_NOTES = 'awaiting_notes'
AI_MODE = 'ai_mode'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Bienvenida inicial"""
    user = update.effective_user
    
    logger.info(f"Usuario {user.id} ({user.username}) inició el bot")
    
    await update.message.reply_text(
        MESSAGES['welcome'],
        reply_markup=get_main_menu_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ayuda - Muestra ayuda"""
    await update.message.reply_text(
        MESSAGES['help'],
        parse_mode=ParseMode.MARKDOWN
    )


async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /contacto - Información de contacto"""
    await update.message.reply_text(
        MESSAGES['contact'],
        parse_mode=ParseMode.MARKDOWN
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /menu - Muestra el menú de categorías"""
    text = f"{EMOJI['bread']} *Menú de {BAKERY_NAME}*\n\n"
    text += "Selecciona una categoría para ver nuestros productos:"
    
    await update.message.reply_text(
        text,
        reply_markup=get_categories_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


async def cart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /carrito - Muestra el carrito"""
    user_id = update.effective_user.id
    cart_text = order_manager.format_cart(user_id)
    summary = order_manager.get_cart_summary(user_id)
    
    has_items = summary and summary['item_count'] > 0
    
    await update.message.reply_text(
        cart_text,
        reply_markup=get_cart_keyboard(has_items),
        parse_mode=ParseMode.MARKDOWN
    )


async def orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /pedidos - Muestra historial de pedidos"""
    user_id = update.effective_user.id
    orders = order_manager.get_user_orders(user_id, limit=5)
    
    if not orders:
        text = f"{EMOJI['info']} No tienes pedidos anteriores.\n\n"
        text += f"¡Haz tu primer pedido! {EMOJI['bread']}"
        await update.message.reply_text(text)
        return
    
    text = f"📋 *Tus últimos pedidos:*\n\n"
    
    for order in orders:
        text += f"▫️ Pedido #{order['id']} - ${order['total']:.2f}\n"
        text += f"  Estado: {order['status']}\n"
        text += f"  Fecha: {order['created_at']}\n\n"
    
    text += "Usa /pedido [número] para ver detalles"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def ai_mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Activa el modo de conversación con IA"""
    context.user_data['mode'] = AI_MODE
    
    text = f"{EMOJI['robot']} *Modo IA Activado*\n\n"
    text += "Ahora puedes hablar conmigo de forma natural. Por ejemplo:\n"
    text += "• \"Quiero algo dulce\"\n"
    text += "• \"¿Tienen pan sin gluten?\"\n"
    text += "• \"Recomiéndame algo para el desayuno\"\n\n"
    text += "Escribe /salir para volver al menú normal."
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def exit_ai_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sale del modo IA"""
    if context.user_data.get('mode') == AI_MODE:
        context.user_data['mode'] = None
        await update.message.reply_text(
            f"{EMOJI['check']} Modo IA desactivado. Volviendo al menú normal.",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await update.message.reply_text("No estabas en modo IA.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes de texto del usuario - AGENTE IA CONVERSACIONAL"""
    text = update.message.text
    user_id = update.effective_user.id
    
    # === PRIORIDAD 1: Estados especiales (no interrumpir flujos) ===
    
    # Si está esperando dirección
    if context.user_data.get('state') == AWAITING_ADDRESS:
        context.user_data['delivery_address'] = text
        context.user_data['state'] = AWAITING_PHONE
        await update.message.reply_text(
            f"📍 Dirección guardada.\n\n📞 Ahora, ¿cuál es tu número de teléfono?"
        )
        return
    
    # Si está esperando teléfono
    if context.user_data.get('state') == AWAITING_PHONE:
        context.user_data['delivery_phone'] = text
        context.user_data['state'] = AWAITING_NOTES
        await update.message.reply_text(
            f"📞 Teléfono guardado.\n\n"
            f"¿Tienes alguna nota o instrucción especial para tu pedido?\n"
            f"(Escribe 'ninguna' si no)"
        )
        return
    
    # Si está esperando notas
    if context.user_data.get('state') == AWAITING_NOTES:
        notes = text if text.lower() != 'ninguna' else ''
        context.user_data['delivery_notes'] = notes
        context.user_data['state'] = None
        
        # Mostrar resumen y confirmar
        await show_order_summary(update, context)
        return
    
    # === PRIORIDAD 2: Botones del menú principal ===
    
    if f"{EMOJI['bread']} Ver Menú" in text:
        await menu_command(update, context)
        return
    
    if f"{EMOJI['cart']} Mi Carrito" in text:
        await cart_command(update, context)
        return
    
    if "📋 Mis Pedidos" in text:
        await orders_command(update, context)
        return
    
    if f"{EMOJI['info']} Ayuda" in text:
        await help_command(update, context)
        return
    
    if f"{EMOJI['phone']} Contacto" in text:
        await contact_command(update, context)
        return
    
    # === PRIORIDAD 3: AGENTE IA - Analizar intención ===
    
    try:
        # Mostrar indicador de escritura
        await update.message.chat.send_action("typing")
        
        # Detectar intención con IA
        intention_data = await bakery_ai.detect_intention(text)
        intention = intention_data.get('intention', 'chat')
        search_term = intention_data.get('search_term')
        
        logger.info(f"Usuario {user_id}: '{text}' → Intención: {intention}")
        
        # Ejecutar acción según intención
        
        if intention == 'view_menu':
            # Usuario quiere ver el menú
            await update.message.reply_text("¡Claro! Te muestro nuestro menú 🎂")
            await menu_command(update, context)
        
        elif intention == 'view_cart':
            # Usuario quiere ver su carrito
            await cart_command(update, context)
        
        elif intention == 'search_product':
            # Usuario busca un producto - responder con IA + mostrar botones
            
            # Primero responder conversacionalmente con IA
            response = await bakery_ai.process_message(user_id, text)
            await update.message.reply_text(response, parse_mode=ParseMode.HTML)
            
            # Luego mostrar categorías para que navegue
            await update.message.reply_text(
                "👇 Explora nuestros productos:",
                reply_markup=get_categories_keyboard()
            )
        
        elif intention == 'ask_price':
            # Pregunta por precio
            cart = context.user_data.get('cart', {})
            
            if cart:
                # Tiene carrito, mostrar total
                await cart_command(update, context)
            else:
                # No tiene carrito, responder con IA
                response = await bakery_ai.process_message(user_id, text)
                await update.message.reply_text(response, parse_mode=ParseMode.HTML)
        
        elif intention == 'help':
            # Necesita ayuda
            await help_command(update, context)
        
        elif intention == 'order':
            # Quiere hacer un pedido
            cart = context.user_data.get('cart', {})
            
            if cart:
                # Tiene items, mostrar carrito para confirmar
                await update.message.reply_text("¡Perfecto! Aquí está tu carrito 🛒")
                await cart_command(update, context)
            else:
                # No tiene items
                await update.message.reply_text(
                    "¡Genial! ¿Qué te gustaría ordenar? 😊\n\n"
                    "Puedes decirme qué buscas o ver el menú completo.",
                    reply_markup=get_categories_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
        
        else:  # intention == 'chat'
            # Conversación general
            response = await bakery_ai.process_message(user_id, text)
            await update.message.reply_text(response, parse_mode=ParseMode.HTML)
    
    except Exception as e:
        logger.error(f"Error en agente IA: {e}")
        # Fallback: responder con IA directamente
        try:
            response = await bakery_ai.process_message(user_id, text)
            await update.message.reply_text(response, parse_mode=ParseMode.HTML)
        except:
            await update.message.reply_text(
                "Disculpa, tuve un problema procesando tu mensaje. "
                "¿Podrías intentar de nuevo o usar los botones del menú?"
            )


async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa mensajes en modo IA"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Mostrar que está escribiendo
    await update.message.chat.send_action("typing")
    
    # Procesar con IA
    response = await bakery_ai.process_message(user_id, user_message)
    
    await update.message.reply_text(response, parse_mode=ParseMode.HTML)


async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str):
    """Maneja búsquedas de productos"""
    results = search_products(query)
    
    if not results:
        text = f"No encontré productos para '{query}' {EMOJI['warning']}\n\n"
        text += "¿Quieres que te ayude a buscar? Habla conmigo en modo IA:"
        await update.message.reply_text(text)
        await ai_mode_command(update, context)
        return
    
    text = f"🔍 Resultados para '{query}':\n\n"
    
    for product in results[:5]:  # Máximo 5 resultados
        text += f"• {product.name} - ${product.price:.2f}\n"
        text += f"  {product.description}\n\n"
    
    text += "Usa /menu para ver el catálogo completo"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja callbacks de botones inline"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    # Categorías
    if data.startswith('cat_'):
        category = data.replace('cat_', '')
        emoji = get_category_emoji(category)
        
        text = f"{emoji} *{category}*\n\n"
        text += "Selecciona un producto para ver detalles:"
        
        await query.edit_message_text(
            text,
            reply_markup=get_products_keyboard(category),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Ver producto
    elif data.startswith('prod_'):
        product_id = int(data.replace('prod_', ''))
        product = get_product_by_id(product_id)
        
        if product:
            context.user_data['current_category'] = product.category
            
            # Eliminar mensaje del menú
            try:
                await query.delete_message()
            except:
                pass
            
            # Verificar si tiene imagen
            has_image = False
            image_path = None
            
            if product.image_path:
                # Intentar encontrar la imagen
                path = Path(product.image_path)
                
                # Si es ruta absoluta, usarla directamente
                if path.exists() and path.is_file():
                    image_path = path
                    has_image = True
                # Si es ruta relativa, buscar desde la raíz del proyecto
                elif Path(product.image_path).exists():
                    image_path = Path(product.image_path)
                    has_image = True
            
            # 1. Enviar imagen primero (si existe)
            if has_image:
                try:
                    with open(image_path, 'rb') as photo:
                        await query.message.reply_photo(
                            photo=photo,
                            caption=f"📸 *{product.name}*",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    logger.info(f"✅ Imagen enviada: {image_path}")
                except Exception as e:
                    logger.error(f"❌ Error enviando imagen {image_path}: {e}")
            
            # 2. Luego enviar descripción con botones (siempre)
            await query.message.reply_text(
                product.get_detail(),
                reply_markup=get_product_detail_keyboard(product_id),
                parse_mode=ParseMode.MARKDOWN
            )
    
    # Agregar al carrito
    elif data.startswith('add_'):
        parts = data.replace('add_', '').split('_')
        product_id = int(parts[0])
        quantity = int(parts[1]) if len(parts) > 1 else 1
        
        success, message = order_manager.add_to_cart(user_id, product_id, quantity)
        
        # Mostrar notificación Y mensaje de confirmación
        await query.answer(message, show_alert=True)
        
        # Enviar mensaje de confirmación adicional
        if success:
            product = get_product_by_id(product_id)
            confirmation = f"✅ *Agregado al carrito*\n\n"
            confirmation += f"{quantity}x {product.name}\n"
            confirmation += f"Total: ${product.price * quantity:.2f} USD\n\n"
            confirmation += f"Usa /carrito para ver tu pedido completo."
            
            await query.message.reply_text(
                confirmation,
                parse_mode=ParseMode.MARKDOWN
            )
    
    # Incrementar/Decrementar cantidad (botones ➖ y ➕)
    elif data.startswith('qty_'):
        parts = data.replace('qty_', '').split('_')
        product_id = int(parts[0])
        action = parts[1] if len(parts) > 1 else 'show'
        
        # Obtener cantidad actual
        current_qty = context.user_data.get('current_quantity', {}).get(product_id, 1)
        
        # Ajustar cantidad según la acción
        if action == '+1':
            current_qty = min(current_qty + 1, 99)  # Máximo 99
        elif action == '-1':
            current_qty = max(current_qty - 1, 1)   # Mínimo 1
        
        # Guardar nueva cantidad
        if 'current_quantity' not in context.user_data:
            context.user_data['current_quantity'] = {}
        context.user_data['current_quantity'][product_id] = current_qty
        
        # Actualizar el texto del botón del medio y el botón de agregar
        product = get_product_by_id(product_id)
        
        # Crear teclado actualizado
        keyboard = [
            [
                InlineKeyboardButton("➖", callback_data=f"qty_{product_id}_-1"),
                InlineKeyboardButton(str(current_qty), callback_data=f"qty_{product_id}_show"),
                InlineKeyboardButton("➕", callback_data=f"qty_{product_id}_+1"),
            ],
            [InlineKeyboardButton(f"{EMOJI['cart']} Agregar {current_qty} al Carrito", callback_data=f"add_{product_id}_{current_qty}")],
            [InlineKeyboardButton("🔙 Volver", callback_data="back_to_category")]
        ]
        
        # Intentar editar el mensaje
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await query.answer(f"Cantidad: {current_qty}")
        except:
            # Si no se puede editar, solo mostrar notificación
            await query.answer(f"Cantidad: {current_qty}")
    
    # Ajustar cantidad
    elif data.startswith('setqty_'):
        parts = data.replace('setqty_', '').split('_')
        product_id = int(parts[0])
        quantity = int(parts[1])
        
        context.user_data['temp_quantity'] = quantity
        
        # Solo mostrar notificación
        await query.answer(f"Cantidad: {quantity}", show_alert=False)
    
    # Volver a categorías
    elif data == 'categories':
        text = f"{EMOJI['bread']} *Menú de {BAKERY_NAME}*\n\n"
        text += "Selecciona una categoría:"
        
        await query.edit_message_text(
            text,
            reply_markup=get_categories_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Volver a categoría anterior
    elif data == 'back_to_category':
        category = context.user_data.get('current_category')
        if category:
            emoji = get_category_emoji(category)
            text = f"{emoji} *{category}*\n\nSelecciona un producto:"
            
            try:
                # Intentar editar (funciona si el mensaje es editable)
                await query.edit_message_text(
                    text,
                    reply_markup=get_products_keyboard(category),
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                # Si no se puede editar, enviar nuevo mensaje
                await query.message.reply_text(
                    text,
                    reply_markup=get_products_keyboard(category),
                    parse_mode=ParseMode.MARKDOWN
                )
    
    # Ver carrito
    elif data == 'view_cart':
        cart_text = order_manager.format_cart(user_id)
        summary = order_manager.get_cart_summary(user_id)
        has_items = summary and summary['item_count'] > 0
        
        await query.edit_message_text(
            cart_text,
            reply_markup=get_cart_keyboard(has_items),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Vaciar carrito
    elif data == 'clear_cart':
        order_manager.clear_cart(user_id)
        await query.answer("Carrito vaciado", show_alert=True)
        
        cart_text = order_manager.format_cart(user_id)
        await query.edit_message_text(
            cart_text,
            reply_markup=get_cart_keyboard(False),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Confirmar pedido
    elif data == 'confirm_order':
        text = f"{EMOJI['info']} ¿Cómo prefieres recibir tu pedido?"
        
        await query.edit_message_text(
            text,
            reply_markup=get_delivery_type_keyboard()
        )
    
    # Tipo de entrega
    elif data.startswith('delivery_type_'):
        delivery_type = data.replace('delivery_type_', '')
        context.user_data['delivery_type'] = delivery_type
        
        if delivery_type == 'delivery':
            context.user_data['state'] = AWAITING_ADDRESS
            await query.edit_message_text(
                f"🚚 Entrega a domicilio seleccionada.\n\n"
                f"Por favor, escribe tu dirección completa:"
            )
        else:
            context.user_data['delivery_address'] = 'Recoger en tienda'
            context.user_data['state'] = AWAITING_PHONE
            await query.edit_message_text(
                f"🏪 Recogida en tienda.\n\n"
                f"📞 Por favor, escribe tu número de teléfono:"
            )
    
    # Confirmar pedido final
    elif data == 'final_confirm':
        await create_final_order(update, context)
    
    # Cancelar pedido
    elif data == 'cancel_order':
        context.user_data.clear()
        await query.edit_message_text(
            f"❌ Pedido cancelado.\n\nTu carrito sigue guardado. {EMOJI['cart']}"
        )


async def show_order_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el resumen del pedido antes de confirmar"""
    user_id = update.effective_user.id
    summary = order_manager.get_cart_summary(user_id)
    
    if not summary:
        await update.message.reply_text("Error: carrito vacío")
        return
    
    text = f"📋 *RESUMEN DE TU PEDIDO*\n\n"
    
    # Productos
    for item in summary['items']:
        text += f"• {item['quantity']}x {item['name']} - ${item['subtotal']:.2f}\n"
    
    text += f"\n*Total: ${summary['total']:.2f} MXN*\n\n"
    
    # Información de entrega
    delivery_type = context.user_data.get('delivery_type')
    if delivery_type == 'delivery':
        text += f"🚚 Entrega a domicilio\n"
        text += f"📍 {context.user_data.get('delivery_address')}\n"
    else:
        text += f"🏪 Recoger en tienda\n"
    
    text += f"📞 {context.user_data.get('delivery_phone')}\n"
    
    notes = context.user_data.get('delivery_notes')
    if notes:
        text += f"\n📝 Notas: {notes}\n"
    
    text += f"\n¿Todo correcto?"
    
    await update.message.reply_text(
        text,
        reply_markup=get_confirm_order_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


async def create_final_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crea el pedido final en la base de datos"""
    query = update.callback_query
    user = update.effective_user
    user_id = user.id
    
    delivery_info = {
        'type': context.user_data.get('delivery_type'),
        'address': context.user_data.get('delivery_address'),
        'phone': context.user_data.get('delivery_phone'),
        'notes': context.user_data.get('delivery_notes', ''),
        'time': context.user_data.get('delivery_time', 'Lo antes posible')
    }
    
    order_id, error = order_manager.create_order(user_id, user.username or user.first_name, delivery_info)
    
    if error:
        await query.edit_message_text(f"❌ Error creando pedido: {error}")
        return
    
    # Limpiar datos temporales
    context.user_data.clear()
    
    # Mensaje de confirmación
    text = f"{EMOJI['check']} *¡PEDIDO CONFIRMADO!*\n\n"
    text += f"Número de pedido: *#{order_id}*\n\n"
    text += f"Te notificaremos cuando esté listo. {EMOJI['robot']}\n"
    text += f"¡Gracias por tu preferencia!"
    
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    
    # Notificar a administradores
    await notify_admins(context, order_id)


async def notify_admins(context: ContextTypes.DEFAULT_TYPE, order_id: int):
    """Notifica a los administradores sobre un nuevo pedido"""
    order = order_manager.get_order(order_id)
    
    if not order or not ADMIN_USER_IDS:
        return
    
    text = f"🔔 *NUEVO PEDIDO*\n\n"
    text += order_manager.format_order(order)
    
    for admin_id in ADMIN_USER_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=text,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error notificando admin {admin_id}: {e}")


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Panel de administración (solo para admins)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_USER_IDS:
        await update.message.reply_text("❌ No tienes permisos de administrador")
        return
    
    text = f"👨‍💼 *Panel de Administración*\n\n"
    text += "Selecciona una opción:"
    
    await update.message.reply_text(
        text,
        reply_markup=get_admin_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja errores del bot"""
    logger.error(f"Error: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"😔 Disculpa, ocurrió un error. Por favor intenta de nuevo."
        )
