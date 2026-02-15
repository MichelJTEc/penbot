"""
Servidor web para administrar productos de la panadería
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from pathlib import Path

app = Flask(__name__)

# Ruta al archivo de productos
MENU_FILE = Path(__file__).parent / 'bot' / 'menu.py'

def read_products():
    """Lee los productos del archivo menu.py"""
    products = []
    
    with open(MENU_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extraer productos usando parsing simple
    in_products = False
    current_product = {}
    
    for line in content.split('\n'):
        line = line.strip()
        
        if 'Product(' in line:
            in_products = True
            current_product = {}
            
        elif in_products and '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().rstrip(',')
            
            # Limpiar valores
            if value.startswith('"') or value.startswith("'"):
                value = value[1:-1]
            elif value.startswith('['):
                value = eval(value)
            elif value in ['True', 'False']:
                value = value == 'True'
            else:
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except:
                    pass
            
            current_product[key] = value
            
        elif in_products and '),' in line:
            in_products = False
            if current_product:
                products.append(current_product)
    
    return products

def write_products(products):
    """Escribe los productos al archivo menu.py"""
    
    # Leer el archivo original
    with open(MENU_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar donde comienza PRODUCTS
    start_marker = "PRODUCTS = ["
    end_marker = "# Organizar productos por categoría"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        raise Exception("No se pudo encontrar la sección de productos")
    
    # Generar nuevo código de productos
    products_code = "PRODUCTS = [\n"
    
    for product in products:
        products_code += "    # CATEGORÍA: {}\n".format(product.get('category', 'Sin categoría').upper())
        products_code += "    Product(\n"
        products_code += f"        id={product['id']},\n"
        products_code += f"        name=\"{product['name']}\",\n"
        products_code += f"        price={product['price']},\n"
        products_code += f"        category=\"{product['category']}\",\n"
        products_code += f"        description=\"{product['description']}\",\n"
        products_code += f"        ingredients={product.get('ingredients', [])},\n"
        products_code += f"        allergens={product.get('allergens', [])},\n"
        products_code += f"        preparation_time={product.get('preparation_time', 30)}"
        
        if 'available' in product and not product['available']:
            products_code += ",\n        available=False"
        
        products_code += "\n    ),\n"
    
    products_code += "]\n\n"
    
    # Reemplazar la sección
    new_content = content[:start_idx] + products_code + content[end_idx:]
    
    # Escribir archivo
    with open(MENU_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

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
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    """API para agregar producto"""
    try:
        data = request.json
        products = read_products()
        
        # Generar nuevo ID
        max_id = max([p['id'] for p in products]) if products else 0
        data['id'] = max_id + 1
        
        products.append(data)
        write_products(products)
        
        return jsonify({'success': True, 'product': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """API para actualizar producto"""
    try:
        data = request.json
        products = read_products()
        
        # Encontrar y actualizar producto
        for i, p in enumerate(products):
            if p['id'] == product_id:
                data['id'] = product_id
                products[i] = data
                break
        
        write_products(products)
        
        return jsonify({'success': True, 'product': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """API para eliminar producto"""
    try:
        products = read_products()
        products = [p for p in products if p['id'] != product_id]
        
        write_products(products)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Crear carpeta templates si no existe
    os.makedirs('templates', exist_ok=True)
    
    print("🌐 Servidor de administración iniciado")
    print("📱 Abre en tu navegador: http://localhost:8000")
    print("⚠️  Presiona Ctrl+C para detener")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
