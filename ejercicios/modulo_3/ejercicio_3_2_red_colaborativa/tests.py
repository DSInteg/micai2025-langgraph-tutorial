"""
Tests para el Ejercicio 3.2: Red Colaborativa con Handoffs
"""

import pytest
from solution import (
    build_graph,
    triage_agent,
    code_agent,
    network_agent,
    security_agent,
    final_agent,
    route_from_triage,
    route_from_specialist,
    CollaborativeState,
)


def test_triage_classifies_code_query():
    """Test: El triage debe clasificar consultas de código correctamente"""
    state: CollaborativeState = {
        "query": "Tengo un bug en mi función que retorna None cuando debería retornar una lista",
        "current_agent": "",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    result = triage_agent(state)

    assert "current_agent" in result
    assert "code" in result["current_agent"].lower()
    assert len(result["conversation_history"]) > 0


def test_triage_classifies_network_query():
    """Test: El triage debe clasificar consultas de red correctamente"""
    state: CollaborativeState = {
        "query": "El servidor no responde en el puerto 8080 y creo que el firewall está bloqueando",
        "current_agent": "",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    result = triage_agent(state)

    assert "current_agent" in result
    assert "network" in result["current_agent"].lower()


def test_triage_classifies_security_query():
    """Test: El triage debe clasificar consultas de seguridad correctamente"""
    state: CollaborativeState = {
        "query": "Los usuarios pueden acceder sin autenticación y creo que hay una vulnerabilidad",
        "current_agent": "",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    result = triage_agent(state)

    assert "current_agent" in result
    assert "security" in result["current_agent"].lower()


def test_code_agent_generates_report():
    """Test: El code agent debe generar reporte"""
    state: CollaborativeState = {
        "query": "Mi función tiene un error de índice fuera de rango",
        "current_agent": "code_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    result = code_agent(state)

    assert "specialist_reports" in result
    assert "code_agent" in result["specialist_reports"]
    assert len(result["specialist_reports"]["code_agent"]) > 0
    assert "current_agent" in result


def test_network_agent_generates_report():
    """Test: El network agent debe generar reporte"""
    state: CollaborativeState = {
        "query": "No puedo conectarme al servidor por el puerto 443",
        "current_agent": "network_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    result = network_agent(state)

    assert "specialist_reports" in result
    assert "network_agent" in result["specialist_reports"]
    assert len(result["specialist_reports"]["network_agent"]) > 0


def test_security_agent_generates_report():
    """Test: El security agent debe generar reporte"""
    state: CollaborativeState = {
        "query": "Hay usuarios accediendo sin las credenciales correctas",
        "current_agent": "security_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    result = security_agent(state)

    assert "specialist_reports" in result
    assert "security_agent" in result["specialist_reports"]
    assert len(result["specialist_reports"]["security_agent"]) > 0


def test_final_agent_synthesizes():
    """Test: El final agent debe sintetizar múltiples reportes"""
    state: CollaborativeState = {
        "query": "Problema complejo con múltiples dimensiones",
        "current_agent": "final",
        "conversation_history": [
            {"agent": "triage", "action": "classify"},
            {"agent": "code_agent", "action": "analysis"},
            {"agent": "network_agent", "action": "analysis"}
        ],
        "specialist_reports": {
            "code_agent": "Encontré un bug en la conexión a BD",
            "network_agent": "El firewall bloquea el puerto 5432"
        },
        "handoff_reason": "",
        "final_response": ""
    }
    result = final_agent(state)

    assert "final_response" in result
    assert len(result["final_response"]) > 0


def test_route_from_triage_maps_correctly():
    """Test: El routing desde triage debe mapear correctamente"""
    state_code: CollaborativeState = {
        "query": "",
        "current_agent": "code_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    assert route_from_triage(state_code) == "code"

    state_network: CollaborativeState = {
        "query": "",
        "current_agent": "network_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    assert route_from_triage(state_network) == "network"

    state_security: CollaborativeState = {
        "query": "",
        "current_agent": "security_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    assert route_from_triage(state_security) == "security"


def test_route_from_specialist_to_final():
    """Test: El routing desde especialista a final"""
    state: CollaborativeState = {
        "query": "",
        "current_agent": "final",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    assert route_from_specialist(state) == "final"


def test_route_from_specialist_to_other():
    """Test: El routing desde especialista a otro especialista"""
    state: CollaborativeState = {
        "query": "",
        "current_agent": "network_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }
    result = route_from_specialist(state)
    assert result in ["code", "network", "security", "final"]


def test_graph_builds():
    """Test: El grafo debe construirse sin errores"""
    app = build_graph()
    assert app is not None


def test_graph_end_to_end_simple():
    """Test: El grafo debe ejecutar completamente con consulta simple"""
    app = build_graph()

    initial_state: CollaborativeState = {
        "query": "Mi código tiene un error de sintaxis en la línea 42",
        "current_agent": "",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }

    final_state = app.invoke(initial_state, {"recursion_limit": 20})

    # Debe haber generado respuesta final
    assert len(final_state["final_response"]) > 0
    # Debe haber al menos un reporte de especialista
    assert len(final_state["specialist_reports"]) > 0
    # Debe haber historial de conversación
    assert len(final_state["conversation_history"]) > 0


def test_graph_end_to_end_complex():
    """Test: El grafo debe manejar consulta compleja con handoffs"""
    app = build_graph()

    initial_state: CollaborativeState = {
        "query": "No puedo conectarme a la base de datos. Hay un error de autenticación y el firewall podría estar bloqueando el puerto.",
        "current_agent": "",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }

    final_state = app.invoke(initial_state, {"recursion_limit": 20})

    # Debe haber generado respuesta final
    assert len(final_state["final_response"]) > 0
    # Debe haber múltiples reportes (consulta compleja)
    assert len(final_state["specialist_reports"]) >= 1
    # Debe haber historial mostrando el flujo
    assert len(final_state["conversation_history"]) >= 2


def test_conversation_history_tracks_handoffs():
    """Test: El historial debe rastrear los handoffs correctamente"""
    app = build_graph()

    initial_state: CollaborativeState = {
        "query": "Problema de red y seguridad combinados",
        "current_agent": "",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }

    final_state = app.invoke(initial_state, {"recursion_limit": 20})

    # Verificar que el historial tiene entradas
    assert len(final_state["conversation_history"]) > 0

    # Verificar que cada entrada tiene campos necesarios
    for entry in final_state["conversation_history"]:
        assert "agent" in entry
        assert "action" in entry or "handoff_to" in entry


def test_specialist_reports_accumulate():
    """Test: Los reportes de especialistas deben acumularse"""
    state: CollaborativeState = {
        "query": "Test query",
        "current_agent": "code_agent",
        "conversation_history": [],
        "specialist_reports": {},
        "handoff_reason": "",
        "final_response": ""
    }

    # Primer agente
    result1 = code_agent(state)
    assert "code_agent" in result1["specialist_reports"]

    # Segundo agente debe preservar el reporte anterior
    state2 = state.copy()
    state2["specialist_reports"] = result1["specialist_reports"]
    state2["current_agent"] = "network_agent"

    result2 = network_agent(state2)
    assert "code_agent" in result2["specialist_reports"]
    assert "network_agent" in result2["specialist_reports"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
