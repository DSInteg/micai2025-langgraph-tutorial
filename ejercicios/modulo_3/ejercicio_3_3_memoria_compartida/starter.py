"""
Ejercicio 3.3: Memoria Compartida entre Agentes - STARTER

Implementa un sistema con memoria compartida persistente.
"""

from typing import TypedDict, List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import datetime

load_dotenv()

# =============================================================================
# ESTADO CON MEMORIA
# =============================================================================

class MemoryState(TypedDict):
    """
    Estado que incluye acceso a memoria compartida.

    La memoria permite que los agentes:
    - Aprendan de casos pasados
    - Reutilicen soluciones exitosas
    - Mejoren con el tiempo
    """
    # TODO: Define los campos del estado
    # - query: str (consulta actual)
    # - user_id: str (ID del usuario)
    # - similar_cases: List[Dict] (casos similares encontrados en memoria)
    # - solution: str (solución generada)
    # - should_save: bool (si guardar en memoria)
    # - memory: Dict (memoria compartida - en producción sería una BD)
    pass


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# =============================================================================
# FUNCIONES DE GESTIÓN DE MEMORIA
# =============================================================================

def search_similar_cases(query: str, memory: Dict, top_k: int = 3) -> List[Dict]:
    """
    Busca casos similares en la memoria.

    En este ejercicio usamos búsqueda simple por keywords.
    En producción usarías embeddings y búsqueda semántica.

    Args:
        query: Consulta a buscar
        memory: Diccionario con la memoria compartida
        top_k: Número de casos más relevantes a retornar

    Returns:
        Lista de casos similares ordenados por relevancia
    """
    # TODO: Implementar búsqueda
    # 1. Obtener palabras de la query
    # 2. Para cada caso en memory["cases"]:
    #    - Calcular overlap de palabras
    #    - Si hay overlap, guardar con score
    # 3. Ordenar por score (descendente)
    # 4. Retornar top_k casos

    # HINT: Usa set intersection para calcular overlap
    # HINT: query.lower().split() para palabras

    pass


def save_to_memory(query: str, solution: str, user_id: str, memory: Dict) -> str:
    """
    Guarda un nuevo caso en memoria.

    Args:
        query: Consulta del usuario
        solution: Solución generada
        user_id: ID del usuario
        memory: Diccionario de memoria (se modifica in-place)

    Returns:
        ID del caso guardado
    """
    # TODO: Implementar guardado
    # 1. Crear nueva entrada con:
    #    - id: case_XXX
    #    - timestamp: datetime.now().isoformat()
    #    - user_id
    #    - query
    #    - solution
    #    - tags: lista de keywords
    #    - success_count: 0
    #    - last_used: timestamp
    # 2. Agregar a memory["cases"]
    # 3. Retornar el ID generado

    # HINT: len(memory.get("cases", [])) para el número de casos
    # HINT: Modifica memory in-place (es un dict mutable)

    pass


def extract_tags(text: str) -> List[str]:
    """
    Extrae tags relevantes de un texto.

    Helper function para categorizar casos.
    """
    # TODO: Implementar extracción simple de tags
    # Buscar keywords técnicas comunes

    keywords = [
        "database", "bd", "postgresql", "mysql",
        "network", "red", "firewall", "puerto",
        "security", "seguridad", "autenticacion", "auth",
        "code", "codigo", "bug", "error",
        "api", "rest", "http", "https"
    ]

    # TODO: Retornar keywords encontradas en el texto

    pass


# =============================================================================
# AGENTES
# =============================================================================

def memory_agent(state: MemoryState) -> dict:
    """
    Agente que busca en memoria casos similares.

    Este agente es el primero en ejecutarse.
    Su trabajo es encontrar si hay casos similares que puedan
    ayudar a resolver el problema actual.

    Args:
        state: Estado actual con la query

    Returns:
        dict con similar_cases actualizado
    """
    print("\n" + "="*70)
    print("🧠 MEMORY AGENT: Buscando casos similares...")
    print("="*70)

    query = state["query"]
    memory = state.get("memory", {"cases": []})

    # TODO: Implementar búsqueda en memoria
    # 1. Llamar a search_similar_cases
    # 2. Si encuentra casos: mostrar información
    # 3. Si no encuentra: indicar que es caso nuevo

    # HINT: Usa search_similar_cases(query, memory)

    print(f"   → Memoria contiene {len(memory.get('cases', []))} casos totales")

    # TODO: Implementar

    return {}


