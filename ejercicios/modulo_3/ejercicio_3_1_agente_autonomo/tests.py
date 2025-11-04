"""
Tests para el Ejercicio 3.1: Agente con Planificación Dinámica
"""

import pytest
from solution import (
    build_graph,
    planner_node,
    executor_node,
    evaluator_node,
    finish_node,
    route_decision,
    PlanExecuteState,
)


def test_planner_creates_plan():
    """Test: El planner debe crear un plan"""
    state: PlanExecuteState = {
        "objective": "Buscar información sobre IA",
        "plan": "",
        "current_step": 0,
        "observations": [],
        "decision": "",
        "final_response": ""
    }
    result = planner_node(state)

    assert "plan" in result
    assert len(result["plan"]) > 0
    assert result["current_step"] == 0
    assert "observations" in result


def test_executor_executes_step():
    """Test: El executor debe ejecutar un paso"""
    state: PlanExecuteState = {
        "objective": "Test",
        "plan": "1. Buscar información\n2. Analizar resultados",
        "current_step": 0,
        "observations": [],
        "decision": "",
        "final_response": ""
    }
    result = executor_node(state)

    assert "observations" in result
    assert len(result["observations"]) > 0
    assert result["current_step"] == 1


def test_evaluator_makes_decision():
    """Test: El evaluator debe tomar una decisión"""
    state: PlanExecuteState = {
        "objective": "Test",
        "plan": "1. Test step",
        "current_step": 1,
        "observations": [{"step": 0, "action": "test", "result": "done"}],
        "decision": "",
        "final_response": ""
    }
    result = evaluator_node(state)

    assert "decision" in result
    assert result["decision"] in ["CONTINUE", "REPLAN", "FINISH"]


def test_finish_generates_response():
    """Test: El finish debe generar respuesta final"""
    state: PlanExecuteState = {
        "objective": "Test objective",
        "plan": "Test plan",
        "current_step": 1,
        "observations": [{"step": 0, "action": "test", "result": "success"}],
        "decision": "FINISH",
        "final_response": ""
    }
    result = finish_node(state)

    assert "final_response" in result
    assert len(result["final_response"]) > 0


def test_route_decision_maps_correctly():
    """Test: El routing debe mapear decisiones correctamente"""
    assert route_decision({"decision": "CONTINUE"}) == "executor"
    assert route_decision({"decision": "REPLAN"}) == "planner"
    assert route_decision({"decision": "FINISH"}) == "finish"


def test_graph_builds():
    """Test: El grafo debe construirse sin errores"""
    app = build_graph()
    assert app is not None


def test_graph_end_to_end():
    """Test: El grafo debe ejecutar completamente"""
    app = build_graph()

    initial_state: PlanExecuteState = {
        "objective": "Calcula 2 + 2",
        "plan": "",
        "current_step": 0,
        "observations": [],
        "decision": "",
        "final_response": ""
    }

    final_state = app.invoke(initial_state, {"recursion_limit": 15})

    # Debe haber generado respuesta final
    assert len(final_state["final_response"]) > 0
    # Debe haber ejecutado al menos un paso
    assert len(final_state["observations"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
