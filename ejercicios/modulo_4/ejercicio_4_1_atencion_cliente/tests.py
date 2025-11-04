"""
Tests para el Ejercicio 4.1: Sistema de Atención al Cliente
"""

import pytest
from solution import (
    build_graph,
    intake_agent,
    product_agent,
    support_agent,
    order_agent,
    synthesizer_agent,
    search_knowledge_base,
    route_to_specialist,
    route_after_synthesis,
    CustomerSupportState,
    knowledge_base,
)
from langchain_core.messages import HumanMessage


def test_search_knowledge_base_finds_products():
    """Test: Búsqueda en KB debe encontrar productos relevantes"""
    query = "laptop 16GB RAM"
    results = search_knowledge_base(query, "product", knowledge_base)

    assert len(results) > 0
    # Debe encontrar productos con RAM en specs
    product_results = [r for r in results if r["type"] == "product"]
    assert len(product_results) > 0


def test_search_knowledge_base_finds_technical_docs():
    """Test: Búsqueda debe encontrar docs técnicas"""
    query = "laptop no enciende"
    results = search_knowledge_base(query, "support", knowledge_base)

    assert len(results) > 0
    # Debe encontrar docs técnicas
    tech_docs = [r for r in results if r["type"] == "technical_doc"]
    assert len(tech_docs) > 0


def test_search_knowledge_base_finds_faqs():
    """Test: Búsqueda debe encontrar FAQs"""
    query = "política de devoluciones"
    results = search_knowledge_base(query, "order", knowledge_base)

    assert len(results) > 0
    # Debe encontrar FAQs
    faqs = [r for r in results if r["type"] == "faq"]
    assert len(faqs) > 0


