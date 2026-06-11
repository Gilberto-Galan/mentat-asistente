import os
import json
import subprocess
from dotenv import load_dotenv
from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from typing import Optional

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
mcp = FastMCP("groq_mcp")


# ---- Diccionarios de lenguajes ----

FRAMEWORKS_POR_LENGUAJE = {
    ".py":    ("Python",        "pytest"),
    ".js":    ("JavaScript",    "Jest"),
    ".ts":    ("TypeScript",    "Jest con ts-jest"),
    ".jsx":   ("React",         "Jest + React Testing Library"),
    ".tsx":   ("React TSX",     "Jest + React Testing Library"),
    ".java":  ("Java",          "JUnit 5"),
    ".cs":    ("C#",            "xUnit"),
    ".go":    ("Go",            "testing (builtin)"),
    ".rb":    ("Ruby",          "RSpec"),
    ".php":   ("PHP",           "PHPUnit"),
    ".rs":    ("Rust",          "módulo tests builtin"),
    ".cpp":   ("C++",           "Google Test"),
    ".c":     ("C",             "Unity Test Framework"),
    ".swift": ("Swift",         "XCTest"),
    ".kt":    ("Kotlin",        "JUnit 5 + Kotest"),
}

DOCS_POR_LENGUAJE = {
    ".py":    ("Python",        "Google Style Docstrings",     "sphinx"),
    ".js":    ("JavaScript",    "JSDoc",                       "jsdoc"),
    ".ts":    ("TypeScript",    "TSDoc",                       "typedoc"),
    ".jsx":   ("React JSX",     "JSDoc + PropTypes",           "jsdoc"),
    ".tsx":   ("React TSX",     "TSDoc + Props interfaces",    "typedoc"),
    ".java":  ("Java",          "Javadoc",                     "javadoc"),
    ".cs":    ("C#",            "XML Documentation Comments",  "docfx"),
    ".go":    ("Go",            "GoDoc",                       "godoc"),
    ".rb":    ("Ruby",          "YARD",                        "yard"),
    ".php":   ("PHP",           "PHPDoc",                      "phpdoc"),
    ".rs":    ("Rust",          "Rustdoc",                     "rustdoc"),
    ".cpp":   ("C++",           "Doxygen",                     "doxygen"),
    ".c":     ("C",             "Doxygen",                     "doxygen"),
    ".swift": ("Swift",         "Swift-DocC",                  "docc"),
    ".kt":    ("Kotlin",        "KDoc",                        "dokka"),
}


# ---- Función helper para ejemplos de documentación ----

def _ejemplo_doc(extension: str) -> str:
    """Devuelve un ejemplo del estilo de documentación según la extensión."""
    ejemplos = {
        ".py": '''
def calcular(a: int, b: int) -> int:
    """Suma dos números enteros.

    Args:
        a: Primer número.
        b: Segundo número.

    Returns:
        La suma de a y b.

    Raises:
        TypeError: Si los argumentos no son enteros.

    Example:
        >>> calcular(2, 3)
        5
    """''',
        ".js": '''
/**
 * Suma dos números.
 * @param {number} a - Primer número.
 * @param {number} b - Segundo número.
 * @returns {number} La suma de a y b.
 * @throws {TypeError} Si los argumentos no son números.
 * @example
 * calcular(2, 3); // 5
 */''',
        ".ts": '''
/**
 * Suma dos números.
 * @param a - Primer número.
 * @param b - Segundo número.
 * @returns La suma de a y b.
 * @throws {TypeError} Si los argumentos no son números.
 * @example
 * ```ts
 * calcular(2, 3); // 5
 * ```
 */''',
        ".java": '''
/**
 * Suma dos números enteros.
 *
 * @param a el primer número
 * @param b el segundo número
 * @return la suma de a y b
 * @throws IllegalArgumentException si los argumentos son negativos
 */''',
        ".cs": '''
/// <summary>
/// Suma dos números enteros.
/// </summary>
/// <param name="a">El primer número.</param>
/// <param name="b">El segundo número.</param>
/// <returns>La suma de a y b.</returns>
/// <exception cref="ArgumentException">
/// Si los argumentos son negativos.
/// </exception>''',
        ".go": '''
// Calcular suma dos números enteros.
// Retorna la suma de a y b.
// Retorna error si los argumentos son negativos.''',
        ".rb": '''
# Suma dos números.
#
# @param a [Integer] el primer número
# @param b [Integer] el segundo número
# @return [Integer] la suma de a y b
# @raise [ArgumentError] si los argumentos no son enteros''',
        ".rs": '''
/// Suma dos números enteros.
///
/// # Arguments
/// * `a` - El primer número
/// * `b` - El segundo número
///
/// # Returns
/// La suma de a y b
///
/// # Examples
/// ```
/// let result = calcular(2, 3);
/// assert_eq!(result, 5);
/// ```''',
        ".cpp": '''
/**
 * @brief Suma dos números enteros.
 * @param a El primer número.
 * @param b El segundo número.
 * @return La suma de a y b.
 * @throws std::invalid_argument Si los argumentos son negativos.
 */''',
        ".swift": '''
/// Suma dos números enteros.
///
/// - Parameters:
///   - a: El primer número.
///   - b: El segundo número.
/// - Returns: La suma de a y b.
/// - Throws: `ValueError` si los argumentos son negativos.''',
        ".kt": '''
/**
 * Suma dos números enteros.
 *
 * @param a El primer número.
 * @param b El segundo número.
 * @return La suma de a y b.
 * @throws IllegalArgumentException si los argumentos son negativos.
 */''',
    }
    return ejemplos.get(extension, "/* Documenta siguiendo el estilo oficial del lenguaje */")


