# Módulo 3: Redes de Agentes Autónomos

## 📖 Índice

1. [Introducción a Agentes Autónomos](#introducción)
2. [Plan-Execute-Evaluate Pattern](#plan-execute-evaluate)
3. [Red Colaborativa con Handoffs](#handoffs)
4. [Memoria Compartida](#memoria-compartida)
5. [Comparación de Patterns](#comparación)
6. [Mejores Prácticas](#mejores-prácticas)
7. [Casos de Uso](#casos-de-uso)

---

## 🎯 Introducción a Agentes Autónomos {#introducción}

### ¿Qué es un Agente Autónomo?

Un **agente autónomo** es un sistema que puede:
- Tomar decisiones sin supervisión constante
- Adaptarse dinámicamente a nuevas situaciones
- Planificar secuencias de acciones
- Aprender de experiencias pasadas
- Colaborar con otros agentes

### Diferencia: Agente Simple vs Autónomo

**Agente Simple (Módulo 1.2 - ReAct):**
```python
# Ciclo simple: Pensar → Actuar → Repetir
while not finished:
    thought = think(observation)
    action = decide_action(thought)
    observation = execute(action)
```

**Agente Autónomo (Módulo 3):**
```python
# Planificación explícita + Adaptación dinámica
plan = create_plan(objective)
while not finished:
    step = execute_next_step(plan)
    evaluation = evaluate_progress(step, plan, objective)
    if evaluation == "REPLAN":
        plan = create_new_plan(observations, objective)
    elif evaluation == "CONTINUE":
        continue
    else:  # FINISH
        break
```

### Características de Agentes Autónomos

| Característica | Agente Simple | Agente Autónomo |
|---|---|---|
| **Planificación** | Implícita (paso a paso) | Explícita (plan completo) |
| **Adaptación** | Limitada | Dinámica (puede replanificar) |
| **Visibilidad** | Baja (caja negra) | Alta (plan visible) |
| **Colaboración** | No | Sí (múltiples agentes) |
| **Memoria** | Corto plazo | Largo plazo (persistente) |
| **Optimización** | No | Sí (puede optimizar plan) |

---

## 📋 Plan-Execute-Evaluate Pattern {#plan-execute-evaluate}

### Concepto

El pattern **Plan-Execute-Evaluate** separa tres responsabilidades:

1. **PLAN**: Crear un plan explícito de acción
2. **EXECUTE**: Ejecutar un paso del plan
3. **EVALUATE**: Evaluar progreso y decidir siguiente acción

### Arquitectura

```
┌─────────────┐
│   PLANNER   │ ← Crea plan explícito
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  EXECUTOR   │ ← Ejecuta un paso
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  EVALUATOR  │ ← Decide: CONTINUE, REPLAN, FINISH
└──────┬──────┘
       │
       ↓
  [Decision]
       ├─→ CONTINUE ──→ (back to EXECUTOR)
       ├─→ REPLAN ───→ (back to PLANNER)
       └─→ FINISH ───→ END
```

### Ventajas

✅ **Visibilidad del Plan**: Puedes ver qué hará el agente antes de ejecutar
✅ **Depuración Fácil**: Si algo falla, sabes en qué paso
✅ **Optimización**: El plan puede optimizarse antes de ejecutar
✅ **Adaptación**: Puede replanificar si algo sale mal
✅ **Validación**: Puedes validar el plan antes de ejecutar

### Cuándo Usar

Usa este pattern cuando:
- La tarea tiene múltiples pasos interdependientes
- Necesitas visibilidad del proceso completo
- El plan debe ser validado antes de ejecutar
- La adaptación dinámica es importante
- Quieres optimizar antes de actuar

### Ejemplo de Implementación

```python
class PlanExecuteState(TypedDict):
    objective: str
    plan: str
    current_step: int
    observations: List[Dict]
    decision: str
    final_response: str

def planner_node(state: PlanExecuteState) -> dict:
    """Crea plan explícito."""
    objective = state["objective"]

    prompt = f"""Crea un plan detallado para: {objective}

    Requisitos:
    1. Pasos numerados
    2. Herramientas a usar en cada paso
    3. Orden lógico

    PLAN:"""

    plan = llm.invoke(prompt).content

    return {
        "plan": plan,
        "current_step": 0,
        "observations": []
    }

def executor_node(state: PlanExecuteState) -> dict:
    """Ejecuta un paso del plan."""
    plan = state["plan"]
    current_step = state["current_step"]

    # Extraer pasos
    steps = extract_steps(plan)

    if current_step >= len(steps):
        return {"current_step": current_step}

    step_to_execute = steps[current_step]

    # Ejecutar con herramientas
    result = execute_with_tools(step_to_execute)

    observation = {
        "step": current_step,
        "action": step_to_execute,
        "result": result
    }

    observations = state["observations"] + [observation]

    return {
        "observations": observations,
        "current_step": current_step + 1
    }

def evaluator_node(state: PlanExecuteState) -> dict:
    """Evalúa progreso y decide siguiente acción."""
    objective = state["objective"]
    plan = state["plan"]
    observations = state["observations"]

    prompt = f"""Evalúa el progreso:

    OBJETIVO: {objective}
    PLAN: {plan}
    PASOS EJECUTADOS: {observations}

    Decisión:
    - CONTINUE: Si el plan funciona y hay más pasos
    - REPLAN: Si el plan no funciona
    - FINISH: Si el objetivo está completado

    DECISIÓN:"""

    decision = llm.invoke(prompt).content.strip().upper()

    return {"decision": decision}

def build_graph():
    workflow = StateGraph(PlanExecuteState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("finish", finish_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "evaluator")

    # Routing condicional crea ciclos
    workflow.add_conditional_edges(
        "evaluator",
        route_decision,
        {
            "executor": "executor",  # CONTINUE
            "planner": "planner",    # REPLAN
            "finish": "finish"       # FINISH
        }
    )

    workflow.add_edge("finish", END)

    return workflow.compile()
```

### Comparación con ReAct

| Aspecto | ReAct (Módulo 1.2) | Plan-Execute-Evaluate |
|---|---|---|
| **Planificación** | Implícita | Explícita |
| **Pasos** | Uno a la vez | Plan completo primero |
| **Visibilidad** | Baja | Alta (plan visible) |
| **Adaptación** | Paso a paso | Puede replanificar todo |
| **Debugging** | Difícil | Fácil (plan explícito) |
| **Overhead** | Bajo | Medio (crear plan) |
| **Optimización** | No | Sí (optimizar plan) |

---

## 🤝 Red Colaborativa con Handoffs {#handoffs}

### Concepto

Una **red colaborativa con handoffs** permite que múltiples agentes especializados trabajen juntos pasándose el control dinámicamente.

### ¿Qué es un Handoff?

Un **handoff** es una transferencia de control de un agente a otro, junto con contexto completo.

```
Agente A: "He analizado el código, pero veo un problema de seguridad.
           Paso el control a Security Agent con mi análisis."

           [HANDOFF A → Security Agent]

Security Agent: "He validado la vulnerabilidad. Es grave.
                 Paso el control a Code Agent para que implemente fix."

                 [HANDOFF Security → Code Agent]

Code Agent: "He implementado el fix. Problema resuelto."
```

### Diferencia con Otros Patterns

**Routing (Módulo 2.1):**
```
Classifier → [Decide UNO] → Specialist → END
```
- Un clasificador decide QUÉ agente
- Solo UN agente ejecuta
- No hay transferencias dinámicas

**Parallelization (Módulo 2.2):**
```
Broadcast → [Specialist A, Specialist B, Specialist C] → Aggregator
```
- TODOS los agentes ejecutan
- Ejecutan en paralelo sobre lo mismo
- No hay transferencias secuenciales

**Orchestrator-Workers (Módulo 2.3):**
```
Orchestrator → [Divide] → [Worker A, Worker B, Worker C] → [Aggregate] → END
```
- Orquestador divide y asigna
- Workers ejecutan en paralelo
- No hay handoffs entre workers

**Handoffs (este módulo):**
```
Triage → Specialist A → [Needs help?] → Specialist B → [Can finish?] → Final
                ↓                              ↓
            [Solved?]                      [Needs C?]
                ↓                              ↓
             Final                      Specialist C
```
- Agentes se pasan control dinámicamente
- Secuencia no predefinida
- Cada agente decide siguiente paso
- Contexto se comparte

### Arquitectura de Handoffs

```python
class CollaborativeState(TypedDict):
    query: str
    current_agent: str              # Quién tiene el control
    conversation_history: List[Dict]  # Historial de handoffs
    specialist_reports: Dict[str, str]  # Reportes acumulados
    handoff_reason: str            # Por qué se hizo handoff
    final_response: str

def specialist_agent(state: CollaborativeState) -> dict:
    """Agente especialista que puede hacer handoff."""

    # 1. Hacer su análisis
    my_analysis = analyze_from_my_expertise(state["query"])

    # 2. Decidir si necesita ayuda
    prompt = f"""Has analizado: {my_analysis}

    ¿Necesitas ayuda de otro especialista?
    - FINAL: Si puedes terminar
    - CODE: Si necesitas expertise en código
    - NETWORK: Si necesitas expertise en redes
    - SECURITY: Si necesitas expertise en seguridad

    DECISIÓN:"""

    decision = llm.invoke(prompt).content.strip().upper()

    # 3. Preparar handoff
    next_agent = decision_to_agent_map[decision]

    # 4. Actualizar contexto compartido
    reports = state["specialist_reports"].copy()
    reports["my_specialty"] = my_analysis

    history = state["conversation_history"] + [{
        "agent": "my_specialty",
        "handoff_to": next_agent,
        "reason": f"Completed analysis, {'ready to finish' if decision == 'FINAL' else f'need {decision} expertise'}"
    }]

    return {
        "current_agent": next_agent,
        "specialist_reports": reports,
        "conversation_history": history
    }
```

### Ventajas de Handoffs

✅ **Expertise Especializado**: Cada agente tiene su dominio
✅ **Colaboración Dinámica**: El flujo se adapta al problema
✅ **Contexto Compartido**: Todos ven lo que hicieron los demás
✅ **Escalabilidad**: Fácil agregar nuevos especialistas
✅ **Debugging**: El historial muestra todo el flujo

### Cuándo Usar

Usa handoffs cuando:
- El problema requiere múltiples expertises
- No sabes de antemano qué secuencia de agentes necesitas
- Los agentes deben ver el trabajo de los anteriores
- La complejidad emerge durante el análisis
- Quieres colaboración dinámica

### Ejemplo de Flujo Real

**Query**: "Mi app no conecta a la BD. Hay error de autenticación y el firewall podría bloquear el puerto."

```
🎯 TRIAGE
   → Clasifica como NETWORK (menciona firewall)
   → Handoff a NETWORK AGENT

🔧 NETWORK AGENT
   → Analiza: "Puerto 5432 bloqueado por firewall"
   → Detecta: También hay mención de autenticación
   → Handoff a SECURITY AGENT (necesita validar auth)

🔒 SECURITY AGENT
   → Analiza: "Credenciales incorrectas en config"
   → Detecta: El error viene del código de conexión
   → Handoff a CODE AGENT (necesita ver código)

💻 CODE AGENT
   → Analiza: "String de conexión malformado en db.py"
   → Con contexto de network + security, tiene solución completa
   → Handoff a FINAL

✅ FINAL AGENT
   → Sintetiza reportes de network, security y code
   → Genera respuesta integrada con 3 dimensiones del problema
```

---

## 🧠 Memoria Compartida {#memoria-compartida}

### Concepto

La **memoria compartida** permite que los agentes:
- Aprendan de experiencias pasadas
- Reutilicen soluciones exitosas
- Mejoren con el tiempo
- Compartan conocimiento entre sesiones

### Tipos de Memoria

#### 1. Short-Term Memory (Memoria de Corto Plazo)

**Características:**
- Solo durante una sesión
- Se pierde al terminar
- En el estado del grafo

**Ejemplo:**
```python
class State(TypedDict):
    messages: List[BaseMessage]  # Memoria de corto plazo
    current_context: str
```

**Uso:**
- Contexto inmediato de conversación
- Pasos ejecutados en la sesión actual
- Decisiones tomadas recientemente

#### 2. Long-Term Memory (Memoria de Largo Plazo)

**Características:**
- Persiste entre sesiones
- Crece con el tiempo
- Almacenada externamente (DB, vector store)

**Ejemplo:**
```python
class MemoryState(TypedDict):
    query: str
    similar_cases: List[Dict]  # Recuperados de memoria persistente
    memory: Dict               # Referencia a almacenamiento persistente
```

**Uso:**
- Casos resueltos previamente
- Patrones detectados
- Perfiles de usuario
- Soluciones exitosas

### Arquitectura de Memoria Compartida

```
┌───────────────────────────────────────┐
│     MEMORIA PERSISTENTE               │
│  (Vector DB / SQL / Cache)            │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │ Cases:                          │ │
│  │  - case_001: "DB error" → sol   │ │
│  │  - case_002: "Auth fail" → sol  │ │
│  │  - case_003: "Port block" → sol │ │
│  └─────────────────────────────────┘ │
└───────────────────────────────────────┘
         ↑                    ↑
         │ READ               │ WRITE
         ↓                    ↓
┌─────────────┐      ┌─────────────┐
│   Memory    │      │   Update    │
│   Agent     │      │   Memory    │
│             │      │   Agent     │
│ - Search    │      │ - Save      │
│ - Retrieve  │      │ - Index     │
└─────────────┘      └─────────────┘
         │                    ↑
         ↓                    │
┌─────────────────────────────┴─────┐
│      Solution Agent                │
│                                    │
│  Uses similar cases as context    │
│  Generates adapted solution       │
└────────────────────────────────────┘
```

### Operaciones de Memoria

#### 1. Búsqueda (Retrieval)

**Búsqueda Simple (Keywords):**
```python
def search_simple(query: str, memory: Dict) -> List[Dict]:
    query_words = set(query.lower().split())

    results = []
    for case in memory["cases"]:
        case_words = set(case["query"].lower().split())
        overlap = len(query_words & case_words)
        if overlap > 0:
            results.append((overlap, case))

    results.sort(reverse=True, key=lambda x: x[0])
    return [case for score, case in results[:top_k]]
```

**Búsqueda Semántica (Embeddings):**
```python
def search_semantic(query: str, vector_db) -> List[Dict]:
    # 1. Generar embedding de la query
    query_embedding = embeddings.embed_query(query)

    # 2. Búsqueda de similaridad en vector DB
    similar_docs = vector_db.similarity_search_by_vector(
        query_embedding,
        k=5,
        filter={"category": "technical_support"}
    )

    return similar_docs
```

#### 2. Almacenamiento (Storage)

```python
def save_to_memory(case: Dict, memory_store):
    """
    Guarda un caso en memoria persistente.
    """
    # 1. Generar embedding si usas vector DB
    if isinstance(memory_store, VectorStore):
        embedding = embeddings.embed_query(case["query"])
        case["embedding"] = embedding

    # 2. Agregar metadata
    case["timestamp"] = datetime.now().isoformat()
    case["tags"] = extract_tags(case["query"])

    # 3. Guardar
    memory_store.add(case)

    # 4. Indexar si es necesario
    memory_store.index()
```

#### 3. Actualización (Update)

```python
def update_case_stats(case_id: str, success: bool, memory_store):
    """
    Actualiza estadísticas de un caso.
    """
    case = memory_store.get(case_id)

    if success:
        case["success_count"] += 1
    else:
        case["failure_count"] += 1

    case["last_used"] = datetime.now().isoformat()

    memory_store.update(case_id, case)
```

### Implementación con Vector Databases

**Usando ChromaDB:**
```python
import chromadb
from chromadb.config import Settings

# 1. Inicializar cliente
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./memory_db"
))

# 2. Crear o obtener colección
collection = client.get_or_create_collection(
    name="support_cases",
    metadata={"description": "Technical support cases"}
)

# 3. Agregar casos
collection.add(
    documents=[case["query"] for case in cases],
    metadatas=[case["metadata"] for case in cases],
    ids=[case["id"] for case in cases]
)

# 4. Buscar casos similares
results = collection.query(
    query_texts=["Database connection error"],
    n_results=5
)
```

**Usando LangChain + Pinecone:**
```python
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone

# 1. Inicializar Pinecone
pinecone.init(api_key="...", environment="...")

# 2. Crear index
index = pinecone.Index("support-cases")

# 3. Crear vector store
embeddings = OpenAIEmbeddings()
vectorstore = Pinecone(index, embeddings, "text")

# 4. Agregar casos
vectorstore.add_texts(
    texts=[case["query"] for case in cases],
    metadatas=[case["metadata"] for case in cases]
)

# 5. Buscar similares
similar_docs = vectorstore.similarity_search(
    "Database connection error",
    k=5
)
```

### Estructura de un Caso en Memoria

```python
case = {
    # Identificación
    "id": "case_001",
    "timestamp": "2024-01-15T10:30:00Z",

    # Contenido
    "query": "No puedo conectarme a PostgreSQL",
    "solution": "1. Verificar firewall...",

    # Metadata
    "user_id": "user_123",
    "category": "database",
    "tags": ["database", "postgresql", "connection"],
    "priority": "high",

    # Estadísticas
    "success_count": 5,
    "failure_count": 0,
    "avg_resolution_time": 120,  # segundos
    "last_used": "2024-01-20T14:00:00Z",

    # Para búsqueda semántica
    "embedding": [0.1, 0.2, ...],  # Vector de 1536 dimensiones

    # Relaciones
    "related_cases": ["case_002", "case_015"],
    "supersedes": "case_000"  # Caso antiguo que este reemplaza
}
```

### Strategies de Memory Management

#### 1. Memory Pruning (Limpieza)

Eliminar casos obsoletos o de baja utilidad:

```python
def prune_memory(memory_store, strategy="low_success"):
    """
    Limpia la memoria según estrategia.
    """
    if strategy == "low_success":
        # Eliminar casos con baja tasa de éxito
        for case in memory_store.get_all():
            if case["success_count"] < 2 and case["failure_count"] > 5:
                memory_store.delete(case["id"])

    elif strategy == "old_unused":
        # Eliminar casos viejos no usados
        cutoff = datetime.now() - timedelta(days=90)
        for case in memory_store.get_all():
            last_used = datetime.fromisoformat(case["last_used"])
            if last_used < cutoff:
                memory_store.delete(case["id"])

    elif strategy == "duplicate":
        # Eliminar duplicados (alta similitud)
        cases = memory_store.get_all()
        for i, case1 in enumerate(cases):
            for case2 in cases[i+1:]:
                similarity = compute_similarity(case1, case2)
                if similarity > 0.95:
                    # Mantener el más exitoso
                    if case1["success_count"] >= case2["success_count"]:
                        memory_store.delete(case2["id"])
                    else:
                        memory_store.delete(case1["id"])
```

#### 2. Case Consolidation (Consolidación)

Fusionar casos similares:

```python
def consolidate_cases(memory_store, threshold=0.9):
    """
    Fusiona casos muy similares en uno solo.
    """
    cases = memory_store.get_all()
    clusters = cluster_similar_cases(cases, threshold)

    for cluster in clusters:
        if len(cluster) > 1:
            # Crear caso consolidado
            consolidated = {
                "id": f"consolidated_{uuid4()}",
                "query": most_common_query(cluster),
                "solution": best_solution(cluster),
                "success_count": sum(c["success_count"] for c in cluster),
                "variants": [c["query"] for c in cluster]
            }

            # Guardar consolidado
            memory_store.add(consolidated)

            # Eliminar originales
            for case in cluster:
                memory_store.delete(case["id"])
```

#### 3. Adaptive Learning (Aprendizaje Adaptativo)

Actualizar casos según feedback:

```python
def update_with_feedback(case_id: str, worked: bool, user_feedback: str, memory_store):
    """
    Actualiza caso con feedback del usuario.
    """
    case = memory_store.get(case_id)

    if worked:
        case["success_count"] += 1
        case["confidence_score"] += 0.1
    else:
        case["failure_count"] += 1
        case["confidence_score"] -= 0.05

        # Si falla mucho, marcar para revisión
        if case["failure_count"] > 3:
            case["needs_review"] = True

    # Agregar feedback
    if "feedback" not in case:
        case["feedback"] = []
    case["feedback"].append({
        "timestamp": datetime.now().isoformat(),
        "worked": worked,
        "comment": user_feedback
    })

    memory_store.update(case_id, case)
```

### Ventajas de Memoria Compartida

✅ **Aprendizaje Continuo**: El sistema mejora con cada caso
✅ **Reutilización**: Soluciones exitosas se reutilizan
✅ **Consistencia**: Respuestas consistentes a problemas similares
✅ **Eficiencia**: Resolver más rápido con conocimiento previo
✅ **Escalabilidad**: La memoria puede crecer indefinidamente
✅ **Personalización**: Puede recordar preferencias por usuario

### Cuándo Usar

Usa memoria compartida cuando:
- Los problemas se repiten con variaciones
- El valor aumenta con el conocimiento acumulado
- Quieres que el sistema aprenda con el uso
- La consistencia en respuestas es importante
- Tienes recursos para almacenamiento persistente

---

## 📊 Comparación de Patterns {#comparación}

### Tabla Comparativa

| Aspecto | Plan-Execute-Evaluate | Handoffs | Memoria Compartida |
|---|---|---|---|
| **Objetivo** | Autonomía con plan explícito | Colaboración dinámica | Aprendizaje continuo |
| **Complejidad** | Media | Alta | Media-Alta |
| **Agentes** | 1 con múltiples roles | Múltiples especializados | Variable |
| **Estado** | Plan + Observaciones | Reports + History | Memory + Query |
| **Ciclos** | Sí (replan) | Sí (handoffs) | No (lineal) |
| **Persistencia** | No | No | Sí |
| **Overhead** | Medio (crear plan) | Bajo-Medio | Alto (DB queries) |
| **Escalabilidad** | Limitada | Alta (+ agentes) | Alta (+ memoria) |

### Cuándo Usar Cada Pattern

#### Plan-Execute-Evaluate

**Úsalo para:**
- Tareas multi-paso complejas
- Cuando necesitas visibilidad del plan
- Debugging y validación importantes
- Adaptación dinámica necesaria

**Ejemplo:** Sistema de automatización que debe planificar secuencia de tareas antes de ejecutar.

#### Handoffs

**Úsalo para:**
- Problemas multi-dimensionales
- Expertise especializado requerido
- Flujo no predefinido
- Colaboración dinámica

**Ejemplo:** Sistema de soporte técnico donde problemas pueden requerir múltiples especialistas.

#### Memoria Compartida

**Úsalo para:**
- Problemas recurrentes
- Aprendizaje de experiencias
- Mejora continua
- Personalización

**Ejemplo:** Chatbot de soporte que mejora con cada interacción.

### Combinación de Patterns

Los patterns pueden combinarse:

```python
# Agente Autónomo + Memoria + Handoffs
class AdvancedState(TypedDict):
    # Plan-Execute
    objective: str
    plan: str
    current_step: int

    # Handoffs
    current_agent: str
    specialist_reports: Dict[str, str]

    # Memoria
    similar_cases: List[Dict]
    memory: Dict

def advanced_agent(state: AdvancedState) -> dict:
    """
    Agente que combina:
    - Planificación explícita
    - Colaboración con handoffs
    - Aprendizaje de memoria
    """
    # 1. Buscar en memoria
    similar = search_memory(state["objective"], state["memory"])

    # 2. Crear plan (informado por memoria)
    plan = create_plan(state["objective"], similar_cases=similar)

    # 3. Ejecutar con handoffs si necesario
    if needs_specialist(plan):
        handoff_to_specialist(plan)

    # 4. Guardar resultado en memoria
    save_to_memory(result, state["memory"])
```

---

## ✅ Mejores Prácticas {#mejores-prácticas}

### 1. Plan-Execute-Evaluate

**✅ DO:**
- Crear planes específicos y accionables
- Incluir condiciones de éxito en cada paso
- Validar el plan antes de ejecutar
- Proporcionar contexto al evaluador
- Limitar ciclos de replaneación (max 3-5)

**❌ DON'T:**
- Planes demasiado genéricos
- Evaluar sin contexto suficiente
- Ciclos infinitos de replaneación
- Ignorar observaciones previas
- Planificar sin considerar herramientas disponibles

```python
# ✅ BIEN: Plan específico
plan = """
1. Buscar información sobre Python 3.12 usando search_web
2. Filtrar resultados para nuevas features
3. Usar calculator para comparar performance vs 3.11
4. Generar resumen estructurado
"""

# ❌ MAL: Plan genérico
plan = """
1. Investigar
2. Analizar
3. Reportar
"""
```

### 2. Handoffs

**✅ DO:**
- Documentar razón de cada handoff
- Compartir contexto completo
- Limitar handoffs (max 4-5 agentes)
- Validar que handoff es necesario
- Mantener historial de handoffs

**❌ DON'T:**
- Handoffs innecesarios
- Perder contexto en transferencias
- Ciclos infinitos entre agentes
- Handoffs sin razón clara
- Demasiados agentes en cadena

```python
# ✅ BIEN: Handoff justificado
if "authentication" in problem and current_agent == "code":
    return {
        "current_agent": "security",
        "handoff_reason": "Detected security issue requiring expertise"
    }

# ❌ MAL: Handoff arbitrario
return {"current_agent": random.choice(agents)}
```

### 3. Memoria Compartida

**✅ DO:**
- Usar embeddings para búsqueda semántica
- Implementar memory pruning regular
- Validar calidad antes de guardar
- Indexar para búsqueda rápida
- Trackear estadísticas de uso

**❌ DON'T:**
- Guardar todo sin filtro
- Búsqueda lineal en memoria grande
- Memoria sin estructura
- No limpiar casos obsoletos
- Ignorar feedback de usuarios

```python
# ✅ BIEN: Búsqueda semántica con filtros
similar = vector_db.similarity_search(
    query,
    k=5,
    filter={"success_count": {"$gt": 2}},
    score_threshold=0.7
)

# ❌ MAL: Búsqueda sin criterio
similar = [case for case in all_cases if query in case["query"]]
```

### 4. General

**Logging y Observabilidad:**
```python
import logging

logger = logging.getLogger(__name__)

def planner_node(state):
    logger.info(f"PLANNER: Creating plan for objective: {state['objective'][:50]}...")

    plan = create_plan(state["objective"])

    logger.info(f"PLANNER: Plan created with {len(plan.split('\\n'))} steps")
    logger.debug(f"PLANNER: Full plan: {plan}")

    return {"plan": plan}
```

**Error Handling:**
```python
def executor_node(state):
    try:
        result = execute_step(state["current_step"])
        return {"observations": [result]}
    except ToolExecutionError as e:
        logger.error(f"EXECUTOR: Tool execution failed: {e}")
        # Registrar error en observaciones
        return {
            "observations": [{
                "step": state["current_step"],
                "error": str(e),
                "requires_replan": True
            }]
        }
    except Exception as e:
        logger.critical(f"EXECUTOR: Unexpected error: {e}")
        raise
```

**Testing:**
```python
def test_handoff_preserves_context():
    """Verificar que handoffs preservan contexto completo."""
    initial_state = {
        "query": "Test query",
        "current_agent": "code",
        "specialist_reports": {"code": "Initial analysis"}
    }

    result = code_agent(initial_state)

    # Verificar que reporte previo se preserva
    assert "code" in result["specialist_reports"]

    # Verificar que nuevo agente recibe contexto
    assert "current_agent" in result
```

---

## 🎯 Casos de Uso {#casos-de-uso}

### 1. Sistema de Automatización de Tareas

**Pattern:** Plan-Execute-Evaluate

**Escenario:** Automatizar proceso de despliegue de aplicación.

```python
objective = """
Desplegar aplicación web a producción:
1. Verificar que tests pasen
2. Crear build de producción
3. Subir a servidor
4. Ejecutar migraciones de DB
5. Reiniciar servicios
6. Verificar health checks
"""

# El agente crea plan detallado, ejecuta paso a paso,
# evalúa si cada paso fue exitoso, y puede replanificar
# si algo falla (ej: tests fallan → replantear para fix primero)
```

**Beneficio:** Visibilidad de cada paso, fácil debugging, adaptación automática.

### 2. Sistema de Soporte Técnico

**Pattern:** Handoffs

**Escenario:** Usuario reporta problema complejo.

```python
query = """
Mi aplicación web arroja error 500.
Revisé logs y dice 'Connection refused to PostgreSQL'.
El firewall está configurado para permitir puerto 5432.
Pero la aplicación usa credenciales hardcodeadas.
"""

# Flujo:
# Triage → Network (verifica connectivity)
#       → Security (detecta credenciales hardcoded)
#       → Code (encuentra dónde cambiar config)
#       → Final (sintetiza solución completa)
```

**Beneficio:** Múltiples expertas colaboran, solución integral.

### 3. Chatbot de Servicio al Cliente

**Pattern:** Memoria Compartida

**Escenario:** Chatbot que aprende de interacciones.

```python
# Consulta 1
query = "¿Cómo reseteo mi contraseña?"
# Sistema genera solución y guarda en memoria

# Consulta 2 (similar)
query = "No puedo acceder a mi cuenta, olvidé la contraseña"
# Sistema encuentra caso similar en memoria
# Adapta solución previa → respuesta más rápida y precisa
```

**Beneficio:** Aprende con cada interacción, mejora continua.

### 4. Asistente de Investigación

**Pattern:** Combinación (Plan + Memoria)

**Escenario:** Investigar tema técnico y generar reporte.

```python
objective = "Investigar estado del arte en RAG (Retrieval Augmented Generation)"

# 1. Buscar en memoria si ya se investigó antes
similar_research = search_memory("RAG")

# 2. Crear plan informado por investigaciones previas
plan = create_plan(objective, context=similar_research)

# 3. Ejecutar plan con agentes especializados
results = execute_plan(plan)

# 4. Guardar hallazgos en memoria para futuras investigaciones
save_to_memory(results)
```

**Beneficio:** No duplica trabajo, reutiliza investigación previa.

### 5. Sistema de Análisis de Datos

**Pattern:** Handoffs + Memoria

**Escenario:** Análisis multi-dimensional de dataset.

```python
query = "Analizar dataset de ventas Q4 2024"

# Handoffs entre especialistas:
# Data Cleaning Agent → Statistical Analysis Agent
#                    → Visualization Agent
#                    → Business Insights Agent

# Memoria:
# - Recuerda análisis previos de Q3, Q2
# - Reutiliza queries SQL exitosas
# - Aplica mismas visualizaciones que gustaron
```

**Beneficio:** Análisis profundo + aprendizaje de análisis previos.

---

## 📚 Referencias y Recursos

### Papers y Research

1. **"ReAct: Synergizing Reasoning and Acting in Language Models"** (Yao et al., 2023)
   - Base teórica de agentes autónomos

2. **"Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning"** (Wang et al., 2023)
   - Fundamentos de Plan-Execute-Evaluate

3. **"Generative Agents: Interactive Simulacra of Human Behavior"** (Park et al., 2023)
   - Memoria a largo plazo en agentes

### Documentación Oficial

- [LangGraph Multi-Agent Systems](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)
- [LangGraph Plan-Execute](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [Vector Stores](https://python.langchain.com/docs/integrations/vectorstores/)

### Herramientas

**Vector Databases:**
- [Pinecone](https://www.pinecone.io/)
- [Weaviate](https://weaviate.io/)
- [ChromaDB](https://www.trychroma.com/)
- [Qdrant](https://qdrant.tech/)

**Observability:**
- [LangSmith](https://www.langchain.com/langsmith)
- [Weights & Biases](https://wandb.ai/)
- [Arize AI](https://arize.com/)

---

## 🎓 Resumen del Módulo

En este módulo aprendiste:

✅ **Plan-Execute-Evaluate**: Agentes con planificación explícita
✅ **Handoffs**: Colaboración dinámica entre especialistas
✅ **Memoria Compartida**: Aprendizaje continuo y persistente
✅ **Combinación de Patterns**: Cómo integrarlos para sistemas avanzados
✅ **Mejores Prácticas**: Cómo implementar cada pattern correctamente

**Próximos Pasos:**
- Módulo 4: Aplicaciones de Negocio
- Implementar sistemas completos end-to-end
- Integrar con sistemas reales
- Despliegue y producción

---

**¡Felicitaciones por completar el Módulo 3!** 🎉

Ahora tienes el conocimiento para construir agentes autónomos avanzados que pueden planificar, colaborar y aprender.
