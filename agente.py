"""
agente.py — Agente de WhatsApp para Tacos El Papaloapan
Proyecto demo de NeuroLinkmx
"""

import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def cargar_info_restaurante() -> dict:
    """Lee el archivo JSON con la información del restaurante."""
    ruta = Path(__file__).parent / "datos" / "restaurante.json"
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def construir_system_prompt(info: dict) -> str:
    """
    Construye el prompt del sistema con toda la información del restaurante.
    Este prompt define la personalidad y conocimiento del agente.
    """
    menu_texto = []

    # Formatear el menú de tacos
    menu_texto.append("TACOS:")
    for item in info["menu"]["tacos"]:
        linea = f"  - {item['nombre']}: ${item['precio']} MXN"
        if "descripcion" in item:
            linea += f" — {item['descripcion']}"
        if item.get("disponibilidad"):
            linea += f" ({item['disponibilidad']})"
        menu_texto.append(linea)

    # Formatear quesadillas
    menu_texto.append("\nQUESADILLAS:")
    for item in info["menu"]["quesadillas"]:
        linea = f"  - {item['nombre']}: ${item['precio']} MXN — {item['descripcion']}"
        menu_texto.append(linea)

    # Formatear gorditas
    menu_texto.append("\nGORDITAS:")
    for item in info["menu"]["gorditas"]:
        linea = f"  - {item['nombre']}: ${item['precio']} MXN — {item['descripcion']}"
        menu_texto.append(linea)

    # Formatear bebidas
    menu_texto.append("\nBEBIDAS:")
    for item in info["menu"]["bebidas"]:
        linea = f"  - {item['nombre']}: ${item['precio']} MXN"
        if "descripcion" in item:
            linea += f" — {item['descripcion']}"
        menu_texto.append(linea)

    # Formatear extras
    menu_texto.append("\nEXTRAS Y COMPLEMENTOS:")
    for item in info["menu"]["extras"]:
        if item["precio"] == 0:
            linea = f"  - {item['nombre']}: GRATIS"
        else:
            linea = f"  - {item['nombre']}: ${item['precio']} MXN"
        if "descripcion" in item:
            linea += f" — {item['descripcion']}"
        menu_texto.append(linea)

    # Formatear preguntas frecuentes
    faq_texto = []
    for faq in info["preguntas_frecuentes"]:
        faq_texto.append(f"P: {faq['pregunta']}\nR: {faq['respuesta']}")

    # Construir el prompt completo del sistema
    prompt = f"""Eres el asistente virtual de {info['nombre']}, una taquería ubicada en {info['ubicacion']['ciudad']}.

Tu nombre es "Lupita" y representas al negocio con un tono amigable, cálido y natural, como si fueras parte del equipo. Siempre respondes en español mexicano coloquial pero sin ser informal en exceso. Usas expresiones como "¡Claro que sí!", "Con mucho gusto", "¡Qué rica elección!", etc.

INFORMACIÓN DEL NEGOCIO:
- Nombre: {info['nombre']}
- Dirección: {info['ubicacion']['direccion']}
- Referencias: {info['ubicacion']['referencias']}
- Horarios: Lun-Vie {info['horarios']['lunes_viernes']}, Sábado {info['horarios']['sabado']}, Domingo {info['horarios']['domingo']}
- Nota de horarios: {info['horarios']['nota']}
- WhatsApp: {info['contacto']['whatsapp']}
- Instagram: {info['contacto']['instagram']}

SOBRE NOSOTROS:
{info['sobre_nosotros']}

MENÚ COMPLETO Y PRECIOS:
{chr(10).join(menu_texto)}

FORMAS DE PAGO:
{', '.join(info['formas_de_pago'])}

SERVICIOS:
{', '.join(info['servicios'])}

PREGUNTAS FRECUENTES:
{chr(10).join(faq_texto)}

INSTRUCCIONES IMPORTANTES:
1. Si te preguntan algo que no está en esta información, di: "Mmm, esa pregunta me la tienes que hacer al equipo directamente, ¡pero te aseguro que te van a ayudar! Escríbenos al WhatsApp {info['contacto']['whatsapp']}."
2. Si alguien quiere hacer un pedido, guíalo con amabilidad: pregunta cuántos tacos quiere, qué tipo y si es para comer aquí, para llevar o a domicilio.
3. Nunca inventes precios, horarios ni información que no esté en los datos anteriores.
4. Si alguien pregunta por algo del menú que no existe, sugiérele alternativas de lo que sí tenemos.
5. Mantén respuestas cortas y claras, como lo haría alguien en WhatsApp. No más de 3-4 párrafos por respuesta.
6. Usa emojis de forma moderada para dar calidez (🌮🔥✅👍).
"""
    return prompt


class AgenteRestaurante:
    """
    Clase principal del agente. Maneja el historial de conversación
    y se comunica con la API de Claude.
    """

    def __init__(self):
        # Verificar que la API key esté disponible
        api_key = os.getenv("ANTHROPIC_API_KEY")
        print(f"[DIAG] API key leída: {api_key[:20] if api_key else 'NO ENCONTRADA'}")
        if not api_key:
            raise ValueError(
                "No se encontró ANTHROPIC_API_KEY. "
                "Crea un archivo .env con tu clave de Anthropic."
            )

        # Inicializar el cliente de Anthropic
        self.cliente = anthropic.Anthropic(api_key=api_key)

        # Cargar info del restaurante y construir el prompt del sistema
        self.info = cargar_info_restaurante()
        self.system_prompt = construir_system_prompt(self.info)

        # Historial de mensajes de la conversación (multi-turno)
        self.historial: list[dict] = []

        # Modelo a usar (solicitado por el cliente)
        self.modelo = "claude-haiku-4-5-20251001"

    def responder(self, mensaje_usuario: str) -> str:
        """
        Recibe un mensaje del usuario y devuelve la respuesta del agente.
        Mantiene el historial completo de la conversación.
        """
        # Agregar el mensaje del usuario al historial
        self.historial.append({
            "role": "user",
            "content": mensaje_usuario
        })

        try:
            # Llamar a la API de Claude con el historial completo
            respuesta = self.cliente.messages.create(
                model=self.modelo,
                max_tokens=1024,
                system=self.system_prompt,
                messages=self.historial
            )

            # Extraer el texto de la respuesta
            texto_respuesta = respuesta.content[0].text

            # Agregar la respuesta al historial para mantener el contexto
            self.historial.append({
                "role": "assistant",
                "content": texto_respuesta
            })

            return texto_respuesta

        except anthropic.AuthenticationError:
            return "❌ Error de autenticación: verifica que tu API key de Anthropic sea válida."

        except anthropic.RateLimitError:
            return "⏳ Demasiadas solicitudes por ahora. Por favor intenta de nuevo en unos segundos."

        except anthropic.APIConnectionError:
            return "🌐 Sin conexión a la API. Verifica tu conexión a internet e intenta de nuevo."

        except anthropic.APIStatusError as e:
            return f"⚠️ Error de la API (código {e.status_code}). Por favor intenta de nuevo."

        except Exception as e:
            return f"⚠️ Ocurrió un error inesperado: {str(e)}"

    def limpiar_historial(self):
        """Reinicia la conversación borrando el historial."""
        self.historial = []
