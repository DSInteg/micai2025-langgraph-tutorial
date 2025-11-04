# Ejercicio 3.2: Red Colaborativa con Handoffs

## 🎯 Objetivo

Implementar una red de agentes especializados que colaboran mediante **handoffs** (transferencias de control) para resolver tareas complejas que requieren múltiples expertises.

## 📚 Contexto

### ¿Qué es el Pattern de Handoffs?

El pattern de **handoffs** permite que múltiples agentes especializados trabajen juntos pasándose el control dinámicamente según la naturaleza de la tarea.

**Diferencia con patterns anteriores:**

- **Routing (Módulo 2.1)**: Un clasificador decide QUÉ agente trabaja, pero solo UNO ejecuta
- **Parallelization (Módulo 2.2)**: TODOS los agentes trabajan simultáneamente sobre lo mismo
- **Orchestrator-Workers (Módulo 2.3)**: Un orquestador divide y asigna, pero no hay transferencia dinámica
- **Handoffs (este ejercicio)**: Los agentes se pasan el control entre sí según necesidad

### ¿Cuándo usar Handoffs?

✅ **Úsalo cuando:**
- La tarea requiere múltiples expertises secuencialmente
- No sabes de antemano la secuencia exacta de agentes
- Los agentes necesitan contexto de lo que hicieron los anteriores
- La colaboración debe ser dinámica y adaptativa

❌ **NO lo uses cuando:**
- Solo necesitas UN experto (usa routing simple)
- Todos los agentes deben trabajar en paralelo (usa parallelization)
- La secuencia es fija y predecible (usa workflow simple)

### Arquitectura del Ejercicio

En este ejercicio implementaremos un **Sistema de Soporte Técnico** con tres agentes especializados:

```
Usuario pregunta
      ↓
┌─────────────────┐
│  Triage Agent   │ ← Clasifica y deriva
└─────────────────┘
      ↓
   [Decide]
      ↓
┌─────────────────┬─────────────────┬─────────────────┐
│  Code Agent     │ Network Agent   │  Security Agent │
└─────────────────┴─────────────────┴─────────────────┘
      ↓                   ↓                   ↓
   [Puede solicitar ayuda de otro agente]
      ↓
┌─────────────────┐
│  Final Agent    │ ← Sintetiza respuesta
└─────────────────┘
```

**Flujo de handoffs:**
1. **Triage Agent**: Analiza la consulta y decide qué especialista necesita
2. **Specialist Agent**: Trabaja en su área, puede hacer handoff a otro si necesita ayuda
3. **Final Agent**: Sintetiza todas las contribuciones en una respuesta coherente

## 🏗️ Componentes Clave

### 1. Estado Compartido

```python
class CollaborativeState(TypedDict):
    """Estado compartido entre todos los agentes."""
    query: str                    # Consulta original del usuario
    current_agent: str            # Agente que tiene el control ahora
    conversation_history: List[Dict]  # Historial de conversación
    specialist_reports: Dict[str, str]  # Reportes de cada especialista
    handoff_reason: str          # Por qué se hizo el handoff
    final_response: str          # Respuesta final sintetizada
```

### 2. Agentes Especializados

Cada agente tiene dos responsabilidades:
1. **Resolver** su parte del problema
2. **Decidir** si necesita hacer handoff a otro agente

### 3. Handoff Mechanism

Los handoffs se implementan mediante:
- **Conditional edges**: El agente decide a quién pasar el control
- **Estado compartido**: Todos los agentes tienen acceso al contexto completo
- **Razones explícitas**: Cada handoff documenta por qué se hizo

## 📝 Tareas

### Paso 1: Definir el Estado

Define `CollaborativeState` con todos los campos necesarios para la colaboración.

### Paso 2: Implementar Triage Agent

```python
def triage_agent(state: CollaborativeState) -> dict:
    """
    Analiza la consulta y decide qué especialista debe atenderla primero.

    TODO:
    1. Analizar la consulta del usuario
    2. Clasificarla en: CODE, NETWORK, SECURITY
    3. Actualizar current_agent con el especialista apropiado
    4. Agregar entrada al conversation_history
    """
    pass
```

### Paso 3: Implementar Agentes Especialistas

Cada agente debe:
1. Analizar si puede resolver completamente la consulta
2. Si SÍ puede: Generar reporte y decidir ir a FINAL
3. Si NO puede completamente: Decidir a qué otro agente hacer handoff

```python
def code_agent(state: CollaborativeState) -> dict:
    """
    Especialista en problemas de código.

    TODO:
    1. Revisar la consulta y el historial
    2. Generar análisis desde perspectiva de código
    3. Decidir si necesita ayuda de network_agent o security_agent
    4. O si puede pasar a final_agent
    """
    pass
```

### Paso 4: Implementar Final Agent

