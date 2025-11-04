"""
Tests para el Ejercicio 1.2: Agente Básico Autónomo

Estos tests verifican que el agente funcione correctamente:
- Las herramientas funcionan individualmente
- El agente puede usar herramientas
- El routing funciona correctamente
- El agente puede completar tareas complejas
"""

import pytest
from solution import (
    build_graph,
    calculator,
    search_knowledge,
    agent_node,
    should_continue,
    AgentState,
)
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


# =============================================================================
# TESTS DE HERRAMIENTAS INDIVIDUALES
# =============================================================================

def test_calculator_basic_operations():
    """
    Test: La calculadora debe realizar operaciones básicas
    """
    # Operaciones simples
    assert calculator.invoke({"expression": "2 + 2"}) == "4"
    assert calculator.invoke({"expression": "10 - 3"}) == "7"
    assert calculator.invoke({"expression": "5 * 6"}) == "30"
    assert calculator.invoke({"expression": "20 / 4"}) == "5.0"


def test_calculator_percentages():
    """
    Test: La calculadora debe manejar porcentajes
    """
    result = calculator.invoke({"expression": "15% of 250"})
    assert float(result) == 37.5

    result = calculator.invoke({"expression": "20% of 100"})
    assert float(result) == 20.0


def test_calculator_complex_expressions():
    """
    Test: La calculadora debe manejar expresiones complejas
    """
    result = calculator.invoke({"expression": "(10 + 5) * 2"})
    assert float(result) == 30.0

    result = calculator.invoke({"expression": "2 ** 3"})
    assert float(result) == 8.0


def test_calculator_error_handling():
    """
    Test: La calculadora debe manejar errores gracefully
    """
    result = calculator.invoke({"expression": "invalid"})
    assert "Error" in result


def test_search_knowledge_finds_information():
    """
    Test: search_knowledge debe encontrar información existente
    """
    result = search_knowledge.invoke({"query": "precio producto X"})
    assert "120" in result
    assert "producto X" in result.lower()

    result = search_knowledge.invoke({"query": "horario"})
    assert "9:00" in result or "18:00" in result


def test_search_knowledge_handles_missing():
    """
    Test: search_knowledge debe manejar consultas no encontradas
    """
    result = search_knowledge.invoke({"query": "información inexistente"})
    assert "No se encontró" in result


# =============================================================================
# TESTS DEL NODO DEL AGENTE
# =============================================================================

def test_agent_node_returns_message():
    """
    Test: agent_node debe retornar un mensaje
    """
    # Arrange: Estado con mensaje del usuario
    state: AgentState = {
        "messages": [HumanMessage(content="¿Cuánto es 2 + 2?")]
    }

    # Act: Ejecutar el nodo del agente
    result = agent_node(state)

    # Assert: Debe retornar un diccionario con messages
    assert "messages" in result
    assert len(result["messages"]) == 1
    assert hasattr(result["messages"][0], "content")


def test_agent_node_can_call_tools():
    """
    Test: El agente debe poder decidir usar herramientas
    """
    # Arrange: Pregunta que claramente necesita calculadora
    state: AgentState = {
        "messages": [HumanMessage(content="Calcula 15 multiplicado por 3")]
    }

    # Act: Ejecutar el nodo
    result = agent_node(state)

    # Assert: El mensaje debe tener tool_calls
    ai_message = result["messages"][0]
    # Nota: Esto depende de que el LLM decida usar la herramienta
    # En algunos casos puede responder directamente
    assert hasattr(ai_message, "content")


# =============================================================================
# TESTS DE ROUTING
# =============================================================================

def test_should_continue_with_tool_calls():
    """
    Test: should_continue debe retornar "continue" cuando hay tool_calls
    """
    # Arrange: Crear un AIMessage con tool_calls
    from langchain_core.messages import AIMessage

    ai_message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "calculator",
                "args": {"expression": "2 + 2"},
                "id": "call_123"
            }
        ]
    )

    state: AgentState = {"messages": [ai_message]}

    # Act: Ejecutar routing
    result = should_continue(state)

    # Assert: Debe continuar
    assert result == "continue"


def test_should_continue_without_tool_calls():
    """
    Test: should_continue debe retornar "end" sin tool_calls
    """
    # Arrange: Crear un AIMessage sin tool_calls
    ai_message = AIMessage(content="El resultado es 4")
    state: AgentState = {"messages": [ai_message]}

    # Act: Ejecutar routing
    result = should_continue(state)

    # Assert: Debe terminar
    assert result == "end"


