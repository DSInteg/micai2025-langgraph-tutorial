# 🎯 Grafos LangGraph - Módulo 1 Fundamentos

Este directorio contiene **4 grafos educativos** listos para ser abiertos en **LangGraph Studio**.

## 📁 Grafos Disponibles

### 1. `simple.py` - Grafo Básico
**Complejidad**: ⭐ Principiante
**Requiere API**: ❌ No

Grafo simple que demuestra:
- State básico con TypedDict
- 3 nodos conectados
- Conditional edge con decisión aleatoria (50/50)

```python
# Estado: {"graph_state": "Hi, this is Lance."}
# Output: "Hi, this is Lance. I am happy!" o "... sad!"
```

### 2. `router.py` - Router con Tool
**Complejidad**: ⭐⭐ Intermedio
**Requiere API**: ✅ OPENAI_API_KEY

Demuestra routing con LLM:
- Tool de multiplicación
- Conditional edge basado en tool calling
- Usa GPT-4o

### 3. `agent.py` - Agente Matemático
**Complejidad**: ⭐⭐⭐ Intermedio-Avanzado
**Requiere API**: ✅ OPENAI_API_KEY

Agente completo con:
- 3 tools (add, multiply, divide)
- Loop de tool calling
- MessagesState
- Usa GPT-4o

### 4. `graph.py` - Sistema de Clasificación de Tickets ⭐ RECOMENDADO
**Complejidad**: ⭐⭐ Intermedio
**Requiere API**: ❌ No (solo Python)

**🎯 Mejor para aprender los fundamentos**

Sistema profesional de clasificación de tickets que demuestra:
- State complejo con 5 campos
- 3 nodos de procesamiento
- Conditional edge con lógica de negocio
- Caso de uso real y motivador

```python
# Input:
{
  "ticket_id": "TICKET-001",
  "mensaje": "El servidor está caído",
  "prioridad": "",
  "estado": "nuevo",
  "asignado_a": ""
}

# Output:
{
  "ticket_id": "TICKET-001",
  "mensaje": "El servidor está caído",
  "prioridad": "urgente",
  "estado": "procesado",
  "asignado_a": "Equipo de Ingeniería"
}
```

## 🚀 Abrir en LangGraph Studio

### Opción 1: Desde la línea de comandos

```bash
# Navegar al directorio
cd /home/jcordova/lang/micai2025/notebooks/modulo_1/studio

# Abrir en LangGraph Studio
langgraph dev
```

### Opción 2: Desde LangGraph Studio UI

1. Abre LangGraph Studio
2. Click en "Open Folder"
3. Selecciona la carpeta `/home/jcordova/lang/micai2025/notebooks/modulo_1/studio`
4. Selecciona el grafo que quieres explorar del dropdown

## 📊 Comparación de Grafos

| Grafo | Nodos | Edges | State Fields | LLM | Tools | Caso de Uso |
|-------|-------|-------|--------------|-----|-------|-------------|
| simple | 3 | 1 condicional | 1 | ❌ | ❌ | Ejemplo básico |
| router | 2 | 1 condicional | messages | ✅ | 1 | Routing con LLM |
| agent | 2 | loop | messages | ✅ | 3 | Agente matemático |
| **graph** | **3** | **1 condicional** | **5** | **❌** | **❌** | **Tickets de soporte** |

## 🎓 Ruta de Aprendizaje Recomendada

### Para Principiantes (Sin experiencia con LangGraph)

1. **Empieza con `graph.py`** (Sistema de Tickets)
   - ⏱️ 30 minutos
   - No requiere API keys
   - Caso de uso familiar
   - Conceptos fundamentales claros

2. **Luego `simple.py`** (Grafo Básico)
   - ⏱️ 10 minutos
   - Ver el ejemplo original más simple
   - Entender la progresión de complejidad

3. **Después `router.py`** (Router con LLM)
   - ⏱️ 15 minutos
   - Requiere configurar OPENAI_API_KEY
   - Introduce LLMs y tools

4. **Finalmente `agent.py`** (Agente Completo)
   - ⏱️ 20 minutos
   - Agente con múltiples tools
   - Loops y tool calling avanzado

### Para Usuarios Intermedios

Puedes explorar los grafos en cualquier orden según tu interés.

## 🎬 Uso en LangGraph Studio

### Visualización del Grafo

En Studio verás:
- Diagrama visual del grafo
- Nodos y sus conexiones
- Conditional edges resaltados
- Flujo de ejecución

### Ejecutar un Grafo

1. Selecciona el grafo del dropdown
2. Ve a la sección "Playground"
3. Ingresa el input según el formato del grafo
4. Observa la ejecución paso a paso

### Ejemplos de Input

**Para `graph.py` (Tickets):**
```json
{
  "ticket_id": "TICKET-001",
  "mensaje": "El servidor está caído",
  "prioridad": "",
  "estado": "nuevo",
  "asignado_a": ""
}
```

