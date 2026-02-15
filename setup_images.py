#!/usr/bin/env python3
"""
Script para configurar las carpetas de imágenes
"""
import os
from pathlib import Path

def setup_image_folders():
    """Crea las carpetas necesarias para imágenes"""
    
    # Carpetas a crear
    folders = [
        'static/images/productos',
        'static/images/categorias',
    ]
    
    print("🖼️  Configurando carpetas de imágenes...\n")
    
    for folder in folders:
        path = Path(folder)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Creada: {folder}/")
        else:
            print(f"ℹ️  Ya existe: {folder}/")
    
    print("\n📝 Carpetas configuradas correctamente!\n")
    print("📸 Ahora puedes copiar tus fotos de tortas a:")
    print("   → static/images/productos/\n")
    print("💡 Ejemplo de nombres de archivo:")
    print("   → torta_15_anos_redonda_40p.jpg")
    print("   → torta_matrimonio_rectangular.jpg")
    print("   → torta_bautizo_2_pisos.jpg")
    print("\n✨ Luego edita los productos en el panel admin")
    print("   y pon la ruta: static/images/productos/nombre_foto.jpg")

if __name__ == '__main__':
    setup_image_folders()
