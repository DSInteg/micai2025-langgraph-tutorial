# Tutorial: Building Multi-Agent Networks with LangGraph
## Mexican Conference on Artificial Intelligence (MICAI) 2025

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0.2-green.svg)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-1.0.3-orange.svg)](https://github.com/langchain-ai/langchain)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Tutorial práctico de 4 horas sobre construcción de redes multi-agente con LangGraph, presentado en MICAI 2025.

## 📋 Información General

**Duración**: 4 horas
**Nivel**: Intermedio a Avanzado
**Enfoque**: Hands-on learning - De teoría a aplicaciones de negocio
**Instructor**: Dr. Juan Jose Cordova Zamorano (DSInteg)

### Objetivos de Aprendizaje

Al finalizar este tutorial, podrás:

1. ✅ **Distinguir** entre workflows determinísticos y agentes autónomos
2. ✅ **Diseñar** arquitecturas de redes multi-agente apropiadas
3. ✅ **Implementar** sistemas multi-agente usando LangGraph
4. ✅ **Aplicar** patrones de comunicación y coordinación entre agentes
5. ✅ **Evaluar** el rendimiento y confiabilidad de sistemas multi-agente
6. ✅ **Optimizar** redes de agentes para casos de uso reales

## 🚀 Setup Rápido

### 1. Requisitos Previos

- Python 3.13+ (instalado y configurado)
- Git
- Cuenta de OpenAI (o Anthropic)
- Editor de código (VS Code recomendado)

### 2. Instalación

**✅ El entorno virtual ya está creado con Python 3.13.7**

```bash
# Activar ambiente virtual
# Opción 1: Script con información (recomendado)
source activate.sh

# Opción 2: Activación directa
source venv/bin/activate
```

**📦 Paquetes instalados:**
- LangGraph 1.0.2
- LangChain 1.0.3 (con OpenAI y Anthropic)
- Jupyter Lab 4.4.10
- Pytest 8.4.2, Black 25.9.0, Ruff 0.14.3

Ver [SETUP.md](SETUP.md) para detalles completos de instalación y troubleshooting.

### 3. Configurar API Keys

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tus API keys
# OPENAI_API_KEY=sk-...

# Opcional pero ALTAMENTE RECOMENDADO: LangSmith para debugging
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=ls__...
# LANGCHAIN_PROJECT=micai-tutorial
```

> **💡 Tip**: LangSmith es **opcional** pero **muy recomendado**. Te permite visualizar el flujo completo de tus agentes, ver exactamente qué prompts se envían al LLM, medir latencia y costos, y debuggear problemas. [Crea una cuenta gratuita aquí](https://smith.langchain.com).

### 4. Verificar Instalación

```bash
# Ejecutar test de setup
python -c "from utils import get_openai_llm; llm = get_openai_llm(); print('✅ Setup correcto!')"
```

## 📚 Estructura del Tutorial

### Módulo 1: Fundamentos (45 min)

**Teoría** (25 min):
- Workflows vs Agentes: Diferencias fundamentales
- Cuándo usar cada enfoque
- Componentes de un sistema agéntico
- Introducción a LangGraph

**Práctica** (20 min):
- **[Ejercicio 1.1](ejercicios/modulo_1/ejercicio_1_1_workflow_simple/)**: Workflow simple (prompt chaining)
- **[Ejercicio 1.2](ejercicios/modulo_1/ejercicio_1_2_agente_basico/)**: Agente autónomo básico

**Documentación**:
- [📖 Fundamentos - Teoría Completa](docs/01_fundamentos.md)

### Módulo 2: Patrones Multi-Agente (60 min)

**Teoría** (20 min):
- Routing y clasificación
- Paralelización (sectioning y voting)
- Orchestrator-Workers
- Evaluator-Optimizer

**Práctica** (40 min):
- **[Ejercicio 2.1](ejercicios/modulo_2/ejercicio_2_1_routing/)**: Sistema de routing con agentes especializados
- **[Ejercicio 2.2](ejercicios/modulo_2/ejercicio_2_2_parallelization/)**: Paralelización con agregación
- **[Ejercicio 2.3](ejercicios/modulo_2/ejercicio_2_3_orchestrator/)**: Orchestrator-Workers para análisis

**Documentación**:
- [📖 Patrones Multi-Agente - Teoría Completa](docs/02_patrones_workflows.md)

### Módulo 3: Agentes Autónomos (60 min)

**Teoría** (20 min):
- Arquitecturas de agentes autónomos
- Gestión de estado en grafos complejos
- Memoria compartida y comunicación
- Condiciones de parada y safety

**Práctica** (40 min):
- **[Ejercicio 3.1](ejercicios/modulo_3/ejercicio_3_1_agente_autonomo/)**: Agente con planificación dinámica
- **[Ejercicio 3.2](ejercicios/modulo_3/ejercicio_3_2_red_colaborativa/)**: Red colaborativa con handoffs
- **[Ejercicio 3.3](ejercicios/modulo_3/ejercicio_3_3_memoria_compartida/)**: Memoria compartida entre agentes

**Documentación**:
- [📖 Agentes Autónomos - Teoría Completa](docs/03_agentes_autonomos.md)

### Módulo 4: Aplicaciones de Negocio (75 min)

**Teoría** (15 min):
- Casos de uso empresariales
- Consideraciones de producción
- Monitoreo y observabilidad
- Costos y optimización

**Práctica** (60 min):
- **[Ejercicio 4.1](ejercicios/modulo_4/ejercicio_4_1_atencion_cliente/)**: Sistema de atención al cliente
- **[Ejercicio 4.2](ejercicios/modulo_4/ejercicio_4_2_analisis_datos/)**: Pipeline de análisis de documentos
- **[Ejercicio 4.3](ejercicios/modulo_4/ejercicio_4_3_investigacion/)**: Asistente de investigación empresarial
- **[Ejercicio 4.4](ejercicios/modulo_4/ejercicio_4_4_debugging/)**: 🆕 Debugging con LangSmith (Opcional)

**Documentación**:
- [📖 Aplicaciones de Negocio - Teoría Completa](docs/04_aplicaciones_negocio.md)
- [🔍 Debugging con LangSmith - Guía Completa](docs/05_debugging_langsmith.md)

## 🏗️ Estructura del Proyecto

```
micai2025/
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias Python
├── .env.example                 # Variables de entorno ejemplo
│
├── docs/                        # Documentación teórica
│   ├── 01_fundamentos.md        # ✅ Módulo 1
│   ├── 02_patrones_workflows.md # ✅ Módulo 2
│   ├── 03_agentes_autonomos.md  # ✅ Módulo 3
│   ├── 04_aplicaciones_negocio.md # ✅ Módulo 4
│   └── 05_debugging_langsmith.md  # 🆕 Debugging y Observabilidad
│
├── ejercicios/                  # Ejercicios prácticos (12 ejercicios)
│   ├── modulo_1/                # ✅ Completado
│   │   ├── ejercicio_1_1_workflow_simple/
│   │   └── ejercicio_1_2_agente_basico/
│   ├── modulo_2/                # ✅ Completado
│   │   ├── ejercicio_2_1_routing/
│   │   ├── ejercicio_2_2_parallelization/
│   │   └── ejercicio_2_3_orchestrator/
│   ├── modulo_3/                # ✅ Completado
│   │   ├── ejercicio_3_1_agente_autonomo/
│   │   ├── ejercicio_3_2_red_colaborativa/
│   │   └── ejercicio_3_3_memoria_compartida/
│   └── modulo_4/                # ✅ Completado
│       ├── ejercicio_4_1_atencion_cliente/
│       ├── ejercicio_4_2_analisis_datos/
│       ├── ejercicio_4_3_investigacion/
│       └── ejercicio_4_4_debugging/      # 🆕 Debugging con LangSmith
│
├── utils/                       # Utilidades compartidas
│   ├── __init__.py
│   ├── llm_config.py           # ✅ Configuración de LLMs
│   ├── logging_config.py       # ✅ Configuración de logs
│   └── langsmith_config.py     # 🆕 Utilidades de LangSmith
│
├── notebooks/                   # Notebooks explicativos (TODO)
└── ejemplos/                    # ✅ Ejemplos de referencia (11 ejemplos)
    ├── modulo_1_workflow_simple.py
    ├── modulo_1_agente_basico.py
    ├── modulo_2_routing.py
    ├── modulo_2_parallelization.py
    ├── modulo_2_orchestrator.py
    ├── modulo_3_plan_execute.py
    ├── modulo_3_handoffs.py
    ├── modulo_3_memoria.py
    ├── modulo_4_customer_support.py
    ├── modulo_4_document_pipeline.py
    └── debugging_langsmith.py       # 🆕 Debugging y tracing
```

## 🛠️ Stack Tecnológico

### Dependencias Principales
- `langgraph>=0.2.0` - Framework para construir grafos de agentes
- `langchain>=0.3.0` - Librería base de LangChain
- `langchain-openai>=0.2.0` - Integración con OpenAI
- `langchain-anthropic>=0.2.0` - Integración con Anthropic
- `python-dotenv>=1.0.0` - Gestión de variables de entorno

### APIs Requeridas
- **OpenAI API** (GPT-4, GPT-4o-mini) - Principal
- **Anthropic API** (Claude) - Opcional
- **Tavily API** - Opcional (para web search)
- **LangSmith API** - 🆕 Altamente recomendado (para debugging y observabilidad)

## 📝 Cómo Usar Este Tutorial

### Opción 1: Seguir en Orden (Recomendado)

1. Lee la documentación teórica del módulo en `docs/`
2. Completa los ejercicios en orden en `ejercicios/`
3. Compara tu solución con `solution.py`
4. Ejecuta los tests con `pytest tests.py`

### Opción 2: Aprendizaje Guiado

1. Lee el README del ejercicio
2. Intenta completar el código en `starter.py`
3. Si te atoras, revisa las pistas en el README
4. Como último recurso, consulta `solution.py`

### Opción 3: Estudio Independiente

1. Lee directamente `solution.py` con comentarios extensos
2. Experimenta modificando el código
3. Ejecuta y observa los resultados

## 🧪 Ejecutar Tests

```bash
# Test de un ejercicio específico
cd ejercicios/modulo_1/ejercicio_1_1_workflow_simple
pytest tests.py -v

# Tests de todos los ejercicios del módulo
pytest ejercicios/modulo_1/ -v

# Tests de todo el proyecto
pytest ejercicios/ -v
```

## 📚 Referencias y Recursos

### Documentación Oficial
- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/overview.md)
- [LangChain Documentation](https://docs.langchain.com/oss/python/langchain/overview.md)
- [LangSmith Documentation](https://docs.smith.langchain.com/) - 🆕 Debugging y observabilidad
- [OpenAI API](https://platform.openai.com/docs)
- [Anthropic API](https://docs.anthropic.com/)

### Papers Importantes
- **ReAct**: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)
- **Chain-of-Thought**: Prompting Elicits Reasoning (Wei et al., 2022)
- **Reflexion**: Language Agents with Verbal Reinforcement Learning (Shinn et al., 2023)

### Comunidad y Soporte
- [LangChain Discord](https://discord.gg/langchain)
- [GitHub Discussions](https://github.com/langchain-ai/langgraph/discussions)
- [LangChain Academy](https://docs.langchain.com/oss/python/langchain/academy.md)

## 🤝 Contribuciones

Este es un proyecto educativo para MICAI 2025. Si encuentras errores o tienes sugerencias:

1. Abre un Issue describiendo el problema
2. Si tienes una solución, crea un Pull Request
3. Asegúrate de que los tests pasen

## 📄 Licencia

MIT License - ver archivo LICENSE para detalles

## 🎓 Créditos

**Instructor**: Dr. Juan Jose Cordova Zamorano
**Institución**: DSInteg
**Conferencia**: Mexican Conference on Artificial Intelligence (MICAI) 2025
**Organización**: Sociedad Mexicana de Inteligencia Artificial

**Agradecimientos**:
- LangChain y LangGraph teams
- Comunidad de IA en México
- Participantes de MICAI 2025

---

## 📞 Contacto

Para preguntas sobre el tutorial:
- **Durante el evento**: Pregunta en el canal de Slack/Discord
- **Después del evento**: Abre un Issue en GitHub

---

## ✅ Progreso del Tutorial

- [x] **Módulo 1: Fundamentos** (100%)
  - [x] Ejercicio 1.1: Workflow Simple
  - [x] Ejercicio 1.2: Agente Básico
  - [x] Documentación teórica
  - [x] Tests
- [x] **Módulo 2: Patrones Multi-Agente** (100%)
  - [x] Ejercicio 2.1: Sistema de Routing
  - [x] Ejercicio 2.2: Paralelización
  - [x] Ejercicio 2.3: Orchestrator-Workers
  - [x] Documentación teórica
  - [x] Tests
- [x] **Módulo 3: Agentes Autónomos** (100%)
  - [x] Ejercicio 3.1: Plan-Execute-Evaluate
  - [x] Ejercicio 3.2: Red Colaborativa con Handoffs
  - [x] Ejercicio 3.3: Memoria Compartida
  - [x] Documentación teórica
  - [x] Tests
- [x] **Módulo 4: Aplicaciones de Negocio** (100%)
  - [x] Ejercicio 4.1: Sistema de Atención al Cliente
  - [x] Ejercicio 4.2: Pipeline de Análisis de Documentos
  - [x] Ejercicio 4.3: Asistente de Investigación
  - [x] Ejercicio 4.4: Debugging con LangSmith 🆕
  - [x] Documentación teórica
  - [x] Tests
- [x] **Debugging y Observabilidad** (100%) 🆕
  - [x] Documentación completa (05_debugging_langsmith.md)
  - [x] Utilidades de LangSmith (langsmith_config.py)
  - [x] Ejemplo de debugging (debugging_langsmith.py)
  - [x] Ejercicio práctico con bugs intencionales
- [x] **Ejemplos de Referencia** (100%)
  - [x] 11 ejemplos concisos (uno por concepto clave)
  - [x] Documentación de ejemplos

## 📊 Estadísticas del Tutorial

| Métrica | Cantidad |
|---------|----------|
| **Módulos** | 4 + Debugging 🆕 |
| **Ejercicios completos** | 13 (12 + 1 debugging) 🆕 |
| **Ejemplos de referencia** | 11 🆕 |
| **Líneas de código** | ~16,000 🆕 |
| **Líneas de documentación** | ~14,000 🆕 |
| **Tests** | 180+ casos 🆕 |
| **Patterns implementados** | 10+ |

**Última actualización**: 2025-01-03 (Tutorial COMPLETO + Debugging con LangSmith ✅)

---

## 🔍 Nuevo: Debugging y Observabilidad con LangSmith

Este tutorial ahora incluye una sección completa sobre debugging y observabilidad:

### ¿Qué es LangSmith?

LangSmith es la plataforma oficial de LangChain para **debugging, tracing y evaluación** de aplicaciones LLM. Te permite:

- 📊 **Ver exactamente qué está pasando** dentro de tus agentes
- 🔍 **Inspeccionar prompts y respuestas** completos
- ⚡ **Medir latencia, tokens y costos** en tiempo real
- 🐛 **Debuggear problemas** visualmente
- 📈 **Comparar versiones** de prompts y flujos
- 🚨 **Configurar alertas** para producción

### Recursos de Debugging

1. **📚 Documentación Completa**: [docs/05_debugging_langsmith.md](docs/05_debugging_langsmith.md)
   - Configuración paso a paso
   - Conceptos clave (Runs, Traces, Tags, Metadata)
   - Mejores prácticas
   - Casos de uso avanzados

2. **🔧 Utilidades**: [utils/langsmith_config.py](utils/langsmith_config.py)
   - Funciones helper para tracing
   - Decoradores para instrumentación
   - Gestión de metadata y tags
   - Logging de decisiones de agentes

3. **💡 Ejemplo Básico**: [ejemplos/debugging_langsmith.py](ejemplos/debugging_langsmith.py)
   - Sistema multi-agente con tracing
   - Demostración de todas las features
   - Casos de debugging comunes

4. **🎯 Ejercicio Práctico**: [ejercicios/modulo_4/ejercicio_4_4_debugging/](ejercicios/modulo_4/ejercicio_4_4_debugging/)
   - Sistema con bugs intencionales
   - Práctica de debugging con LangSmith
   - Optimización de performance
   - Comparación antes/después

### Por Qué LangSmith es Importante

Sin LangSmith, debuggear agentes es como programar a ciegas:
```python
# Sin LangSmith - debugging difícil
print(state)  # Solo ves variables
print(response)  # No ves el contexto
# ❌ No sabes qué prompt se envió al LLM
# ❌ No sabes por qué eligió esa herramienta
# ❌ No puedes comparar versiones fácilmente
```

Con LangSmith, tienes visibilidad completa:
```python
# Con LangSmith - debugging fácil
# ✅ Ves el prompt exacto enviado
# ✅ Ves la respuesta completa del LLM
# ✅ Ves el flujo completo del grafo
# ✅ Mides latencia y costos
# ✅ Comparas diferentes ejecuciones
```

### Cómo Empezar

1. **Crea cuenta gratuita**: https://smith.langchain.com
2. **Configura variables** en `.env`:
   ```bash
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=ls__tu_key
   LANGCHAIN_PROJECT=micai-tutorial
   ```
3. **Ejecuta cualquier ejemplo** - ¡el tracing es automático!
4. **Ve los traces** en la UI de LangSmith

**Plan gratuito**: 5,000 traces/mes - suficiente para aprender y desarrollar.

---
