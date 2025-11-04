# 🔍 Debugging y Observabilidad con LangSmith

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [¿Qué es LangSmith?](#qué-es-langsmith)
3. [Configuración Inicial](#configuración-inicial)
4. [Conceptos Clave](#conceptos-clave)
5. [Tracing Automático](#tracing-automático)
6. [Análisis de Traces](#análisis-de-traces)
7. [Debugging de Agentes](#debugging-de-agentes)
8. [Debugging de Multi-Agentes](#debugging-de-multi-agentes)
9. [Mejores Prácticas](#mejores-prácticas)
10. [Casos de Uso Avanzados](#casos-de-uso-avanzados)

---

## Introducción

En sistemas de agentes complejos, el debugging tradicional con `print()` o `logging` no es suficiente. Necesitamos:

- **Visibilidad completa** de las llamadas a LLMs
- **Trazabilidad** de decisiones y razonamiento
- **Métricas** de rendimiento y costos
- **Análisis** de comportamiento de agentes

LangSmith es la plataforma oficial de LangChain para **observabilidad, debugging y evaluación** de aplicaciones LLM.

---

## ¿Qué es LangSmith?

### Características Principales

1. **Tracing**: Captura automática de todas las ejecuciones
2. **Debugging**: Visualización de flujos de agentes
3. **Evaluación**: Testing y benchmarking de prompts
4. **Monitoreo**: Métricas en tiempo real
5. **Datasets**: Gestión de casos de prueba

### ¿Por qué LangSmith?

```python
# Sin LangSmith
print(f"Estado: {state}")  # Solo ves variables
print(f"Respuesta: {response}")  # No ves el contexto completo

# Con LangSmith
# Ves automáticamente:
# - Prompts exactos enviados al LLM
# - Respuestas completas
# - Tiempo de ejecución
# - Tokens utilizados
# - Costos por llamada
# - Flujo completo del grafo
```

---

## Configuración Inicial

### 1. Crear Cuenta en LangSmith

```bash
# Visita: https://smith.langchain.com
# 1. Crea una cuenta gratuita
# 2. Crea un proyecto (ej: "micai-tutorial")
# 3. Genera una API key
```

### 2. Configurar Variables de Entorno

```bash
# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_api_key_here
LANGCHAIN_PROJECT=micai-tutorial
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### 3. Verificar Configuración

```python
import os
from langchain_openai import ChatOpenAI

# Verificar que las variables estén configuradas
print(f"Tracing: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"Project: {os.getenv('LANGCHAIN_PROJECT')}")

# Ejecutar una llamada simple
llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke("Hello, world!")

# Si todo está configurado correctamente, verás la traza en:
# https://smith.langchain.com/o/[tu-org]/projects/p/[tu-proyecto]
```

---

## Conceptos Clave

### 1. Runs (Ejecuciones)

Cada vez que ejecutas tu código, LangSmith crea un **Run** que captura:

```python
Run {
    "id": "uuid",
    "name": "ChatOpenAI",
    "run_type": "llm",  # llm, chain, tool, retriever, etc.
    "inputs": {...},
    "outputs": {...},
    "start_time": "2025-01-15T10:00:00Z",
    "end_time": "2025-01-15T10:00:02Z",
    "latency": 2000,  # ms
    "token_usage": {"prompt": 50, "completion": 100},
    "metadata": {...}
}
```

### 2. Traces (Trazas)

Un **Trace** es un árbol de Runs que muestra la jerarquía completa:

```
Root Run: AgentExecutor
├── Run: Planning Node
│   ├── Run: ChatOpenAI (planner)
│   └── Run: OutputParser
├── Run: Tool Node
│   ├── Run: search_tool
│   └── Run: calculator_tool
└── Run: Synthesis Node
    └── Run: ChatOpenAI (synthesizer)
```

### 3. Tags y Metadata

Añade información contextual a tus traces:

```python
from langsmith import traceable

@traceable(
    run_type="chain",
    name="CustomAgent",
    tags=["production", "v1.0", "customer-support"],
    metadata={"user_id": "123", "session_id": "abc"}
)
def my_agent(input: str) -> str:
    # Tu lógica aquí
    pass
```

---

## Tracing Automático

### LangChain/LangGraph (Automático)

```python
# Solo con las variables de entorno configuradas,
# TODO el código de LangChain/LangGraph se traza automáticamente

from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_edge(START, "agent")

app = graph.compile()

# Esta ejecución se traza automáticamente
result = app.invoke({"messages": [("user", "Hello")]})
```

### Funciones Personalizadas

```python
from langsmith import traceable

@traceable(run_type="chain", name="DataProcessor")
def process_data(data: dict) -> dict:
    """
    Funciones decoradas con @traceable también se capturan
    """
    # Procesamiento
    result = transform(data)
    validate(result)
    return result

# Esta ejecución también se traza
output = process_data({"input": "test"})
```

### Context Manager

```python
from langsmith import trace

def complex_workflow():
    with trace(name="ComplexWorkflow", run_type="chain") as run_tree:
        # Todo dentro de este contexto se agrupa
        step1 = preprocess()
        step2 = analyze(step1)
        step3 = synthesize(step2)

        # Puedes añadir metadata dinámicamente
        run_tree.metadata["steps_completed"] = 3

        return step3
```

---

## Análisis de Traces

### Navegación en la UI

1. **Vista de Lista**: Todos los runs recientes
   - Filtrar por estado (success, error)
   - Buscar por inputs/outputs
   - Ordenar por latencia, tokens, costo

2. **Vista de Detalle**: Un run específico
   - Timeline de ejecución
   - Inputs/outputs exactos
   - Metadata y tags
   - Árbol de llamadas anidadas

3. **Vista de Comparación**: Múltiples runs
   - Comparar prompts
   - Comparar outputs
   - Identificar regresiones

### Métricas Clave

```python
# Métricas que LangSmith rastrea automáticamente:

1. Latencia:
   - Total: Tiempo desde inicio hasta fin
   - LLM: Tiempo solo en llamadas LLM
   - Tool: Tiempo en ejecución de herramientas

2. Tokens:
   - Prompt tokens: Entrada al LLM
   - Completion tokens: Salida del LLM
   - Total tokens: Suma

3. Costos:
   - Calculado automáticamente según precios de OpenAI
   - Desglosado por modelo

4. Errores:
   - Stack traces completos
   - Contexto de fallo
   - Estado antes del error
```

### Búsqueda Avanzada

```python
# En la UI de LangSmith, puedes buscar por:

# 1. Contenido de inputs/outputs
"error en la búsqueda"  # Busca en todos los textos

# 2. Metadata
metadata.user_id = "123"

# 3. Tags
has:tag:production

# 4. Estado
status:error

# 5. Rango de fechas
start_time > "2025-01-01"

# 6. Métricas
latency > 5000  # Más de 5 segundos
total_tokens > 10000
```

---

## Debugging de Agentes

### Caso 1: Agente No Selecciona la Herramienta Correcta

```python
# Problema: El agente siempre usa search_web en vez de query_database

# 1. Ve el trace en LangSmith
# 2. Inspecciona el prompt exacto enviado al LLM
# 3. Verás algo como:

"""
System: You are a helpful assistant.
Tools: search_web, query_database

User: What is the price of product X?
"""

# 4. Identificas el problema: faltan descripciones claras

# 5. Corriges:
@tool
def query_database(product: str) -> str:
    """
    Query the internal product database.
    Use this for: prices, inventory, product details.
    """
    pass

@tool
def search_web(query: str) -> str:
    """
    Search the internet for information.
    Use this for: external info, news, general knowledge.
    """
    pass
```

### Caso 2: Bucle Infinito

```python
# Problema: El agente entra en loop entre dos nodos

# En LangSmith verás:
# agent_node -> tool_node -> agent_node -> tool_node -> ...

# 1. Inspecciona el estado en cada iteración
# 2. Identifica qué no está cambiando
# 3. Descubres que el mensaje de error no se agrega al estado

# Corrección:
def should_continue(state: State) -> str:
    messages = state["messages"]
    last = messages[-1]

    # Añade un contador de intentos
    attempts = state.get("attempts", 0)
    if attempts > 3:
        return "end"  # Evita loops infinitos

    if last.tool_calls:
        return "continue"
    return "end"
```

### Caso 3: Output Inesperado

```python
# Problema: El agente genera formato JSON incorrecto

# 1. En LangSmith, ve la respuesta exacta del LLM:
"""
{
  "answer": "The price is $99",
  "confidence": high  # ❌ Falta comillas
}
"""

# 2. Identificas que el prompt no especifica formato estricto

# 3. Corriges con structured output:
from langchain_core.pydantic_v1 import BaseModel, Field

class Response(BaseModel):
    answer: str = Field(description="The answer to the question")
    confidence: str = Field(description="high, medium, or low")

llm_with_structure = llm.with_structured_output(Response)
```

---

## Debugging de Multi-Agentes

### Visualización de Flujos Complejos

```python
# Sistema con 4 agentes especializados
# En LangSmith verás:

Root: OrchestatorAgent
├── Run: ClassifierNode
│   └── Run: ChatOpenAI (classify intent)
│       Input: "I need help with billing"
│       Output: "billing"
│
├── Run: BillingAgent
│   ├── Run: RetrieveBillingInfo
│   │   └── Run: VectorStore.search
│   └── Run: ChatOpenAI (billing specialist)
│       Input: "User needs help with billing..."
│       Output: "Your last invoice..."
│
└── Run: ValidatorNode
    └── Run: ChatOpenAI (validator)
        Input: "Validate this response..."
        Output: "Response is appropriate"
```

### Análisis de Handoffs

```python
# Problema: Los handoffs no funcionan correctamente

# En el trace verás:
# 1. SupportAgent -> tool_call: transfer_to_technical
# 2. TechnicalAgent recibe el contexto

# Puedes inspeccionar:
# - ¿Se transfirió el contexto completo?
# - ¿El agente receptor tiene toda la información?
# - ¿Hay pérdida de información en el handoff?

# Ejemplo de trace real:
{
    "name": "transfer_to_technical",
    "inputs": {
        "reason": "User has technical issue",
        "context": {
            "user_id": "123",
            "conversation": [...],  # ✓ Historial completo
            "issue_type": "login_error"  # ✓ Metadata
        }
    },
    "outputs": {
        "agent": "technical",
        "status": "transferred"
    }
}
```

### Identificar Cuellos de Botella

```python
# En sistemas paralelos, identifica qué agente es más lento

# Timeline en LangSmith:
# 0ms ────────────────────────── 5000ms
# Agent1: [████████]              (800ms)
# Agent2: [████]                  (400ms)
# Agent3: [███████████████████]   (5000ms) ⚠️ Cuello de botella

# Soluciones:
# 1. Optimizar Agent3
# 2. Paralelizar más su trabajo
# 3. Usar modelo más rápido
# 4. Cachear resultados comunes
```

---

## Mejores Prácticas

### 1. Nombres Descriptivos

```python
# ❌ Mal
@traceable(name="node1")
def process(x):
    pass

# ✓ Bien
@traceable(name="CustomerDataEnrichment")
def enrich_customer_data(customer_id: str):
    pass
```

### 2. Tags Consistentes

```python
# Define una estrategia de tags:
TAGS = {
    "environment": ["dev", "staging", "prod"],
    "version": ["v1.0", "v1.1"],
    "agent_type": ["support", "technical", "billing"],
    "priority": ["high", "medium", "low"]
}

@traceable(tags=["prod", "v1.1", "support", "high"])
def handle_urgent_support(issue):
    pass
```

### 3. Metadata Rico

```python
@traceable(
    metadata={
        "user_id": user.id,
        "session_id": session.id,
        "feature_flags": get_flags(),
        "model_version": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 1000
    }
)
def agent_call(input):
    pass
```

### 4. Agrupar Runs Relacionados

```python
from langsmith import get_current_run_tree

def main_workflow(request_id: str):
    run_tree = get_current_run_tree()
    if run_tree:
        # Todos los runs hijos tendrán este metadata
        run_tree.metadata["request_id"] = request_id

    step1()  # Heredará request_id
    step2()  # Heredará request_id
    step3()  # Heredará request_id
```

### 5. Logging de Errores

```python
from langsmith import trace

def robust_agent_call(input: str):
    try:
        with trace(name="AgentCall", run_type="chain") as run:
            result = agent.invoke(input)
            run.metadata["status"] = "success"
            return result
    except Exception as e:
        # LangSmith captura automáticamente el error
        # Pero puedes añadir contexto adicional
        run.metadata["error_type"] = type(e).__name__
        run.metadata["recovery_attempted"] = True
        raise
```

---

## Casos de Uso Avanzados

### 1. A/B Testing de Prompts

```python
import random
from langsmith import traceable

def get_prompt_version():
    return random.choice(["v1", "v2"])

@traceable(tags=["ab-test"])
def agent_with_ab_test(input: str):
    version = get_prompt_version()

    prompts = {
        "v1": "You are a helpful assistant. Answer concisely.",
        "v2": "You are an expert assistant. Provide detailed answers."
    }

    # El tag permite filtrar y comparar resultados
    with trace(tags=[f"prompt-{version}"]) as run:
        run.metadata["prompt_version"] = version
        llm = ChatOpenAI(model="gpt-4o-mini")
        response = llm.invoke(prompts[version] + f"\n\n{input}")
        return response

# Después en LangSmith:
# 1. Filtra por tag:prompt-v1 vs tag:prompt-v2
# 2. Compara métricas: latencia, tokens, calidad
# 3. Decide qué versión es mejor
```

### 2. Monitoreo de Producción

```python
from langsmith import Client

client = Client()

# Crea alertas automáticas
def check_production_health():
    # Obtiene runs de las últimas 24 horas
    runs = client.list_runs(
        project_name="micai-tutorial",
        start_time=datetime.now() - timedelta(days=1),
        filter='tags:"production"'
    )

    error_rate = sum(1 for r in runs if r.error) / len(runs)
    avg_latency = sum(r.latency for r in runs) / len(runs)

    if error_rate > 0.05:  # 5% error rate
        alert_team(f"High error rate: {error_rate:.2%}")

    if avg_latency > 5000:  # 5 segundos
        alert_team(f"High latency: {avg_latency}ms")
```

### 3. Datasets para Testing

```python
from langsmith import Client

client = Client()

# Crea un dataset de casos de prueba
dataset_name = "customer_support_tests"

# Añade ejemplos
examples = [
    {
        "inputs": {"question": "What is my account balance?"},
        "outputs": {"expected_intent": "billing"}
    },
    {
        "inputs": {"question": "How do I reset my password?"},
        "outputs": {"expected_intent": "technical"}
    }
]

dataset = client.create_dataset(dataset_name)
for example in examples:
    client.create_example(
        inputs=example["inputs"],
        outputs=example["outputs"],
        dataset_id=dataset.id
    )

# Evalúa tu agente contra el dataset
def evaluate_agent():
    results = client.run_on_dataset(
        dataset_name=dataset_name,
        llm_or_chain_factory=lambda: my_agent,
        evaluation=evaluate_intent_classification
    )
    return results
```

### 4. Debugging con Feedback

```python
from langsmith import Client

client = Client()

# Durante la ejecución, guarda el run_id
run_id = None

def my_agent(input: str):
    global run_id
    run_tree = get_current_run_tree()
    if run_tree:
        run_id = run_tree.id

    return agent.invoke(input)

# Si el usuario reporta un problema, añade feedback
def report_issue(issue_description: str):
    if run_id:
        client.create_feedback(
            run_id=run_id,
            key="user_feedback",
            score=0,  # 0 = malo, 1 = bueno
            comment=issue_description
        )

# Luego en LangSmith:
# Filtra runs con feedback negativo
# Analiza patrones comunes
# Identifica problemas recurrentes
```

### 5. Custom Evaluators

```python
from langsmith.evaluation import evaluate

def accuracy_evaluator(run, example):
    """
    Evalúa si la respuesta es correcta
    """
    predicted = run.outputs["answer"]
    expected = example.outputs["expected"]

    return {
        "key": "accuracy",
        "score": int(predicted == expected)
    }

def latency_evaluator(run, example):
    """
    Evalúa si la latencia es aceptable
    """
    latency_ms = run.latency
    threshold_ms = 3000

    return {
        "key": "latency_acceptable",
        "score": int(latency_ms < threshold_ms),
        "comment": f"{latency_ms}ms (threshold: {threshold_ms}ms)"
    }

# Ejecuta evaluación
results = evaluate(
    lambda inputs: my_agent(inputs["question"]),
    data=dataset_name,
    evaluators=[accuracy_evaluator, latency_evaluator],
    experiment_prefix="support-agent-v1"
)
```

---

## Resumen

### Checklist de Debugging

- [ ] **Configuración**
  - Variables de entorno correctas
  - Proyecto en LangSmith creado
  - Tracing funcionando

- [ ] **Durante Desarrollo**
  - Nombres descriptivos en todos los nodos
  - Tags apropiados (dev, feature-name)
  - Metadata relevante (version, user-id)

- [ ] **Debugging Activo**
  - Revisar traces en tiempo real
  - Inspeccionar prompts exactos
  - Analizar flujo de estado
  - Verificar costos y tokens

- [ ] **Pre-Producción**
  - Crear dataset de test cases
  - Ejecutar evaluaciones
  - Comparar versiones (A/B)
  - Establecer baselines de métricas

- [ ] **Producción**
  - Tags de producción consistentes
  - Alertas configuradas
  - Monitoreo de métricas
  - Feedback loop activo

### Recursos Adicionales

- **Documentación Oficial**: https://docs.smith.langchain.com/
- **Ejemplos**: https://github.com/langchain-ai/langsmith-cookbook
- **Pricing**: https://www.langchain.com/pricing (Free tier disponible)

### Próximos Pasos

1. **Configura tu cuenta** en smith.langchain.com
2. **Ejecuta el ejemplo** `ejemplos/debugging_langsmith.py`
3. **Practica con el ejercicio** `ejercicios/modulo_4/ejercicio_4_4_debugging/`
4. **Experimenta** agregando tracing a tus propios agentes

---

**📝 Nota**: LangSmith es una herramienta poderosa pero opcional. Todos los ejercicios funcionan sin ella, pero te recomendamos fuertemente usarla para entender profundamente cómo funcionan tus agentes.
