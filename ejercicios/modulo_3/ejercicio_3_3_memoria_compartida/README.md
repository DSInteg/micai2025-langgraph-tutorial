# Ejercicio 3.3: Memoria Compartida entre Agentes

## 🎯 Objetivo

Implementar un sistema multi-agente con **memoria compartida persistente** que permite a los agentes aprender de interacciones pasadas y mantener contexto a través de múltiples sesiones.

## 📚 Contexto

### ¿Qué es Memoria Compartida?

La **memoria compartida** permite que múltiples agentes:
- Accedan a un repositorio común de conocimiento
- Aprendan de interacciones pasadas
- Mantengan contexto entre sesiones
- Compartan descubrimientos entre ellos

**Diferencia con ejercicios anteriores:**

- **Ejercicio 3.1 (Plan-Execute)**: Memoria de corto plazo solo durante ejecución
- **Ejercicio 3.2 (Handoffs)**: Memoria compartida solo en `specialist_reports` durante una sesión
- **Ejercicio 3.3 (este)**: Memoria persistente que sobrevive entre sesiones

### ¿Cuándo usar Memoria Compartida?

✅ **Úsalo cuando:**
- Los agentes necesitan aprender de interacciones pasadas
- El contexto debe mantenerse entre sesiones
- Múltiples agentes deben acceder al mismo conocimiento
- Quieres que el sistema mejore con el uso

❌ **NO lo uses cuando:**
- Cada consulta es completamente independiente
- No hay valor en recordar interacciones pasadas
- La privacidad requiere no persistir datos
- El costo de almacenamiento no se justifica

### Arquitectura del Ejercicio

Implementaremos un **Sistema de Soporte Técnico con Memoria** que:
- Recuerda problemas resueltos anteriormente
- Aprende de soluciones exitosas
- Mantiene perfil de usuarios
- Detecta patrones en problemas

```
┌─────────────────────────────────────────┐
│       MEMORIA COMPARTIDA                │
│  ┌─────────────────────────────────┐   │
│  │ - Casos resueltos               │   │
│  │ - Perfiles de usuario           │   │
│  │ - Soluciones exitosas           │   │
│  │ - Patrones detectados           │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         ↑                    ↑
         │ READ/WRITE         │
         ↓                    ↓
┌─────────────┐      ┌─────────────┐
│   Memory    │      │  Solution   │
│   Agent     │ ───→ │   Agent     │
└─────────────┘      └─────────────┘
         │                    │
         └────────┬───────────┘
                  ↓
         ┌─────────────┐
         │   Update    │
         │   Memory    │
         │   Agent     │
         └─────────────┘
```

**Flujo:**
1. **Memory Agent**: Busca en memoria casos similares
2. **Solution Agent**: Resuelve usando contexto + memoria
3. **Update Memory Agent**: Actualiza memoria con nueva solución

## 🏗️ Componentes Clave

### 1. Estado con Memoria

```python
class MemoryState(TypedDict):
    """Estado que incluye acceso a memoria compartida."""
    query: str                  # Consulta actual
    user_id: str               # ID del usuario
    similar_cases: List[Dict]  # Casos similares de memoria
    solution: str              # Solución generada
    should_save: bool          # Si guardar en memoria
    memory: Dict               # Memoria compartida (simulada)
```

### 2. Memoria como Recurso Compartido

En este ejercicio simularemos la memoria con un diccionario Python.
En producción usarías:
- **Vector DB**: Pinecone, Weaviate, ChromaDB para búsqueda semántica
- **SQL/NoSQL**: PostgreSQL, MongoDB para datos estructurados
- **Cache**: Redis para acceso rápido
- **LangChain Memory**: Módulos de memoria de LangChain

### 3. Operaciones de Memoria

```python
# LEER: Buscar casos similares
similar_cases = search_memory(query, memory)

# ESCRIBIR: Guardar nueva solución
save_to_memory(query, solution, user_id, memory)

# ACTUALIZAR: Incrementar contador de éxito
update_solution_stats(case_id, success=True, memory)
```

## 📝 Tareas

### Paso 1: Definir el Estado

Define `MemoryState` con campos para la memoria compartida.

### Paso 2: Implementar Funciones de Memoria

