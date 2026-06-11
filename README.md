# 🧠 Mentat — MCP Code Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-SDK-6C3DD4?style=flat&logo=anthropic&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-F55036?style=flat&logo=groq&logoColor=white)
![Model](https://img.shields.io/badge/Model-Llama%203.3%2070B-00A67E?style=flat&logo=meta&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-1.99%2B-007ACC?style=flat&logo=visualstudiocode&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)

Servidor **MCP (Model Context Protocol)** integrado con **GitHub Copilot** en VS Code. Actúa como asistente de desarrollo inteligente que amplía las capacidades nativas de Copilot usando la API de **Groq** con el modelo **Llama 3.3 70B**. 

Permite revisar código, generar tests, documentar, ejecutar comandos y más en múltiples lenguajes de programación, directamente desde el chat de Copilot en VS Code.

---

## ✨ Características

- ✅ Integración nativa con GitHub Copilot Chat en VS Code
- ✅ Soporte multi-lenguaje (Python, JavaScript, TypeScript, Java, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, C++, C y más)
- ✅ Revisión automática de código con sugerencias de mejora
- ✅ Generación de unit tests (pytest, Jest, JUnit, xUnit, RSpec, PHPUnit, etc.)
- ✅ Generación de documentación con estilos nativos (Google Docstrings, JSDoc, TSDoc, Javadoc, etc.)
- ✅ Lectura y exploración de archivos del proyecto
- ✅ Ejecución de comandos desde el chat
- ✅ Sugerencias inteligentes de commits con Conventional Commits
- ✅ Chat conversacional con historial completo
- ✅ Motor: **Llama 3.3 70B** via Groq (gratuito)

---

## 🛠️ Tools disponibles

| Tool | Descripción |
|---|---|
| `chat` | Chat simple con un prompt |
| `chat_with_history` | Chat multi-turno con historial |
| `list_models` | Lista los modelos disponibles |
| `leer_archivo` | Lee el contenido de un archivo |
| `listar_archivos` | Muestra la estructura del proyecto |
| `revisar_codigo` | Revisa un archivo y sugiere mejoras |
| `generar_tests` | Genera unit tests con pytest |
| `generar_docs` | Genera docstrings y documentación |
| `ejecutar_comando` | Ejecuta comandos en la terminal |
| `sugerir_commit` | Sugiere mensajes de commit |

---

## 📦 Dependencias principales

| Paquete | Descripción |
|---|---|
| `mcp` | SDK oficial de Model Context Protocol |
| `groq` | Cliente oficial de la API de Groq |
| `python-dotenv` | Carga variables de entorno desde `.env` |
| `rich` | Renderizado de terminal con estilos avanzados |

---

## 📋 Requisitos

- Python 3.10 o superior
- VS Code 1.99 o superior
- Extensión GitHub Copilot instalada en VS Code
- Cuenta gratuita en [Groq Console](https://console.groq.com)
- Git

---

## 🚀 Instalación

### 1 — Clona el repositorio

```bash
git clone https://github.com/tu-usuario/mentat.git
cd mentat
```

### 2 — Crea y activa el entorno virtual

```bash
# Crear el venv
python -m venv venv

# Activar en Mac / Linux
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

### 3 — Instala las dependencias

```bash
pip install mcp groq python-dotenv rich
```

### 4 — Configura tu API Key

Crea un archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

> Obtén tu API Key gratis en [console.groq.com](https://console.groq.com) → API Keys.

---

## ⚙️ Configuración en VS Code

### 1 — Verifica tu versión de VS Code

```
Help → About → debe ser 1.99 o superior
```

Si necesitas actualizar: [code.visualstudio.com](https://code.visualstudio.com)

### 2 — Obtén la ruta del Python de tu venv

Con el venv activado en la terminal:

```bash
# Windows
where python

# Mac / Linux
which python
```

Copia esa ruta, la necesitarás en el siguiente paso.

### 3 — Abre la configuración MCP de VS Code

```
Ctrl + Shift + P → "MCP: Open User Configuration" → Enter
```

### 4 — Agrega la configuración del servidor

```json
{
    "servers": {
        "mentat": {
            "type": "stdio",
            "command": "C:\\TuUsuario\\TuUsuario\\ruta\\mentat\\venv\\Scripts\\python.exe",
            "args": ["C:\\TuUsuario\\TuUsuario\\ruta\\mentat\\server.py"],
            "env": {
                "GROQ_API_KEY": "gsk_xxxxxxxxxxxxxxxx"
            }
        }
    }
}
```

> **Windows:** usa doble barra invertida `\\` en las rutas.
> **Mac / Linux:** usa `/` normal, por ejemplo `/home/usuario/mentat/venv/bin/python`.

Reemplaza:
- `TuUsuario` por tu usuario del sistema
- `ruta` por la carpeta donde clonaste el proyecto
- `gsk_xxxxxxxxxxxxxxxx` por tu API Key de Groq

### 5 — Verifica que el servidor está corriendo

```
Ctrl + Shift + P → "MCP: List Servers"
```

Debe aparecer `mentat` con estado **En ejecución** y mostrar las 10 tools descubiertas.

---

## 💬 Uso en Copilot Chat

### Abre Copilot Chat en modo Agent

```
Ctrl + Alt + I
```

Cambia el modo a **Agent** en el selector superior del chat.

### Invoca a Mentat

```
#mentat revisa el archivo server.py
```

```
#mentat genera tests para utils.py
```

```
#mentat lista los archivos del proyecto
```

```
#mentat sugiere un mensaje de commit
```

```
#mentat explícame este error: [pega tu error aquí]
```

### En modo Agent también puedes escribir directamente

```
revisa este código y dime si hay mejoras
```

Copilot llamará a Mentat automáticamente cuando lo considere necesario.

---

## 🖥️ Uso por CLI (Alternativa)

Si prefieres usar Mentat sin VS Code, existe un cliente CLI interactivo:

### Ejecutar el CLI

```bash
python cli.py
```

Se abrirá una interfaz interactiva con banner y menús:

```
███╗   ███╗███████╗███╗   ██╗████████╗ █████╗ ████████╗
████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚══██╔══╝
██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████║   ██║   
██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██║   ██║   
██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ██║  ██║   ██║   
╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   

MCP Code Assistant  │  Universal Multi-Language Engine
```

### Comandos disponibles

```
/ayuda              Muestra todos los comandos
/capacidades        Qué puede hacer Mentat
/historial          Muestra la conversación completa
/modelo             Muestra el modelo en uso (Llama 3.3 70B)
/limpiar            Borra el historial y empieza de nuevo
/salir              Cierra Mentat
```

### Ejemplos de uso

```
> revisa este código: [pega tu código aquí]

> genera tests para mi función calcular()

> explícame este error: [error message]

> ¿cuáles son las mejores prácticas en Python?
```

### Características del CLI

- ✅ Renderizado de código con sintaxis coloreada
- ✅ Historial conversacional persistente
- ✅ Soporte para múltiples lenguajes
- ✅ Interfaz amigable con paneles y tablas

---

###  🔄 Actualizar el servidor

Cada vez que modifiques `server.py` reinicia el servidor:

```
Ctrl + Shift + P → "MCP: Restart Server" → mentat
```

---

## 🤝 Apoyo

Si te gusta Mentat y te ha sido útil, **¡tu apoyo es bienvenido!**

### ⭐ Dale una estrella

Si el proyecto te es útil, **considéralo merecedor de una estrella** ⭐ en GitHub. Nos ayuda a crecer y a que otros desarrolladores descubran Mentat.

[⭐ Dale una estrella al proyecto](https://github.com/Gilberto-Galan/mentat-asistente)

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

Creado con ❤️ por **Gilberto Galán**

- GitHub: [@Gilberto-Galan](https://github.com/Gilberto-Galan)
- Proyecto: [Mentat - MCP Code Assistant](https://github.com/Gilberto-Galan/mentat-asistente)
