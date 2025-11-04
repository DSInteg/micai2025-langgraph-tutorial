"""
Tests para el Ejercicio 2.2: Paralelización con Agregación
"""

import pytest
from solution import (
    build_graph,
    optimistic_agent,
    pessimistic_agent,
    neutral_agent,
    aggregator_node,
    AnalysisState,
)


def test_optimistic_agent_responds():
    """Test: El agente optimista debe generar análisis"""
    state: AnalysisState = {
        "review": "Buen producto, rápido envío",
        "optimistic_analysis": "",
        "pessimistic_analysis": "",
        "neutral_analysis": "",
        "final_analysis": ""
    }
    result = optimistic_agent(state)
    assert "optimistic_analysis" in result
    assert len(result["optimistic_analysis"]) > 0


def test_pessimistic_agent_responds():
    """Test: El agente pesimista debe generar análisis"""
    state: AnalysisState = {
        "review": "Producto decente pero caro",
        "optimistic_analysis": "",
        "pessimistic_analysis": "",
        "neutral_analysis": "",
        "final_analysis": ""
    }
    result = pessimistic_agent(state)
    assert "pessimistic_analysis" in result
    assert len(result["pessimistic_analysis"]) > 0


def test_neutral_agent_responds():
    """Test: El agente neutral debe generar análisis"""
    state: AnalysisState = {
        "review": "Tiene pros y contras",
        "optimistic_analysis": "",
        "pessimistic_analysis": "",
        "neutral_analysis": "",
        "final_analysis": ""
    }
    result = neutral_agent(state)
    assert "neutral_analysis" in result
    assert len(result["neutral_analysis"]) > 0


def test_aggregator_synthesizes():
    """Test: El aggregator debe sintetizar las tres perspectivas"""
    state: AnalysisState = {
        "review": "Test review",
        "optimistic_analysis": "Muy positivo, excelente producto",
        "pessimistic_analysis": "Tiene varios problemas serios",
        "neutral_analysis": "Balance de pros y contras",
        "final_analysis": ""
    }
    result = aggregator_node(state)
    assert "final_analysis" in result
    assert len(result["final_analysis"]) > 0


def test_graph_builds():
    """Test: El grafo debe construirse sin errores"""
    app = build_graph()
    assert app is not None


def test_graph_end_to_end():
    """Test: El grafo debe ejecutar completamente"""
    app = build_graph()
    initial_state: AnalysisState = {
        "review": "Producto bueno pero con algunos defectos menores",
        "optimistic_analysis": "",
        "pessimistic_analysis": "",
        "neutral_analysis": "",
        "final_analysis": ""
    }

    final_state = app.invoke(initial_state)

    # Verificar que todos los análisis se generaron
    assert len(final_state["optimistic_analysis"]) > 0
    assert len(final_state["pessimistic_analysis"]) > 0
    assert len(final_state["neutral_analysis"]) > 0
    assert len(final_state["final_analysis"]) > 0


def test_parallel_execution_generates_all_analyses():
    """Test: La ejecución paralela debe generar los tres análisis"""
    app = build_graph()
    initial_state: AnalysisState = {
        "review": "Excelente calidad pero precio alto",
        "optimistic_analysis": "",
        "pessimistic_analysis": "",
        "neutral_analysis": "",
        "final_analysis": ""
    }

    final_state = app.invoke(initial_state)

    # Todos los análisis deben estar presentes
    analyses = [
        final_state["optimistic_analysis"],
        final_state["pessimistic_analysis"],
        final_state["neutral_analysis"]
    ]

    for analysis in analyses:
        assert len(analysis) > 0, "Un análisis está vacío"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
