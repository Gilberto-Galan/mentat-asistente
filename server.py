import os
import json
from dotenv import load_dotenv
from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from typing import Optional

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
mcp = FastMCP("groq_mcp")


@mcp.tool()
async def chat(
    prompt: str,
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.7
) -> str:
    """Envía un mensaje a Groq y devuelve la respuesta.

    Args:
        prompt: El mensaje o pregunta
        model: Modelo a usar
        temperature: Creatividad (0.0 a 2.0)
    """
    try:
        response = await client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool()
async def chat_with_history(
    messages: list,
    model: str = "llama-3.3-70b-versatile",
    system_prompt: Optional[str] = None
) -> str:
    """Envía una conversación completa con historial a Groq.

    Args:
        messages: Lista de mensajes [{"role": "user"/"assistant", "content": "..."}]
        model: Modelo a usar
        system_prompt: Instrucción de sistema opcional
    """
    try:
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        for msg in messages:
            msgs.append({"role": msg["role"], "content": msg["content"]})

        response = await client.chat.completions.create(
            model=model,
            messages=msgs
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


@mcp.tool()
async def list_models() -> str:
    """Lista los modelos de Groq disponibles."""
    modelos = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    return json.dumps({"models": modelos, "total": len(modelos)}, indent=2)


if __name__ == "__main__":
    mcp.run()