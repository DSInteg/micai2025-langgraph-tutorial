# Ejercicio 4.4: Debugging y Observabilidad con LangSmith

## Objetivos

En este ejercicio aprenderás a:

1. ✅ Configurar LangSmith para tracing de agentes
2. ✅ Debuggear sistemas multi-agente complejos
3. ✅ Identificar y resolver problemas de rendimiento
4. ✅ Analizar decisiones y comportamiento de agentes
5. ✅ Optimizar costos y latencia usando métricas

## Contexto

Tienes un sistema de análisis de documentos multi-agente que presenta varios problemas:

- **Problema 1**: A veces selecciona herramientas incorrectas
- **Problema 2**: Ocasionalmente entra en bucles infinitos
- **Problema 3**: La latencia es muy alta en algunos casos
- **Problema 4**: Los costos son más altos de lo esperado

Tu tarea es usar LangSmith para identificar y resolver estos problemas.

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    Document Analyzer                     │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Classifier  │   │   Extractor  │   │  Summarizer  │
│              │   │              │   │              │
│ - PDF?       │   │ - Extract    │   │ - Summarize  │
│ - Text?      │   │ - Parse      │   │ - Analyze    │
│ - Image?     │   │ - Structure  │   │ - Report     │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Validator   │
                    └──────────────┘
```

## Parte 1: Configuración de LangSmith (15 min)

### Paso 1.1: Crear Cuenta y Proyecto

1. Ve a https://smith.langchain.com
2. Crea una cuenta gratuita
3. Crea un proyecto llamado "micai-debugging-exercise"
4. Genera una API key

### Paso 1.2: Configurar Variables de Entorno

```bash
# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__tu_api_key_aqui
LANGCHAIN_PROJECT=micai-debugging-exercise
```

### Paso 1.3: Verificar Configuración

Ejecuta el código de verificación en `starter.py` para confirmar que LangSmith está funcionando.

## Parte 2: Implementar Sistema con Bugs Intencionales (30 min)

### Tarea 2.1: Implementar Classifier Node

Implementa un nodo clasificador que categoriza documentos pero con un bug:

- ❌ **Bug intencional**: Las descripciones de herramientas son ambiguas
- 🎯 **Objetivo**: LangSmith mostrará que el LLM se confunde al elegir

```python
# TODO: Implementa classifier_node con descripciones ambiguas de herramientas
def classifier_node(state: DocumentState) -> DocumentState:
    """
    Clasifica el tipo de documento.

    Bug intencional: descripciones de tools poco claras
    """
    pass
```

### Tarea 2.2: Implementar Processing Loop

Implementa un loop de procesamiento con un bug:

- ❌ **Bug intencional**: No hay límite de iteraciones
- 🎯 **Objetivo**: LangSmith mostrará el bucle infinito en el trace

```python
# TODO: Implementa should_continue sin protección contra loops
def should_continue(state: DocumentState) -> str:
    """
    Decide si continuar procesando.

    Bug intencional: puede causar loop infinito
    """
    pass
```

### Tarea 2.3: Implementar Extractor Node

Implementa extracción con un bug de rendimiento:

- ❌ **Bug intencional**: Hace llamadas redundantes al LLM
- 🎯 **Objetivo**: LangSmith mostrará múltiples llamadas innecesarias

```python
# TODO: Implementa extractor_node con llamadas redundantes
def extractor_node(state: DocumentState) -> DocumentState:
    """
    Extrae información del documento.

    Bug intencional: múltiples llamadas redundantes
    """
    pass
```

## Parte 3: Debugging con LangSmith (45 min)

### Tarea 3.1: Identificar Problema de Selección de Herramientas

1. Ejecuta el sistema con diferentes tipos de documentos
2. Ve a LangSmith y observa los traces
3. Encuentra el nodo donde se selecciona la herramienta incorrecta
4. Inspecciona el prompt exacto enviado al LLM
5. Identifica por qué las descripciones son confusas

**Pistas**:
- Busca en el trace el nodo "Classifier"
- Inspecciona la sección "Inputs" para ver el prompt completo
- Compara las descripciones de las herramientas
- Fíjate en qué herramienta eligió vs cuál debería haber elegido

**Pregunta**: ¿Qué cambiarías en las descripciones de herramientas?

### Tarea 3.2: Detectar y Resolver Bucle Infinito

1. Ejecuta con un documento que cause loop
2. Observa en LangSmith el patrón de repetición
3. Cuenta cuántas iteraciones ocurren
4. Identifica qué no está cambiando en el estado
5. Añade protección contra loops

**Pistas**:
- En el trace verás: node_a -> node_b -> node_a -> node_b...
- Inspecciona el estado en cada iteración
- Busca qué variable debería cambiar pero no lo hace
- Añade un contador de intentos al estado

**Pregunta**: ¿En qué iteración deberías cortar el loop?

### Tarea 3.3: Optimizar Llamadas al LLM

1. Analiza las métricas de latencia en LangSmith
2. Identifica nodos con múltiples llamadas al LLM
3. Encuentra llamadas redundantes o duplicadas
4. Refactoriza para minimizar llamadas

**Pistas**:
- Ordena runs por "Total Tokens" descendente
- Expande el trace y cuenta llamadas LLM en cada nodo
- Busca patrones donde se llama al LLM con el mismo prompt
- Considera cachear resultados o combinar prompts

**Pregunta**: ¿Cuántas llamadas eliminaste? ¿Cuánto ahorraste en tokens?

### Tarea 3.4: Analizar Costos y Optimizar

1. Ve a la vista de métricas en LangSmith
2. Identifica el componente más costoso
3. Analiza si el costo está justificado
4. Experimenta con modelos más baratos donde sea apropiado

**Pistas**:
- Compara costo de gpt-4o-mini vs gpt-4o
- Identifica tareas simples que no necesitan el modelo más potente
- Considera usar gpt-3.5-turbo para clasificación simple
- Mantén modelos más potentes solo para tareas complejas

**Pregunta**: ¿Qué porcentaje del costo puedes reducir?

## Parte 4: Instrumentación Avanzada (30 min)

### Tarea 4.1: Añadir Metadata Rico

Implementa metadata que ayude al debugging futuro:

```python
from utils.langsmith_config import add_run_metadata

