#!/usr/bin/env python3
"""
Script de verificación del sistema
Verifica que todas las dependencias y configuraciones estén correctas
"""
import sys
import os

def check_python_version():
    """Verifica la versión de Python"""
    print("✓ Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (Se requiere 3.10+)")
        return False

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n✓ Verificando dependencias...")
    required = [
        'telegram',
        'google.generativeai',
        'dotenv',
        'pytz'
    ]
    
    all_ok = True
    for module in required:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} no instalado")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Verifica que exista el archivo .env"""
    print("\n✓ Verificando archivo .env...")
    if os.path.exists('.env'):
        print("  ✅ Archivo .env encontrado")
        return True
    else:
        print("  ❌ Archivo .env no encontrado")
        print("  → Copia .env.example a .env y configúralo")
        return False

def check_env_variables():
    """Verifica las variables de entorno necesarias"""
    print("\n✓ Verificando variables de entorno...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = {
            'TELEGRAM_BOT_TOKEN': 'Token del bot de Telegram',
            'GEMINI_API_KEY': 'API Key de Google Gemini'
        }
        
        all_ok = True
        for var, description in required_vars.items():
            value = os.getenv(var)
            if value and value != f'tu_{var.lower()}_aqui':
                print(f"  ✅ {var}: {'*' * 10}{value[-4:]}")
            else:
                print(f"  ❌ {var} no configurado")
                print(f"     → {description}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def check_directories():
    """Verifica que existan los directorios necesarios"""
    print("\n✓ Verificando estructura de directorios...")
    
    required_dirs = ['bot', 'config', 'utils']
    all_ok = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ no encontrado")
            all_ok = False
    
    return all_ok

def check_files():
    """Verifica que existan los archivos necesarios"""
    print("\n✓ Verificando archivos principales...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'bot/handlers.py',
        'bot/ai_assistant.py',
        'bot/menu.py',
        'bot/order_manager.py',
        'config/settings.py',
        'utils/keyboards.py'
    ]
    
    all_ok = True
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} no encontrado")
            all_ok = False
    
    return all_ok

def test_imports():
    """Prueba importar los módulos del proyecto"""
    print("\n✓ Probando importaciones del proyecto...")
    
    try:
        sys.path.insert(0, os.getcwd())
        
        modules = [
            'config.settings',
            'bot.menu',
            'bot.order_manager',
            'utils.keyboards'
        ]
        
        all_ok = True
        for module in modules:
            try:
                __import__(module)
                print(f"  ✅ {module}")
            except Exception as e:
                print(f"  ❌ {module}: {str(e)[:50]}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"  ❌ Error general: {e}")
        return False

def print_summary(results):
    """Imprime resumen de la verificación"""
    print("\n" + "="*50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*50)
    
    total = len(results)
    passed = sum(results.values())
    
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
    
    print("="*50)
    print(f"Total: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print("\n🎉 ¡TODO ESTÁ LISTO!")
        print("Ejecuta: python main.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} problema(s) encontrado(s)")
        print("Por favor corrige los errores arriba.")
        return False

def main():
    """Función principal"""
    print("🔍 VERIFICADOR DEL SISTEMA")
    print("="*50)
    
    results = {
        'Python 3.10+': check_python_version(),
        'Dependencias': check_dependencies(),
        'Archivo .env': check_env_file(),
        'Variables de entorno': check_env_variables(),
        'Directorios': check_directories(),
        'Archivos': check_files(),
        'Importaciones': test_imports()
    }
    
    success = print_summary(results)
    
    if not success:
        print("\n💡 SOLUCIONES RÁPIDAS:")
        
        if not results['Dependencias']:
            print("  → pip install -r requirements.txt")
        
        if not results['Archivo .env']:
            print("  → cp .env.example .env")
            print("  → Edita .env con tus credenciales")
        
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada")
        sys.exit(1)