```python
def search_similar_cases(query: str, memory: Dict) -> List[Dict]:
    """
    Busca casos similares en la memoria.

    TODO:
    1. Implementar búsqueda por keywords (versión simple)
    2. En producción: usar embeddings y búsqueda semántica
    3. Retornar top-k casos más relevantes
    """
    pass

def save_to_memory(query: str, solution: str, user_id: str, memory: Dict):
    """
    Guarda un nuevo caso en memoria.

    TODO:
    1. Crear entrada con timestamp
    2. Agregar a memoria persistente
    3. Actualizar índices si aplica
    """
    pass
```

### Paso 3: Implementar Memory Agent

```python
def memory_agent(state: MemoryState) -> dict:
    """
    Busca en memoria casos similares al problema actual.

    TODO:
    1. Extraer la consulta del estado
    2. Buscar casos similares en memoria
    3. Si encuentra casos relevantes: prepararlos para Solution Agent
    4. Si no encuentra nada: indicar que es caso nuevo
    """
    pass
```

### Paso 4: Implementar Solution Agent

```python
def solution_agent(state: MemoryState) -> dict:
    """
    Genera solución usando contexto + memoria.

    TODO:
    1. Si hay casos similares: usarlos como contexto
    2. Generar solución considerando el historial
    3. Decidir si la solución debe guardarse en memoria
    """
    pass
```

### Paso 5: Implementar Update Memory Agent

```python
def update_memory_agent(state: MemoryState) -> dict:
    """
    Actualiza la memoria con la nueva solución.

    TODO:
    1. Verificar si should_save es True
    2. Guardar caso en memoria
    3. Actualizar estadísticas si aplica
    """
    pass
```

### Paso 6: Construir el Grafo

```python
def build_graph():
    """
    TODO:
    1. Agregar nodos: memory, solution, update_memory
    2. Entry: memory
    3. Edges: memory → solution → update_memory → END
    """
    pass
```

## 🎓 Conceptos Clave

### 1. Tipos de Memoria

**Short-term Memory (ejercicio 3.2):**
- Solo durante una sesión
- Se pierde al terminar
- Útil para contexto inmediato

**Long-term Memory (este ejercicio):**
- Persiste entre sesiones
- Permite aprendizaje continuo
- Crece con el tiempo

### 2. Búsqueda en Memoria

**Búsqueda Simple (este ejercicio):**
```python
# Buscar por keywords
if keyword in case["query"]:
    similar_cases.append(case)
```

**Búsqueda Semántica (producción):**
```python
# Usar embeddings
query_embedding = get_embedding(query)
similar_cases = vector_db.search(
    query_embedding,
    top_k=5,
    threshold=0.8
)
```

### 3. Estructura de Memoria

Cada entrada en memoria puede tener:
```python
{
    "id": "case_001",
    "timestamp": "2024-01-15T10:30:00",
    "user_id": "user_123",
    "query": "No puedo conectarme a la BD",
    "solution": "Verificar firewall puerto 5432...",
    "tags": ["database", "connection", "firewall"],
    "success_count": 5,  # Cuántas veces funcionó
    "last_used": "2024-01-20T14:00:00"
}
```

## 🧪 Testing

Los tests verifican:
1. ✅ Búsqueda en memoria encuentra casos relevantes
2. ✅ Memory agent recupera casos similares
3. ✅ Solution agent usa memoria como contexto
4. ✅ Update memory agent guarda nuevos casos
5. ✅ Memoria persiste entre invocaciones
6. ✅ Casos similares mejoran la solución

## 💡 Pistas

### Pista 1: Búsqueda Simple

Para este ejercicio, usa búsqueda por keywords:
```python
def search_similar_cases(query: str, memory: Dict, top_k: int = 3) -> List[Dict]:
    query_lower = query.lower()
    query_words = set(query_lower.split())

    # Calcular relevancia para cada caso
    scored_cases = []
    for case in memory.get("cases", []):
        case_words = set(case["query"].lower().split())
        # Intersección de palabras
        overlap = len(query_words & case_words)
        if overlap > 0:
            scored_cases.append((overlap, case))

    # Ordenar por relevancia y retornar top-k
    scored_cases.sort(reverse=True, key=lambda x: x[0])
    return [case for score, case in scored_cases[:top_k]]
```

