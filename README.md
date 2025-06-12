# 🚀 Proyecto FastAPI - Configuración del Entorno Python

Este proyecto utiliza **FastAPI** para construir APIs rápidas, modernas y eficientes. A continuación encontrarás los pasos necesarios para configurar el entorno Python, instalar las dependencias y ejecutar el proyecto.

🧠 Integración con OpenAI y Análisis de Hojas de Vida
Este proyecto incluye la generación de una API robusta utilizando FastAPI, con conexión a OpenAI para el análisis inteligente de hojas de vida (CVs) dentro de un sistema interno. La solución permite procesar de forma automática y eficiente la información extraída de los CVs, identificando habilidades, experiencia laboral, educación y otros criterios relevantes mediante modelos de lenguaje avanzados.

Además, la API se conecta a una base de datos MongoDB, donde se almacena y organiza toda la información procesada. El origen de los archivos de hoja de vida proviene de un servidor FTP, desde el cual se descargan los documentos en distintos formatos (PDF, DOCX, etc.) para su análisis.

Esta integración facilita un flujo completo de procesamiento automático de hojas de vida: desde su recepción vía FTP, pasando por el análisis con inteligencia artificial, hasta su almacenamiento y posterior consulta en MongoDB

---

## 📦 Requisitos previos

Asegúrate de tener instalado lo siguiente:

- **Python 3.10 o superior**  
  Puedes verificarlo con:

```bash
  python --version
```

## 🐍 1. Crear entorno virtual

En la raíz del proyecto, ejecuta el siguiente comando:

```bash
python -m venv env
```

## ⚙️ 2. Activar el entorno virtual

- **En Windows**  
  Puedes verificarlo con:

```bash
  .\env\Scripts\activate
```

- **En macOS / Linux**  
  Puedes verificarlo con:

```bash
  source env/bin/activate.bat
```

Verás algo como **(env)** al inicio de tu línea de comandos cuando esté activo.

## 📥3. Instalar dependencias

Instala todas las dependencias necesarias ejecutando:

```bash
  pip install -r requirements.txt
```

## ✅ 4. Verificar paquetes instalados

```bash
  pip list
```

## 📁 5 Script para creacion de la estructura

Antes crear carpeta **/app**

```bash
    mkdir app
```

Script para crear estrucura de carpetas

- **crear_estructura.py**

```bash
    python crear_estructura.py
```

## 📁  Estructura del proyecto

```bash
fastapi/
│
├── app/
│   ├── controllers/       # Controladores (manejan lógica de rutas)
│   ├── core/              # Configuraciones generales (middlewares, settings)
│   ├── database/          # Conexión a base de datos y modelos base
│   ├── interfaces/        # Definiciones de contratos e interfaces (SOLID)
│   ├── models/            # Modelos de datos (ORM, Pydantic, etc.)
│   ├── repositories/      # Acceso a datos (consultas a BD)
│   ├── routes/            # Definición de rutas
│   ├── schemas/           # Esquemas de entrada/salida (Pydantic)
│   ├── services/          # Lógica de negocio
│   └── main.py            # Punto de entrada de la aplicación
│
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación del proyecto
```

## 🧪 6. Ejecutar el servidor FastAPI

```bash
  uvicorn app.main:app --reload
```

### Abir entorno con Swagguer

<http://127.0.0.1:8000/docs>

## ❌ 7. Desactivar entorno virtual

```bash
  .\env\Scripts\deactivate.bat
```

## 🛠 Recomendaciones

- Usa .env para variables de entorno (usa python-dotenv).

- Sigue principios SOLID en arquitectura.

- Mantén tus dependencias actualizadas.
