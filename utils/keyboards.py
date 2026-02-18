"""
Teclados personalizados para el bot de Telegram
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot.menu import CATEGORIES, get_category_emoji, get_products_by_category
from config.settings import EMOJI


def get_main_menu_keyboard():
    """Teclado del menú principal"""
    keyboard = [
        [KeyboardButton(f"{EMOJI['bread']} Ver Menú"), KeyboardButton(f"{EMOJI['cart']} Mi Carrito")],
        [KeyboardButton(f"{EMOJI['robot']} Hablar con IA"), KeyboardButton(f"📋 Mis Pedidos")],
        [KeyboardButton(f"{EMOJI['info']} Ayuda"), KeyboardButton(f"{EMOJI['phone']} Contacto")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_categories_keyboard():
    """Teclado de categorías de productos"""
    keyboard = []
    
    for category in CATEGORIES.keys():
        emoji = get_category_emoji(category)
        keyboard.append([InlineKeyboardButton(
            f"{emoji} {category}", 
            callback_data=f"cat_{category}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)


def shorten_product_name(name):
    """Acorta el nombre del producto para que quepa en el botón"""
    # Eliminar texto redundante común
    name = name.replace("Torta ", "")
    name = name.replace(" Años", "A")
    name = name.replace("Redonda", "Red")
    name = name.replace("Rectangular", "Rect")
    name = name.replace("Cuadrada", "Cuad")
    name = name.replace(" Pisos", "P")
    name = name.replace(" Piso", "P")
    name = name.replace("porciones", "p")
    name = name.replace("(", "")
    name = name.replace(")", "")
    
    # Si sigue siendo muy largo, acortar más
    if len(name) > 35:
        # Extraer info clave: tipo, forma, porciones
        parts = name.split("-")
        if len(parts) >= 2:
            tipo = parts[0].strip()[:15]  # Primeros 15 caracteres del tipo
            resto = parts[1].strip() if len(parts) > 1 else ""
            name = f"{tipo} {resto}"[:35]
    
    return name.strip()


def get_products_keyboard(category):
    """Teclado de productos de una categoría"""
    keyboard = []
    products = get_products_by_category(category)
    
    for product in products:
        if product.available:
            # Nombre corto + precio
            short_name = shorten_product_name(product.name)
            
            # Mostrar porciones si están disponibles
            portions_text = f" ({product.portions}p)" if product.portions else ""
            
            button_text = f"{short_name}{portions_text}\n${product.price:.2f}"
            
            keyboard.append([InlineKeyboardButton(
                button_text,
                callback_data=f"prod_{product.id}"
            )])
    
    keyboard.append([InlineKeyboardButton("🔙 Categorías", callback_data="categories")])
    
    return InlineKeyboardMarkup(keyboard)


def get_product_detail_keyboard(product_id):
    """Teclado para detalles de un producto"""
    keyboard = [
        [
            InlineKeyboardButton("➖", callback_data=f"qty_{product_id}_-1"),
            InlineKeyboardButton("1", callback_data=f"qty_{product_id}_show"),
            InlineKeyboardButton("➕", callback_data=f"qty_{product_id}_+1"),
        ],
        [InlineKeyboardButton(f"{EMOJI['cart']} Agregar al Carrito", callback_data=f"add_{product_id}_1")],
        [InlineKeyboardButton("🔙 Volver", callback_data="back_to_category")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_cart_keyboard(has_items=True):
    """Teclado para el carrito"""
    keyboard = []
    
    if has_items:
        keyboard.append([InlineKeyboardButton(
            f"{EMOJI['check']} Confirmar Pedido", 
            callback_data="confirm_order"
        )])
        keyboard.append([InlineKeyboardButton(
            "🗑️ Vaciar Carrito", 
            callback_data="clear_cart"
        )])
    
    keyboard.append([InlineKeyboardButton(
        f"{EMOJI['bread']} Seguir Comprando", 
        callback_data="categories"
    )])
    
    return InlineKeyboardMarkup(keyboard)


def get_delivery_type_keyboard():
    """Teclado para seleccionar tipo de entrega"""
    keyboard = [
        [InlineKeyboardButton("🚚 Entrega a domicilio", callback_data="delivery_type_delivery")],
        [InlineKeyboardButton("🏪 Recoger en tienda", callback_data="delivery_type_pickup")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel_order")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_time_slots_keyboard():
    """Teclado para seleccionar hora de entrega/recogida"""
    from datetime import datetime, timedelta
    from config.settings import TIMEZONE, OPENING_HOUR, CLOSING_HOUR, MIN_PREPARATION_TIME
    
    keyboard = []
    now = datetime.now(TIMEZONE)
    
    # Generar slots de tiempo
    current_hour = now.hour + MIN_PREPARATION_TIME
    
    for hour in range(max(current_hour, OPENING_HOUR), CLOSING_HOUR):
        time_slot = f"{hour:02d}:00"
        keyboard.append([InlineKeyboardButton(
            f"🕐 {time_slot}",
            callback_data=f"time_{time_slot}"
        )])
    
    # Si es muy tarde, ofrecer mañana
    if current_hour >= CLOSING_HOUR:
        tomorrow = now + timedelta(days=1)
        keyboard.append([InlineKeyboardButton(
            f"📅 Mañana {tomorrow.strftime('%d/%m')}",
            callback_data="time_tomorrow"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data="back_to_delivery_type")])
    
    return InlineKeyboardMarkup(keyboard)


def get_confirm_order_keyboard():
    """Teclado para confirmar el pedido final"""
    keyboard = [
        [InlineKeyboardButton(f"{EMOJI['check']} Sí, confirmar pedido", callback_data="final_confirm")],
        [InlineKeyboardButton("✏️ Modificar", callback_data="modify_order")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel_order")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_order_status_keyboard(order_id):
    """Teclado para gestión de pedido (solo para admins)"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirmar", callback_data=f"status_{order_id}_confirmed"),
            InlineKeyboardButton("👨‍🍳 En preparación", callback_data=f"status_{order_id}_preparing"),
        ],
        [
            InlineKeyboardButton("📦 Listo", callback_data=f"status_{order_id}_ready"),
            InlineKeyboardButton("🎉 Entregado", callback_data=f"status_{order_id}_delivered"),
        ],
        [
            InlineKeyboardButton("❌ Cancelar", callback_data=f"status_{order_id}_cancelled"),
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_admin_keyboard():
    """Teclado para panel de administrador"""
    keyboard = [
        [InlineKeyboardButton("📋 Pedidos Pendientes", callback_data="admin_pending")],
        [InlineKeyboardButton("📊 Estadísticas", callback_data="admin_stats")],
        [InlineKeyboardButton("🔙 Menú Principal", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_gestion_pedidos_keyboard():
    """Teclado para gestión de pedidos (/pedidos)"""
    keyboard = [
        [InlineKeyboardButton("⏳ Pendientes", callback_data="gestion_pendientes")],
        [InlineKeyboardButton("✅ Despachar", callback_data="gestion_despachar")],
        [InlineKeyboardButton("🎉 Despachados", callback_data="gestion_despachados")],
        [InlineKeyboardButton("📊 Historial", callback_data="gestion_historial")],
        [InlineKeyboardButton("🔙 Cerrar", callback_data="gestion_cerrar")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_pedido_actions_keyboard(order_id):
    """Teclado con acciones para un pedido específico"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Despachar", callback_data=f"action_despachar_{order_id}"),
            InlineKeyboardButton("❌ Cancelar", callback_data=f"action_cancelar_{order_id}")
        ],
        [InlineKeyboardButton("🔙 Volver", callback_data="gestion_pendientes")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_quantity_keyboard(product_id, current_qty=1):
    """Teclado dinámico para ajustar cantidad"""
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=f"setqty_{product_id}_1"),
            InlineKeyboardButton("2", callback_data=f"setqty_{product_id}_2"),
            InlineKeyboardButton("3", callback_data=f"setqty_{product_id}_3"),
        ],
        [
            InlineKeyboardButton("4", callback_data=f"setqty_{product_id}_4"),
            InlineKeyboardButton("5", callback_data=f"setqty_{product_id}_5"),
            InlineKeyboardButton("6", callback_data=f"setqty_{product_id}_6"),
        ],
        [InlineKeyboardButton(
            f"{EMOJI['cart']} Agregar ({current_qty})", 
            callback_data=f"add_{product_id}_{current_qty}"
        )],
        [InlineKeyboardButton("🔙 Volver", callback_data=f"prod_{product_id}")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard():
    """Teclado simple para cancelar"""
    keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data="cancel")]]
    return InlineKeyboardMarkup(keyboard)
