"""
demo.py — Script de demostración en terminal
Simula una conversación de WhatsApp con el agente de Tacos El Papaloapan

Uso:
    python demo.py
"""

import os
import sys

from agente import AgenteRestaurante


# ─── Colores para la terminal (ANSI) ──────────────────────────────────────────
VERDE = "\033[92m"
AZUL = "\033[94m"
AMARILLO = "\033[93m"
GRIS = "\033[90m"
RESET = "\033[0m"
NEGRITA = "\033[1m"


def imprimir_bienvenida():
    """Muestra el encabezado de la demo al iniciar."""
    print()
    print(f"{NEGRITA}{'═' * 60}{RESET}")
    print(f"{NEGRITA}  🌮  DEMO — Agente de WhatsApp — NeuroLinkmx{RESET}")
    print(f"{GRIS}  Cliente: Tacos El Papaloapan | Huatusco, Ver.{RESET}")
    print(f"{NEGRITA}{'═' * 60}{RESET}")
    print()
    print(f"{GRIS}Comandos especiales:{RESET}")
    print(f"  {AMARILLO}/limpiar{RESET}  — Reinicia la conversación")
    print(f"  {AMARILLO}/salir{RESET}    — Termina el programa")
    print()


def imprimir_mensaje_usuario(texto: str):
    """Imprime el mensaje del usuario con formato de WhatsApp."""
    print(f"\n{AZUL}{NEGRITA}  Tú:{RESET}")
    print(f"  {texto}")


def imprimir_mensaje_agente(texto: str):
    """Imprime la respuesta del agente con formato de WhatsApp."""
    print(f"\n{VERDE}{NEGRITA}  Lupita (Tacos El Papaloapan):{RESET}")
    # Indentar cada línea de la respuesta para mejor legibilidad
    for linea in texto.split("\n"):
        print(f"  {linea}")


def imprimir_pensando():
    """Muestra un indicador mientras el agente procesa."""
    print(f"\n  {GRIS}✍️  Lupita está escribiendo...{RESET}", end="", flush=True)


def imprimir_separador():
    """Imprime una línea separadora ligera."""
    print(f"\n{GRIS}  {'─' * 56}{RESET}")


def main():
    """Función principal que ejecuta el loop de conversación."""
    imprimir_bienvenida()

    # Inicializar el agente (carga info del restaurante y valida API key)
    try:
        agente = AgenteRestaurante()
    except ValueError as e:
        print(f"\n❌  {e}")
        print(f"\n{AMARILLO}Pasos para configurar:{RESET}")
        print("  1. Copia el archivo .env.example como .env")
        print("  2. Agrega tu ANTHROPIC_API_KEY al archivo .env")
        print("  3. Vuelve a correr el script")
        sys.exit(1)

    print(f"{GRIS}✅ Agente iniciado correctamente. ¡Listo para chatear!{RESET}")
    imprimir_separador()

    # Saludo local — sin llamar a la API
    imprimir_mensaje_agente(
        "¡Hola! Bienvenido a Tacos El Papaloapan 🌮🔥\n"
        "Soy Lupita, tu asistente virtual. Puedo ayudarte con:\n"
        "  ✅ Menú y precios\n"
        "  ✅ Horarios y ubicación\n"
        "  ✅ Pedidos para llevar o a domicilio\n"
        "  ✅ Reservaciones y eventos\n\n"
        "¿En qué te puedo ayudar hoy? 😊"
    )

    # ── Loop principal de conversación ────────────────────────────────────────
    while True:
        imprimir_separador()

        try:
            # Leer input del usuario
            entrada = input(f"\n{AZUL}{NEGRITA}  Tú:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            # El usuario presionó Ctrl+C o Ctrl+D
            print(f"\n\n{GRIS}  Sesión terminada. ¡Hasta luego! 👋{RESET}\n")
            break

        # Ignorar entradas vacías
        if not entrada:
            continue

        # Comandos especiales
        if entrada.lower() in ("/salir", "/exit", "salir", "exit", "q", "quit"):
            print(f"\n{GRIS}  ¡Hasta la próxima! 🌮{RESET}\n")
            break

        if entrada.lower() in ("/limpiar", "/reset", "/nuevo"):
            agente.limpiar_historial()
            print(f"\n{AMARILLO}  🔄 Conversación reiniciada.{RESET}")
            continue

        # Enviar mensaje al agente y mostrar respuesta
        imprimir_pensando()
        respuesta = agente.responder(entrada)

        # Borrar el "está escribiendo..." y mostrar la respuesta
        print("\r" + " " * 50 + "\r", end="")
        imprimir_mensaje_agente(respuesta)


if __name__ == "__main__":
    main()
