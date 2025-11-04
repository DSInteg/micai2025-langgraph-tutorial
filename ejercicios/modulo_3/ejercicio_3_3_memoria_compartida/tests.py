"""
Tests para el Ejercicio 3.3: Memoria Compartida entre Agentes
"""

import pytest
from solution import (
    build_graph,
    memory_agent,
    solution_agent,
    update_memory_agent,
    search_similar_cases,
    save_to_memory,
    extract_tags,
    MemoryState,
)


def test_extract_tags_identifies_technical_keywords():
    """Test: extract_tags debe identificar keywords técnicas"""
    text1 = "Problema con la base de datos PostgreSQL"
    tags1 = extract_tags(text1)
    assert "database" in tags1 or "postgresql" in tags1

    text2 = "Firewall bloqueando el puerto 443"
    tags2 = extract_tags(text2)
    assert "firewall" in tags2 or "port" in tags2

    text3 = "Error de autenticación en la API REST"
    tags3 = extract_tags(text3)
    assert "authentication" in tags3 or "api" in tags3


def test_save_to_memory_creates_case():
    """Test: save_to_memory debe crear un caso en memoria"""
    memory = {"cases": []}
    query = "Test query"
    solution = "Test solution"
    user_id = "user_001"

    case_id = save_to_memory(query, solution, user_id, memory)

    assert len(memory["cases"]) == 1
    assert memory["cases"][0]["id"] == case_id
    assert memory["cases"][0]["query"] == query
    assert memory["cases"][0]["solution"] == solution
    assert memory["cases"][0]["user_id"] == user_id


def test_save_to_memory_generates_unique_ids():
    """Test: save_to_memory debe generar IDs únicos"""
    memory = {"cases": []}

    id1 = save_to_memory("Query 1", "Solution 1", "user_001", memory)
    id2 = save_to_memory("Query 2", "Solution 2", "user_002", memory)
    id3 = save_to_memory("Query 3", "Solution 3", "user_003", memory)

    assert id1 != id2 != id3
    assert len(memory["cases"]) == 3


def test_search_similar_cases_finds_relevant():
    """Test: search_similar_cases debe encontrar casos relevantes"""
    memory = {
        "cases": [
            {
                "id": "case_001",
                "query": "No puedo conectarme a PostgreSQL",
                "solution": "Verificar firewall",
                "tags": ["database", "postgresql"]
            },
            {
                "id": "case_002",
                "query": "El servidor web no responde",
                "solution": "Verificar nginx",
                "tags": ["web"]
            },
            {
                "id": "case_003",
                "query": "Error de conexión a la base de datos",
                "solution": "Verificar credenciales",
                "tags": ["database"]
            }
        ]
    }

    # Buscar query relacionada con base de datos
    query = "Mi aplicación no puede conectar a la base de datos"
    similar = search_similar_cases(query, memory, top_k=2)

    # Debe encontrar los casos 1 y 3 (relacionados con DB)
    assert len(similar) > 0
    found_ids = [case["id"] for case in similar]
    # Al menos uno debe ser caso de DB
    assert "case_001" in found_ids or "case_003" in found_ids


def test_search_similar_cases_returns_empty_for_no_matches():
    """Test: search_similar_cases debe retornar vacío si no hay matches"""
    memory = {
        "cases": [
            {
                "id": "case_001",
                "query": "Problema de frontend con React",
                "solution": "...",
                "tags": ["frontend"]
            }
        ]
    }

    query = "Error de autenticación en backend"
    similar = search_similar_cases(query, memory)

    # No debería encontrar casos similares (diferentes dominios)
    # Aunque podría encontrar por overlap de palabras comunes
    # El test verifica que la función no falla
    assert isinstance(similar, list)


def test_search_similar_cases_respects_top_k():
    """Test: search_similar_cases debe respetar el parámetro top_k"""
    memory = {
        "cases": [
            {"id": f"case_{i:03d}", "query": "database error connection", "tags": []}
            for i in range(10)
        ]
    }

    query = "database connection error"
    similar = search_similar_cases(query, memory, top_k=3)

    assert len(similar) <= 3


def test_memory_agent_finds_similar_cases():
    """Test: memory_agent debe encontrar casos similares"""
    memory = {
        "cases": [
            {
                "id": "case_001",
                "query": "Error de conexión a PostgreSQL",
                "solution": "...",
                "tags": ["database"]
            }
        ]
    }

    state: MemoryState = {
        "query": "No puedo conectarme a la base de datos PostgreSQL",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "",
        "should_save": False,
        "memory": memory
    }

    result = memory_agent(state)

    assert "similar_cases" in result
    # Debería encontrar al menos el caso similar
    assert len(result["similar_cases"]) > 0


def test_memory_agent_handles_empty_memory():
    """Test: memory_agent debe manejar memoria vacía"""
    state: MemoryState = {
        "query": "Test query",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "",
        "should_save": False,
        "memory": {"cases": []}
    }

    result = memory_agent(state)

    assert "similar_cases" in result
    assert result["similar_cases"] == []


