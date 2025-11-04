"""
Ejemplo: Debugging con LangSmith

Este ejemplo demuestra cómo usar LangSmith para debugging y observabilidad
de sistemas multi-agente construidos con LangGraph.

Aprenderás:
1. Configuración básica de LangSmith
2. Tracing automático de grafos
3. Añadir metadata y tags personalizados
4. Debugging de decisiones de agentes
5. Análisis de rendimiento

Requisitos:
- Cuenta en https://smith.langchain.com (gratis)
- Variables de entorno configuradas (ver .env.example)
"""

import operator
from typing import Annotated, TypedDict, Literal
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# Importar utilidades de LangSmith
from utils.langsmith_config import (
    LangSmithConfig,
    get_runnable_config,
    add_run_metadata,
    trace_section,
    log_agent_decision,
    trace_agent
)


# ============================================================================
# 1. CONFIGURACIÓN INICIAL
# ============================================================================

def setup_langsmith():
    """
    Configura y verifica LangSmith.

    Si no está configurado, el código seguirá funcionando pero sin tracing.
    """
    config = LangSmithConfig(project_name="micai-debugging-demo")
    config.print_status()
    return config


# ============================================================================
# 2. DEFINIR HERRAMIENTAS
# ============================================================================

@tool
def search_knowledge_base(query: str) -> str:
    """
    Busca información en la base de conocimientos interna.
    Usa esto para: preguntas sobre productos, políticas, procedimientos.
    """
    # Simulación
    knowledge = {
        "precio": "El producto X cuesta $99.99",
        "politica": "Devoluciones aceptadas dentro de 30 días",
        "horario": "Atención de 9am a 6pm, Lunes a Viernes"
    }

    for key, value in knowledge.items():
        if key in query.lower():
            return value

    return "No se encontró información relevante en la base de conocimientos."


@tool
def search_web(query: str) -> str:
    """
    Busca información en internet.
    Usa esto para: noticias actuales, información general, tendencias.
    """
    # Simulación
    return f"Resultados de búsqueda web para: {query}"


@tool
def calculate(expression: str) -> str:
    """
    Realiza cálculos matemáticos.
    Usa esto para: operaciones aritméticas, conversiones.
    """
    try:
        result = eval(expression)
        return f"Resultado: {result}"
    except Exception as e:
        return f"Error en el cálculo: {e}"


# ============================================================================
# 3. DEFINIR ESTADO
# ============================================================================

class AgentState(TypedDict):
    """
    Estado del agente con mensajes y metadata para debugging.
    """
    messages: Annotated[list, operator.add]
    # Campos adicionales para debugging
    decision_count: int
    tools_used: list[str]
    current_step: str


# ============================================================================
# 4. NODOS DEL GRAFO CON TRACING
# ============================================================================

@trace_agent(
    name="ClassifierNode",
    tags=["routing", "classification"],
    metadata_fn=lambda state: {
        "message_count": len(state["messages"]),
        "step": state.get("current_step", "unknown")
    }
)
def classifier_node(state: AgentState) -> AgentState:
    """
    Clasifica el tipo de consulta para enrutamiento.

    Este nodo demuestra:
    - Logging de decisiones para debugging
    - Metadata personalizada
    - Razonamiento explicito
    """
    messages = state["messages"]
    last_message = messages[-1].content.lower()

    # Usar trace_section para agrupar lógica relacionada
    with trace_section("IntentClassification", tags=["ml", "classification"]):
        # Clasificación simple basada en keywords
        if any(word in last_message for word in ["precio", "costo", "cuanto"]):
            intent = "pricing"
            confidence = 0.9
        elif any(word in last_message for word in ["política", "devolución", "reembolso"]):
            intent = "policy"
            confidence = 0.85
        elif any(word in last_message for word in ["calcula", "suma", "multiplica"]):
            intent = "calculation"
            confidence = 0.95
        else:
            intent = "general"
            confidence = 0.6

    # Registrar la decisión para debugging
    log_agent_decision(
        agent_name="Classifier",
        decision=intent,
        reasoning=f"Keywords matched for {intent} category",
        confidence=confidence
    )

    # Añadir metadata adicional
    add_run_metadata({
        "classified_intent": intent,
        "confidence_score": confidence,
        "message_length": len(last_message)
    })

    return {
        **state,
        "current_step": "classified",
        "decision_count": state.get("decision_count", 0) + 1
    }


