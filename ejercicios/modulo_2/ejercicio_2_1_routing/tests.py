"""
Tests para el Ejercicio 2.1: Sistema de Routing

Estos tests verifican que el sistema de routing funcione correctamente:
- El clasificador categoriza correctamente
- El routing dirige al agente apropiado
- Cada agente responde adecuadamente
- El grafo está correctamente estructurado
"""

import pytest
from solution import (
    build_graph,
    classifier_node,
    route_query,
    technical_agent,
    sales_agent,
    support_agent,
    RouterState,
)


# =============================================================================
# TESTS DEL CLASIFICADOR
# =============================================================================

def test_classifier_technical_queries():
    """
    Test: El clasificador debe categorizar consultas técnicas correctamente
    """
    technical_queries = [
        "Mi app no funciona y me da error 500",
        "¿Cómo configuro la autenticación?",
        "Tengo un bug en el sistema",
    ]

    for query in technical_queries:
        state: RouterState = {
            "query": query,
            "category": "",
            "response": ""
        }
        result = classifier_node(state)
        assert result["category"] == "technical", \
            f"Consulta técnica mal clasificada: '{query}' → {result['category']}"


def test_classifier_sales_queries():
    """
    Test: El clasificador debe categorizar consultas de ventas correctamente
    """
    sales_queries = [
        "¿Cuánto cuesta el plan pro?",
        "Quiero comprar 5 licencias",
        "¿Tienen promociones disponibles?",
    ]

    for query in sales_queries:
        state: RouterState = {
            "query": query,
            "category": "",
            "response": ""
        }
        result = classifier_node(state)
        assert result["category"] == "sales", \
            f"Consulta de ventas mal clasificada: '{query}' → {result['category']}"


def test_classifier_support_queries():
    """
    Test: El clasificador debe categorizar consultas de soporte correctamente
    """
    support_queries = [
        "Quiero devolver un producto",
        "¿Cuál es su política de garantía?",
        "Necesito un reembolso",
    ]

    for query in support_queries:
        state: RouterState = {
            "query": query,
            "category": "",
            "response": ""
        }
        result = classifier_node(state)
        assert result["category"] == "support", \
            f"Consulta de soporte mal clasificada: '{query}' → {result['category']}"


def test_classifier_returns_valid_category():
    """
    Test: El clasificador debe retornar solo categorías válidas
    """
    state: RouterState = {
        "query": "Consulta aleatoria de prueba",
        "category": "",
        "response": ""
    }
    result = classifier_node(state)

    valid_categories = ["technical", "sales", "support"]
    assert result["category"] in valid_categories, \
        f"Categoría inválida: {result['category']}"


# =============================================================================
# TESTS DE ROUTING
# =============================================================================

def test_route_query_technical():
    """
    Test: route_query debe dirigir consultas técnicas al agente técnico
    """
    state: RouterState = {
        "query": "test query",
        "category": "technical",
        "response": ""
    }
    next_node = route_query(state)
    assert next_node == "technical_agent"


def test_route_query_sales():
    """
    Test: route_query debe dirigir consultas de ventas al agente de ventas
    """
    state: RouterState = {
        "query": "test query",
        "category": "sales",
        "response": ""
    }
    next_node = route_query(state)
    assert next_node == "sales_agent"


def test_route_query_support():
    """
    Test: route_query debe dirigir consultas de soporte al agente de soporte
    """
    state: RouterState = {
        "query": "test query",
        "category": "support",
        "response": ""
    }
    next_node = route_query(state)
    assert next_node == "support_agent"


# =============================================================================
# TESTS DE AGENTES ESPECIALIZADOS
# =============================================================================

def test_technical_agent_responds():
    """
    Test: El agente técnico debe generar una respuesta
    """
    state: RouterState = {
        "query": "Mi app no funciona",
        "category": "technical",
        "response": ""
    }
    result = technical_agent(state)

    assert "response" in result
    assert len(result["response"]) > 0
    assert isinstance(result["response"], str)


def test_sales_agent_responds():
    """
    Test: El agente de ventas debe generar una respuesta
    """
    state: RouterState = {
        "query": "¿Cuánto cuesta?",
        "category": "sales",
        "response": ""
    }
    result = sales_agent(state)

    assert "response" in result
    assert len(result["response"]) > 0
    assert isinstance(result["response"], str)


def test_support_agent_responds():
    """
    Test: El agente de soporte debe generar una respuesta
    """
    state: RouterState = {
        "query": "Quiero devolver un producto",
        "category": "support",
        "response": ""
    }
    result = support_agent(state)

    assert "response" in result
    assert len(result["response"]) > 0
    assert isinstance(result["response"], str)


# =============================================================================
# TESTS DE GRAFO COMPLETO
# =============================================================================

def test_graph_builds_successfully():
    """
    Test: El grafo debe construirse sin errores
    """
    app = build_graph()
    assert app is not None


