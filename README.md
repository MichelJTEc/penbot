# 🥖 Bot de Telegram para Panadería con IA

Bot profesional e inteligente para gestionar pedidos de panadería usando Telegram y Google Gemini AI.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Telegram Bot API](https://img.shields.io/badge/telegram--bot--api-20.7-blue.svg)
![Google Gemini](https://img.shields.io/badge/google--gemini-1.5--flash-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Características Principales

### 🤖 Inteligencia Artificial
- **Conversación Natural**: Interactúa con clientes usando lenguaje natural
- **Recomendaciones Personalizadas**: Sugiere productos según preferencias
- **Comprensión Contextual**: Entiende pedidos complejos y vagos
- **Respuestas Inteligentes**: Informa sobre ingredientes, alérgenos y más

### 🛒 Sistema de Pedidos
- **Carrito de Compras**: Gestión completa de productos
- **Múltiples Categorías**: Panes, pasteles, galletas y especialidades
- **Cálculo Automático**: Precios y totales en tiempo real
- **Historial de Pedidos**: Consulta pedidos anteriores

### 📱 Interfaz Intuitiva
- **Teclados Personalizados**: Navegación fácil y visual
- **Botones Interactivos**: Agregar productos con un toque
- **Menú Organizado**: Categorías claras y bien estructuradas
- **Emojis Informativos**: Mejor experiencia visual

### 🚚 Gestión de Entregas
- **Entrega a Domicilio**: Con captura de dirección
- **Recogida en Tienda**: Opción de pickup
- **Selección de Horario**: Elige cuándo quieres tu pedido
- **Notas Especiales**: Instrucciones personalizadas

### 📊 Base de Datos
- **Persistencia de Datos**: SQLite integrado
- **Historial Completo**: Todos los pedidos guardados
- **Gestión de Usuarios**: Información de clientes
- **Estadísticas**: Seguimiento de ventas

---

## 🚀 Instalación Rápida

### Prerrequisitos

- Python 3.10 o superior
- Una cuenta de Telegram
- Cuenta de Google para Gemini API (gratuita)

### Paso 1: Obtener Credenciales

#### 🔑 Token de Telegram Bot

1. Abre Telegram y busca [@BotFather](https://t.me/botfather)
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot: `Mi Panadería Bot`
   - Username: `mi_panaderia_bot` (debe terminar en 'bot')
4. Copia el token que te proporciona (algo como: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

#### 🔑 Google Gemini API Key

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la API key generada

### Paso 2: Clonar e Instalar

```bash
# Descargar el proyecto
git clone https://github.com/tu-usuario/bakery-telegram-bot.git
cd bakery-telegram-bot

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 3: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tu editor favorito
nano .env  # o vim, code, notepad, etc.
```

**Contenido del .env:**
```env
TELEGRAM_BOT_TOKEN=tu_token_de_telegram_aqui
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
DATABASE_URL=sqlite:///bakery.db
ADMIN_USER_IDS=tu_telegram_user_id
TIMEZONE=America/Mexico_City
DEBUG_MODE=True
BAKERY_NAME=Panadería Artesanal
PHONE_NUMBER=+52 55 1234 5678
EMAIL=contacto@panaderia.com
ADDRESS=Calle Principal #123, Colonia Centro
```

**¿Cómo obtener tu Telegram User ID?**
1. Busca [@userinfobot](https://t.me/userinfobot) en Telegram
2. Envía `/start`
3. El bot te mostrará tu User ID

### Paso 4: Ejecutar el Bot

```bash
python main.py
```

Si todo está correcto, verás:
```
🥖 Iniciando bot de Panadería Artesanal...
✅ Bot iniciado correctamente!
🤖 Esperando mensajes...
```

---

## 📖 Guía de Uso

### Para Clientes

#### Comandos Disponibles

- `/start` - Iniciar el bot
- `/menu` - Ver el catálogo completo
- `/carrito` - Ver tu carrito de compras
- `/pedidos` - Ver tu historial de pedidos
- `/ia` - Activar modo conversación con IA
- `/ayuda` - Mostrar ayuda
- `/contacto` - Información de contacto

#### Ejemplo de Uso con IA

```
Usuario: Quiero algo dulce para el desayuno
Bot: ¡Perfecto! 🥐 Te recomiendo nuestras Conchas de 
     Chocolate ($12) o los deliciosos Roles de Canela 
     ($80 por 4 piezas). Si prefieres algo más ligero, 
     los Croissants de Chocolate ($30) son excelentes 
     con café. ¿Qué te parece?

Usuario: Dame 2 conchas de chocolate
Bot: ✅ Agregado 2x Concha de Chocolate al carrito

Usuario: Y un croissant
Bot: ✅ Agregado 1x Croissant de Chocolate al carrito
     ¿Algo más o confirmamos tu pedido?
```

#### Flujo de Pedido

1. **Explorar Menú**: Usa `/menu` o habla con la IA
2. **Agregar Productos**: Selecciona y agrega al carrito
3. **Revisar Carrito**: Usa `/carrito` para verificar
4. **Confirmar Pedido**: Selecciona tipo de entrega
5. **Proporcionar Datos**: Dirección y teléfono
6. **Confirmar**: ¡Listo! Recibirás un número de pedido

### Para Administradores

#### Panel de Admin

```bash
# Envía este comando en el bot
/admin
```

Funcionalidades:
- Ver pedidos pendientes
- Actualizar estado de pedidos
- Ver estadísticas de ventas
- Gestionar inventario (próximamente)

---

## 🏗️ Estructura del Proyecto

```
bakery-telegram-bot/
│
├── bot/
│   ├── __init__.py
│   ├── handlers.py          # Manejadores de comandos
│   ├── ai_assistant.py      # Integración con Gemini
│   ├── menu.py              # Catálogo de productos
│   └── order_manager.py     # Gestión de pedidos
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuración
│
├── utils/
│   ├── __init__.py
│   └── keyboards.py         # Teclados de Telegram
│
├── .env                     # Variables de entorno (NO commitear)
├── .env.example             # Plantilla de configuración
├── requirements.txt         # Dependencias
├── main.py                  # Punto de entrada
├── PLAN_IMPLEMENTACION.md   # Plan detallado
└── README.md                # Este archivo
```

---

## ⚙️ Configuración Avanzada

### Personalizar el Menú

Edita `bot/menu.py` para agregar/modificar productos:

```python
Product(
    id=99,
    name="Pan de Ajo",
    price=25.00,
    category="Panes",
    description="Pan con mantequilla de ajo",
    ingredients=["Harina", "Ajo", "Mantequilla"],
    allergens=["Gluten", "Lácteos"],
    preparation_time=40
)
```

### Cambiar Zona Horaria

En `.env`:
```env
TIMEZONE=America/New_York  # o tu zona horaria
```

Zonas horarias comunes:
- México: `America/Mexico_City`
- Argentina: `America/Argentina/Buenos_Aires`
- España: `Europe/Madrid`
- Colombia: `America/Bogota`

### Configurar Horarios de Atención

En `.env`:
```env
OPENING_HOUR=7   # Hora de apertura (24h)
CLOSING_HOUR=20  # Hora de cierre (24h)
MIN_PREPARATION_TIME=2  # Horas mínimas de preparación
```

---

## 🐳 Despliegue en Producción

### Opción 1: Railway (Recomendado)

1. Crea una cuenta en [Railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Agrega las variables de entorno
4. Deploy automático ✅

### Opción 2: Render

1. Crea cuenta en [Render.com](https://render.com)
2. New → Web Service
3. Conecta tu repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python main.py`
6. Agrega variables de entorno
7. Deploy ✅

### Opción 3: VPS (DigitalOcean, AWS, etc.)

```bash
# Conectar al servidor
ssh user@tu-servidor.com

# Instalar dependencias del sistema
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Clonar proyecto
git clone tu-repo.git
cd bakery-telegram-bot

# Configurar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Crear .env con tus credenciales
nano .env

# Ejecutar con systemd
sudo nano /etc/systemd/system/bakery-bot.service
```

**Archivo de servicio systemd:**
```ini
[Unit]
Description=Bakery Telegram Bot
After=network.target

[Service]
Type=simple
User=tu-usuario
WorkingDirectory=/home/tu-usuario/bakery-telegram-bot
Environment="PATH=/home/tu-usuario/bakery-telegram-bot/venv/bin"
ExecStart=/home/tu-usuario/bakery-telegram-bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar servicio
sudo systemctl enable bakery-bot
sudo systemctl start bakery-bot
sudo systemctl status bakery-bot
```

---

## 🔧 Solución de Problemas

### El bot no responde

```bash
# Verificar que esté corriendo
ps aux | grep python

# Ver logs
tail -f bot.log  # si configuraste logging a archivo

# Verificar conexión
python -c "import telegram; print('OK')"
```

### Error de importación

```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

### Error de base de datos

```bash
# Eliminar y recrear base de datos
rm bakery.db
python main.py  # Se creará automáticamente
```

### API de Gemini no responde

- Verifica que tu API key sea válida
- Revisa límites de uso (60 req/min en plan gratuito)
- Espera unos minutos y vuelve a intentar

---

## 📊 Características Futuras (Roadmap)

### Version 2.0
- [ ] Pagos integrados (Stripe, MercadoPago)
- [ ] Reconocimiento de imágenes de productos
- [ ] Soporte multiidioma (español/inglés)
- [ ] App web complementaria
- [ ] Reportes avanzados de ventas

### Version 3.0
- [ ] Chatbot de voz
- [ ] Sistema de puntos y descuentos
- [ ] Integración con WhatsApp
- [ ] API para integraciones externas

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

Creado con ❤️ por [Tu Nombre]

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu@email.com

---

## 🙏 Agradecimientos

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Framework del bot
- [Google Gemini](https://deepmind.google/technologies/gemini/) - IA conversacional
- Comunidad de Telegram Bots

---

## 📞 Soporte

¿Necesitas ayuda?

- 📧 Email: soporte@tupanaderia.com
- 💬 Telegram: [@tu_usuario](https://t.me/tu_usuario)
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/bakery-telegram-bot/issues)

---

## ⭐ Dale una Estrella

Si este proyecto te fue útil, ¡considera darle una estrella en GitHub! ⭐

---

**¡Gracias por usar nuestro Bot de Panadería! 🥖🤖**
# penbot