### Pista 2: Memory Agent

```python
def memory_agent(state: MemoryState) -> dict:
    query = state["query"]
    memory = state.get("memory", {"cases": []})

    similar_cases = search_similar_cases(query, memory)

    if similar_cases:
        print(f"   ✓ Encontrados {len(similar_cases)} casos similares")
        for case in similar_cases:
            print(f"      - {case['query'][:50]}...")
    else:
        print("   ℹ No hay casos similares en memoria")

    return {"similar_cases": similar_cases}
```

### Pista 3: Solution Agent con Contexto

```python
similar_context = ""
if state["similar_cases"]:
    similar_context = "\n\nCASOS SIMILARES RESUELTOS ANTERIORMENTE:\n"
    for i, case in enumerate(state["similar_cases"], 1):
        similar_context += f"\n{i}. Problema: {case['query']}\n"
        similar_context += f"   Solución: {case['solution']}\n"
        if "success_count" in case:
            similar_context += f"   Éxitos: {case['success_count']}\n"

prompt = f"""Resuelve esta consulta de soporte técnico.

CONSULTA ACTUAL:
{query}

{similar_context}

Genera una solución detallada. Si hay casos similares,
considera esas soluciones pero adáptalas al problema actual.

SOLUCIÓN:"""
```

### Pista 4: Guardar en Memoria

```python
def save_to_memory(query: str, solution: str, user_id: str, memory: Dict):
    import datetime

    new_case = {
        "id": f"case_{len(memory.get('cases', [])) + 1:03d}",
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": user_id,
        "query": query,
        "solution": solution,
        "tags": extract_tags(query),  # Función helper
        "success_count": 0,
        "last_used": datetime.datetime.now().isoformat()
    }

    if "cases" not in memory:
        memory["cases"] = []

    memory["cases"].append(new_case)
```

## 🎯 Resultado Esperado

Al ejecutar el ejercicio varias veces con consultas similares:

**Primera Ejecución:**
```
🧠 MEMORY AGENT: Buscando casos similares...
   ℹ No hay casos similares en memoria (primera vez)

💡 SOLUTION AGENT: Generando solución...
   ✓ Solución generada

💾 UPDATE MEMORY: Guardando en memoria...
   ✓ Caso guardado: case_001
```

**Segunda Ejecución (consulta similar):**
```
🧠 MEMORY AGENT: Buscando casos similares...
   ✓ Encontrados 1 casos similares
      - No puedo conectarme a la base de datos...

💡 SOLUTION AGENT: Generando solución...
   → Usando 1 caso(s) similar(es) como referencia
   ✓ Solución generada (mejorada con contexto)

💾 UPDATE MEMORY: Guardando en memoria...
   ✓ Caso guardado: case_002
```

**Tercera Ejecución:**
```
🧠 MEMORY AGENT: Buscando casos similares...
   ✓ Encontrados 2 casos similares
      - No puedo conectarme a la base de datos...
      - Error de conexión a PostgreSQL...

💡 SOLUTION AGENT: Generando solución...
   → Usando 2 caso(s) similar(es) como referencia
   ✓ Solución generada (muy mejorada con historial)
```

## 📖 Referencias

- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [Vector Databases for LLMs](https://python.langchain.com/docs/integrations/vectorstores/)
- [Semantic Search](https://python.langchain.com/docs/modules/data_connection/retrievers/similarity)
- [LangGraph Checkpointing](https://langchain-ai.github.io/langgraph/how-tos/persistence/)

## 🚀 Extensiones (Opcional)

Si terminas el ejercicio básico, considera implementar:

1. **Vector Search**: Usar embeddings para búsqueda semántica real
2. **User Profiles**: Mantener perfil de cada usuario
3. **Solution Rating**: Permitir calificar soluciones y usar las mejor calificadas
4. **Pattern Detection**: Detectar patrones comunes en problemas
5. **Memory Pruning**: Eliminar casos obsoletos o de baja utilidad

---

**Tiempo estimado**: 45-60 minutos

**Dificultad**: ⭐⭐⭐⭐ (Avanzado - requiere entender gestión de estado persistente)
