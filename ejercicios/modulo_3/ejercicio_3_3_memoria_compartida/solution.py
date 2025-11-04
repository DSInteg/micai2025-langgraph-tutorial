"""
Ejercicio 3.3: Memoria Compartida entre Agentes - SOLUCIÓN COMPLETA

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

    La clave de este ejercicio es que 'memory' se comparte
    entre múltiples invocaciones del grafo, permitiendo
    aprendizaje acumulativo.
    """
    query: str                   # Consulta actual del usuario
    user_id: str                # ID del usuario
    similar_cases: List[Dict]   # Casos similares encontrados
    solution: str               # Solución generada
    should_save: bool           # Si guardar en memoria
    memory: Dict                # Memoria compartida (persistente)


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# =============================================================================
# FUNCIONES DE GESTIÓN DE MEMORIA
# =============================================================================

def search_similar_cases(query: str, memory: Dict, top_k: int = 3) -> List[Dict]:
    """
    Busca casos similares en la memoria usando búsqueda por keywords.

    Algoritmo simple:
    1. Tokenizar query en palabras
    2. Para cada caso, calcular overlap de palabras
    3. Ordenar por overlap (relevancia)
    4. Retornar top-k

    En producción, usarías:
    - Embeddings (OpenAI, Sentence Transformers)
    - Vector databases (Pinecone, Weaviate, ChromaDB)
    - Búsqueda semántica con cosine similarity

    Args:
        query: Consulta a buscar
        memory: Diccionario con casos previos
        top_k: Número de casos más relevantes

    Returns:
        Lista de hasta top_k casos más similares
    """
    if "cases" not in memory or not memory["cases"]:
        return []

    query_lower = query.lower()
    query_words = set(query_lower.split())

    # Calcular relevancia para cada caso
    scored_cases = []
    for case in memory["cases"]:
        case_query = case["query"].lower()
        case_words = set(case_query.split())

        # Intersección de palabras (Jaccard similarity simplificado)
        overlap = len(query_words & case_words)

        if overlap > 0:
            # Score más alto para casos con más overlap
            # También considerar tags si existen
            tag_bonus = 0
            if "tags" in case:
                case_tags = set(case["tags"])
                # Verificar si algún tag aparece en la query
                for tag in case_tags:
                    if tag.lower() in query_lower:
                        tag_bonus += 1

            total_score = overlap + (tag_bonus * 0.5)
            scored_cases.append((total_score, case))

    # Ordenar por score (descendente) y retornar top-k
    scored_cases.sort(reverse=True, key=lambda x: x[0])
    return [case for score, case in scored_cases[:top_k]]


def save_to_memory(query: str, solution: str, user_id: str, memory: Dict) -> str:
    """
    Guarda un nuevo caso en memoria persistente.

    La memoria se modifica in-place (dict mutable) para simular
    persistencia. En producción, escribirías a una base de datos.

    Args:
        query: Consulta del usuario
        solution: Solución generada
        user_id: ID del usuario
        memory: Diccionario de memoria (modificado in-place)

    Returns:
        ID del caso guardado
    """
    # Inicializar lista de casos si no existe
    if "cases" not in memory:
        memory["cases"] = []

    # Generar ID único
    case_id = f"case_{len(memory['cases']) + 1:03d}"

    # Crear entrada de caso
    new_case = {
        "id": case_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": user_id,
        "query": query,
        "solution": solution,
        "tags": extract_tags(query + " " + solution),
        "success_count": 0,
        "last_used": datetime.datetime.now().isoformat()
    }

    # Agregar a memoria
    memory["cases"].append(new_case)

    return case_id


def extract_tags(text: str) -> List[str]:
    """
    Extrae tags relevantes de un texto.

    Usa keyword matching simple. En producción, podrías usar:
    - NER (Named Entity Recognition)
    - LLM para extraer conceptos clave
    - Clasificación automática
    """
    # Keywords técnicas comunes
    technical_keywords = {
        # Databases
        "database": "database",
        "bd": "database",
        "postgresql": "postgresql",
        "postgres": "postgresql",
        "mysql": "mysql",
        "mongodb": "mongodb",
        "sql": "sql",

        # Network
        "network": "network",
        "red": "network",
        "firewall": "firewall",
        "puerto": "port",
        "port": "port",
        "dns": "dns",
        "conectividad": "connectivity",
        "connectivity": "connectivity",

        # Security
        "security": "security",
        "seguridad": "security",
        "autenticacion": "authentication",
        "autenticación": "authentication",
        "authentication": "authentication",
        "auth": "authentication",
        "permisos": "permissions",
        "permissions": "permissions",
        "vulnerabilidad": "vulnerability",

        # Code
        "code": "code",
        "codigo": "code",
        "código": "code",
        "bug": "bug",
        "error": "error",
        "exception": "exception",

        # Web
        "api": "api",
        "rest": "rest",
        "http": "http",
        "https": "https",
        "ssl": "ssl",
        "tls": "tls",
        "certificado": "certificate",
        "certificate": "certificate"
    }

    text_lower = text.lower()
    found_tags = set()

    for keyword, tag in technical_keywords.items():
        if keyword in text_lower:
            found_tags.add(tag)

    return sorted(list(found_tags))