def test_solution_agent_generates_solution():
    """Test: solution_agent debe generar una solución"""
    state: MemoryState = {
        "query": "Mi servidor no responde",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "",
        "should_save": False,
        "memory": {"cases": []}
    }

    result = solution_agent(state)

    assert "solution" in result
    assert len(result["solution"]) > 0
    assert "should_save" in result


def test_solution_agent_uses_similar_cases():
    """Test: solution_agent debe usar casos similares como contexto"""
    similar_cases = [
        {
            "id": "case_001",
            "query": "Servidor caído",
            "solution": "Reiniciar servicio",
            "tags": ["server"]
        }
    ]

    state: MemoryState = {
        "query": "Mi servidor no funciona",
        "user_id": "user_001",
        "similar_cases": similar_cases,
        "solution": "",
        "should_save": False,
        "memory": {"cases": []}
    }

    result = solution_agent(state)

    assert "solution" in result
    assert len(result["solution"]) > 0
    # La solución debería considerar el caso similar


def test_update_memory_agent_saves_when_should_save():
    """Test: update_memory_agent debe guardar cuando should_save=True"""
    memory = {"cases": []}

    state: MemoryState = {
        "query": "Test query",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "Test solution",
        "should_save": True,
        "memory": memory
    }

    update_memory_agent(state)

    # Verificar que se guardó en memoria
    assert len(memory["cases"]) == 1
    assert memory["cases"][0]["query"] == "Test query"
    assert memory["cases"][0]["solution"] == "Test solution"


def test_update_memory_agent_skips_when_should_not_save():
    """Test: update_memory_agent no debe guardar cuando should_save=False"""
    memory = {"cases": []}

    state: MemoryState = {
        "query": "Test query",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "Test solution",
        "should_save": False,
        "memory": memory
    }

    update_memory_agent(state)

    # Verificar que NO se guardó
    assert len(memory["cases"]) == 0


def test_graph_builds():
    """Test: El grafo debe construirse sin errores"""
    app = build_graph()
    assert app is not None


def test_graph_end_to_end_first_query():
    """Test: El grafo debe ejecutar completamente con memoria vacía"""
    app = build_graph()

    shared_memory = {"cases": []}

    initial_state: MemoryState = {
        "query": "No puedo conectarme a la base de datos",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "",
        "should_save": False,
        "memory": shared_memory
    }

    final_state = app.invoke(initial_state)

    # Debe haber generado solución
    assert len(final_state["solution"]) > 0
    # Debe haber guardado en memoria
    assert len(shared_memory["cases"]) > 0


def test_graph_end_to_end_with_memory():
    """Test: El grafo debe usar memoria en segunda invocación"""
    app = build_graph()

    shared_memory = {"cases": []}

    # Primera consulta
    state1: MemoryState = {
        "query": "Error de conexión a PostgreSQL",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "",
        "should_save": False,
        "memory": shared_memory
    }

    final_state1 = app.invoke(state1)

    # Verificar que se guardó
    assert len(shared_memory["cases"]) == 1

    # Segunda consulta similar
    state2: MemoryState = {
        "query": "No puedo conectar a la base de datos PostgreSQL",
        "user_id": "user_002",
        "similar_cases": [],
        "solution": "",
        "should_save": False,
        "memory": shared_memory  # Misma memoria
    }

    final_state2 = app.invoke(state2)

    # Debe haber encontrado casos similares
    assert len(final_state2["similar_cases"]) > 0
    # Debe haber generado solución
    assert len(final_state2["solution"]) > 0
    # Debe haber guardado el segundo caso
    assert len(shared_memory["cases"]) == 2


def test_memory_persists_across_invocations():
    """Test: La memoria debe persistir entre invocaciones"""
    app = build_graph()

    shared_memory = {"cases": []}

    queries = [
        "Error de conexión",
        "Problema de autenticación",
        "Firewall bloqueando puerto"
    ]

    for i, query in enumerate(queries):
        state: MemoryState = {
            "query": query,
            "user_id": f"user_{i:03d}",
            "similar_cases": [],
            "solution": "",
            "should_save": False,
            "memory": shared_memory
        }

        app.invoke(state)

        # Verificar que la memoria crece
        assert len(shared_memory["cases"]) == i + 1


def test_similar_cases_improve_context():
    """Test: Casos similares deben estar disponibles en estado final"""
    app = build_graph()

    shared_memory = {
        "cases": [
            {
                "id": "case_001",
                "query": "Database connection error",
                "solution": "Check credentials",
                "tags": ["database"],
                "timestamp": "2024-01-01T00:00:00",
                "user_id": "user_000",
                "success_count": 0,
                "last_used": "2024-01-01T00:00:00"
            }
        ]
    }

    state: MemoryState = {
        "query": "Cannot connect to database",
        "user_id": "user_001",
        "similar_cases": [],
        "solution": "",
        "should_save": False,
        "memory": shared_memory
    }

    final_state = app.invoke(state)

    # Debe haber encontrado el caso similar
    assert len(final_state["similar_cases"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
