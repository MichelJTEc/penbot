"""
Servidor web para administrar productos de La Viña Dulce
CON SOPORTE REAL DE IMÁGENES - Guarda archivos en disco
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from pathlib import Path
import re
import base64
import uuid

app = Flask(__name__)

# Rutas
MENU_FILE = Path(__file__).parent / 'bot' / 'menu.py'
UPLOAD_FOLDER = Path(__file__).parent / 'static' / 'images' / 'productos'

# Crear carpetas si no existen
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

print(f"📂 Carpeta de imágenes: {UPLOAD_FOLDER}")
print(f"📂 Archivo menu.py: {MENU_FILE}")

def save_image_file(base64_data, product_id):
    """
    Guarda imagen base64 como archivo real y retorna la ruta
    """
    if not base64_data or base64_data == 'None':
        return None
    
    # Si ya es una ruta de archivo, devolverla
    if not base64_data.startswith('data:image'):
        return base64_data
    
    try:
        # Extraer el formato y los datos
        header, encoded = base64_data.split(',', 1)
        
        # Detectar extensión
        if 'jpeg' in header or 'jpg' in header:
            ext = 'jpg'
        elif 'png' in header:
            ext = 'png'
        elif 'webp' in header:
            ext = 'webp'
        else:
            ext = 'jpg'
        
        # Nombre único para el archivo
        filename = f"producto_{product_id}_{uuid.uuid4().hex[:8]}.{ext}"
        filepath = UPLOAD_FOLDER / filename
        
        # Decodificar y guardar
        image_data = base64.b64decode(encoded)
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        # Retornar ruta relativa
        relative_path = f"static/images/productos/{filename}"
        print(f"✅ Imagen guardada: {relative_path}")
        return relative_path
    
    except Exception as e:
        print(f"❌ Error guardando imagen: {e}")
        return None

def read_products():
    """Lee los productos del archivo menu.py"""
    if not MENU_FILE.exists():
        print(f"❌ ERROR: No se encuentra {MENU_FILE}")
        return []
    
    products = []
    
    try:
        with open(MENU_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar la sección PRODUCTS = [...]
        match = re.search(r'PRODUCTS\s*=\s*\[(.*?)\n\]', content, re.DOTALL)
        if not match:
            print("❌ No se encontró la sección PRODUCTS")
            return []
        
        products_section = match.group(1)
        
        # Parsear cada producto
        product_blocks = re.findall(r'Product\((.*?)\n    \),?', products_section, re.DOTALL)
        
        print(f"✅ Encontrados {len(product_blocks)} productos")
        
        for block in product_blocks:
            product = {}
            
            # Parsear cada campo
            for line in block.split('\n'):
                line = line.strip()
                if '=' not in line or line.startswith('#'):
                    continue
                    
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().rstrip(',')
                
                # Limpiar valores
                if value.startswith('"') or value.startswith("'"):
                    value = value[1:-1]
                elif value.startswith('['):
                    try:
                        value = eval(value)
                    except:
                        value = []
                elif value in ['True', 'False']:
                    value = value == 'True'
                elif value == 'None':
                    value = None
                else:
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except:
                        pass
                
                product[key] = value
            
            if product and 'id' in product:
                products.append(product)
        
        print(f"✅ Cargados {len(products)} productos correctamente")
        return products
    
    except Exception as e:
        print(f"❌ Error leyendo productos: {e}")
        import traceback
        traceback.print_exc()
        return []

def write_products(products):
    """Escribe los productos al archivo menu.py"""
    try:
        with open(MENU_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Encontrar donde comienza PRODUCTS
        start_marker = "PRODUCTS = ["
        end_marker = "# Organizar productos por categoría"
        
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            print("❌ No se encontró la sección de productos")
            return False
        
        # Generar nuevo código de productos
        products_code = "PRODUCTS = [\n"
        
        # Agrupar por categoría
        categories = {}
        for product in products:
            cat = product.get('category', 'Sin Categoría')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(product)
        
        # Escribir productos por categoría
        for category, cat_products in categories.items():
            products_code += f"    # ==================== {category.upper()} ====================\n"
            
            for product in cat_products:
                products_code += "    Product(\n"
                products_code += f"        id={product['id']},\n"
                products_code += f"        name=\"{product['name']}\",\n"
                products_code += f"        price={product['price']},\n"
                products_code += f"        category=\"{product['category']}\",\n"
                products_code += f"        description=\"{product['description']}\",\n"
                
                # Campos opcionales específicos de pastelería
                if product.get('portions'):
                    products_code += f"        portions=\"{product['portions']}\",\n"
                
                if product.get('shape'):
                    products_code += f"        shape=\"{product['shape']}\",\n"
                
                # IMPORTANTE: Solo guardar ruta, NO base64
                if product.get('image_path'):
                    # Asegurar que sea una ruta, no base64
                    image_path = product['image_path']
                    if not image_path.startswith('data:'):
                        products_code += f"        image_path=\"{image_path}\",\n"
                
                if product.get('codigo'):
                    products_code += f"        codigo=\"{product['codigo']}\",\n"
                
                # Tiempo de preparación
                prep_time = product.get('preparation_time', 48)
                products_code += f"        preparation_time={prep_time}"
                
                # Ingredientes
                if product.get('ingredients'):
                    products_code += f",\n        ingredients={product['ingredients']}"
                
                # Alérgenos
                if product.get('allergens'):
                    products_code += f",\n        allergens={product['allergens']}"
                
                # Disponibilidad
                if 'available' in product and not product['available']:
                    products_code += ",\n        available=False"
                
                products_code += "\n    ),\n    \n"
        
        products_code += "]\n\n"
        
        # Reemplazar la sección
        new_content = content[:start_idx] + products_code + content[end_idx:]
        
        # Escribir archivo
        with open(MENU_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Guardados {len(products)} productos en {MENU_FILE}")
        return True
    
    except Exception as e:
        print(f"❌ Error escribiendo productos: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/')
def index():
    """Página principal"""
    return render_template('admin.html')

@app.route('/static/images/productos/<filename>')
def serve_image(filename):
    """Servir imágenes de productos"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/products', methods=['GET'])
