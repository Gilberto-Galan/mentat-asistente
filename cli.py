import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich import box
import re

# ---- Tema personalizado ----

tema = Theme({
    "user":      "bold cyan",
    "assistant": "bold magenta",
    "command":   "bold yellow",
    "success":   "bold green",
    "error":     "bold red",
    "info":      "dim white",
    "banner":    "bold magenta",
})

console = Console(theme=tema)


# ---- Detectar y renderizar bloques de código ----

def renderizar_respuesta(texto: str):
    """Detecta bloques de código en la respuesta y los renderiza con sintaxis."""

    LENGUAJES = {
        "python": "python",   "py": "python",
        "javascript": "javascript", "js": "javascript",
        "typescript": "typescript", "ts": "typescript",
        "java": "java",       "c": "c",
        "cpp": "cpp",         "cs": "csharp",
        "go": "go",           "rust": "rust",
        "ruby": "ruby",       "php": "php",
        "swift": "swift",     "kotlin": "kotlin",
        "bash": "bash",       "sh": "bash",
        "shell": "bash",      "sql": "sql",
        "json": "json",       "yaml": "yaml",
        "html": "html",       "css": "css",
        "jsx": "jsx",         "tsx": "tsx",
    }

    patron = r"```(\w+)?\n(.*?)```"
    partes = re.split(patron, texto, flags=re.DOTALL)

    for i, parte in enumerate(partes):
        if i % 3 == 0:
            if parte.strip():
                console.print(Markdown(parte.strip()))
        elif i % 3 == 1:
            lenguaje_raw = (parte or "").lower().strip()
            lenguaje_rich = LENGUAJES.get(lenguaje_raw, lenguaje_raw or "text")
        elif i % 3 == 2:
            sintaxis = Syntax(
                parte.strip(),
                lenguaje_rich,
                theme="monokai",
                line_numbers=True,
                word_wrap=True,
                padding=(1, 2),
            )
            console.print(Panel(
                sintaxis,
                border_style="magenta",
                box=box.ROUNDED,
                title=f"[dim]{lenguaje_rich}[/dim]",
                title_align="right"
            ))


# ---- Banner ----

def mostrar_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = """
███╗   ███╗███████╗███╗   ██╗████████╗ █████╗ ████████╗
████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚══██╔══╝
██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████║   ██║   
██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██║   ██║   
██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ██║  ██║   ██║   
╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   
"""
    console.print(Text(banner, style="banner"))
    console.print(
        Panel(
            "[cyan]MCP Code Assistant[/cyan]  [dim]│[/dim]  "
            "[green]Universal Multi-Language Engine[/green]\n"
            "[dim]v1.0.0  │  © 2026 Gilberto Galán  │  "
            "https://github.com/Gilberto-Galan[/dim]\n\n"
            "[dim]Escribe [bold white]/ayuda[/bold white] para ver los comandos "
            "o [bold white]/capacidades[/bold white] para ver qué puede hacer Mentat.[/dim]",
            border_style="magenta",
            box=box.ROUNDED,
            padding=(0, 2)
        )
    )
    console.print()


# ---- Capacidades ----

def mostrar_capacidades():
    from rich.table import Table

    tabla = Table(
        title="⚡ ¿Qué puede hacer Mentat?",
        box=box.ROUNDED,
        border_style="magenta",
        header_style="bold cyan",
        show_lines=True,
        padding=(0, 1)
    )

    tabla.add_column("",             style="bold", width=4)
    tabla.add_column("Tool",         style="bold cyan", width=20)
    tabla.add_column("Descripción",  style="dim white")

    capacidades = [
        ("💬", "Conversación",       "Chat con historial y contexto acumulado"),
        ("🔍", "Revisar código",      "Analiza archivos y sugiere mejoras"),
        ("🧪", "Generar tests",       "Crea unit tests con el framework correcto"),
        ("📄", "Documentar",          "Genera docs en el estilo oficial del lenguaje"),
        ("📂", "Explorar proyecto",   "Lista y lee archivos de tu proyecto"),
        ("⚙️", "Ejecutar comandos",   "Corre comandos de terminal desde el chat"),
        ("📝", "Sugerir commits",     "Propone mensajes con Conventional Commits"),
        ("🌐", "Multi-lenguaje",      "Python, JS, TS, Java, Go, Rust, C++ y más"),
        ("🤖", "Listar modelos",      "Muestra los modelos de Groq disponibles"),
    ]

    for icono, titulo, desc in capacidades:
        tabla.add_row(icono, titulo, desc)

    console.print(tabla)
    console.print()