# =============================================================================
# AGENTES
# =============================================================================

def memory_agent(state: MemoryState) -> dict:
    """
    Agente que busca en memoria casos similares.

    Este agente implementa el primer paso del pattern:
    "¿Hemos visto algo similar antes?"

    Si encuentra casos similares, los prepara para que
    solution_agent los use como contexto.
    """
    print("\n" + "="*70)
    print("🧠 MEMORY AGENT: Buscando casos similares...")
    print("="*70)

    query = state["query"]
    memory = state.get("memory", {"cases": []})

    print(f"   → Memoria contiene {len(memory.get('cases', []))} casos totales")

    # Buscar casos similares
    similar_cases = search_similar_cases(query, memory, top_k=3)

    if similar_cases:
        print(f"   ✓ Encontrados {len(similar_cases)} casos similares:")
        for i, case in enumerate(similar_cases, 1):
            print(f"      {i}. {case['id']}: {case['query'][:60]}...")
            if "tags" in case and case["tags"]:
                print(f"         Tags: {', '.join(case['tags'])}")
    else:
        print("   ℹ No hay casos similares en memoria (caso nuevo)")

    return {"similar_cases": similar_cases}


def solution_agent(state: MemoryState) -> dict:
    """
    Agente que genera la solución usando contexto + memoria.

    Este agente es más efectivo cuando tiene acceso a casos similares:
    - Puede aprender de soluciones pasadas
    - Puede adaptar soluciones exitosas
    - Puede evitar errores previos

    La calidad de las soluciones mejora con el tiempo a medida
    que la memoria crece.
    """
    print("\n💡 SOLUTION AGENT: Generando solución...")

    query = state["query"]
    similar_cases = state.get("similar_cases", [])

    # Construir contexto con casos similares
    similar_context = ""
    if similar_cases:
        similar_context = "\n\nCASOS SIMILARES RESUELTOS ANTERIORMENTE:\n"
        for i, case in enumerate(similar_cases, 1):
            similar_context += f"\n{i}. Problema: {case['query']}\n"
            similar_context += f"   Solución: {case['solution']}\n"
            if "success_count" in case and case["success_count"] > 0:
                similar_context += f"   Éxitos: {case['success_count']}\n"
            if "tags" in case:
                similar_context += f"   Tags: {', '.join(case['tags'])}\n"

        print(f"   → Usando {len(similar_cases)} caso(s) similar(es) como referencia")

    # Crear prompt adaptativo
    prompt = f"""Eres un especialista en soporte técnico que aprende de experiencias pasadas.

CONSULTA ACTUAL:
{query}

{similar_context}

Genera una solución detallada y práctica para la consulta actual.

{"Si hay casos similares arriba, CONSIDERA esas soluciones como referencia, pero ADÁPTALAS específicamente al problema actual. No copies textualmente, sino aprende de ellas." if similar_cases else "Este es un caso nuevo sin precedentes en la memoria. Genera una solución original y completa."}

La solución debe incluir:
1. Diagnóstico del problema
2. Pasos específicos para resolverlo
3. Explicación de por qué funciona
4. Prevención de problemas futuros

SOLUCIÓN DETALLADA:"""

    response = llm.invoke(prompt)
    solution = response.content

    # Decidir si guardar en memoria
    # Criterio: Siempre guardar para construir conocimiento
    # En producción podrías:
    # - Solo guardar si es suficientemente diferente de casos existentes
    # - Solo guardar si el usuario confirma que funcionó
    # - Solo guardar casos de cierta complejidad
    should_save = True

    print(f"   ✓ Solución generada ({len(solution)} caracteres)")
    print(f"   → Guardar en memoria: {'Sí' if should_save else 'No'}")

    return {
        "solution": solution,
        "should_save": should_save
    }