def solution_agent(state: MemoryState) -> dict:
    """
    Agente que genera la solución usando contexto + memoria.

    Este agente es más inteligente si tiene acceso a casos similares.
    Puede aprender de soluciones pasadas y adaptarlas al problema actual.

    Args:
        state: Estado con query y similar_cases

    Returns:
        dict con solution y should_save
    """
    print("\n💡 SOLUTION AGENT: Generando solución...")

    query = state["query"]
    similar_cases = state.get("similar_cases", [])

    # TODO: Construir contexto con casos similares
    # Si hay similar_cases, incluirlos en el prompt
    # Formato:
    # """
    # CASOS SIMILARES RESUELTOS ANTERIORMENTE:
    #
    # 1. Problema: [query del caso]
    #    Solución: [solution del caso]
    #    Éxitos: [success_count]
    # ...
    # """

    similar_context = ""  # TODO: Construir contexto

    if similar_cases:
        print(f"   → Usando {len(similar_cases)} caso(s) similar(es) como referencia")

    # TODO: Crear prompt que incluya:
    # 1. La consulta actual
    # 2. Los casos similares (si existen)
    # 3. Instrucción de generar solución adaptada

    prompt = ""  # TODO: Crear prompt

    # TODO: Invocar LLM

    # TODO: Decidir si guardar en memoria
    # Criterio simple: siempre guardar para aprender
    should_save = True

    print(f"   ✓ Solución generada ({len('solution')} caracteres)")

    # TODO: Retornar solution y should_save

    return {}


def update_memory_agent(state: MemoryState) -> dict:
    """
    Agente que actualiza la memoria con la nueva solución.

    Este agente decide si guardar el caso en memoria persistente.
    No todos los casos deben guardarse (por ejemplo, consultas triviales).

    Args:
        state: Estado con solution y should_save

    Returns:
        dict vacío (solo efecto secundario de actualizar memoria)
    """
    print("\n💾 UPDATE MEMORY: Actualizando memoria...")

    should_save = state.get("should_save", False)
    memory = state.get("memory", {"cases": []})

    if not should_save:
        print("   ℹ Caso no guardado (no amerita memoria persistente)")
        return {}

    query = state["query"]
    solution = state["solution"]
    user_id = state.get("user_id", "unknown")

    # TODO: Guardar en memoria
    # 1. Llamar a save_to_memory
    # 2. Mostrar confirmación

    # HINT: case_id = save_to_memory(query, solution, user_id, memory)

    # TODO: Implementar

    return {}


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo con memoria compartida.

    Flujo simple:
    - memory_agent: Busca casos similares
    - solution_agent: Genera solución usando memoria
    - update_memory_agent: Actualiza memoria con nueva solución
    """
    workflow = StateGraph(MemoryState)

    # TODO: Agregar nodos
    # - memory (memory_agent)
    # - solution (solution_agent)
    # - update_memory (update_memory_agent)

    # TODO: Set entry point a "memory"

    # TODO: Agregar edges
    # memory → solution → update_memory → END

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🧠 SISTEMA CON MEMORIA COMPARTIDA")
    print("="*70)

    # Memoria compartida (en producción sería una BD)
    shared_memory: Dict = {
        "cases": []
    }

    queries = [
        ("user_001", "No puedo conectarme a la base de datos PostgreSQL"),
        ("user_002", "Mi aplicación no puede acceder a PostgreSQL"),
        ("user_001", "El servidor web no responde en el puerto 443"),
        ("user_003", "Error de conexión a la base de datos"),
    ]

    app = build_graph()

    for i, (user_id, query) in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"📋 CONSULTA {i} (Usuario: {user_id}):")
        print(f"{'='*70}")
        print(f"{query}")

        initial_state = {
            "query": query,
            "user_id": user_id,
            "similar_cases": [],
            "solution": "",
            "should_save": False,
            "memory": shared_memory  # Mismo diccionario compartido
        }

        # TODO: Invocar el grafo
        # final_state = app.invoke(initial_state)

        # TODO: Mostrar resultado
        # print("\n" + "="*70)
        # print("📊 SOLUCIÓN")
        # print("="*70)
        # print(final_state["solution"])

        # Mostrar estado de memoria
        print(f"\n📈 Estado de memoria:")
        print(f"   • Total de casos: {len(shared_memory['cases'])}")
        if shared_memory["cases"]:
            print(f"   • Últimos casos guardados:")
            for case in shared_memory["cases"][-3:]:
                print(f"      - {case['id']}: {case['query'][:50]}...")

        if i < len(queries):
            input("\n[Presiona Enter para continuar...]")

    # Mostrar resumen final de memoria
    print("\n" + "="*70)
    print("📚 RESUMEN DE MEMORIA FINAL")
    print("="*70)
    print(f"Total de casos guardados: {len(shared_memory['cases'])}")
    if shared_memory["cases"]:
        print("\nTodos los casos:")
        for case in shared_memory["cases"]:
            print(f"\n{case['id']} ({case['user_id']}):")
            print(f"  Query: {case['query']}")
            print(f"  Tags: {', '.join(case.get('tags', []))}")
            print(f"  Timestamp: {case['timestamp']}")


if __name__ == "__main__":
    main()
