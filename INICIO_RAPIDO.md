# 🚀 Inicio Rápido - 5 Minutos

Esta guía te llevará desde cero hasta tener tu bot funcionando en menos de 5 minutos.

## ✅ Checklist Pre-inicio

- [ ] Python 3.10+ instalado
- [ ] Cuenta de Telegram
- [ ] 5 minutos de tu tiempo

---

## Paso 1️⃣: Crear el Bot (1 minuto)

1. Abre Telegram
2. Busca: `@BotFather`
3. Envía: `/newbot`
4. Nombre: `Mi Panadería`
5. Username: `mi_panaderia_bot`
6. **COPIA EL TOKEN** que te da

---

## Paso 2️⃣: Obtener Gemini API (1 minuto)

1. Ve a: https://makersuite.google.com/app/apikey
2. Login con Google
3. Clic en "Create API Key"
4. **COPIA LA API KEY**

---

## Paso 3️⃣: Instalar (2 minutos)

```bash
# Descargar archivos
cd ~/Desktop
# (descomprime los archivos del proyecto aquí)

# Crear entorno
python3 -m venv venv

# Activar
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar
pip install -r requirements.txt
```

---

## Paso 4️⃣: Configurar (1 minuto)

```bash
# Copiar plantilla
cp .env.example .env

# Editar (usa tu editor favorito)
nano .env
```

**Solo necesitas cambiar estas 2 líneas:**
```env
TELEGRAM_BOT_TOKEN=PEGA_TU_TOKEN_AQUI
GEMINI_API_KEY=PEGA_TU_API_KEY_AQUI
```

Guarda y cierra (Ctrl+X, Y, Enter en nano)

---

## Paso 5️⃣: ¡Ejecutar! (10 segundos)

```bash
python main.py
```

Deberías ver:
```
🥖 Iniciando bot de Panadería Artesanal...
✅ Bot iniciado correctamente!
🤖 Esperando mensajes...
```

---

## 🎉 ¡Listo!

Ahora ve a Telegram y busca tu bot. Envía `/start`

---

## 🆘 ¿Problemas?

### Error: "No module named 'telegram'"
```bash
pip install python-telegram-bot
```

### Error: "TELEGRAM_BOT_TOKEN no está configurado"
- Revisa que el archivo `.env` existe
- Verifica que pegaste el token correctamente

### El bot no responde
- Espera 30 segundos después de crear el bot
- Verifica que el token sea correcto
- Revisa que el bot esté corriendo (ventana con "Esperando mensajes...")

---

## 📱 Primer Uso

1. Abre Telegram
2. Busca: `@mi_panaderia_bot` (o el nombre que elegiste)
3. Presiona "START"
4. Prueba escribir: "Quiero pan integral"
5. ¡Explora el menú!

---

## 🔥 Comandos Útiles

```bash
# Ver logs en tiempo real
python main.py

# Detener el bot
Ctrl + C

# Reiniciar
python main.py

# Actualizar código
git pull
pip install -r requirements.txt
```

---

## 📚 Siguiente Paso

Lee el `README.md` completo para:
- Personalizar el menú
- Configurar entregas
- Agregar productos
- Desplegar en servidor

---

**¡Felicitaciones! Tu bot está funcionando 🎊**