```python
def final_agent(state: CollaborativeState) -> dict:
    """
    Sintetiza todos los reportes de especialistas en una respuesta coherente.

    TODO:
    1. Recopilar todos los specialist_reports
    2. Integrar el conversation_history
    3. Generar respuesta final unificada
    """
    pass
```

### Paso 5: Implementar Routing Functions

```python
def route_from_triage(state: CollaborativeState) -> Literal["code", "network", "security"]:
    """Decide a qué especialista derivar desde triage."""
    pass

def route_from_specialist(state: CollaborativeState) -> Literal["code", "network", "security", "final"]:
    """Decide el siguiente agente basado en current_agent."""
    pass
```

### Paso 6: Construir el Grafo

```python
def build_graph():
    """
    TODO:
    1. Agregar todos los nodos (triage, code, network, security, final)
    2. Entry point: triage
    3. Conditional edge desde triage a especialistas
    4. Conditional edges entre especialistas (handoffs)
    5. Edge de final a END
    """
    pass
```

## 🎓 Conceptos Clave

### 1. Handoff vs Routing

**Routing (Módulo 2.1):**
```
Classifier → [Decision] → ONE Specialist → END
```

**Handoff (este ejercicio):**
```
Triage → Specialist A → [Needs help?] → Specialist B → Final
                ↓
           [Can solve?]
                ↓
             Final
```

### 2. Shared Context

Todos los agentes pueden ver:
- Qué hicieron los agentes anteriores (`conversation_history`)
- Qué encontraron (`specialist_reports`)
- Por qué se hizo el handoff (`handoff_reason`)

Esto permite **colaboración informada**, no solo delegación ciega.

### 3. Dynamic Flow

A diferencia de un workflow fijo, el flujo es dinámico:
- El agente A puede decidir que necesita ayuda del B
- El agente B puede decidir que en realidad necesita al C
- La secuencia se determina en tiempo de ejecución

## 🧪 Testing

Los tests verifican:
1. ✅ Triage clasifica correctamente diferentes tipos de consultas
2. ✅ Cada especialista genera su reporte
3. ✅ Los handoffs ocurren cuando son necesarios
4. ✅ El final_agent sintetiza múltiples reportes
5. ✅ End-to-end: Una consulta compleja pasa por múltiples agentes

## 💡 Pistas

### Pista 1: Clasificación en Triage

Usa el LLM para clasificar la consulta:
```python
prompt = f"""Analiza esta consulta de soporte técnico y clasifica en UNA categoría:

Consulta: {query}

Categorías:
- CODE: Problemas de código, bugs, errores de programación
- NETWORK: Problemas de conectividad, DNS, firewall, puertos
- SECURITY: Vulnerabilidades, permisos, autenticación, cifrado

Responde SOLO con: CODE, NETWORK, o SECURITY

Clasificación:"""
```

### Pista 2: Decidir Handoffs

Cada especialista debe preguntar al LLM:
```python
prompt = f"""Eres un especialista en {specialty}.

Consulta original: {query}
Tu análisis: {your_report}
Otros reportes: {other_reports}

¿Necesitas ayuda de otro especialista?
- Si la consulta está completamente resuelta: FINAL
- Si necesitas ayuda de código: CODE
- Si necesitas ayuda de red: NETWORK
- Si necesitas ayuda de seguridad: SECURITY

Responde SOLO con: FINAL, CODE, NETWORK, o SECURITY

Decisión:"""
```

### Pista 3: Historial de Conversación

Mantén un historial detallado:
```python
conversation_history.append({
    "agent": "code_agent",
    "action": "analysis",
    "content": "Identifiqué un problema de SQL injection...",
    "handoff_to": "security_agent",
    "reason": "Necesito expertise en seguridad para validar la vulnerabilidad"
})
```

## 🎯 Resultado Esperado

Al ejecutar el ejercicio con una consulta compleja como:

> "Mi aplicación web no puede conectarse a la base de datos. El código usa SQLAlchemy y parece que hay un problema de autenticación, pero el firewall también podría estar bloqueando el puerto 5432."

Deberías ver un flujo como:
```
🎯 TRIAGE → Deriva a NETWORK (problema de conectividad)
🔧 NETWORK → Analiza firewall/puertos → Handoff a CODE (SQLAlchemy)
💻 CODE → Analiza código → Handoff a SECURITY (autenticación)
🔒 SECURITY → Valida credenciales → Puede ir a FINAL
✅ FINAL → Sintetiza: "El problema tiene 3 capas: firewall bloqueando puerto, configuración SQLAlchemy incorrecta, credenciales expiradas. Aquí las soluciones..."
```

## 📖 Referencias

- [LangGraph Conditional Edges](https://langchain-ai.github.io/langgraph/how-tos/branching/)
- [Multi-Agent Collaboration](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/)
- [State Management](https://langchain-ai.github.io/langgraph/concepts/low_level/#state)

---

**Tiempo estimado**: 45-60 minutos

**Dificultad**: ⭐⭐⭐⭐ (Avanzado - requiere entender flujos dinámicos y colaboración)
