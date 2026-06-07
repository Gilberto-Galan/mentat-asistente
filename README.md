# 🤖 MCP-GROQ-SERVER

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-SDK-6C3DD4?style=flat&logo=anthropic&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-F55036?style=flat&logo=groq&logoColor=white)
![Model](https://img.shields.io/badge/Model-Llama%203.3%2070B-00A67E?style=flat&logo=meta&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)

Servidor MCP (Model Context Protocol) con interfaz de línea de comandos (CLI) para chatear con modelos LLM a través de la API de Groq. Mantiene historial de conversación y permite interacción multi-turno directamente desde la terminal.

---

## ✨ Características

- Chat conversacional con historial completo desde la terminal
- Tres tools MCP disponibles: chat simple, chat con historial y listado de modelos
- Integración con la API de Groq (gratuita y de alta velocidad)
- Modelo por defecto: `llama-3.3-70b-versatile`
- Configuración de API Key mediante variables de entorno
- Entorno virtual aislado con venv

---

## 🧠 Modelo de IA

| Modelo | Proveedor | Tokens de contexto | Velocidad |
|---|---|---|---|
| `llama-3.3-70b-versatile` | Meta via Groq | 128,000 | ~900 tok/s |
| `llama-3.1-8b-instant` | Meta via Groq | 128,000 | ~2,000 tok/s |
| `mixtral-8x7b-32768` | Mistral via Groq | 32,768 | ~700 tok/s |
| `gemma2-9b-it` | Google via Groq | 8,192 | ~800 tok/s |

---

## 📦 Paquetes instalados

| Paquete | Versión | Descripción |
|---|---|---|
| `mcp` | latest | SDK oficial de Model Context Protocol |
| `groq` | latest | Cliente oficial de la API de Groq |
| `python-dotenv` | latest | Carga variables de entorno desde `.env` |

---

## 📋 Requisitos

- Python 3.10 o superior
- Cuenta gratuita en [Groq Console](https://console.groq.com)
- Git

---

## 🚀 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/MCP-GROQ-SERVER.git
cd MCP-GROQ-SERVER
```

### 2. Crea y activa el entorno virtual

```bash
# Crear el venv
python -m venv venv

# Activar en Mac / Linux
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

### 3. Instala las dependencias

```bash
pip install mcp groq python-dotenv
```

### 4. Configura tu API Key

Crea un archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

> Obtén tu API Key gratis en [console.groq.com](https://console.groq.com) → API Keys.

---

## ▶️ Uso

Con el venv activado, ejecuta:

```bash
python cli.py
```

El cliente levanta el servidor MCP automáticamente en segundo plano y abre la interfaz de chat:

```
=== Cliente MCP ===
Escribe 'salir' para terminar.

Tú: ¿Qué es Docker?
Asistente: Docker es una plataforma de contenedores que permite...

Tú: ¿Y cómo se diferencia de una máquina virtual?
Asistente: A diferencia de una VM, Docker no virtualiza el hardware...

Tú: salir
```

Escribe `salir` para cerrar el chat. El servidor se cierra automáticamente.

---

## 🗂️ Estructura del proyecto

```
MCP-GROQ-SERVER/
├── server.py       # Servidor MCP con las tools de Groq
├── cli.py          # Cliente CLI interactivo
├── .env            # API Key (no se sube a git)
├── .gitignore
└── README.md
```

---

## 🛠️ Tools MCP disponibles

| Tool | Descripción |
|---|---|
| `chat` | Chat simple con un prompt |
| `chat_with_history` | Chat multi-turno con historial completo |
| `list_models` | Lista los modelos disponibles |

---

## 🔒 Seguridad

El archivo `.env` está incluido en `.gitignore` y **nunca se sube al repositorio**. Nunca compartas tu API Key públicamente.

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.