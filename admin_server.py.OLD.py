"""
Servidor web para administrar productos de La Viña Dulce
VERSIÓN COMPLETA - Soporta todos los campos nuevos
"""
from flask import Flask, render_template, request, jsonify
import json
import os
from pathlib import Path
import re

app = Flask(__name__)

# Ruta al archivo de productos
MENU_FILE = Path(__file__).parent / 'bot' / 'menu.py'

print(f"📂 Buscando menu.py en: {MENU_FILE}")
print(f"📂 Existe: {MENU_FILE.exists()}")

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
        # Buscar bloques Product(...),
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
                        # Si no se puede convertir, dejarlo como string
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
        
        if start_idx == -1:
            print("❌ No se encontró 'PRODUCTS = ['")
            return False
        if end_idx == -1:
            print("❌ No se encontró '# Organizar productos por categoría'")
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
                
                if product.get('image_path'):
                    products_code += f"        image_path=\"{product['image_path']}\",\n"
                
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
        
        # Asegurar campos por defecto
        data.setdefault('portions', '')
        data.setdefault('shape', '')
        data.setdefault('codigo', '')
        data.setdefault('image_path', None)
        data.setdefault('preparation_time', 48)
        data.setdefault('available', True)
        data.setdefault('ingredients', [])
        data.setdefault('allergens', [])
        
        products.append(data)
        
        if write_products(products):
            print(f"✅ Producto agregado exitosamente: {data['name']}")
            return jsonify({'success': True, 'product': data})
        else:
            print(f"❌ Error al guardar producto")
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
        
        # Encontrar y actualizar producto
        found = False
        for i, p in enumerate(products):
            if p['id'] == product_id:
                data['id'] = product_id
                
                # Asegurar campos
                data.setdefault('portions', '')
                data.setdefault('shape', '')
                data.setdefault('codigo', '')
                data.setdefault('image_path', None)
                data.setdefault('preparation_time', 48)
                data.setdefault('available', True)
                data.setdefault('ingredients', [])
                data.setdefault('allergens', [])
                
                products[i] = data
                found = True
                break
        
        if not found:
            print(f"❌ Producto ID {product_id} no encontrado")
            return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
        
        if write_products(products):
            print(f"✅ Producto actualizado: {data['name']}")
            return jsonify({'success': True, 'product': data})
        else:
            print(f"❌ Error al guardar cambios")
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
        original_count = len(products)
        
        products = [p for p in products if p['id'] != product_id]
        
        if len(products) == original_count:
            print(f"❌ Producto ID {product_id} no encontrado")
            return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
        
        if write_products(products):
            print(f"✅ Producto eliminado")
            return jsonify({'success': True})
        else:
            print(f"❌ Error al guardar cambios")
            return jsonify({'success': False, 'error': 'Error al guardar'}), 500
    
    except Exception as e:
        print(f"❌ Error en DELETE /api/products/{product_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Verificar que exista la carpeta templates
    if not os.path.exists('templates'):
        print("⚠️ Creando carpeta templates/")
        os.makedirs('templates', exist_ok=True)
    
    # Verificar que exista admin.html
    if not os.path.exists('templates/admin.html'):
        print("⚠️ ADVERTENCIA: No se encuentra templates/admin.html")
        print("   Asegúrate de copiar el archivo admin.html a la carpeta templates/")
    
    print("\n" + "="*60)
    print("🎂 Panel de Administración - La Viña Dulce")
    print("="*60)
    print(f"✅ Archivo menu.py: {MENU_FILE}")
    
    # Cargar productos de prueba
    test_products = read_products()
    print(f"✅ Productos cargados: {len(test_products)}")
    
    if len(test_products) > 0:
        print(f"📋 Ejemplo: {test_products[0].get('name', 'Sin nombre')}")
    
    print("\n🌐 Servidor web iniciado:")
    print("📱 http://localhost:8000")
    print("📱 http://127.0.0.1:8000")
    print("\n⚠️  Presiona Ctrl+C para detener\n")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
