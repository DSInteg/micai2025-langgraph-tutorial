"""
Tests para el Ejercicio 4.2: Pipeline de Análisis de Documentos
"""

import pytest
from solution import (
    build_graph,
    preprocess_node,
    financial_analyst,
    risk_analyst,
    legal_analyst,
    obligations_analyst,
    aggregator_node,
    validator_node,
    DocumentAnalysisState,
)

SAMPLE_DOC = """
SERVICE AGREEMENT
Date: March 1, 2024
PAYMENT: Total $150,000
TERM: 12 months
"""

def test_preprocess_extracts_metadata():
    """Test: Preprocessing debe extraer metadata"""
    state: DocumentAnalysisState = {
        "document_text": SAMPLE_DOC,
        "document_type": "contract",
        "cleaned_text": "", "sections": {}, "metadata": {},
        "financial_analysis": {}, "risk_analysis": {},
        "legal_analysis": {}, "obligations_analysis": {},
        "combined_insights": [], "executive_summary": "",
        "validation_results": {}, "confidence_score": 0.0,
        "requires_human_review": False, "review_reasons": []
    }

    result = preprocess_node(state)

    assert "cleaned_text" in result
    assert "sections" in result
    assert "metadata" in result
    assert len(result["cleaned_text"]) > 0

def test_financial_analyst_generates_analysis():
    """Test: Financial analyst debe generar análisis"""
    state: DocumentAnalysisState = {
        "document_text": SAMPLE_DOC, "document_type": "contract",
        "cleaned_text": SAMPLE_DOC, "sections": {"PAYMENT": "Total $150,000"},
        "metadata": {}, "financial_analysis": {}, "risk_analysis": {},
        "legal_analysis": {}, "obligations_analysis": {},
        "combined_insights": [], "executive_summary": "",
        "validation_results": {}, "confidence_score": 0.0,
        "requires_human_review": False, "review_reasons": []
    }

    result = financial_analyst(state)

    assert "financial_analysis" in result
    assert "combined_insights" in result
    assert len(result["combined_insights"]) > 0

def test_all_analysts_run_in_parallel():
    """Test: Todos los analistas deben ejecutar"""
    state: DocumentAnalysisState = {
        "document_text": SAMPLE_DOC, "document_type": "contract",
        "cleaned_text": SAMPLE_DOC, "sections": {},
        "metadata": {}, "financial_analysis": {}, "risk_analysis": {},
        "legal_analysis": {}, "obligations_analysis": {},
        "combined_insights": [], "executive_summary": "",
        "validation_results": {}, "confidence_score": 0.0,
        "requires_human_review": False, "review_reasons": []
    }

    # Ejecutar todos
    fin = financial_analyst(state)
    risk = risk_analyst(state)
    legal = legal_analyst(state)
    oblig = obligations_analyst(state)

    assert fin.get("financial_analysis")
    assert risk.get("risk_analysis")
    assert legal.get("legal_analysis")
    assert oblig.get("obligations_analysis")

def test_aggregator_combines_insights():
    """Test: Aggregator debe combinar insights"""
    state: DocumentAnalysisState = {
        "document_text": SAMPLE_DOC, "document_type": "contract",
        "cleaned_text": SAMPLE_DOC, "sections": {},
        "metadata": {}, "financial_analysis": {}, "risk_analysis": {},
        "legal_analysis": {}, "obligations_analysis": {},
        "combined_insights": [
            {"type": "financial", "summary": "Financial summary"},
            {"type": "risk", "summary": "Risk summary"}
        ],
        "executive_summary": "", "validation_results": {},
        "confidence_score": 0.0, "requires_human_review": False,
        "review_reasons": []
    }

    result = aggregator_node(state)

    assert "executive_summary" in result
    assert len(result["executive_summary"]) > 0

def test_validator_calculates_confidence():
    """Test: Validator debe calcular confidence"""
    state: DocumentAnalysisState = {
        "document_text": SAMPLE_DOC, "document_type": "contract",
        "cleaned_text": SAMPLE_DOC, "sections": {},
        "metadata": {"amounts": ["$150,000"]},
        "financial_analysis": {"content": "Analysis"},
        "risk_analysis": {"content": "Analysis"},
        "legal_analysis": {"content": "Analysis"},
        "obligations_analysis": {"content": "Analysis"},
        "combined_insights": [],
        "executive_summary": "Good summary with enough content",
        "validation_results": {}, "confidence_score": 0.0,
        "requires_human_review": False, "review_reasons": []
    }

    result = validator_node(state)

    assert "confidence_score" in result
    assert 0 <= result["confidence_score"] <= 1
    assert "requires_human_review" in result

def test_validator_flags_incomplete_analysis():
    """Test: Validator debe detectar análisis incompleto"""
    state: DocumentAnalysisState = {
        "document_text": SAMPLE_DOC, "document_type": "contract",
        "cleaned_text": SAMPLE_DOC, "sections": {},
        "metadata": {}, "financial_analysis": {},
        "risk_analysis": {}, "legal_analysis": {},
        "obligations_analysis": {}, "combined_insights": [],
        "executive_summary": "Short", "validation_results": {},
        "confidence_score": 0.0, "requires_human_review": False,
        "review_reasons": []
    }

    result = validator_node(state)

    assert result["confidence_score"] < 0.7
    assert result["requires_human_review"] == True
    assert len(result["review_reasons"]) > 0

def test_graph_builds():
    """Test: El grafo debe construirse"""
    app = build_graph()
    assert app is not None

def test_graph_end_to_end():
    """Test: Pipeline completo end-to-end"""
    app = build_graph()

    initial_state: DocumentAnalysisState = {
        "document_text": SAMPLE_DOC, "document_type": "contract",
        "cleaned_text": "", "sections": {}, "metadata": {},
        "financial_analysis": {}, "risk_analysis": {},
        "legal_analysis": {}, "obligations_analysis": {},
        "combined_insights": [], "executive_summary": "",
        "validation_results": {}, "confidence_score": 0.0,
        "requires_human_review": False, "review_reasons": []
    }

    final_state = app.invoke(initial_state)

    assert len(final_state["executive_summary"]) > 0
    assert final_state["confidence_score"] > 0
    assert len(final_state["combined_insights"]) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