def agent_node(state: AgentState) -> AgentState:
    """
    Agente principal que usa herramientas.

    Demuestra tracing automático de:
    - Llamadas a LLM
    - Uso de herramientas
    - Selección de tools
    """
    tools = [search_knowledge_base, search_web, calculate]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    # El system prompt es crítico para debugging
    # LangSmith te mostrará exactamente qué ve el LLM
    system_msg = SystemMessage(
        content="""Eres un asistente útil y preciso.

Tienes acceso a tres herramientas:
1. search_knowledge_base: Para información interna (productos, políticas)
2. search_web: Para información externa (noticias, general)
3. calculate: Para cálculos matemáticos

Selecciona la herramienta MÁS APROPIADA para cada consulta.
"""
    )

    messages = [system_msg] + state["messages"]

    # Esta llamada se traza automáticamente en LangSmith
    # Verás: prompt completo, respuesta, tokens, latencia, costo
    response = llm_with_tools.invoke(messages)

    # Registrar qué herramientas se solicitaron
    if hasattr(response, 'tool_calls') and response.tool_calls:
        tool_names = [tc["name"] for tc in response.tool_calls]
        add_run_metadata({
            "tools_requested": tool_names,
            "tool_call_count": len(tool_names)
        })

        # Actualizar lista de herramientas usadas
        tools_used = state.get("tools_used", [])
        tools_used.extend(tool_names)

        return {
            **state,
            "messages": [response],
            "tools_used": tools_used,
            "current_step": "tool_called"
        }

    return {
        **state,
        "messages": [response],
        "current_step": "completed"
    }


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Decide si continuar con herramientas o terminar.

    Esta función de routing también se traza, mostrando
    la lógica de decisión en el flujo del grafo.
    """
    messages = state["messages"]
    last_message = messages[-1]

    # Logging para debugging
    has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls

    add_run_metadata({
        "routing_decision": "tools" if has_tool_calls else "end",
        "has_tool_calls": has_tool_calls,
        "message_type": type(last_message).__name__
    })

    if has_tool_calls:
        return "tools"
    return "end"


# ============================================================================
# 5. CONSTRUIR GRAFO
# ============================================================================

def create_debugging_graph():
    """
    Crea un grafo con nodos que demuestran diferentes aspectos de debugging.
    """
    # Crear grafo
    workflow = StateGraph(AgentState)

    # Añadir nodos
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode([search_knowledge_base, search_web, calculate]))

    # Definir flujo
    workflow.add_edge(START, "classifier")
    workflow.add_edge("classifier", "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")

    return workflow.compile()


# ============================================================================
# 6. FUNCIÓN PRINCIPAL CON EJEMPLOS
# ============================================================================

def run_example(query: str, example_name: str):
    """
    Ejecuta un ejemplo con configuración de LangSmith apropiada.

    Args:
        query: La consulta a procesar
        example_name: Nombre del ejemplo (para tags y metadata)
    """
    print(f"\n{'='*70}")
    print(f"Ejemplo: {example_name}")
    print(f"Query: {query}")
    print(f"{'='*70}\n")

    # Crear configuración con tags y metadata
    config = get_runnable_config(
        tags=["example", example_name.lower().replace(" ", "-")],
        metadata={
            "example_name": example_name,
            "query": query,
            "demo": True
        },
        run_name=f"DebuggingExample_{example_name.replace(' ', '')}"
    )

    # Estado inicial
    initial_state: AgentState = {
        "messages": [HumanMessage(content=query)],
        "decision_count": 0,
        "tools_used": [],
        "current_step": "started"
    }

    # Ejecutar grafo
    graph = create_debugging_graph()
    result = graph.invoke(initial_state, config=config)

    # Mostrar resultados
    final_message = result["messages"][-1]
    print(f"✓ Respuesta: {final_message.content}")
    print(f"✓ Decisiones tomadas: {result['decision_count']}")
    print(f"✓ Herramientas usadas: {result.get('tools_used', [])}")

    return result


def demonstrate_debugging_scenarios():
    """
    Demuestra diferentes escenarios de debugging.
    """
    scenarios = [
        {
            "name": "Búsqueda de Precio",
            "query": "¿Cuál es el precio del producto X?",
            "expected_tool": "search_knowledge_base",
            "debugging_focus": "Verificar que se selecciona la herramienta correcta"
        },
        {
            "name": "Cálculo Simple",
            "query": "Calcula 25 * 4 + 10",
            "expected_tool": "calculate",
            "debugging_focus": "Verificar ejecución de herramienta matemática"
        },
        {
            "name": "Consulta General",
            "query": "¿Qué es la inteligencia artificial?",
            "expected_tool": "search_web",
            "debugging_focus": "Verificar routing a búsqueda web"
        },
        {
            "name": "Pregunta Ambigua",
            "query": "Hola, ¿cómo estás?",
            "expected_tool": None,
            "debugging_focus": "Verificar manejo de consultas sin herramientas"
        }
    ]

    print("\n" + "="*70)
    print("🔍 DEMOSTRACION DE DEBUGGING CON LANGSMITH")
    print("="*70)
    print("\nEn cada ejemplo, ve a LangSmith para analizar:")
    print("1. ¿Qué herramienta seleccionó el agente?")
    print("2. ¿Cuál fue el prompt exacto enviado al LLM?")
    print("3. ¿Cuánto tiempo tomó cada paso?")
    print("4. ¿Cuántos tokens y cuánto costó?")
    print("5. ¿Cuál fue el flujo completo del grafo?")

    results = []
    for scenario in scenarios:
        print(f"\n📍 Focus de debugging: {scenario['debugging_focus']}")
        result = run_example(scenario["query"], scenario["name"])
        results.append(result)

    return results


# ============================================================================
# 7. EJEMPLO DE ANALISIS POST-EJECUCION
# ============================================================================

def analyze_performance():
    """
    Demuestra cómo analizar performance después de ejecutar.

    Nota: Para análisis completo, usa la UI de LangSmith.
    Este es un ejemplo simplificado.
    """
    print("\n" + "="*70)
    print("📊 ANÁLISIS DE PERFORMANCE")
    print("="*70)

    print("""