def test_intake_agent_classifies_product_query():
    """Test: Intake debe clasificar consulta de producto"""
    state: CustomerSupportState = {
        "user_query": "¿Cuánto cuesta la Laptop Pro X15?",
        "user_id": "user_001",
        "conversation_history": [],
        "category": "",
        "urgency": "",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = intake_agent(state)

    assert "category" in result
    assert result["category"] == "product"
    assert "urgency" in result
    assert "kb_results" in result


def test_intake_agent_classifies_support_query():
    """Test: Intake debe clasificar consulta de soporte"""
    state: CustomerSupportState = {
        "user_query": "Mi laptop no enciende, ¿qué hago?",
        "user_id": "user_002",
        "conversation_history": [],
        "category": "",
        "urgency": "",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = intake_agent(state)

    assert "category" in result
    assert result["category"] == "support"


def test_intake_agent_detects_high_urgency():
    """Test: Intake debe detectar alta urgencia"""
    state: CustomerSupportState = {
        "user_query": "URGENTE: necesito ayuda YA con mi pedido!",
        "user_id": "user_003",
        "conversation_history": [],
        "category": "",
        "urgency": "",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = intake_agent(state)

    assert "urgency" in result
    assert result["urgency"] == "high"


def test_product_agent_generates_analysis():
    """Test: Product agent debe generar análisis"""
    state: CustomerSupportState = {
        "user_query": "¿La Laptop Pro X15 es buena para diseño?",
        "user_id": "user_001",
        "conversation_history": [],
        "category": "product",
        "urgency": "low",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [
            {
                "type": "product",
                "data": knowledge_base["products"][0],
                "relevance": 3
            }
        ],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = product_agent(state)

    assert "product_analysis" in result
    assert len(result["product_analysis"]) > 0


def test_support_agent_generates_analysis():
    """Test: Support agent debe generar análisis"""
    state: CustomerSupportState = {
        "user_query": "Mi teléfono no carga",
        "user_id": "user_002",
        "conversation_history": [],
        "category": "support",
        "urgency": "medium",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = support_agent(state)

    assert "support_analysis" in result
    assert len(result["support_analysis"]) > 0


def test_order_agent_generates_analysis():
    """Test: Order agent debe generar análisis"""
    state: CustomerSupportState = {
        "user_query": "¿Cómo devuelvo un producto?",
        "user_id": "user_003",
        "conversation_history": [],
        "category": "order",
        "urgency": "low",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = order_agent(state)

    assert "order_analysis" in result
    assert len(result["order_analysis"]) > 0


def test_synthesizer_generates_response():
    """Test: Synthesizer debe generar respuesta final"""
    state: CustomerSupportState = {
        "user_query": "Test query",
        "user_id": "user_001",
        "conversation_history": [],
        "category": "product",
        "urgency": "low",
        "product_analysis": "This is a detailed product analysis with specifications.",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [{"type": "product", "data": {}, "relevance": 2}],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = synthesizer_agent(state)

    assert "final_response" in result
    assert len(result["final_response"]) > 0
    assert "confidence_score" in result
    assert 0 <= result["confidence_score"] <= 1
    assert "should_escalate" in result


def test_synthesizer_calculates_confidence():
    """Test: Synthesizer debe calcular confidence correctamente"""
    state: CustomerSupportState = {
        "user_query": "Test query",
        "user_id": "user_001",
        "conversation_history": [],
        "category": "product",
        "urgency": "low",
        "product_analysis": "Detailed analysis " * 20,  # Long analysis
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [{"type": "product", "data": {}}],  # Has KB results
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = synthesizer_agent(state)

    # Con KB results, análisis largo, y low urgency, confidence debe ser alto
    assert result["confidence_score"] > 0.5


def test_synthesizer_escalates_on_low_confidence():
    """Test: Synthesizer debe escalar cuando confidence es bajo"""
    state: CustomerSupportState = {
        "user_query": "Test query",
        "user_id": "user_001",
        "conversation_history": [],
        "category": "support",
        "urgency": "high",
        "product_analysis": "",
        "support_analysis": "Short",  # Muy corto
        "order_analysis": "",
        "kb_results": [],  # No KB results
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    result = synthesizer_agent(state)

    # Con high urgency, análisis corto y sin KB, debería escalar
    assert result["should_escalate"] == True


def test_route_to_specialist_routes_correctly():
    """Test: Routing debe mapear categorías correctamente"""
    state_product: CustomerSupportState = {
        "user_query": "",
        "user_id": "user_001",
        "conversation_history": [],
        "category": "product",
        "urgency": "low",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    assert route_to_specialist(state_product) == "product"

    state_support = state_product.copy()
    state_support["category"] = "support"
    assert route_to_specialist(state_support) == "support"

    state_order = state_product.copy()
    state_order["category"] = "order"
    assert route_to_specialist(state_order) == "order"


def test_route_after_synthesis_routes_correctly():
    """Test: Routing post-síntesis debe funcionar correctamente"""
    state_respond: CustomerSupportState = {
        "user_query": "",
        "user_id": "user_001",
        "conversation_history": [],
        "category": "product",
        "urgency": "low",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.8,
        "should_escalate": False,
        "escalation_reason": ""
    }

    assert route_after_synthesis(state_respond) == "respond"

    state_escalate = state_respond.copy()
    state_escalate["should_escalate"] = True
    assert route_after_synthesis(state_escalate) == "escalate"


def test_graph_builds():
    """Test: El grafo debe construirse sin errores"""
    app = build_graph()
    assert app is not None


def test_graph_end_to_end_product_query():
    """Test: Flujo completo con consulta de producto"""
    app = build_graph()

    initial_state: CustomerSupportState = {
        "user_query": "¿Cuánto cuesta la Laptop Pro X15?",
        "user_id": "user_001",
        "conversation_history": [HumanMessage(content="¿Cuánto cuesta la Laptop Pro X15?")],
        "category": "",
        "urgency": "",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    final_state = app.invoke(initial_state)

    # Verificaciones
    assert final_state["category"] == "product"
    assert len(final_state["final_response"]) > 0
    assert final_state["confidence_score"] > 0


def test_graph_end_to_end_support_query():
    """Test: Flujo completo con consulta de soporte"""
    app = build_graph()

    initial_state: CustomerSupportState = {
        "user_query": "Mi teléfono no carga",
        "user_id": "user_002",
        "conversation_history": [HumanMessage(content="Mi teléfono no carga")],
        "category": "",
        "urgency": "",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    final_state = app.invoke(initial_state)

    assert final_state["category"] == "support"
    assert len(final_state["final_response"]) > 0


def test_graph_end_to_end_urgent_query():
    """Test: Consulta urgente debe ser manejada apropiadamente"""
    app = build_graph()

    initial_state: CustomerSupportState = {
        "user_query": "URGENTE: Mi laptop no enciende y tengo presentación mañana!",
        "user_id": "user_003",
        "conversation_history": [],
        "category": "",
        "urgency": "",
        "product_analysis": "",
        "support_analysis": "",
        "order_analysis": "",
        "kb_results": [],
        "final_response": "",
        "confidence_score": 0.0,
        "should_escalate": False,
        "escalation_reason": ""
    }

    final_state = app.invoke(initial_state)

    # Consulta urgente debe tener urgency=high
    assert final_state["urgency"] == "high"
    # Puede o no escalar, pero debe haber tomado una decisión
    assert "should_escalate" in final_state


def test_kb_search_relevance_ranking():
    """Test: KB search debe rankear por relevancia"""
    query = "laptop RAM SSD"
    results = search_knowledge_base(query, "product", knowledge_base)

    if len(results) > 1:
        # El primero debe tener relevancia mayor o igual que el segundo
        assert results[0].get("relevance", 0) >= results[1].get("relevance", 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