**Para `simple.py`:**
```json
{
  "graph_state": "Hi, this is Lance."
}
```

**Para `agent.py` y `router.py`:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is 3 times 5?"
    }
  ]
}
```

## 🔧 Configuración

### Dependencias

Las dependencias están en `requirements.txt`:
```bash
langgraph>=1.0.0
langchain-core>=1.0.0
langchain-openai  # Solo para agent.py y router.py
typing-extensions>=4.7.0
```

### Variables de Entorno

Si vas a usar `agent.py` o `router.py`, necesitas configurar `.env`:

```bash
# Copiar el template
cp .env.example .env

# Editar y agregar tu API key
# OPENAI_API_KEY=sk-...
```

**Nota**: `graph.py` y `simple.py` **NO requieren** API keys.

## 🧪 Ejecutar Localmente (Sin Studio)

Todos los grafos pueden ejecutarse sin Studio:

```bash
# Activar entorno virtual
source ../../../venv/bin/activate

# Ejecutar el grafo de tickets (incluye tests)
python graph.py

# O importar y usar en Python
python -c "from graph import graph; print(graph.invoke({'ticket_id': 'T1', 'mensaje': 'test', 'prioridad': '', 'estado': 'nuevo', 'asignado_a': ''}))"
```

## 📚 Conceptos Demostrados

### State (Estado)
- **simple.py**: Estado mínimo con 1 campo
- **agent.py/router.py**: MessagesState (built-in)
- **graph.py**: Estado custom con 5 campos ⭐

### Nodes (Nodos)
- Funciones que procesan el estado
- Pueden retornar actualizaciones parciales
- Todos los grafos demuestran esto

### Edges (Aristas)
- **Normal edges**: Conexión fija entre nodos
- **Conditional edges**: Routing dinámico
  - `simple.py`: Aleatorio
  - `agent.py/router.py`: Basado en tool calling
  - `graph.py`: Basado en lógica de negocio ⭐

### Graph Construction
- Todos usan `StateGraph(State)`
- `add_node()`, `add_edge()`, `add_conditional_edges()`
- `compile()` para finalizar

## 🎓 Para el Instructor

### Demostración en Clase

**Orden sugerido para demostración:**

1. **`graph.py`** (30 min) - Fundamentos con caso real
   - Ejecutar varios ejemplos
   - Mostrar cómo cambia el routing
   - Modificar palabras_urgentes en vivo

2. **`simple.py`** (10 min) - Mostrar el ejemplo más minimalista
   - Comparar con graph.py
   - Discutir trade-offs de simplicidad

3. **`router.py`** (10 min) - Introducir LLMs
   - Mostrar cómo el LLM decide usar tools
   - Primer contacto con MessagesState

4. **`agent.py`** (15 min) - Agente completo
   - Loops de tool calling
   - Múltiples tools
   - Comparar con los anteriores

### Puntos Clave

- ✅ `graph.py` es **perfecto para comenzar** (no requiere API, caso real)
- ✅ `simple.py` es **el más minimalista** (entender lo esencial)
- ✅ `router.py` **introduce LLMs** (transición a agentes)
- ✅ `agent.py` **demuestra capacidades completas** (loops, múltiples tools)

### Preguntas para la Audiencia

1. "¿Qué diferencia ven entre `simple.py` y `graph.py`?"
2. "¿Por qué `graph.py` no necesita un LLM?"
3. "¿Cuándo usarían lógica de negocio vs LLM para routing?"
4. "¿Qué ventajas tiene `graph.py` para aprender?"

## 🔍 Debugging

### En Studio

- Inspecciona el state en cada paso
- Ve los prints de cada nodo
- Observa qué ruta tomó el conditional edge
- Compara inputs vs outputs

### En Terminal

Los prints de cada grafo muestran:
- **graph.py**: Flujo completo con emojis
- **simple.py**: Nombres de nodos
- **agent.py/router.py**: Llamadas a LLM y tools

## 📖 Recursos Adicionales

- [LangGraph Studio Documentation](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)
- [StateGraph API](https://langchain-ai.github.io/langgraph/reference/graphs/)
- [Conditional Edges Guide](https://langchain-ai.github.io/langgraph/how-tos/branching/)
- [Notebook Tutorial](../00_primer_grafo_interactivo.ipynb) - Versión interactiva de `graph.py`

## 🆘 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found" (solo agent.py y router.py)
```bash
cp .env.example .env
# Editar .env y agregar tu key
```

### "langgraph command not found"
```bash
pip install langgraph-cli
```

### El grafo no aparece en Studio
- Verifica que `langgraph.json` tiene el grafo listado
- Recarga Studio (Cmd+R o Ctrl+R)
- Verifica que el archivo .py no tiene errores de sintaxis

---

**🎉 ¡Explora los 4 grafos y aprende LangGraph hands-on!**

**Recomendación**: Empieza con `graph.py` si eres nuevo en LangGraph.
