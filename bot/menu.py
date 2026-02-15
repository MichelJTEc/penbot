"""
Catálogo de productos de La Viña Dulce - Pastelería
"""
from config.settings import EMOJI
import os

# Opciones de personalización
MASAS = {
    'vainilla_especial': {
        'nombre': 'Vainilla Especial ⭐',
        'descripcion': 'Bizcocho suave con doble capa de relleno (La Favorita)',
        'precio_extra': 0
    },
    'duo_mixto': {
        'nombre': 'Dúo Mixto',
        'descripcion': 'Vainilla clásica y chocolate intenso combinados',
        'precio_extra': 3
    },
    'red_velvet': {
        'nombre': 'Red Velvet',
        'descripcion': 'Textura aterciopelada, ideal para eventos elegantes',
        'precio_extra': 5
    },
    'tradicional_vainilla': {
        'nombre': 'Tradicional Vainilla',
        'descripcion': 'Esponjosa, no necesita hidratarse',
        'precio_extra': 0
    },
    'tradicional_chocolate': {
        'nombre': 'Tradicional Chocolate',
        'descripcion': 'Chocolate intenso y esponjoso',
        'precio_extra': 0
    },
    'tradicional_naranja': {
        'nombre': 'Tradicional Naranja',
        'descripcion': 'Con suave aroma cítrico',
        'precio_extra': 0
    }
}

RELLENOS = {
    'durazno': {'nombre': 'Durazno', 'precio_extra': 0},
    'gelatina': {'nombre': 'Gelatina', 'precio_extra': 0},
    'muss_mora': {'nombre': 'Muss de Mora', 'precio_extra': 2},
    'muss_fresa': {'nombre': 'Muss de Fresa', 'precio_extra': 2},
    'muss_pina': {'nombre': 'Muss de Piña', 'precio_extra': 2},
    'crema_mosca': {'nombre': 'Crema Mosca', 'precio_extra': 3},
    'arequipeños': {'nombre': 'Arequipeños', 'precio_extra': 3},
    'frutos_secos': {'nombre': 'Frutos Secos', 'precio_extra': 3}
}


class Product:
    """Clase para representar un producto de pastelería"""
    def __init__(self, id, name, price, category, description, 
                 portions=None, shape=None, image_path=None,
                 masas_disponibles=None, rellenos_disponibles=None,
                 preparation_time=48, codigo=None, available=True,
                 ingredients=None, allergens=None):
        self.id = id
        self.name = name
        self.price = price  # Precio base en USD
        self.category = category
        self.description = description
        self.portions = portions  # "40" o "40-50"
        self.shape = shape  # "Redonda", "Rectangular", "Cuadrada"
        self.image_path = image_path  # Ruta relativa a la imagen
        self.masas_disponibles = masas_disponibles or list(MASAS.keys())
        self.rellenos_disponibles = rellenos_disponibles or list(RELLENOS.keys())
        self.preparation_time = preparation_time  # en horas
        self.codigo = codigo  # VDM12, VDM125, etc.
        self.available = available
        self.ingredients = ingredients or []
        self.allergens = allergens or []
    
    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"
    
    def get_detail(self):
        """Retorna descripción detallada del producto"""
        detail = f"*{self.name}*\n"
        detail += f"{self.description}\n\n"
        
        if self.portions:
            detail += f"👥 Porciones: {self.portions} personas\n"
        
        if self.shape:
            detail += f"📐 Forma: {self.shape}\n"
        
        detail += f"{EMOJI['money']} Precio base: ${self.price:.2f} USD\n"
        detail += f"{EMOJI['clock']} Preparación: {self.preparation_time} horas\n"
        
        if self.codigo:
            detail += f"🔖 Código: {self.codigo}\n"
        
        detail += f"\n✨ *Personalización incluida:*\n"
        detail += f"• Selección de masa (6 opciones)\n"
        detail += f"• Selección de relleno (8 opciones)\n"
        detail += f"• Diseño personalizado según tu evento\n"
        detail += f"• Texto y colores a tu gusto\n"
        
        if self.ingredients:
            detail += f"\n📋 Base: {', '.join(self.ingredients[:3])}\n"
        
        status = f"{EMOJI['check']} Disponible" if self.available else f"{EMOJI['cross']} No disponible"
        detail += f"\n{status}"
        
        return detail
    
    def has_image(self):
        """Verifica si el producto tiene imagen"""
        if not self.image_path:
            return False
        return os.path.exists(self.image_path)
    
    def calculate_price(self, masa_key=None, relleno_key=None):
        """Calcula el precio total con personalizaciones"""
        total = self.price
        
        if masa_key and masa_key in MASAS:
            total += MASAS[masa_key]['precio_extra']
        
        if relleno_key and relleno_key in RELLENOS:
            total += RELLENOS[relleno_key]['precio_extra']
        
        return total


