# Setup del Entorno de Desarrollo

## Requisitos

- Python 3.13+ (instalado en `/usr/bin/python3.13`)
- Conexión a Internet (para APIs de OpenAI/Anthropic)

## Instalación Completada ✅

El entorno virtual ya está creado y configurado con Python 3.13.7.

### Paquetes Instalados

- **LangGraph**: 1.0.2 - Framework para sistemas multi-agente
- **LangChain**: 1.0.3 - Core framework con integraciones
- **LangChain-OpenAI**: 1.0.2 - Integración con OpenAI
- **LangChain-Anthropic**: 1.0.1 - Integración con Claude
- **Jupyter Lab**: 4.4.10 - Entorno interactivo para notebooks
- **Pytest**: 8.4.2 - Framework de testing
- **Black**: 25.9.0 - Formateador de código
- **Ruff**: 0.14.3 - Linter ultra rápido
- **IPython**: 9.6.0 - REPL interactivo mejorado

## Uso del Entorno Virtual

### Activación Rápida

```bash
# Opción 1: Script de activación con información
source activate.sh

# Opción 2: Activación directa
source venv/bin/activate
```

### Desactivación

```bash
deactivate
```

## Configuración de Variables de Entorno

Antes de ejecutar los ejemplos, copia y configura el archivo `.env`:

```bash
cp .env.example .env
```

Edita `.env` y agrega tus API keys:

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic (opcional)
ANTHROPIC_API_KEY=sk-ant-...

# LangSmith (opcional, para debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=micai-tutorial
```

## Comandos Útiles

### Jupyter Lab

```bash
# Iniciar Jupyter Lab
jupyter lab

# Iniciar en puerto específico
jupyter lab --port=8888

# Iniciar sin abrir navegador
jupyter lab --no-browser
```

### Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests de un módulo específico
pytest ejercicios/modulo_1/

# Ejecutar con verbose
pytest -v

# Ejecutar con cobertura
pytest --cov=utils --cov-report=html
```

### Formateo y Linting

```bash
# Formatear todo el código
black .

# Formatear archivo específico
black ejemplos/ejemplo_basico.py

# Verificar sin modificar
black --check .

# Linting con Ruff
ruff check .

# Auto-fix con Ruff
ruff check --fix .
```

### Ejecutar Ejemplos

```bash
# Ejemplo básico
python ejemplos/ejemplo_basico.py

# Con debugging de LangSmith
python ejemplos/debugging_langsmith.py
```

## Estructura del Proyecto

```
micai2025/
├── venv/                    # Entorno virtual (Python 3.13)
├── activate.sh              # Script de activación
├── requirements.txt         # Dependencias del proyecto
├── .env.example            # Template de variables de entorno
├── .env                    # Tu configuración (no en git)
├── docs/                   # Documentación del tutorial
│   ├── 01_introduccion.md
│   ├── 02_arquitectura.md
│   ├── 03_patrones.md
│   ├── 04_aplicaciones_negocio.md
│   ├── 05_debugging_langsmith.md
│   └── GUIA_INSTRUCTOR.md
├── notebooks/              # Notebooks para instructor
│   ├── modulo_1/          # 3 notebooks
│   ├── modulo_2/          # 4 notebooks
│   ├── modulo_3/          # 4 notebooks
│   └── modulo_4/          # 4 notebooks
├── ejemplos/              # Ejemplos completos
├── ejercicios/            # Ejercicios para estudiantes
│   ├── modulo_1/
│   ├── modulo_2/
│   ├── modulo_3/
│   └── modulo_4/
└── utils/                 # Utilidades compartidas
    ├── langsmith_config.py
    └── ...
```

## Verificación del Setup

Para verificar que todo está correctamente instalado:

```bash
source venv/bin/activate
python -c "
import langgraph
import langchain
import langchain_openai
import langchain_anthropic
print('✅ Todas las dependencias importadas correctamente')
print(f'LangGraph version: {langgraph.__version__}')
print(f'LangChain version: {langchain.__version__}')
"
```

## Solución de Problemas

### Error: "Module not found"

```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "API Key not found"

Verifica que el archivo `.env` existe y contiene las API keys correctas.

```bash
# Verificar variables de entorno
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI_API_KEY:', os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

### Jupyter no abre notebooks

```bash
# Reinstalar jupyter
pip install --upgrade jupyter jupyterlab
```

## Recursos Adicionales

- [Documentación de LangGraph](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangSmith Platform](https://smith.langchain.com/)
- [Jupyter Lab Documentation](https://jupyterlab.readthedocs.io/)

## Soporte

Si encuentras problemas durante el setup:

1. Revisa los logs de instalación
2. Verifica la versión de Python: `python --version`
3. Asegúrate de tener conexión a Internet
4. Consulta la [Guía del Instructor](docs/GUIA_INSTRUCTOR.md) para troubleshooting común
