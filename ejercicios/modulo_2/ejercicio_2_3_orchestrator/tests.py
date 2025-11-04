"""
Tests para el Ejercicio 2.3: Orchestrator-Workers
"""

import pytest
from solution import (
    build_graph,
    orchestrator_plan,
    executive_summary_worker,
    technical_details_worker,
    financial_analysis_worker,
    orchestrator_synthesize,
    DocumentAnalysisState,
    extract_sections_smart,
)


def test_orchestrator_plan_divides_document():
    """Test: El orchestrator debe dividir el documento en secciones"""
    state: DocumentAnalysisState = {
        "document": "Resumen ejecutivo aquí. Detalles técnicos allá. Costos: $1000.",
        "executive": "",
        "technical": "",
        "financial": "",
        "executive_analysis": "",
        "technical_analysis": "",
        "financial_analysis": "",
        "final_report": ""
    }
    result = orchestrator_plan(state)

    assert "executive" in result
    assert "technical" in result
    assert "financial" in result


def test_executive_worker_analyzes():
    """Test: El worker ejecutivo debe analizar su sección"""
    state: DocumentAnalysisState = {
        "document": "",
        "executive": "Este proyecto es estratégico para la empresa.",
        "technical": "",
        "financial": "",
        "executive_analysis": "",
        "technical_analysis": "",
        "financial_analysis": "",
        "final_report": ""
    }
    result = executive_summary_worker(state)

    assert "executive_analysis" in result
    assert len(result["executive_analysis"]) > 0


def test_technical_worker_analyzes():
    """Test: El worker técnico debe analizar su sección"""
    state: DocumentAnalysisState = {
        "document": "",
        "executive": "",
        "technical": "La arquitectura será microservicios con Docker.",
        "financial": "",
        "executive_analysis": "",
        "technical_analysis": "",
        "financial_analysis": "",
        "final_report": ""
    }
    result = technical_details_worker(state)

    assert "technical_analysis" in result
    assert len(result["technical_analysis"]) > 0


def test_financial_worker_analyzes():
    """Test: El worker financiero debe analizar su sección"""
    state: DocumentAnalysisState = {
        "document": "",
        "executive": "",
        "technical": "",
        "financial": "El costo total es $100,000 con ROI de 12 meses.",
        "executive_analysis": "",
        "technical_analysis": "",
        "financial_analysis": "",
        "final_report": ""
    }
    result = financial_analysis_worker(state)

    assert "financial_analysis" in result
    assert len(result["financial_analysis"]) > 0


def test_orchestrator_synthesize_creates_report():
    """Test: El orchestrator debe sintetizar los análisis"""
    state: DocumentAnalysisState = {
        "document": "",
        "executive": "",
        "technical": "",
        "financial": "",
        "executive_analysis": "Análisis ejecutivo completo",
        "technical_analysis": "Análisis técnico detallado",
        "financial_analysis": "Análisis financiero profundo",
        "final_report": ""
    }
    result = orchestrator_synthesize(state)

    assert "final_report" in result
    assert len(result["final_report"]) > 0


def test_graph_builds():
    """Test: El grafo debe construirse sin errores"""
    app = build_graph()
    assert app is not None


def test_graph_end_to_end():
    """Test: El grafo debe ejecutar completamente"""
    app = build_graph()

    document = """
    Resumen ejecutivo del proyecto de transformación digital.

    Detalles técnicos: implementaremos con Python y React.

    Análisis financiero: inversión de $50,000 con ROI de 15 meses.
    """

    initial_state: DocumentAnalysisState = {
        "document": document,
        "executive": "",
        "technical": "",
        "financial": "",
        "executive_analysis": "",
        "technical_analysis": "",
        "financial_analysis": "",
        "final_report": ""
    }

    final_state = app.invoke(initial_state)

    # Verificar que todos los análisis se generaron
    assert len(final_state["executive_analysis"]) > 0
    assert len(final_state["technical_analysis"]) > 0
    assert len(final_state["financial_analysis"]) > 0
    assert len(final_state["final_report"]) > 0


def test_extract_sections_identifies_executive():
    """Test: La función debe identificar contenido ejecutivo"""
    doc = "Resumen ejecutivo: Esta es una iniciativa estratégica importante."
    sections = extract_sections_smart(doc)
    assert "ejecutivo" in sections["executive"].lower() or "estratégica" in sections["executive"].lower()


def test_extract_sections_identifies_technical():
    """Test: La función debe identificar contenido técnico"""
    doc = "Arquitectura técnica: usaremos microservicios con Docker y Kubernetes."
    sections = extract_sections_smart(doc)
    assert len(sections["technical"]) > 0


def test_extract_sections_identifies_financial():
    """Test: La función debe identificar contenido financiero"""
    doc = "Análisis financiero: El costo total es $100,000 con ROI de 18 meses."
    sections = extract_sections_smart(doc)
    assert len(sections["financial"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