# Catálogo de productos de La Viña Dulce
PRODUCTS = [
    # ==================== TORTAS 15 AÑOS ====================
    Product(
        id=1,
        name="Torta 15 Años - Redonda 2 Pisos (40 porciones)",
        price=42,
        category="Tortas 15 Años",
        description="Elegante torta de 2 pisos perfecta para quinceañera. Diseño personalizado con corona, flores y detalles elegantes según tus colores favoritos.",
        portions="40",
        shape="Redonda",
        image_path="static/images/productos/producto_1_60946627.png",
        codigo="VDM168",
        preparation_time=48,
        ingredients=['Bizcocho', 'Relleno cremoso', 'Decoración personalizada']
    ),
    
    Product(
        id=2,
        name="Torta 15 Años - Redonda 2 Pisos (50 porciones)",
        price=55.0,
        category="Tortas 15 Años",
        description="Torta de 2 pisos para celebraciones grandes. Decoración elegante con mariposas, flores naturales o diseño moderno.",
        portions="50",
        shape="Redonda",
        codigo="VDM3012",
        preparation_time=48,
        ingredients=['Bizcocho premium', 'Relleno gourmet', 'Flores comestibles']
    ),
    
    Product(
        id=3,
        name="Torta 15 Años - Redonda 3 Pisos (70 porciones)",
        price=65.0,
        category="Tortas 15 Años",
        description="Impresionante torta de 3 pisos, ideal para eventos grandes. Centro de atención garantizado con diseño espectacular.",
        portions="70",
        shape="Redonda",
        codigo="VDM30126",
        preparation_time=72,
        ingredients=['Bizcocho especial', 'Triple relleno', 'Decoración premium']
    ),
    
    Product(
        id=4,
        name="Torta 15 Años - Cuadrada (30 porciones)",
        price=32.0,
        category="Tortas 15 Años",
        description="Torta cuadrada moderna con diseños contemporáneos.",
        portions="30",
        shape="Cuadrada",
        codigo="VDM16C",
        preparation_time=48
    ),
    
    Product(
        id=5,
        name="Torta 15 Años - Rectangular (50 porciones)",
        price=50.0,
        category="Tortas 15 Años",
        description="Torta rectangular ideal para mesas amplias. Diseño elegante y sofisticado.",
        portions="50",
        shape="Rectangular",
        codigo="VDM40R",
        preparation_time=48
    ),
    
    # ==================== TORTAS MATRIMONIO ====================
    Product(
        id=10,
        name="Torta Matrimonio - Redonda 2 Pisos (40 porciones)",
        price=42.0,
        category="Tortas Matrimonio",
        description="Elegante torta para bodas con decoración clásica. Personalización según los colores de tu boda, flores naturales y detalles románticos.",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=72,
        ingredients=['Bizcocho nupcial', 'Relleno delicado', 'Flores frescas']
    ),
    
    Product(
        id=11,
        name="Torta Matrimonio - Redonda 2 Pisos (50 porciones)",
        price=55.0,
        category="Tortas Matrimonio",
        description="Torta de bodas de 2 pisos con diseño sofisticado. Ideal para recepciones elegantes.",
        portions="50",
        shape="Redonda",
        codigo="VDM3012",
        preparation_time=72
    ),
    
    Product(
        id=12,
        name="Torta Matrimonio - Redonda 3 Pisos (65 porciones)",
        price=65.0,
        category="Tortas Matrimonio",
        description="Espectacular torta de 3 pisos para bodas elegantes. Diseño de ensueño para tu día especial.",
        portions="65",
        shape="Redonda",
        codigo="VDM30126",
        preparation_time=72
    ),
    
    Product(
        id=13,
        name="Torta Matrimonio - Rectangular (50 porciones)",
        price=50.0,
        category="Tortas Matrimonio",
        description="Torta rectangular para bodas con estilo moderno.",
        portions="50",
        shape="Rectangular",
        codigo="VDM40R",
        preparation_time=72
    ),
    
    # ==================== TORTAS BAUTIZO ====================
    Product(
        id=20,
        name="Torta Bautizo - Rectangular (40 porciones)",
        price=42.0,
        category="Tortas Bautizo",
        description="Torta dulce para celebrar el bautizo. Diseños personalizados en azul o rosa con símbolos religiosos, angelitos y cruces.",
        portions="40",
        shape="Rectangular",
        codigo="VDM30R",
        preparation_time=48,
        ingredients=['Bizcocho suave', 'Relleno cremoso', 'Decoración religiosa']
    ),
    
    Product(
        id=21,
        name="Torta Bautizo - Redonda 2 Pisos (40 porciones)",
        price=42.0,
        category="Tortas Bautizo",
        description="Tierna torta de 2 pisos para bautizo con decoración religiosa y detalles celestiales.",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=48
    ),
    
    Product(
        id=22,
        name="Torta Bautizo - Redonda 3 Pisos (65 porciones)",
        price=65.0,
        category="Tortas Bautizo",
        description="Torta de 3 pisos para bautizos grandes con decoración angelical.",
        portions="65",
        shape="Redonda",
        codigo="VDM30126",
        preparation_time=48
    ),
    
    # ==================== PRIMERA COMUNIÓN ====================
    Product(
        id=30,
        name="Torta Primera Comunión - Rectangular (40 porciones)",
        price=42.0,
        category="Primera Comunión",
        description="Torta para primera comunión con cáliz, hostia, rosarios y decoración religiosa personalizada.",
        portions="40",
        shape="Rectangular",
        codigo="VDM30R",
        preparation_time=48
    ),
    
    Product(
        id=31,
        name="Torta Primera Comunión - Redonda 2 Pisos (40 porciones)",
        price=42.0,
        category="Primera Comunión",
        description="Elegante torta de 2 pisos para este sacramento especial.",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=48
    ),
    
    # ==================== CUMPLEAÑOS CABALLEROS ====================
    Product(
        id=40,
        name="Torta Caballeros - Rectangular (50 porciones)",
        price=50.0,
        category="Cumpleaños Caballeros",
        description="Diseños personalizados para hombres: deportes (fútbol, básquet), hobbies, profesiones, música, autos, tecnología, etc. ¡Dinos su pasión y lo hacemos realidad!",
        portions="50",
        shape="Rectangular",
        codigo="VDM40R",
        preparation_time=48,
        ingredients=['Bizcocho premium', 'Relleno masculino', 'Decoración temática']
    ),
    
    Product(
        id=41,
        name="Torta Caballeros - Redonda 2 Pisos (40 porciones)",
        price=42.0,
        category="Cumpleaños Caballeros",
        description="Torta elegante con temas masculinos: whisky, puros, deportes, profesión.",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=48
    ),
    
    Product(
        id=42,
        name="Torta Caballeros - Cuadrada (30 porciones)",
        price=32.0,
        category="Cumpleaños Caballeros",
        description="Torta cuadrada moderna con diseños para hombres.",
        portions="30",
        shape="Cuadrada",
        codigo="VDM16C",
        preparation_time=48
    ),
    
    # ==================== CUMPLEAÑOS SEÑORAS ====================
    Product(
        id=50,
        name="Torta Señoras - Redonda 2 Pisos (40 porciones)",
        price=42.0,
        category="Cumpleaños Señoras",
        description="Tortas elegantes y sofisticadas para damas. Diseños florales, elegantes, vintage o temáticos según sus gustos (costura, cocina, viajes, jardinería, etc.)",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=48,
        ingredients=['Bizcocho fino', 'Relleno gourmet', 'Flores comestibles']
    ),
    
    Product(
        id=51,
        name="Torta Señoras - Rectangular (50 porciones)",
        price=50.0,
        category="Cumpleaños Señoras",
        description="Torta rectangular con diseños personalizados según gustos e intereses.",
        portions="50",
        shape="Rectangular",
        codigo="VDM40R",
        preparation_time=48
    ),
    
    Product(
        id=52,
        name="Torta Señoras - Redonda 3 Pisos (65 porciones)",
        price=65.0,
        category="Cumpleaños Señoras",
        description="Impresionante torta de 3 pisos para celebraciones especiales.",
        portions="65",
        shape="Redonda",
        codigo="VDM30126",
        preparation_time=48
    ),
    
    # ==================== CUMPLEAÑOS SEÑORITAS/PRINCESAS ====================
    Product(
        id=60,
        name="Torta Señoritas/Princesas - Redonda (40 porciones)",
        price=42.0,
        category="Cumpleaños Señoritas/Princesas",
        description="Tortas con diseños de princesa, elegantes y dulces. Coronas, brillos, mariposas y detalles finos. Perfectas para jóvenes que quieren sentirse especiales.",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=48,
        ingredients=['Bizcocho esponjoso', 'Relleno cremoso', 'Decoración brillante']
    ),
    
    Product(
        id=61,
        name="Torta Señoritas/Princesas - Rectangular (50 porciones)",
        price=50.0,
        category="Cumpleaños Señoritas/Princesas",
        description="Diseños modernos y elegantes para jóvenes: unicornios, estrellas, brillo.",
        portions="50",
        shape="Rectangular",
        codigo="VDM40R",
        preparation_time=48
    ),
    
    Product(
        id=62,
        name="Torta Señoritas/Princesas - Redonda 3 Pisos (65 porciones)",
        price=65.0,
        category="Cumpleaños Señoritas/Princesas",
        description="Torta de ensueño de 3 pisos digna de una princesa.",
        portions="65",
        shape="Redonda",
        codigo="VDM30126",
        preparation_time=48
    ),
    
    # ==================== GRADUACIÓN ====================
    Product(
        id=70,
        name="Torta Graduación - Redonda 2 Pisos (40 porciones)",
        price=42.0,
        category="Graduación",
        description="Celebra el logro académico con una torta personalizada. Incluye birrete, diploma, borla y colores de tu institución educativa.",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=48,
        ingredients=['Bizcocho del éxito', 'Relleno triunfal', 'Decoración académica']
    ),
    
    Product(
        id=71,
        name="Torta Graduación - Rectangular (50 porciones)",
        price=50.0,
        category="Graduación",
        description="Torta rectangular perfecta para fiestas de graduación con logos universitarios.",
        portions="50",
        shape="Rectangular",
        codigo="VDM40R",
        preparation_time=48
    ),
    
    Product(
        id=72,
        name="Torta Graduación - Redonda (20-30 porciones)",
        price=30.0,
        category="Graduación",
        description="Torta individual perfecta para graduaciones pequeñas o familiares.",
        portions="20-30",
        shape="Redonda",
        codigo="VDM20",
        preparation_time=48
    ),
    
    # ==================== BABY SHOWER ====================
    Product(
        id=80,
        name="Torta Baby Shower - Rectangular (40 porciones)",
        price=42.0,
        category="Baby Shower",
        description="Dulces diseños para celebrar la llegada del bebé. Disponible en azul, rosa o neutro con ositos, chupetes, biberones y más.",
        portions="40",
        shape="Rectangular",
        codigo="VDM30R",
        preparation_time=48,
        ingredients=['Bizcocho tierno', 'Relleno suave', 'Decoración infantil']
    ),
    
    Product(
        id=81,
        name="Torta Revelación de Género - Rectangular (50 porciones)",
        price=50.0,
        category="Baby Shower",
        description="¡Torta sorpresa! Exterior neutro con relleno de color (azul o rosa) para revelar el sexo del bebé. ¡El momento más emocionante!",
        portions="50",
        shape="Rectangular",
        codigo="VDM40R",
        preparation_time=48
    ),
    
    Product(
        id=82,
        name="Torta Baby Shower - Redonda 2 Pisos (50 porciones)",
        price=55.0,
        category="Baby Shower",
        description="Elegante torta de 2 pisos para baby showers grandes.",
        portions="50",
        shape="Redonda",
        codigo="VDM3012",
        preparation_time=48
    ),
    
    # ==================== NIÑAS Y PERSONAJES ====================
    Product(
        id=90,
        name="Torta Personajes - Redonda (20-30 porciones)",
        price=30.0,
        category="Niñas y Personajes",
        description="Tortas temáticas de personajes infantiles: Frozen, Princesas Disney, Stitch, Paw Patrol, Encanto, Miraculous y más. ¡Dinos el personaje favorito!",
        portions="20-30",
        shape="Redonda",
        codigo="VDM20",
        preparation_time=48,
        ingredients=['Bizcocho colorido', 'Relleno divertido', 'Decoración temática']
    ),
    
    Product(
        id=91,
        name="Torta Niñas Personajes - Rectangular (40 porciones)",
        price=42.0,
        category="Niñas y Personajes",
        description="Torta rectangular con diseños de personajes para fiestas grandes.",
        portions="40",
        shape="Rectangular",
        codigo="VDM30R",
        preparation_time=48
    ),
    
    Product(
        id=92,
        name="Torta Niñas Personajes - Redonda 2 Pisos (40 porciones)",
        price=42.0,
        category="Niñas y Personajes",
        description="Torta de 2 pisos con el personaje favorito de tu pequeña.",
        portions="40",
        shape="Redonda",
        codigo="VDM168",
        preparation_time=48
    ),
    
]

