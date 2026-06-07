import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def mostrar_historial(historial: list):
    if not historial:
        print("\n  (No hay mensajes aún)\n")
        return
    print("\n" + "="*40)
    print("  HISTORIAL DE CONVERSACIÓN")
    print("="*40)
    for i, msg in enumerate(historial, 1):
        rol = "Tú" if msg["role"] == "user" else "Asistente"
        print(f"\n[{i}] {rol}:")
        print(f"  {msg['content']}")
    print("\n" + "="*40 + "\n")

def mostrar_ayuda():
    print("""
Comandos disponibles:
  /historial  → muestra toda la conversación
  /limpiar    → borra el historial y empieza de nuevo
  /modelo     → muestra el modelo en uso
  /salir      → cierra el chat
    """)

async def chat():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            modelo = "llama-3.3-70b-versatile"
            historial = []

            print("="*40)
            print("   MCP-GROQ-SERVER  |  CLI Chat")
            print("="*40)
            print("Escribe /ayuda para ver los comandos.\n")

            while True:
                user_input = input("Tú: ").strip()

                if not user_input:
                    continue

                # Comandos especiales
                if user_input.lower() in ("/salir", "salir"):
                    print("\nCerrando chat. ¡Hasta luego!\n")
                    break

                elif user_input.lower() == "/historial":
                    mostrar_historial(historial)
                    continue

                elif user_input.lower() == "/limpiar":
                    historial = []
                    print("\n  Historial borrado. Nueva conversación iniciada.\n")
                    continue

                elif user_input.lower() == "/modelo":
                    print(f"\n  Modelo actual: {modelo}\n")
                    continue

                elif user_input.lower() == "/ayuda":
                    mostrar_ayuda()
                    continue

                # Mensaje normal → llama al MCP
                historial.append({"role": "user", "content": user_input})

                result = await session.call_tool(
                    "chat_with_history",
                    arguments={
                        "messages": historial,
                        "model": modelo,
                        "system_prompt": "Eres un asistente útil y conciso."
                    }
                )

                respuesta = result.content[0].text
                historial.append({"role": "assistant", "content": respuesta})

                print(f"\nAsistente: {respuesta}\n")

asyncio.run(chat())