def test_graph_end_to_end_technical():
    """
    Test: El grafo debe procesar una consulta técnica de principio a fin
    """
    app = build_graph()
    initial_state = {
        "query": "Tengo un error 404 en mi aplicación",
        "category": "",
        "response": ""
    }

    final_state = app.invoke(initial_state)

    # Verificar que se asignó la categoría
    assert final_state["category"] == "technical"

    # Verificar que se generó una respuesta
    assert len(final_state["response"]) > 0


def test_graph_end_to_end_sales():
    """
    Test: El grafo debe procesar una consulta de ventas de principio a fin
    """
    app = build_graph()
    initial_state = {
        "query": "¿Cuánto cuesta el plan empresarial?",
        "category": "",
        "response": ""
    }

    final_state = app.invoke(initial_state)

    # Verificar que se asignó la categoría
    assert final_state["category"] == "sales"

    # Verificar que se generó una respuesta
    assert len(final_state["response"]) > 0


def test_graph_end_to_end_support():
    """
    Test: El grafo debe procesar una consulta de soporte de principio a fin
    """
    app = build_graph()
    initial_state = {
        "query": "Necesito devolver un producto defectuoso",
        "category": "",
        "response": ""
    }

    final_state = app.invoke(initial_state)

    # Verificar que se asignó la categoría
    assert final_state["category"] == "support"

    # Verificar que se generó una respuesta
    assert len(final_state["response"]) > 0


def test_graph_preserves_original_query():
    """
    Test: El grafo debe preservar la consulta original
    """
    app = build_graph()
    original_query = "Esta es una consulta de prueba"
    initial_state = {
        "query": original_query,
        "category": "",
        "response": ""
    }

    final_state = app.invoke(initial_state)

    assert final_state["query"] == original_query


# =============================================================================
# TESTS DE CASOS EDGE
# =============================================================================

def test_ambiguous_query_is_classified():
    """
    Test: El sistema debe manejar consultas ambiguas sin crashear
    """
    app = build_graph()
    initial_state = {
        "query": "Hola, necesito ayuda",
        "category": "",
        "response": ""
    }

    # No debe crashear
    try:
        final_state = app.invoke(initial_state)
        # Debe asignar alguna categoría
        assert final_state["category"] in ["technical", "sales", "support"]
        # Debe generar alguna respuesta
        assert len(final_state["response"]) > 0
    except Exception as e:
        pytest.fail(f"El sistema crasheó con consulta ambigua: {str(e)}")


def test_complex_query_is_handled():
    """
    Test: El sistema debe manejar consultas complejas multi-dominio
    """
    app = build_graph()
    # Consulta que podría pertenecer a múltiples categorías
    initial_state = {
        "query": "Compré el producto pero no funciona y quiero devolverlo",
        "category": "",
        "response": ""
    }

    try:
        final_state = app.invoke(initial_state)
        # Debe elegir una categoría (probablemente support o technical)
        assert final_state["category"] in ["technical", "support"]
        assert len(final_state["response"]) > 0
    except Exception as e:
        pytest.fail(f"El sistema crasheó con consulta compleja: {str(e)}")


def test_very_short_query():
    """
    Test: El sistema debe manejar consultas muy cortas
    """
    app = build_graph()
    initial_state = {
        "query": "Precio?",
        "category": "",
        "response": ""
    }

    try:
        final_state = app.invoke(initial_state)
        # Probablemente debe ir a sales
        assert final_state["category"] in ["technical", "sales", "support"]
        assert len(final_state["response"]) > 0
    except Exception as e:
        pytest.fail(f"El sistema crasheó con consulta corta: {str(e)}")


# =============================================================================
# TESTS DE CALIDAD DE RESPUESTAS
# =============================================================================

def test_technical_response_has_technical_content():
    """
    Test: Las respuestas técnicas deben tener contenido técnico
    """
    state: RouterState = {
        "query": "Mi aplicación muestra error 500",
        "category": "technical",
        "response": ""
    }
    result = technical_agent(state)

    # La respuesta debería mencionar aspectos técnicos
    # (esto es una verificación simple, no perfecta)
    response_lower = result["response"].lower()
    technical_terms = ["error", "problema", "solución", "paso", "verifica"]

    assert any(term in response_lower for term in technical_terms), \
        "La respuesta técnica no parece contener contenido técnico"


def test_sales_response_has_sales_content():
    """
    Test: Las respuestas de ventas deben tener contenido de ventas
    """
    state: RouterState = {
        "query": "¿Cuánto cuesta el producto?",
        "category": "sales",
        "response": ""
    }
    result = sales_agent(state)

    response_lower = result["response"].lower()
    sales_terms = ["precio", "plan", "producto", "incluye", "opción"]

    assert any(term in response_lower for term in sales_terms), \
        "La respuesta de ventas no parece contener contenido de ventas"


# =============================================================================
# EJECUCIÓN DE TESTS
# =============================================================================

if __name__ == "__main__":
    """
    Ejecutar tests con pytest:
        pytest tests.py -v

    O ejecutar este archivo directamente:
        python tests.py
    """
    print("Ejecutando tests del Ejercicio 2.1...")
    print("=" * 70)
    pytest.main([__file__, "-v", "--tb=short"])