# ---- Tool 1: Chat simple ----

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


# ---- Tool 2: Chat con historial ----

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


# ---- Tool 3: Listar modelos ----

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


# ---- Tool 4: Leer archivo ----

@mcp.tool()
async def leer_archivo(ruta: str) -> str:
    """Lee el contenido de un archivo del proyecto.

    Args:
        ruta: Ruta relativa o absoluta del archivo (ej: src/main.py)
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        lineas = contenido.count("\n") + 1
        return f"Archivo: {ruta}\nLíneas: {lineas}\n\n{contenido}"
    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{ruta}'"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# ---- Tool 5: Listar archivos del proyecto ----

@mcp.tool()
async def listar_archivos(directorio: str = ".") -> str:
    """Lista todos los archivos de una carpeta del proyecto.

    Args:
        directorio: Carpeta a explorar (por defecto la raíz del proyecto)
    """
    try:
        ignorar = {"venv", "__pycache__", ".git", "node_modules", ".env", "dist", "build"}
        archivos = []

        for root, dirs, files in os.walk(directorio):
            dirs[:] = [d for d in dirs if d not in ignorar]
            for file in files:
                ruta = os.path.join(root, file)
                archivos.append(ruta)

        if not archivos:
            return "No se encontraron archivos."

        return f"Archivos encontrados ({len(archivos)}):\n" + "\n".join(sorted(archivos))
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# ---- Tool 6: Revisar código (multi-lenguaje) ----

@mcp.tool()
async def revisar_codigo(ruta: str) -> str:
    """Lee un archivo y lo revisa según las buenas prácticas
    del lenguaje detectado automáticamente.

    Args:
        ruta: Ruta del archivo a revisar
    """
    try:
        _, extension = os.path.splitext(ruta.lower())
        lenguaje, _ = FRAMEWORKS_POR_LENGUAJE.get(
            extension,
            ("desconocido", "")
        )

        with open(ruta, "r", encoding="utf-8") as f:
            codigo = f.read()

        prompt = f"""Eres un experto en {lenguaje}.

Revisa el siguiente código del archivo '{ruta}' y proporciona:
1. Errores o bugs encontrados
2. Problemas de seguridad
3. Mejoras de rendimiento
4. Mejoras de legibilidad
5. Buenas prácticas de {lenguaje} que faltan
6. Sugerencias de refactorización

Sé específico y da ejemplos de cómo corregir cada punto.

