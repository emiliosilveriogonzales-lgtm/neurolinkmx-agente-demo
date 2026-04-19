# 🌮 Agente Demo — Tacos El Papaloapan
### Proyecto NeuroLinkmx | Huatusco, Veracruz

Agente conversacional que simula el asistente de WhatsApp de una taquería, construido con la API de Anthropic (Claude).

---

## ¿Qué hace este proyecto?

- Responde preguntas sobre menú, precios, horarios y ubicación
- Atiende pedidos de forma conversacional
- Mantiene el contexto de la conversación (memoria multi-turno)
- Responde en español mexicano con tono amigable y natural
- Si no sabe algo, redirige al equipo vía WhatsApp

---

## Estructura del proyecto

```
neurolinkmx/
├── agente.py           ← Lógica principal del agente (Claude API)
├── demo.py             ← Script de terminal para probar el agente
├── requirements.txt    ← Dependencias de Python
├── .env.example        ← Plantilla de variables de entorno
├── .env                ← Tu archivo de configuración (no subir a git)
├── datos/
│   └── restaurante.json ← Info del restaurante: menú, horarios, FAQ
└── README.md
```

---

## Instalación

### 1. Requisitos previos

- Python 3.9 o superior
- Una cuenta en [Anthropic Console](https://console.anthropic.com) con créditos

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la API Key

Copia el archivo de ejemplo y edítalo:

```bash
# En Windows:
copy .env.example .env

# En Mac/Linux:
cp .env.example .env
```

Abre `.env` con cualquier editor y reemplaza el valor:

```
ANTHROPIC_API_KEY=sk-ant-api03-TU_CLAVE_AQUI
```

> Puedes obtener tu API key en: https://console.anthropic.com/keys

---

## Cómo correr el proyecto

```bash
python demo.py
```

Verás algo así:

```
════════════════════════════════════════════════════════════
  🌮  DEMO — Agente de WhatsApp — NeuroLinkmx
  Cliente: Tacos El Papaloapan | Huatusco, Ver.
════════════════════════════════════════════════════════════

  Lupita (Tacos El Papaloapan):
  ¡Hola! Bienvenido a Tacos El Papaloapan 🌮🔥 ...

  Tú: ▌
```

### Comandos disponibles en la terminal

| Comando | Acción |
|---------|--------|
| `/limpiar` | Reinicia la conversación desde cero |
| `/salir` | Cierra el programa |
| `Ctrl+C` | También cierra el programa |

---

## Personalización

### Cambiar la información del restaurante

Edita el archivo `datos/restaurante.json`. Puedes modificar:
- Nombre y ubicación
- Menú y precios
- Horarios
- Formas de pago
- Preguntas frecuentes

Los cambios se reflejan automáticamente al reiniciar el script.

### Cambiar el modelo de Claude

En `agente.py`, línea donde dice `self.modelo`, puedes cambiar el modelo:

```python
self.modelo = "claude-sonnet-4-5"   # actual (recomendado para demos)
self.modelo = "claude-haiku-4-5"    # más rápido y económico
self.modelo = "claude-opus-4-7"     # más capaz (mayor costo)
```

### Cambiar la personalidad del agente

En `agente.py`, la función `construir_system_prompt()` define cómo se comporta el agente. Puedes cambiar:
- El nombre ("Lupita")
- El tono (más formal, más informal)
- Las instrucciones de comportamiento

---

## Integración con WhatsApp real

Este proyecto es la base del agente. Para conectarlo a WhatsApp real se usa **Twilio** o la **API oficial de WhatsApp Business**. NeuroLinkmx puede ayudarte con esa integración.

La función `agente.responder(mensaje)` es todo lo que necesitas:

```python
from agente import AgenteRestaurante

agente = AgenteRestaurante()
respuesta = agente.responder("¿Cuánto cuestan los tacos de pastor?")
print(respuesta)
```

---

## Costos aproximados

Con `claude-sonnet-4-5`, una conversación típica de 10 mensajes cuesta alrededor de **$0.01 USD**. Muy económico para un demo o prototipo.

---

## Soporte

**NeuroLinkmx** — Automatización inteligente para negocios
- WhatsApp: +52 XXX XXX XXXX
- Email: hola@neurolinkmx.com