def classifier_node(state: DocumentState) -> DocumentState:
    # TODO: Añade metadata útil
    add_run_metadata({
        "document_type": "???",
        "document_size": "???",
        "confidence": "???"
    })
    pass
```

### Tarea 4.2: Logging de Decisiones

Documenta las decisiones importantes del agente:

```python
from utils.langsmith_config import log_agent_decision

# TODO: Registra decisiones con razonamiento
log_agent_decision(
    agent_name="Classifier",
    decision="???",
    reasoning="???",
    confidence=???
)
```

### Tarea 4.3: Secciones de Trace

Organiza el trace en secciones lógicas:

```python
from utils.langsmith_config import trace_section

# TODO: Usa trace_section para agrupar operaciones relacionadas
with trace_section("DocumentParsing", tags=["io", "parsing"]):
    # Operaciones de parsing
    pass

with trace_section("ContentAnalysis", tags=["llm", "analysis"]):
    # Análisis con LLM
    pass
```

## Parte 5: Testing y Validación (20 min)

### Tarea 5.1: Crear Dataset de Test

Crea casos de prueba en LangSmith:

```python
# TODO: Crea dataset con diferentes tipos de documentos
test_cases = [
    {"input": "documento.pdf", "expected_type": "pdf"},
    {"input": "imagen.png", "expected_type": "image"},
    {"input": "texto.txt", "expected_type": "text"}
]
```

### Tarea 5.2: Implementar Tests

```python
# TODO: Implementa tests que usen LangSmith para validación
def test_classifier_accuracy():
    """Verifica que el clasificador funciona correctamente."""
    pass

def test_no_infinite_loops():
    """Verifica que no hay bucles infinitos."""
    pass

def test_performance_acceptable():
    """Verifica que la latencia es aceptable."""
    pass
```

## Criterios de Éxito

Tu solución debe:

- [ ] **Funcionalidad**
  - Sistema completo funciona sin bugs
  - Clasificación correcta de documentos
  - Extracción exitosa de información
  - Validación apropiada de resultados

- [ ] **Debugging**
  - Identificados y documentados todos los bugs
  - Resueltos los 3 problemas principales
  - Evidencia en LangSmith del antes/después

- [ ] **Observabilidad**
  - Metadata rica en todos los nodos
  - Logging de decisiones importantes
  - Tags y nombres descriptivos
  - Traces bien organizados

- [ ] **Performance**
  - Latencia reducida al menos 30%
  - Llamadas LLM optimizadas
  - Costos reducidos significativamente
  - No hay loops infinitos

- [ ] **Testing**
  - Tests implementados y pasando
  - Dataset de casos de prueba creado
  - Métricas baseline establecidas

## Entregables

1. **Código**:
   - `solution.py` con sistema corregido
   - `tests.py` con tests comprehensivos
   - Documentación de bugs encontrados

2. **Análisis en LangSmith**:
   - Screenshots del trace con bugs
   - Screenshots del trace corregido
   - Comparación de métricas antes/después

3. **Reporte**:
   - Lista de bugs encontrados y cómo se resolvieron
   - Métricas de mejora (latencia, tokens, costo)
   - Lecciones aprendidas

## Recursos

- **Documentación**: [`docs/05_debugging_langsmith.md`](../../../docs/05_debugging_langsmith.md)
- **Ejemplo**: [`ejemplos/debugging_langsmith.py`](../../../ejemplos/debugging_langsmith.py)
- **Utilidades**: [`utils/langsmith_config.py`](../../../utils/langsmith_config.py)
- **LangSmith Docs**: https://docs.smith.langchain.com/

## Preguntas para Reflexión

1. **Antes de LangSmith**:
   - ¿Cómo habrías debuggeado estos problemas sin LangSmith?
   - ¿Cuánto tiempo te habría tomado encontrar el bug de loop infinito?

2. **Con LangSmith**:
   - ¿Qué información fue más útil del trace?
   - ¿Qué métricas fueron más sorprendentes?

3. **Producción**:
   - ¿Qué alertas configurarías?
   - ¿Cómo monitorearías la salud del sistema?
   - ¿Qué SLOs (Service Level Objectives) establecerías?

4. **Optimización**:
   - ¿Hay trade-offs entre calidad y costo?
   - ¿Dónde vale la pena usar modelos más potentes?
   - ¿Qué más podrías optimizar?

## Bonus (Opcional)

Si terminas temprano, intenta:

1. **A/B Testing**: Implementa dos versiones del classifier y compara en LangSmith
2. **Feedback Loop**: Añade un sistema para capturar feedback de usuarios
3. **Custom Evaluators**: Crea evaluadores personalizados para métricas específicas
4. **Dashboard**: Exporta métricas y crea un dashboard simple
5. **Alerting**: Implementa alertas automáticas para anomalías

## Tiempo Estimado

- ⏱️ Configuración: 15 min
- ⏱️ Implementación: 30 min
- ⏱️ Debugging: 45 min
- ⏱️ Instrumentación: 30 min
- ⏱️ Testing: 20 min
- **Total: ~2.5 horas**

---

¡Buena suerte! Recuerda: el debugging efectivo es una habilidad crítica para sistemas de producción. LangSmith es tu mejor aliado. 🔍
