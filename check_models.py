import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar entorno
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"Probando clave que empieza con: {api_key[:5]}...")

try:
    genai.configure(api_key=api_key)
    
    print("\n--- MODELOS DISPONIBLES PARA TI ---")
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            available_models.append(m.name)
            
    if not available_models:
        print("❌ No se encontraron modelos. Verifica tu API Key.")
        
except Exception as e:
    print(f"\n❌ Error fatal: {e}")