# ---- Ayuda ----

def mostrar_ayuda():
    from rich.table import Table

    tabla = Table(
        title="📋 Comandos disponibles",
        box=box.ROUNDED,
        border_style="yellow",
        header_style="bold yellow",
        show_lines=True,
        padding=(0, 1)
    )

    tabla.add_column("Comando",      style="bold green", width=16)
    tabla.add_column("Descripción",  style="dim white")

    comandos = [
        ("/ayuda",       "Muestra esta lista de comandos"),
        ("/historial",   "Muestra toda la conversación"),
        ("/limpiar",     "Borra el historial y empieza de nuevo"),
        ("/modelo",      "Muestra el modelo en uso"),
        ("/capacidades", "Muestra todo lo que puede hacer Mentat"),
        ("/salir",       "Cierra Mentat"),
    ]

    for cmd, desc in comandos:
        tabla.add_row(cmd, desc)

    console.print(tabla)
    console.print()


# ---- Historial ----

def mostrar_historial(historial: list):
    if not historial:
        console.print(Panel("[dim]No hay mensajes aún.[/dim]", border_style="dim"))
        return

    console.print()
    for i, msg in enumerate(historial, 1):
        if msg["role"] == "user":
            console.print(Panel(
                msg["content"],
                title=f"[cyan]Tú  #{i}[/cyan]",
                border_style="cyan",
                box=box.ROUNDED,
                padding=(0, 1)
            ))
        else:
            renderizar_respuesta(msg["content"])
    console.print()


# ---- Chat principal ----

async def chat():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            modelo = "llama-3.3-70b-versatile"

            mostrar_banner()

            historial = []

            while True:
                try:
                    user_input = console.input("[cyan]  You ›[/cyan] ").strip()
                except KeyboardInterrupt:
                    console.print("\n[dim]  Cerrando Mentat... ¡Hasta luego![/dim]\n")
                    break

                if not user_input:
                    continue

                if user_input.lower() in ("/salir", "salir", "exit", "quit"):
                    console.print("\n[dim]  Cerrando Mentat... ¡Hasta luego![/dim]\n")
                    break

                elif user_input.lower() == "/historial":
                    mostrar_historial(historial)
                    continue

                elif user_input.lower() == "/limpiar":
                    historial = []
                    console.print("\n[success]  ✓ Historial borrado. Nueva conversación iniciada.[/success]\n")
                    continue

                elif user_input.lower() == "/modelo":
                    console.print(f"\n[info]  Modelo actual: [bold white]{modelo}[/bold white][/info]\n")
                    continue

                elif user_input.lower() == "/capacidades":
                    mostrar_capacidades()
                    continue

                elif user_input.lower() == "/ayuda":
                    mostrar_ayuda()
                    continue

                # Mensaje normal → llama al MCP
                historial.append({"role": "user", "content": user_input})

                console.print("[dim]  Mentat está pensando...[/dim]")

                result = await session.call_tool(
                    "chat_with_history",
                    arguments={
                        "messages": historial,
                        "model": modelo,
                        "system_prompt": (
                            "Eres Mentat, un asistente de desarrollo de software inteligente. "
                            "Eres conciso, preciso y útil. Ayudas con código, errores, tests, "
                            "documentación y cualquier tarea de desarrollo."
                        )
                    }
                )

                respuesta = result.content[0].text
                historial.append({"role": "assistant", "content": respuesta})

                console.print()
                console.print("[assistant]  Mentat ›[/assistant]")
                console.print()
                renderizar_respuesta(respuesta)
                console.print()

asyncio.run(chat())