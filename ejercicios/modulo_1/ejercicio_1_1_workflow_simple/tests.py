"""
Tests para el Ejercicio 1.1: Workflow Simple

Estos tests verifican que el workflow funcione correctamente:
- Los nodos se ejecutan sin errores
- El estado se actualiza correctamente
- Los outputs tienen el formato esperado
- El flujo sigue el orden correcto
"""

import pytest
from solution import (
    build_graph,
    extract_key_points,
    summarize_content,
    translate_summary,
    WorkflowState
)


# =============================================================================
# TESTS DE NODOS INDIVIDUALES
# =============================================================================

def test_extract_key_points_node():
    """
    Test: El nodo extract_key_points debe:
    - Retornar un diccionario con la clave 'key_points'
    - Generar contenido no vacío
    - No modificar otros campos del estado
    """
    # Arrange: Preparar estado de prueba
    test_state: WorkflowState = {
        "article": "La inteligencia artificial es el futuro de la tecnología. "
                   "Machine learning permite a las máquinas aprender de datos. "
                   "Las aplicaciones son infinitas.",
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    # Act: Ejecutar el nodo
    result = extract_key_points(test_state)

    # Assert: Verificar resultados
    assert "key_points" in result, "El resultado debe contener 'key_points'"
    assert isinstance(result["key_points"], str), "key_points debe ser un string"
    assert len(result["key_points"]) > 0, "key_points no debe estar vacío"
    assert len(result) == 1, "Solo debe retornar el campo actualizado"


def test_summarize_content_node():
    """
    Test: El nodo summarize_content debe:
    - Retornar un diccionario con la clave 'summary'
    - Generar un resumen basado en los puntos clave
    - El resumen debe ser coherente (más largo que los puntos)
    """
    # Arrange: Preparar estado con puntos clave
    test_state: WorkflowState = {
        "article": "Artículo original...",
        "key_points": "1. IA es el futuro\n2. ML aprende de datos\n3. Aplicaciones infinitas",
        "summary": "",
        "translation": ""
    }

    # Act: Ejecutar el nodo
    result = summarize_content(test_state)

    # Assert: Verificar resultados
    assert "summary" in result, "El resultado debe contener 'summary'"
    assert isinstance(result["summary"], str), "summary debe ser un string"
    assert len(result["summary"]) > 0, "summary no debe estar vacío"
    # El resumen debería ser más largo que los puntos clave
    assert len(result["summary"]) >= len(test_state["key_points"]) * 0.5
    assert len(result) == 1, "Solo debe retornar el campo actualizado"


def test_translate_summary_node():
    """
    Test: El nodo translate_summary debe:
    - Retornar un diccionario con la clave 'translation'
    - Traducir el resumen al inglés
    - La traducción debe tener longitud similar al original
    """
    # Arrange: Preparar estado con resumen
    test_state: WorkflowState = {
        "article": "Artículo original...",
        "key_points": "Puntos clave...",
        "summary": "La inteligencia artificial está transformando el mundo. "
                   "Los sistemas modernos pueden aprender y adaptarse. "
                   "El futuro es prometedor.",
        "translation": ""
    }

    # Act: Ejecutar el nodo
    result = translate_summary(test_state)

    # Assert: Verificar resultados
    assert "translation" in result, "El resultado debe contener 'translation'"
    assert isinstance(result["translation"], str), "translation debe ser un string"
    assert len(result["translation"]) > 0, "translation no debe estar vacío"
    # La traducción debería tener longitud similar (±50%)
    original_length = len(test_state["summary"])
    translation_length = len(result["translation"])
    assert 0.5 * original_length <= translation_length <= 1.5 * original_length
    assert len(result) == 1, "Solo debe retornar el campo actualizado"


# =============================================================================
# TESTS DE WORKFLOW COMPLETO
# =============================================================================

def test_workflow_builds_successfully():
    """
    Test: El grafo debe construirse sin errores
    """
    # Act: Construir el grafo
    app = build_graph()

    # Assert: El grafo debe existir y ser compilado
    assert app is not None, "El grafo debe construirse correctamente"


def test_workflow_executes_end_to_end():
    """
    Test: El workflow debe ejecutarse de principio a fin
    y actualizar todos los campos del estado.
    """
    # Arrange: Preparar grafo y estado inicial
    app = build_graph()
    initial_state: WorkflowState = {
        "article": "La tecnología blockchain está revolucionando las finanzas. "
                   "Los contratos inteligentes automatizan procesos. "
                   "La descentralización es clave.",
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    # Act: Ejecutar el workflow completo
    final_state = app.invoke(initial_state)

    # Assert: Todos los campos deben estar actualizados
    assert final_state["article"] == initial_state["article"], \
        "El artículo original no debe cambiar"
    assert len(final_state["key_points"]) > 0, \
        "key_points debe ser generado"
    assert len(final_state["summary"]) > 0, \
        "summary debe ser generado"
    assert len(final_state["translation"]) > 0, \
        "translation debe ser generado"


def test_workflow_order_is_correct():
    """
    Test: El workflow debe ejecutar los nodos en el orden correcto.
    Verificamos que cada nodo dependa de la salida del anterior.
    """
    # Arrange: Preparar grafo y estado
    app = build_graph()
    initial_state: WorkflowState = {
        "article": "Test article about AI and machine learning technology.",
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    # Act: Ejecutar workflow
    final_state = app.invoke(initial_state)

    # Assert: Los outputs deben estar relacionados
    # El resumen debe mencionar conceptos de los puntos clave
    # (esto es una verificación simple, no perfecta)
    assert len(final_state["key_points"]) > 0
    assert len(final_state["summary"]) > len(final_state["key_points"])
    assert len(final_state["translation"]) > 0


def test_workflow_with_empty_article():
    """
    Test: El workflow debe manejar artículos vacíos o muy cortos
    sin crashear (aunque el output pueda no ser ideal)
    """
    # Arrange
    app = build_graph()
    initial_state: WorkflowState = {
        "article": "AI.",
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    # Act & Assert: No debe lanzar excepciones
    try:
        final_state = app.invoke(initial_state)
        assert True, "Debe ejecutar sin errores"
    except Exception as e:
        pytest.fail(f"El workflow falló con artículo corto: {str(e)}")


def test_workflow_with_long_article():
    """
    Test: El workflow debe manejar artículos más largos
    """
    # Arrange
    app = build_graph()
    long_article = """
    La inteligencia artificial (IA) ha experimentado un crecimiento exponencial
    en los últimos años, transformando industrias y revolucionando la manera
    en que interactuamos con la tecnología. Desde asistentes virtuales hasta
    sistemas de recomendación personalizados, la IA se ha integrado en nuestra
    vida cotidiana de formas que antes solo imaginábamos en la ciencia ficción.

    El aprendizaje automático, un subcampo de la IA, permite a las máquinas
    aprender de datos sin ser explícitamente programadas. Los algoritmos de
    aprendizaje profundo, inspirados en las redes neuronales del cerebro humano,
    han logrado avances impresionantes en reconocimiento de imágenes, procesamiento
    de lenguaje natural y generación de contenido.

    Las aplicaciones empresariales de la IA son vastas y continúan expandiéndose.
    Desde la automatización de procesos robóticos hasta el análisis predictivo,
    las organizaciones están aprovechando la IA para mejorar la eficiencia,
    reducir costos y ofrecer mejores experiencias a los clientes.
    """

    initial_state: WorkflowState = {
        "article": long_article.strip(),
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    # Act
    final_state = app.invoke(initial_state)

    # Assert: Debe procesar todo correctamente
    assert len(final_state["key_points"]) > 0
    assert len(final_state["summary"]) > 0
    assert len(final_state["translation"]) > 0


# =============================================================================
# TESTS DE CASOS EDGE
# =============================================================================

def test_state_immutability():
    """
    Test: Los nodos no deben modificar el estado original,
    solo retornar nuevos valores
    """
    # Arrange
    original_state: WorkflowState = {
        "article": "Test article",
        "key_points": "Original points",
        "summary": "Original summary",
        "translation": "Original translation"
    }

    # Hacer una copia para comparar
    state_copy = original_state.copy()

    # Act: Ejecutar un nodo
    result = extract_key_points(original_state)

    # Assert: El estado original no debe cambiar
    assert original_state == state_copy, \
        "El nodo no debe modificar el estado original"
    assert result["key_points"] != original_state["key_points"], \
        "El resultado debe ser diferente al estado original"


# =============================================================================
# EJECUCIÓN DE TESTS
# =============================================================================

if __name__ == "__main__":
    """
    Ejecutar tests directamente con pytest:
        pytest tests.py -v

    O ejecutar este archivo directamente:
        python tests.py
    """
    print("Ejecutando tests del Ejercicio 1.1...")
    print("=" * 70)
    pytest.main([__file__, "-v", "--tb=short"])