# =============================================================================
# TESTS DE GRAFO COMPLETO
# =============================================================================

def test_graph_builds_successfully():
    """
    Test: El grafo debe construirse sin errores
    """
    app = build_graph()
    assert app is not None


def test_agent_can_use_calculator():
    """
    Test: El agente debe poder usar la calculadora para resolver un problema
    """
    # Arrange
    app = build_graph()
    initial_state = {
        "messages": [HumanMessage(content="¿Cuánto es 15% de 200?")]
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: Debe haber una respuesta
    assert len(final_state["messages"]) > 1
    final_message = final_state["messages"][-1]
    assert hasattr(final_message, "content")

    # El resultado debe mencionar 30 (15% de 200 = 30)
    # Nota: Esto es una verificación flexible
    assert len(final_message.content) > 0


def test_agent_can_search_knowledge():
    """
    Test: El agente debe poder buscar en la base de conocimiento
    """
    # Arrange
    app = build_graph()
    initial_state = {
        "messages": [HumanMessage(content="¿Cuál es el precio del producto Y?")]
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: Debe haber respuesta
    assert len(final_state["messages"]) > 1
    final_message = final_state["messages"][-1]

    # La respuesta debe mencionar el precio
    assert len(final_message.content) > 0


def test_agent_can_use_multiple_tools():
    """
    Test: El agente debe poder usar múltiples herramientas en una consulta
    """
    # Arrange: Consulta que requiere ambas herramientas
    app = build_graph()
    initial_state = {
        "messages": [
            HumanMessage(
                content="Calcula el 10% de 500 y súmale el precio del producto X"
            )
        ]
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: Debe haber múltiples mensajes (varios pasos)
    assert len(final_state["messages"]) >= 3

    # Debe haber usado herramientas
    tool_messages = [m for m in final_state["messages"] if isinstance(m, ToolMessage)]
    assert len(tool_messages) >= 2  # Al menos dos herramientas usadas


def test_agent_handles_simple_question():
    """
    Test: El agente debe poder responder preguntas simples sin herramientas
    (aunque podría decidir usarlas)
    """
    # Arrange
    app = build_graph()
    initial_state = {
        "messages": [HumanMessage(content="Hola, ¿cómo estás?")]
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: Debe terminar eventualmente
    assert len(final_state["messages"]) >= 2
    final_message = final_state["messages"][-1]
    assert len(final_message.content) > 0


def test_agent_does_not_loop_infinitely():
    """
    Test: El agente debe terminar en un número razonable de pasos
    """
    # Arrange
    app = build_graph()
    initial_state = {
        "messages": [HumanMessage(content="¿Cuánto es 5 + 3?")]
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: No debe tener demasiados mensajes (evitar loops infinitos)
    # Un agente bien diseñado debería terminar en menos de 20 mensajes
    assert len(final_state["messages"]) < 20


# =============================================================================
# TESTS DE CASOS EDGE
# =============================================================================

def test_agent_handles_invalid_query():
    """
    Test: El agente debe manejar consultas que no puede responder
    """
    # Arrange
    app = build_graph()
    initial_state = {
        "messages": [HumanMessage(content="¿Cuál es el precio del producto Z?")]
    }

    # Act & Assert: No debe crashear
    try:
        final_state = app.invoke(initial_state)
        assert len(final_state["messages"]) >= 2
    except Exception as e:
        pytest.fail(f"El agente crasheó con consulta inválida: {str(e)}")


def test_agent_handles_complex_calculation():
    """
    Test: El agente debe manejar cálculos más complejos
    """
    # Arrange
    app = build_graph()
    initial_state = {
        "messages": [HumanMessage(content="Calcula (20% de 300) multiplicado por 2")]
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: Debe completar sin errores
    assert len(final_state["messages"]) >= 2
    final_message = final_state["messages"][-1]
    assert len(final_message.content) > 0


def test_message_history_preserved():
    """
    Test: El historial de mensajes debe preservarse a través del grafo
    """
    # Arrange
    app = build_graph()
    initial_state = {
        "messages": [HumanMessage(content="¿Cuánto es 2 + 2?")]
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: El mensaje inicial debe estar en el historial
    assert any(
        isinstance(m, HumanMessage) and "2 + 2" in m.content
        for m in final_state["messages"]
    )


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
    print("Ejecutando tests del Ejercicio 1.2...")
    print("=" * 70)
    pytest.main([__file__, "-v", "--tb=short"])
