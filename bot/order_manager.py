"""
Gestor de pedidos y base de datos
"""
import sqlite3
import json
from datetime import datetime
from config.settings import DATABASE_URL, TIMEZONE, EMOJI
from bot.menu import get_product_by_id
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderManager:
    """Gestor de pedidos y carrito de compras"""
    
    def __init__(self):
        self.db_path = DATABASE_URL.replace('sqlite:///', '')
        self.init_database()
        self.carts = {}  # Carritos temporales en memoria
    
    def init_database(self):
        """Inicializa la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de pedidos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    items TEXT NOT NULL,
                    total REAL NOT NULL,
                    status TEXT DEFAULT 'pending',
                    delivery_type TEXT,
                    delivery_address TEXT,
                    delivery_time TEXT,
                    phone TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    default_address TEXT,
                    total_orders INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_order_at TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Base de datos inicializada correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando base de datos: {e}")
    
    def get_or_create_cart(self, user_id):
        """Obtiene o crea un carrito para el usuario"""
        if user_id not in self.carts:
            self.carts[user_id] = {}
        return self.carts[user_id]
    
    def add_to_cart(self, user_id, product_id, quantity=1):
        """Agrega un producto al carrito"""
        cart = self.get_or_create_cart(user_id)
        product = get_product_by_id(product_id)
        
        if not product:
            return False, "Producto no encontrado"
        
        if not product.available:
            return False, f"Lo sentimos, {product.name} no está disponible en este momento"
        
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'product': product,
                'quantity': quantity
            }
        
        return True, f"✅ Agregado {quantity}x {product.name} al carrito"
    
    def remove_from_cart(self, user_id, product_id):
        """Elimina un producto del carrito"""
        cart = self.get_or_create_cart(user_id)
        
        if product_id in cart:
            product_name = cart[product_id]['product'].name
            del cart[product_id]
            return True, f"❌ {product_name} eliminado del carrito"
        
        return False, "Producto no encontrado en el carrito"
    
    def update_quantity(self, user_id, product_id, quantity):
        """Actualiza la cantidad de un producto en el carrito"""
        cart = self.get_or_create_cart(user_id)
        
        if product_id not in cart:
            return False, "Producto no encontrado en el carrito"
        
        if quantity <= 0:
            return self.remove_from_cart(user_id, product_id)
        
        cart[product_id]['quantity'] = quantity
        product_name = cart[product_id]['product'].name
        return True, f"✅ Cantidad actualizada: {quantity}x {product_name}"
    
    def clear_cart(self, user_id):
        """Vacía el carrito del usuario"""
        if user_id in self.carts:
            self.carts[user_id] = {}
        return True, "🛒 Carrito vaciado"
    
    def get_cart_summary(self, user_id):
        """Obtiene el resumen del carrito"""
        cart = self.get_or_create_cart(user_id)
        
        if not cart:
            return None
        
        items = []
        total = 0
        
        for product_id, item in cart.items():
            product = item['product']
            quantity = item['quantity']
            subtotal = product.price * quantity
            total += subtotal
            
            items.append({
                'id': product_id,
                'name': product.name,
                'quantity': quantity,
                'price': product.price,
                'subtotal': subtotal
            })
        
        return {
            'items': items,
            'total': total,
            'item_count': len(items)
        }
    
    def format_cart(self, user_id):
        """Formatea el carrito para mostrar al usuario"""
        summary = self.get_cart_summary(user_id)
        
        if not summary or summary['item_count'] == 0:
            return f"{EMOJI['cart']} Tu carrito está vacío\n\n¡Explora nuestro menú con /menu!"
        
        text = f"{EMOJI['cart']} *TU CARRITO*\n\n"
        
        for item in summary['items']:
            text += f"• {item['quantity']}x {item['name']}\n"
            text += f"  ${item['price']:.2f} c/u = ${item['subtotal']:.2f}\n\n"
        
        text += f"{'─' * 30}\n"
        text += f"*TOTAL: ${summary['total']:.2f} USD*\n\n"
        text += "¿Listo para ordenar? Presiona 'Confirmar Pedido'"
        
        return text
    
    def create_order(self, user_id, username, delivery_info):
        """Crea un pedido a partir del carrito"""
        try:
            cart = self.get_or_create_cart(user_id)
            
            if not cart:
                return None, "El carrito está vacío"
            
            # Calcular total y preparar items
            items = []
            total = 0
            
            for product_id, item in cart.items():
                product = item['product']
                quantity = item['quantity']
                subtotal = product.price * quantity
                total += subtotal
                
                items.append({
                    'product_id': product_id,
                    'name': product.name,
                    'quantity': quantity,
                    'price': product.price,
                    'subtotal': subtotal
                })
            
            # Guardar en base de datos
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO orders (
                    user_id, username, items, total, delivery_type, 
                    delivery_address, delivery_time, phone, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                username,
                json.dumps(items),
                total,
                delivery_info.get('type', 'pickup'),
                delivery_info.get('address', ''),
                delivery_info.get('time', ''),
                delivery_info.get('phone', ''),
                delivery_info.get('notes', '')
            ))
            
            order_id = cursor.lastrowid
            
            # Actualizar contador de usuario
            cursor.execute('''
                INSERT INTO users (user_id, username, total_orders, last_order_at)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    total_orders = total_orders + 1,
                    last_order_at = ?
            ''', (user_id, username, datetime.now(TIMEZONE), datetime.now(TIMEZONE)))
            
            conn.commit()
            conn.close()
            
            # Limpiar carrito
            self.clear_cart(user_id)
            
            return order_id, None
            
        except Exception as e:
            logger.error(f"Error creando pedido: {e}")
            return None, f"Error al crear el pedido: {str(e)}"
    
    def get_order(self, order_id):
        """Obtiene un pedido por ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo pedido: {e}")
            return None
    
    def get_user_orders(self, user_id, limit=5):
        """Obtiene los últimos pedidos de un usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM orders 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error obteniendo pedidos del usuario: {e}")
            return []
    
    def update_order_status(self, order_id, status):
        """Actualiza el estado de un pedido"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE orders 
                SET status = ?, updated_at = ? 
                WHERE id = ?
            ''', (status, datetime.now(TIMEZONE), order_id))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando estado del pedido: {e}")
            return False
    
    def format_order(self, order):
        """Formatea un pedido para mostrar"""
        if not order:
            return "Pedido no encontrado"
        
        status_emoji = {
            'pending': '🕐',
            'confirmed': '✅',
            'preparing': '👨‍🍳',
            'ready': '📦',
            'delivered': '🎉',
            'cancelled': '❌'
        }
        
        status_text = {
            'pending': 'Pendiente',
            'confirmed': 'Confirmado',
            'preparing': 'En preparación',
            'ready': 'Listo para entregar',
            'delivered': 'Entregado',
            'cancelled': 'Cancelado'
        }
        
        items = json.loads(order['items'])
        
        text = f"📋 *PEDIDO #{order['id']}*\n\n"
        text += f"Estado: {status_emoji.get(order['status'], '❓')} {status_text.get(order['status'], 'Desconocido')}\n"
        text += f"Fecha: {order['created_at']}\n\n"
        
        text += "*Productos:*\n"
        for item in items:
            text += f"• {item['quantity']}x {item['name']} - ${item['subtotal']:.2f}\n"
        
        text += f"\n*Total: ${order['total']:.2f} USD*\n\n"
        
        if order['delivery_type'] == 'delivery':
            text += f"🚚 Entrega a domicilio\n"
            text += f"📍 {order['delivery_address']}\n"
        else:
            text += f"🏪 Recoger en tienda\n"
        
        if order['delivery_time']:
            text += f"🕐 Hora: {order['delivery_time']}\n"
        
        if order['phone']:
            text += f"📞 Teléfono: {order['phone']}\n"
        
        if order['notes']:
            text += f"\n📝 Notas: {order['notes']}\n"
        
        return text


# Instancia global del gestor
order_manager = OrderManager()