Para análisis detallado, ve a LangSmith y:

1. Filtra por tag:example
2. Compara latencias entre diferentes consultas
3. Identifica cuál fue más costosa (tokens/dinero)
4. Busca patrones en selección de herramientas
5. Identifica oportunidades de optimización

Métricas clave a revisar:
- Latencia total por query
- Tiempo en LLM vs tiempo en herramientas
- Número de llamadas a LLM
- Tokens promedio por consulta
- Costo total

Preguntas para investigar:
- ¿Alguna query fue inusualmente lenta?
- ¿El agente siempre selecciona la herramienta correcta?
- ¿Hay llamadas redundantes al LLM?
- ¿Se puede cachear algún resultado?
""")


# ============================================================================
# 8. MAIN
# ============================================================================

if __name__ == "__main__":
    # Verificar configuración de LangSmith
    langsmith_config = setup_langsmith()

    if not langsmith_config.is_enabled():
        print("\n⚠️ WARNING: LangSmith no está habilitado.")
        print("El código funcionará, pero no habrá tracing.\n")
        print("Para habilitar:")
        print("1. Crea cuenta en https://smith.langchain.com")
        print("2. Configura variables en .env:")
        print("   LANGCHAIN_TRACING_V2=true")
        print("   LANGCHAIN_API_KEY=ls__your_key")
        print("   LANGCHAIN_PROJECT=micai-debugging-demo\n")

        response = input("¿Continuar sin tracing? (y/n): ")
        if response.lower() != 'y':
            print("Abortando. Configura LangSmith primero.")
            exit(0)

    # Ejecutar ejemplos
    results = demonstrate_debugging_scenarios()

    # Mostrar análisis
    analyze_performance()

    # Mensaje final
    print("\n" + "="*70)
    print("✅ EJEMPLOS COMPLETADOS")
    print("="*70)

    if langsmith_config.is_enabled():
        print(f"\n📊 Ve los traces completos en:")
        print(f"   {langsmith_config.get_project_url()}")
        print("\nEn la UI de LangSmith podrás:")
        print("- Ver el flujo completo del grafo (nodos y edges)")
        print("- Inspeccionar cada llamada al LLM")
        print("- Comparar diferentes ejecuciones")
        print("- Identificar errores y cuellos de botella")
        print("- Analizar costos y optimizar")

    print("\n💡 Próximos pasos:")
    print("1. Modifica las consultas y observa cambios en LangSmith")
    print("2. Añade más herramientas y verifica selección correcta")
    print("3. Introduce errores intencionales y debuggea")
    print("4. Experimenta con diferentes modelos LLM")
    print("5. Lee docs/05_debugging_langsmith.md para técnicas avanzadas")
    print("="*70 + "\n")