def update_memory_agent(state: MemoryState) -> dict:
    """
    Agente que actualiza la memoria con la nueva solución.

    Este agente implementa el aprendizaje del sistema:
    cada caso resuelto se convierte en conocimiento para el futuro.

    En producción, este agente podría:
    - Escribir a una base de datos
    - Generar embeddings y guardar en vector DB
    - Actualizar índices de búsqueda
    - Notificar a otros sistemas
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

    # Guardar en memoria
    case_id = save_to_memory(query, solution, user_id, memory)

    print(f"   ✓ Caso guardado: {case_id}")
    print(f"   → Total de casos en memoria: {len(memory['cases'])}")

    return {}


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo con memoria compartida.

    Flujo lineal simple:
    1. memory_agent: Busca casos similares
    2. solution_agent: Genera solución (mejor si hay memoria)
    3. update_memory_agent: Guarda nuevo caso
    4. END

    La magia está en que 'memory' persiste entre invocaciones,
    permitiendo que el sistema aprenda continuamente.
    """
    workflow = StateGraph(MemoryState)

    # Agregar nodos
    workflow.add_node("memory", memory_agent)
    workflow.add_node("solution", solution_agent)
    workflow.add_node("update_memory", update_memory_agent)

    # Entry point
    workflow.set_entry_point("memory")

    # Flujo lineal
    workflow.add_edge("memory", "solution")
    workflow.add_edge("solution", "update_memory")
    workflow.add_edge("update_memory", END)

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🧠 SISTEMA CON MEMORIA COMPARTIDA")
    print("="*70)
    print("\nEste sistema demuestra cómo los agentes aprenden de experiencias pasadas.")
    print("Observa cómo las soluciones mejoran a medida que se acumula conocimiento.\n")

    # Memoria compartida (simula persistencia)
    # En producción, esto sería una base de datos
    shared_memory: Dict = {
        "cases": []
    }

    # Consultas de ejemplo que muestran aprendizaje
    queries = [
        ("user_001", "No puedo conectarme a la base de datos PostgreSQL, me da error de conexión rechazada"),
        ("user_002", "Mi aplicación no puede acceder a PostgreSQL, dice connection refused"),
        ("user_001", "El servidor web no responde en el puerto 443, creo que es un problema de certificado SSL"),
        ("user_003", "Error de conexión a la base de datos, no sé qué hacer"),
        ("user_004", "El certificado SSL expiró y ahora no puedo acceder al servidor HTTPS"),
    ]

    app = build_graph()

    for i, (user_id, query) in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"📋 CONSULTA {i}/5 (Usuario: {user_id}):")
        print(f"{'='*70}")
        print(f"{query}")

        initial_state = {
            "query": query,
            "user_id": user_id,
            "similar_cases": [],
            "solution": "",
            "should_save": False,
            "memory": shared_memory  # ¡El mismo diccionario compartido!
        }

        # Ejecutar grafo
        final_state = app.invoke(initial_state)

        print("\n" + "="*70)
        print("📊 SOLUCIÓN GENERADA")
        print("="*70)
        print(final_state["solution"])

        # Mostrar estado de memoria después de cada consulta
        print(f"\n📈 Estado de memoria después de consulta {i}:")
        print(f"   • Total de casos guardados: {len(shared_memory['cases'])}")

        if shared_memory["cases"]:
            print(f"   • Casos recientes:")
            for case in shared_memory["cases"][-min(3, len(shared_memory['cases'])):]:
                print(f"      - {case['id']}: {case['query'][:50]}...")
                if case.get("tags"):
                    print(f"        Tags: {', '.join(case['tags'])}")

        if i < len(queries):
            input("\n[Presiona Enter para la siguiente consulta...]")

    # Mostrar análisis final de memoria
    print("\n" + "="*70)
    print("📚 ANÁLISIS FINAL DE MEMORIA")
    print("="*70)

    print(f"\nTotal de casos guardados: {len(shared_memory['cases'])}")

    # Estadísticas de tags
    all_tags = {}
    for case in shared_memory["cases"]:
        for tag in case.get("tags", []):
            all_tags[tag] = all_tags.get(tag, 0) + 1

    if all_tags:
        print("\n📊 Temas más comunes (por tags):")
        sorted_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags[:5]:
            print(f"   • {tag}: {count} casos")

    # Usuarios más activos
    user_counts = {}
    for case in shared_memory["cases"]:
        user = case["user_id"]
        user_counts[user] = user_counts.get(user, 0) + 1

    print("\n👥 Usuarios más activos:")
    sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
    for user, count in sorted_users:
        print(f"   • {user}: {count} consultas")

    # Mostrar todos los casos
    print("\n📝 Detalle de todos los casos guardados:")
    for case in shared_memory["cases"]:
        print(f"\n{case['id']} - {case['timestamp']}")
        print(f"   Usuario: {case['user_id']}")
        print(f"   Query: {case['query'][:80]}...")
        print(f"   Solution: {case['solution'][:100]}...")
        print(f"   Tags: {', '.join(case.get('tags', []))}")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)
    print("\n💡 Observaciones sobre Memoria Compartida:")
    print("   • La memoria permite aprendizaje acumulativo")
    print("   • Cada caso resuelto mejora las futuras soluciones")
    print("   • Los casos similares aceleran la resolución")
    print("   • El sistema se vuelve más inteligente con el uso")
    print("   • En producción: usar vector DB para búsqueda semántica")
    print("\n🚀 Próximos pasos:")
    print("   • Implementar embeddings para búsqueda semántica")
    print("   • Agregar rating de soluciones por usuarios")
    print("   • Implementar memory pruning (limpiar casos obsoletos)")
    print("   • Detectar patrones comunes automáticamente")


if __name__ == "__main__":
    main()