# Organizar productos por categoría
CATEGORIES = {}
for product in PRODUCTS:
    if product.category not in CATEGORIES:
        CATEGORIES[product.category] = []
    CATEGORIES[product.category].append(product)

# Diccionario para búsqueda rápida por ID
PRODUCTS_BY_ID = {p.id: p for p in PRODUCTS}


def get_product_by_id(product_id):
    """Obtiene un producto por su ID"""
    return PRODUCTS_BY_ID.get(product_id)


def search_products(query):
    """Busca productos por nombre o descripción"""
    query = query.lower()
    results = []
    for product in PRODUCTS:
        if (query in product.name.lower() or 
            query in product.description.lower() or
            query in product.category.lower()):
            results.append(product)
    return results


def get_products_by_category(category):
    """Obtiene productos de una categoría específica"""
    return CATEGORIES.get(category, [])


def get_available_products():
    """Retorna solo productos disponibles"""
    return [p for p in PRODUCTS if p.available]


def get_category_emoji(category):
    """Retorna el emoji apropiado para cada categoría"""
    emoji_map = {
        "Tortas 15 Años": "👑",
        "Tortas Matrimonio": "💍",
        "Tortas Bautizo": "👼",
        "Primera Comunión": "⛪",
        "Cumpleaños Señoras": "🌸",
        "Cumpleaños Señoritas/Princesas": "👸",
        "Cumpleaños Caballeros": "🎩",
        "Graduación": "🎓",
        "Niñas y Personajes": "🎀",
        "Baby Shower": "🍼",
    }
    return emoji_map.get(category, EMOJI['cake'])
