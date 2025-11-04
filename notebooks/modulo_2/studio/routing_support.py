"""
Sistema de Customer Support con Routing Inteligente
====================================================

Ejercicio 2.1: Demuestra el patrón de Routing con múltiples agentes especializados.

Conceptos:
- Classifier con LLM para categorización
- Agentes especializados por dominio (technical, billing, general)
- Conditional edges para routing dinámico
- Arquitectura de microservicios

Este grafo se puede abrir en LangGraph Studio.
"""

from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END


# =============================================================================
# State Definition
# =============================================================================

class SupportState(TypedDict):
    """Estado del sistema de soporte técnico."""
    query: str          # Consulta del usuario
    intent: str         # Intención clasificada (technical/billing/general)
    response: str       # Respuesta del agente especializado


# =============================================================================
# LLM Configuration
# =============================================================================

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)


# =============================================================================
# Classifier Node
# =============================================================================

def classify_intent(state: SupportState) -> dict:
    """
    Nodo clasificador: Determina la intención del usuario.

    Usa un LLM para categorizar la consulta en una de tres categorías:
    - technical: Problemas técnicos, API, código, errores
    - billing: Facturación, pagos, suscripciones
    - general: Otras consultas generales

    Args:
        state: Estado actual con la consulta del usuario

    Returns:
        Dict con el campo 'intent' actualizado
    """
    prompt = f'''Clasifica esta consulta de soporte técnico en una categoría.

Consulta del usuario: {state["query"]}

Categorías disponibles:
- technical: Problemas técnicos, errores de API, problemas de código, bugs
- billing: Pagos, facturas, suscripciones, precios
- general: Preguntas generales, información, documentación

Instrucciones:
- Analiza cuidadosamente la consulta
- Selecciona la categoría MÁS apropiada
- Responde con UNA SOLA palabra: technical, billing, o general
- No incluyas explicaciones, solo la categoría'''

    response = llm.invoke(prompt)
    intent = response.content.strip().lower()

    print(f'🎯 Clasificador: "{state["query"][:50]}..." → {intent.upper()}')

    return {'intent': intent}


# =============================================================================
# Specialized Agent Nodes
# =============================================================================

def technical_agent(state: SupportState) -> dict:
    """
    Agente técnico especializado.

    Maneja consultas relacionadas con:
    - Errores de API
    - Problemas de código
    - Bugs y troubleshooting
    - Integraciones técnicas
    """
    print(f'🔧 Agente Técnico procesando: "{state["query"][:50]}..."')

    prompt = f'''Eres un agente de soporte técnico especializado.

Consulta del usuario: {state["query"]}

Instrucciones:
- Proporciona una respuesta técnica clara y detallada
- Incluye pasos de troubleshooting si aplica
- Menciona documentación relevante
- Si es un error, explica posibles causas y soluciones
- Máximo 150 palabras'''

    response = llm.invoke(prompt)

    return {'response': response.content}


def billing_agent(state: SupportState) -> dict:
    """
    Agente de facturación especializado.

    Maneja consultas relacionadas con:
    - Pagos y métodos de pago
    - Facturas y recibos
    - Suscripciones y planes
    - Cambios de plan
    """
    print(f'💰 Agente de Facturación procesando: "{state["query"][:50]}..."')

    prompt = f'''Eres un agente de soporte de facturación especializado.

Consulta del usuario: {state["query"]}

Instrucciones:
- Proporciona información clara sobre facturación
- Si es sobre pagos, explica los pasos necesarios
- Si es sobre suscripciones, detalla opciones disponibles
- Sé empático y orientado a soluciones
- Máximo 150 palabras'''

    response = llm.invoke(prompt)

    return {'response': response.content}


def general_agent(state: SupportState) -> dict:
    """
    Agente general para consultas diversas.

    Maneja:
    - Preguntas generales sobre el producto
    - Información de características
    - Guías de uso básico
    - Preguntas que no caen en categorías específicas
    """
    print(f'💬 Agente General procesando: "{state["query"][:50]}..."')

    prompt = f'''Eres un agente de soporte general y amigable.

Consulta del usuario: {state["query"]}

Instrucciones:
- Proporciona información clara y útil
- Si la pregunta es sobre características, descríbelas
- Si pide ayuda general, guía paso a paso
- Mantén un tono profesional y amigable
- Máximo 150 palabras'''

    response = llm.invoke(prompt)

    return {'response': response.content}


# =============================================================================
# Graph Construction
# =============================================================================

def create_graph():
    """
    Construye el grafo de routing de soporte técnico.

    Arquitectura:
        START
          ↓
        classifier (determina: technical/billing/general)
          ↓
        ┌─────────┬─────────┬─────────┐
        ↓         ↓         ↓         ↓
     technical  billing  general    ???
        ↓         ↓         ↓
        END      END      END

    Returns:
        CompiledGraph: Grafo compilado listo para ejecutar
    """
    # 1. Crear el builder
    builder = StateGraph(SupportState)
    print("✅ StateGraph creado")

    # 2. Agregar nodos
    builder.add_node("classifier", classify_intent)
    builder.add_node("technical", technical_agent)
    builder.add_node("billing", billing_agent)
    builder.add_node("general", general_agent)
    print("✅ Nodos agregados")

    # 3. Conectar edges
    # START → classifier
    builder.add_edge(START, "classifier")

    # classifier → routing condicional a agentes especializados
    builder.add_conditional_edges(
        "classifier",
        lambda s: s['intent'],  # Función que retorna el intent
        {
            'technical': 'technical',
            'billing': 'billing',
            'general': 'general'
        }
    )

    # Todos los agentes → END
    builder.add_edge("technical", END)
    builder.add_edge("billing", END)
    builder.add_edge("general", END)

    print("✅ Edges conectados")

    # 4. Compilar
    graph = builder.compile()
    print("🎉 Grafo de routing compilado exitosamente\n")

    return graph


# =============================================================================
# Create the graph (for LangGraph Studio)
# =============================================================================

graph = create_graph()


# =============================================================================
# Testing Function (optional)
# =============================================================================

def main():
    """
    Función de prueba con múltiples escenarios.
    """
    print("="*70)
    print("🎯 Sistema de Customer Support con Routing")
    print("="*70)

    # Casos de prueba
    test_queries = [
        "Mi API está devolviendo error 500 en todas las llamadas",
        "Quiero cancelar mi suscripción actual",
        "¿Qué es LangGraph y para qué sirve?",
        "El SDK de Python no se instala correctamente",
        "No me llegó la factura del mes pasado",
        "¿Tienen documentación en español?",
        "Error de autenticación con mi API key",
        "¿Cuánto cuesta el plan enterprise?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(test_queries)}")
        print(f"{'='*70}")
        print(f"\n📥 CONSULTA:")
        print(f"   '{query}'")

        # Ejecutar el grafo
        result = graph.invoke({
            'query': query,
            'intent': '',
            'response': ''
        })

        print(f"\n📊 RESULTADO:")
        print(f"   Intent: {result['intent'].upper()}")
        print(f"   Respuesta: {result['response'][:100]}...")
        print(f"\n{'='*70}\n")

    print("\n✅ Todos los tests completados")

    # Estadísticas
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Total de consultas: {len(test_queries)}")
    print(f"   Categorías: 3 (technical, billing, general)")
    print(f"   Agentes especializados: 3")


if __name__ == "__main__":
    main()