def get_products():
    """API para obtener productos"""
    try:
        products = read_products()
        return jsonify({'success': True, 'products': products})
    except Exception as e:
        print(f"❌ Error en GET /api/products: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    """API para agregar producto"""
    try:
        data = request.json
        print(f"📝 Agregando producto: {data.get('name')}")
        
        if not data:
            return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
        
        products = read_products()
        
        # Generar nuevo ID
        max_id = max([p['id'] for p in products]) if products else 0
        data['id'] = max_id + 1
        
        # Guardar imagen si viene en base64
        if data.get('image_path'):
            saved_path = save_image_file(data['image_path'], data['id'])
            data['image_path'] = saved_path
        
        # Asegurar campos por defecto
        data.setdefault('portions', '')
        data.setdefault('shape', '')
        data.setdefault('codigo', '')
        data.setdefault('preparation_time', 48)
        data.setdefault('available', True)
        data.setdefault('ingredients', [])
        data.setdefault('allergens', [])
        
        products.append(data)
        
        if write_products(products):
            print(f"✅ Producto agregado: {data['name']}")
            return jsonify({'success': True, 'product': data})
        else:
            return jsonify({'success': False, 'error': 'Error al guardar'}), 500
    
    except Exception as e:
        print(f"❌ Error en POST /api/products: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """API para actualizar producto"""
    try:
        data = request.json
        print(f"✏️ Actualizando producto ID {product_id}: {data.get('name')}")
        
        if not data:
            return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
        
        products = read_products()
        
        # Guardar imagen si viene en base64
        if data.get('image_path'):
            saved_path = save_image_file(data['image_path'], product_id)
            if saved_path:
                data['image_path'] = saved_path
        
        # Encontrar y actualizar producto
        found = False
        for i, p in enumerate(products):
            if p['id'] == product_id:
                data['id'] = product_id
                
                # Asegurar campos
                data.setdefault('portions', '')
                data.setdefault('shape', '')
                data.setdefault('codigo', '')
                data.setdefault('preparation_time', 48)
                data.setdefault('available', True)
                data.setdefault('ingredients', [])
                data.setdefault('allergens', [])
                
                products[i] = data
                found = True
                break
        
        if not found:
            return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
        
        if write_products(products):
            print(f"✅ Producto actualizado: {data['name']}")
            return jsonify({'success': True, 'product': data})
        else:
            return jsonify({'success': False, 'error': 'Error al guardar'}), 500
    
    except Exception as e:
        print(f"❌ Error en PUT /api/products/{product_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """API para eliminar producto"""
    try:
        print(f"🗑️ Eliminando producto ID {product_id}")
        
        products = read_products()
        
        # Buscar el producto para eliminar su imagen
        for p in products:
            if p['id'] == product_id and p.get('image_path'):
                image_path = Path(p['image_path'])
                if image_path.exists():
                    os.remove(image_path)
                    print(f"🗑️ Imagen eliminada: {image_path}")
        
        # Eliminar producto de la lista
        products = [p for p in products if p['id'] != product_id]
        
        if write_products(products):
            print(f"✅ Producto eliminado")
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Error al guardar'}), 500
    
    except Exception as e:
        print(f"❌ Error en DELETE /api/products/{product_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎂 Panel de Administración - La Viña Dulce")
    print("   CON SOPORTE REAL DE IMÁGENES")
    print("="*60)
    print(f"✅ Carpeta de imágenes: {UPLOAD_FOLDER}")
    print(f"✅ Archivo menu.py: {MENU_FILE}")
    
    # Verificar carpetas
    if not os.path.exists('templates'):
        os.makedirs('templates', exist_ok=True)
        print("✅ Carpeta templates/ creada")
    
    # Cargar productos de prueba
    test_products = read_products()
    print(f"✅ Productos cargados: {len(test_products)}")
    
    print("\n🌐 Servidor web iniciado:")
    print("📱 http://localhost:8000")
    print("\n💡 Las imágenes se guardarán en:")
    print(f"   {UPLOAD_FOLDER}/")
    print("\n⚠️  Presiona Ctrl+C para detener\n")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
