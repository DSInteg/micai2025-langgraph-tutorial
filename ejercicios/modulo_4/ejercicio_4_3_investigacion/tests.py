"""
Tests para el Ejercicio 4.3: Asistente de Investigación
"""

import pytest
from solution import (
    build_graph, planner_node, web_researcher, doc_researcher,
    analyzer_node, synthesizer_node, validator_node, ResearchState
)

def test_planner_creates_plan():
    """Test: Planner debe crear plan"""
    state: ResearchState = {
        "topic": "AI in business", "research_plan": "",
        "web_findings": [], "doc_findings": [],
        "analysis": "", "report": "",
        "confidence": 0.0, "validated": False
    }
    result = planner_node(state)
    assert "research_plan" in result
    assert len(result["research_plan"]) > 0

def test_web_researcher_finds_info():
    """Test: Web researcher debe encontrar información"""
    state: ResearchState = {
        "topic": "AI trends", "research_plan": "Plan...",
        "web_findings": [], "doc_findings": [],
        "analysis": "", "report": "",
        "confidence": 0.0, "validated": False
    }
    result = web_researcher(state)
    assert "web_findings" in result
    assert len(result["web_findings"]) > 0

def test_analyzer_processes_findings():
    """Test: Analyzer debe procesar hallazgos"""
    state: ResearchState = {
        "topic": "Test", "research_plan": "Plan",
        "web_findings": [{"source": "web", "content": "Info"}],
        "doc_findings": [{"source": "doc", "content": "Data"}],
        "analysis": "", "report": "",
        "confidence": 0.0, "validated": False
    }
    result = analyzer_node(state)
    assert "analysis" in result
    assert len(result["analysis"]) > 0

def test_synthesizer_generates_report():
    """Test: Synthesizer debe generar reporte"""
    state: ResearchState = {
        "topic": "Test", "research_plan": "Plan",
        "web_findings": [], "doc_findings": [],
        "analysis": "Analysis content",
        "report": "", "confidence": 0.0, "validated": False
    }
    result = synthesizer_node(state)
    assert "report" in result
    assert len(result["report"]) > 0

def test_validator_calculates_confidence():
    """Test: Validator debe calcular confidence"""
    state: ResearchState = {
        "topic": "Test",
        "research_plan": "Plan with enough content",
        "web_findings": [{"source": "web", "content": "Info"}],
        "doc_findings": [{"source": "doc", "content": "Data"}],
        "analysis": "Analysis with sufficient detail",
        "report": "Report with substantial content",
        "confidence": 0.0, "validated": False
    }
    result = validator_node(state)
    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1
    assert "validated" in result

def test_graph_builds():
    """Test: El grafo debe construirse"""
    app = build_graph()
    assert app is not None

def test_graph_end_to_end():
    """Test: Pipeline completo"""
    app = build_graph()
    initial_state: ResearchState = {
        "topic": "AI in healthcare",
        "research_plan": "", "web_findings": [],
        "doc_findings": [], "analysis": "",
        "report": "", "confidence": 0.0, "validated": False
    }
    final_state = app.invoke(initial_state)
    assert len(final_state["report"]) > 0
    assert final_state["confidence"] > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