Código:
{codigo}"""

        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return f"Lenguaje detectado: {lenguaje}\n\n{response.choices[0].message.content}"

    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{ruta}'"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# ---- Tool 7: Generar tests (multi-lenguaje) ----

@mcp.tool()
async def generar_tests(ruta: str) -> str:
    """Lee un archivo de código y genera unit tests automáticamente
    detectando el lenguaje y usando el framework de testing correcto.

    Args:
        ruta: Ruta del archivo a testear (ej: app.py, index.js, Main.java)
    """
    try:
        _, extension = os.path.splitext(ruta.lower())
        lenguaje, framework = FRAMEWORKS_POR_LENGUAJE.get(
            extension,
            ("desconocido", "el framework de testing más apropiado")
        )

        with open(ruta, "r", encoding="utf-8") as f:
            codigo = f.read()

        prompt = f"""Eres un experto en testing de software.

Analiza el siguiente código en {lenguaje} del archivo '{ruta}' y genera unit tests completos usando {framework}.

Requisitos:
1. Cubre todos los casos normales (happy path)
2. Cubre casos borde (valores vacíos, nulos, límites)
3. Cubre casos de error (excepciones esperadas)
4. Usa las mejores prácticas de {framework}
5. Agrega comentarios explicando cada test
6. El código debe estar listo para ejecutarse sin modificaciones

Código a testear:
{codigo}

Devuelve SOLO el código de los tests, sin explicaciones adicionales."""

        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )

        resultado = response.choices[0].message.content
        return f"Lenguaje: {lenguaje}\nFramework: {framework}\n\n{resultado}"

    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{ruta}'"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# ---- Tool 8: Generar documentación (multi-lenguaje) ----

@mcp.tool()
async def generar_docs(ruta: str) -> str:
    """Lee un archivo de código y genera documentación completa
    usando el estilo oficial del lenguaje detectado automáticamente.

    Args:
        ruta: Ruta del archivo a documentar (ej: app.py, index.js, Main.java)
    """
    try:
        _, extension = os.path.splitext(ruta.lower())
        lenguaje, estilo, herramienta = DOCS_POR_LENGUAJE.get(
            extension,
            ("desconocido", "documentación estándar", "el generador oficial")
        )

        with open(ruta, "r", encoding="utf-8") as f:
            codigo = f.read()

        prompt = f"""Eres un experto en documentación de software para {lenguaje}.

Documenta el siguiente código del archivo '{ruta}' usando el estilo {estilo},
compatible con {herramienta}.

Requisitos:
1. Documenta cada función, método y clase
2. Incluye descripción general del módulo/archivo al inicio
3. Documenta todos los parámetros con sus tipos
4. Documenta los valores de retorno con sus tipos
5. Documenta las excepciones que puede lanzar
6. Agrega ejemplos de uso donde sea útil
7. Sigue estrictamente el formato {estilo}
8. Mantén el código original intacto, solo agrega la documentación

Ejemplo del formato {estilo} que debes usar:
{_ejemplo_doc(extension)}

Código a documentar:
{codigo}

Devuelve el código completo con la documentación agregada."""

        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )

        resultado = response.choices[0].message.content
        return f"Lenguaje: {lenguaje}\nEstilo: {estilo}\nHerramienta: {herramienta}\n\n{resultado}"

    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{ruta}'"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# ---- Tool 9: Ejecutar comando ----

@mcp.tool()
async def ejecutar_comando(comando: str) -> str:
    """Ejecuta un comando en la terminal y devuelve el resultado.

    Args:
        comando: Comando a ejecutar (ej: python --version, pip list)
    """
    try:
        result = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        salida = result.stdout or result.stderr
        return salida if salida else "Comando ejecutado sin salida."
    except subprocess.TimeoutExpired:
        return "Error: El comando tardó más de 30 segundos."
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# ---- Tool 10: Sugerir mensaje de commit ----

@mcp.tool()
async def sugerir_commit() -> str:
    """Analiza los cambios actuales de git y sugiere un mensaje de commit."""
    try:
        diff = subprocess.run(
            "git diff --staged",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        if not diff.stdout:
            return "No hay cambios en staging. Usa 'git add' primero."

        prompt = f"""Analiza este git diff y sugiere 3 opciones de mensaje de commit
siguiendo la convención de Conventional Commits (feat, fix, docs, refactor, test, chore).
Sé conciso y descriptivo.

Git diff:
{diff.stdout[:3000]}"""

        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# ---- Punto de entrada ----

if __name__ == "__main__":
    mcp.run()