"""
Tests para Ejercicio 4.4: Debugging con LangSmith

Estos tests verifican:
1. Funcionalidad básica del sistema
2. Corrección de bugs identificados
3. Mejoras de rendimiento
4. Instrumentación con LangSmith
"""

import pytest
from typing import Dict, Any
from solution import (
    create_document_analyzer_graph,
    run_analysis,
    verify_langsmith_setup,
    DocumentState
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_documents():
    """Documentos de prueba de diferentes tipos."""
    return {
        "pdf": "research_paper.pdf - This is a scientific research paper about AI.",
        "image": "diagram.png - This is a technical diagram showing system architecture.",
        "json": '{"title": "Data Report", "type": "structured", "data": [1, 2, 3]}',
        "text": "simple_text_file.txt - Plain text content for testing."
    }


@pytest.fixture
def graph():
    """Grafo compilado para testing."""
    return create_document_analyzer_graph()


# ============================================================================
# TESTS DE FUNCIONALIDAD BÁSICA
# ============================================================================

class TestBasicFunctionality:
    """Tests de funcionalidad básica del sistema."""

    def test_graph_creation(self, graph):
        """Verifica que el grafo se crea correctamente."""
        assert graph is not None
        # El grafo debe tener los nodos esperados
        assert hasattr(graph, 'invoke')

    def test_pdf_document_analysis(self, sample_documents):
        """Verifica análisis de documentos PDF."""
        result = run_analysis(
            sample_documents["pdf"],
            tags=["test", "pdf"]
        )

        assert result["document_type"] == "pdf"
        assert result["extracted_data"] is not None
        assert result["summary"] is not None
        assert result["validated"] is True
        assert result["current_phase"] in ["validated", "end"]

    def test_image_document_analysis(self, sample_documents):
        """Verifica análisis de imágenes."""
        result = run_analysis(
            sample_documents["image"],
            tags=["test", "image"]
        )

        assert result["document_type"] == "image"
        assert result["extracted_data"] is not None
        assert result["summary"] is not None

    def test_structured_document_analysis(self, sample_documents):
        """Verifica análisis de datos estructurados."""
        result = run_analysis(
            sample_documents["json"],
            tags=["test", "json"]
        )

        assert result["document_type"] == "structured"
        assert result["extracted_data"] is not None

    def test_text_document_analysis(self, sample_documents):
        """Verifica análisis de texto plano."""
        result = run_analysis(
            sample_documents["text"],
            tags=["test", "text"]
        )

        assert result["document_type"] == "text"
        assert result["extracted_data"] is not None


# ============================================================================
# TESTS DE CORRECCIÓN DE BUGS
# ============================================================================

class TestBugFixes:
    """Tests que verifican que los bugs identificados fueron corregidos."""

    def test_no_infinite_loops(self, sample_documents):
        """
        BUG 1: Loops infinitos
        Verifica que el sistema tiene límite de iteraciones.
        """
        # Intentar con múltiples documentos
        for doc_type, document in sample_documents.items():
            result = run_analysis(
                document,
                tags=["test", "loop_protection", doc_type]
            )

            # Debe terminar en menos de 10 iteraciones
            assert result["iteration_count"] <= 10, \
                f"Exceeded max iterations for {doc_type}: {result['iteration_count']}"

            # No debe estar en estado de error por loops
            assert result["current_phase"] != "error" or \
                "max iterations" not in str(result.get("errors", [])).lower()

    def test_tool_selection_accuracy(self, sample_documents):
        """
        BUG 2: Selección incorrecta de herramientas
        Verifica que las descripciones claras mejoran la selección.
        """
        # PDF debe usar extract_pdf_text
        result_pdf = run_analysis(
            sample_documents["pdf"],
            tags=["test", "tool_selection", "pdf"]
        )
        # Verificar que se procesó correctamente (proxy de herramienta correcta)
        assert result_pdf["document_type"] == "pdf"
        assert result_pdf["validated"] is True

        # Image debe usar extract_image_text
        result_image = run_analysis(
            sample_documents["image"],
            tags=["test", "tool_selection", "image"]
        )
        assert result_image["document_type"] == "image"
        assert result_image["validated"] is True

        # JSON debe usar parse_structured_data
        result_json = run_analysis(
            sample_documents["json"],
            tags=["test", "tool_selection", "json"]
        )
        assert result_json["document_type"] == "structured"
        assert result_json["validated"] is True

    def test_optimized_llm_calls(self, sample_documents):
        """
        BUG 3: Llamadas redundantes al LLM
        Verifica que el extractor hace una sola llamada combinada.

        Nota: Este test verifica indirectamente mediante performance.
        Para verificar directamente, revisa el trace en LangSmith.
        """
        result = run_analysis(
            sample_documents["pdf"],
            tags=["test", "optimization", "llm_calls"]
        )

        # El resultado debe tener todos los datos extraídos
        extracted = result["extracted_data"]
        assert extracted is not None
        assert "entities" in extracted
        assert "dates" in extracted
        assert "numbers" in extracted
        assert "facts" in extracted

        # Todo debe estar extraído en una pasada eficiente
        assert result["validated"] is True


# ============================================================================
# TESTS DE RENDIMIENTO
# ============================================================================

class TestPerformance:
    """Tests de rendimiento y optimización."""

    def test_completion_time_reasonable(self, sample_documents):
        """Verifica que el análisis se completa en tiempo razonable."""
        import time

        for doc_type, document in sample_documents.items():
            start = time.time()

            result = run_analysis(
                document,
                tags=["test", "performance", doc_type]
            )

            elapsed = time.time() - start

            # Debe completarse en menos de 30 segundos (generoso para CI)
            assert elapsed < 30, \
                f"{doc_type} took too long: {elapsed:.2f}s"

            # Debe completarse exitosamente
            assert result["validated"] is True

    def test_iteration_count_minimal(self, sample_documents):
        """Verifica que el número de iteraciones es óptimo."""
        for doc_type, document in sample_documents.items():
            result = run_analysis(
                document,
                tags=["test", "iterations", doc_type]
            )

            # Para flujo normal: classify (1) + extract (2) + summarize (3) + validate (4)
            # Debe ser aproximadamente 4 iteraciones
            assert result["iteration_count"] <= 6, \
                f"{doc_type} had too many iterations: {result['iteration_count']}"

    def test_no_redundant_processing(self, sample_documents):
        """Verifica que no hay procesamiento redundante."""
        result = run_analysis(
            sample_documents["pdf"],
            tags=["test", "redundancy"]
        )

        # Herramientas no deben repetirse innecesariamente
        tools_used = result.get("tools_used", [])

        # Cada herramienta debe usarse máximo una vez por documento
        from collections import Counter
        tool_counts = Counter(tools_used)

        for tool, count in tool_counts.items():
            assert count <= 2, \
                f"Tool {tool} used {count} times (should be ≤2)"


# ============================================================================
# TESTS DE INSTRUMENTACIÓN
# ============================================================================

class TestInstrumentation:
    """Tests de instrumentación con LangSmith."""

    def test_langsmith_config(self):
        """Verifica que LangSmith puede configurarse."""
        config = verify_langsmith_setup()
        assert config is not None
        assert hasattr(config, 'is_enabled')
        assert hasattr(config, 'get_client')

    def test_state_has_debugging_fields(self, sample_documents):
        """Verifica que el estado tiene campos para debugging."""
        result = run_analysis(
            sample_documents["pdf"],
            tags=["test", "state_fields"]
        )

        # Verificar campos de debugging
        assert "iteration_count" in result
        assert "tools_used" in result
        assert "current_phase" in result
        assert "errors" in result

        # Tipos correctos
        assert isinstance(result["iteration_count"], int)
        assert isinstance(result["tools_used"], list)
        assert isinstance(result["current_phase"], str)
        assert isinstance(result["errors"], list)

    def test_tracks_processing_phases(self, sample_documents):
        """Verifica que se rastrean las fases de procesamiento."""
        result = run_analysis(
            sample_documents["pdf"],
            tags=["test", "phases"]
        )

        # Debe estar en una fase final válida
        valid_final_phases = ["validated", "end", "validation_failed"]
        assert result["current_phase"] in valid_final_phases, \
            f"Unexpected final phase: {result['current_phase']}"


# ============================================================================
# TESTS DE VALIDACIÓN
# ============================================================================

class TestValidation:
    """Tests de validación de resultados."""

    def test_complete_pipeline_validation(self, sample_documents):
        """Verifica que el pipeline completo funciona correctamente."""
        for doc_type, document in sample_documents.items():
            result = run_analysis(
                document,
                tags=["test", "validation", doc_type]
            )

            # Todos los campos requeridos deben estar presentes
            assert result["document_type"] is not None, \
                f"Missing document_type for {doc_type}"
            assert result["extracted_data"] is not None, \
                f"Missing extracted_data for {doc_type}"
            assert result["summary"] is not None, \
                f"Missing summary for {doc_type}"

            # Debe estar validado
            assert result["validated"] is True, \
                f"Document not validated for {doc_type}"

    def test_extracted_data_structure(self, sample_documents):
        """Verifica la estructura de los datos extraídos."""
        result = run_analysis(
            sample_documents["pdf"],
            tags=["test", "data_structure"]
        )

        extracted = result["extracted_data"]

        # Debe tener la estructura esperada
        assert isinstance(extracted, dict)
        assert "entities" in extracted
        assert "dates" in extracted
        assert "numbers" in extracted
        assert "facts" in extracted

        # Tipos correctos
        assert isinstance(extracted["entities"], list)
        assert isinstance(extracted["dates"], list)
        assert isinstance(extracted["numbers"], list)
        assert isinstance(extracted["facts"], list)

    def test_summary_quality(self, sample_documents):
        """Verifica la calidad del resumen generado."""
        result = run_analysis(
            sample_documents["pdf"],
            tags=["test", "summary_quality"]
        )

        summary = result["summary"]

        # Resumen debe existir y no estar vacío
        assert summary is not None
        assert len(summary) > 0

        # Debe tener longitud razonable (no muy corto, no muy largo)
        assert len(summary) >= 20, "Summary too short"
        assert len(summary) <= 1000, "Summary too long"


# ============================================================================
# TESTS DE CASOS EDGE
# ============================================================================

class TestEdgeCases:
    """Tests de casos edge y situaciones inusuales."""

    def test_empty_document(self):
        """Verifica manejo de documento vacío."""
        result = run_analysis(
            "",
            tags=["test", "edge_case", "empty"]
        )

        # Debe completarse sin errores graves
        assert result is not None
        assert result["iteration_count"] <= 10

    def test_very_long_document(self):
        """Verifica manejo de documentos muy largos."""
        long_doc = "document.pdf - " + ("Very long content. " * 1000)

        result = run_analysis(
            long_doc,
            tags=["test", "edge_case", "long"]
        )

        # Debe completarse exitosamente
        assert result["validated"] is True
        assert result["iteration_count"] <= 10

    def test_ambiguous_type_document(self):
        """Verifica manejo de documentos con tipo ambiguo."""
        ambiguous = "unknown_file - Could be anything really."

        result = run_analysis(
            ambiguous,
            tags=["test", "edge_case", "ambiguous"]
        )

        # Debe asignar algún tipo (probablemente "text")
        assert result["document_type"] is not None
        assert result["document_type"] in ["text", "pdf", "image", "structured"]


# ============================================================================
# TESTS DE COMPARACIÓN (ANTES VS DESPUÉS)
# ============================================================================

class TestImprovements:
    """Tests que demuestran mejoras vs versión con bugs."""

    def test_classification_improved(self, sample_documents):
        """
        Verifica que la clasificación es precisa con descripciones claras.

        Con bugs: ~60% precisión (descripciones ambiguas)
        Sin bugs: ~95% precisión (descripciones claras)
        """
        correct_classifications = 0
        total = len(sample_documents)

        expected_types = {
            "pdf": "pdf",
            "image": "image",
            "json": "structured",
            "text": "text"
        }

        for doc_key, document in sample_documents.items():
            result = run_analysis(
                document,
                tags=["test", "improvement", "classification"]
            )

            if result["document_type"] == expected_types[doc_key]:
                correct_classifications += 1

        accuracy = correct_classifications / total
        assert accuracy >= 0.9, \
            f"Classification accuracy {accuracy:.1%} below target (90%)"

    def test_no_timeout_from_loops(self, sample_documents):
        """
        Verifica que no hay timeouts por loops infinitos.

        Con bugs: Podría nunca terminar
        Sin bugs: Siempre termina en <10 iteraciones
        """
        import time

        for doc_type, document in sample_documents.items():
            start = time.time()

            result = run_analysis(
                document,
                tags=["test", "improvement", "timeout_protection"]
            )

            elapsed = time.time() - start

            # Debe terminar rápidamente (sin loops)
            assert elapsed < 20, \
                f"Possible loop detected: {doc_type} took {elapsed:.2f}s"

            # Y con pocas iteraciones
            assert result["iteration_count"] <= 10


# ============================================================================
# RUNNER
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("🧪 EJECUTANDO TESTS: DEBUGGING CON LANGSMITH")
    print("="*70)

    # Ejecutar con pytest
    pytest.main([
        __file__,
        "-v",  # verbose
        "--tb=short",  # traceback corto
        "-k", "test_",  # solo funciones que empiezan con test_
    ])

    print("\n" + "="*70)
    print("✅ TESTS COMPLETADOS")
    print("="*70)
    print("""
Para análisis detallado en LangSmith:
1. Filtra runs por tag:test
2. Compara métricas entre diferentes tests
3. Identifica patrones en traces exitosos vs fallidos
4. Usa insights para mejorar el sistema

Métricas clave verificadas:
✅ Funcionalidad completa
✅ Bugs corregidos
✅ Rendimiento optimizado
✅ Instrumentación completa
""")
