"""
Ejercicio 1.2: Agente Básico Autónomo con Herramientas

Este módulo implementa un agente que puede:
- Razonar sobre qué herramientas necesita
- Ejecutar herramientas dinámicamente
- Decidir cuándo ha completado su tarea

Conceptos clave:
- ReAct pattern (Reasoning + Acting)
- Tool calling y tool binding
- Conditional edges
- Ciclos en grafos
- ToolNode para ejecución de herramientas
"""

from typing import Annotated, Sequence, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Cargar variables de entorno
load_dotenv()

# =============================================================================
# PASO 1: DEFINICIÓN DEL ESTADO DEL AGENTE
# =============================================================================

class AgentState(dict):
    """
    Estado del agente con historial de mensajes.

    A diferencia del Ejercicio 1.1 donde usábamos campos específicos,
    los agentes típicamente usan una secuencia de mensajes que incluye:
    - Mensajes del usuario (HumanMessage)
    - Respuestas del agente (AIMessage)
    - Resultados de herramientas (ToolMessage)

    El tipo Annotated con add_messages es un "reducer" que:
    - Automáticamente agrega nuevos mensajes al historial
    - Mantiene el orden cronológico
    - No duplica mensajes con el mismo ID
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


# =============================================================================
# PASO 2: DEFINICIÓN DE HERRAMIENTAS
# =============================================================================

@tool
def calculator(expression: str) -> str:
    """
    Calcula expresiones matemáticas simples.

    Esta herramienta puede evaluar:
    - Operaciones básicas: +, -, *, /
    - Porcentajes: "15% of 250"
    - Potencias: 2**3
    - Paréntesis para precedencia

    Args:
        expression: Expresión matemática como string (ej: "2 + 2", "15% of 250")

    Returns:
        Resultado del cálculo como string

    Ejemplos:
        calculator("2 + 2") → "4"
        calculator("15% of 250") → "37.5"
        calculator("(10 + 5) * 2") → "30"
    """
    try:
        # Manejar porcentajes: "X% of Y" → (X/100) * Y
        if "%" in expression and "of" in expression:
            parts = expression.replace("%", "").split("of")
            if len(parts) == 2:
                percent = float(parts[0].strip())
                number = float(parts[1].strip())
                result = (percent / 100) * number
                return str(result)

        # Evaluar expresión matemática
        # NOTA: En producción, usar una librería más segura que eval()
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error al calcular: {str(e)}"


@tool
def search_knowledge(query: str) -> str:
    """
    Busca información en una base de conocimiento simulada.

    Esta es una simulación simple de una base de datos.
    En un sistema real, esto podría:
    - Consultar una base de datos
    - Buscar en documentos con RAG
    - Llamar a una API externa

    Args:
        query: Consulta de búsqueda (ej: "precio producto X")

    Returns:
        Información encontrada o mensaje de no encontrado

    Ejemplos:
        search_knowledge("precio producto X") → "El precio del producto X es $120"
        search_knowledge("horario tienda") → "La tienda abre de 9:00 a 18:00"
    """
    # Base de conocimiento simulada
    knowledge_base = {
        "producto x": "El precio del producto X es $120",
        "producto y": "El precio del producto Y es $85",
        "horario": "La tienda abre de 9:00 a 18:00, de lunes a sábado",
        "envío": "El envío es gratuito para compras superiores a $100",
        "garantía": "Todos los productos tienen garantía de 1 año",
        "devoluciones": "Aceptamos devoluciones dentro de los 30 días",
    }

    # Buscar en la base de conocimiento (búsqueda simple)
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value

    return f"No se encontró información sobre: {query}"


# Lista de herramientas disponibles
tools = [calculator, search_knowledge]

# =============================================================================
# PASO 3: CONFIGURACIÓN DEL LLM CON HERRAMIENTAS
# =============================================================================

# Inicializar el modelo
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,  # Temperatura 0 para razonamiento más determinístico
)

# Vincular herramientas al LLM
# bind_tools() permite al LLM:
# - Ver qué herramientas están disponibles
# - Ver sus descripciones y parámetros
# - Decidir cuándo y cómo llamarlas
llm_with_tools = llm.bind_tools(tools)

# System prompt que guía el comportamiento del agente
SYSTEM_PROMPT = """Eres un asistente útil que puede realizar cálculos y buscar información.

Tienes acceso a las siguientes herramientas:
- calculator: Para realizar cálculos matemáticos
- search_knowledge: Para buscar información en la base de conocimiento

Cuando recibas una pregunta:
1. Piensa qué información necesitas
2. Usa las herramientas apropiadas
3. Una vez que tengas toda la información, proporciona una respuesta clara

Siempre explica tu razonamiento brevemente."""


# =============================================================================
# PASO 4: DEFINICIÓN DE NODOS
# =============================================================================

def agent_node(state: AgentState) -> dict:
    """
    Nodo del agente: razona y decide qué hacer.

    Este nodo:
    1. Recibe el historial de mensajes
    2. Invoca el LLM con herramientas vinculadas
    3. El LLM decide:
       - Llamar una o más herramientas, O
       - Responder directamente al usuario

    Args:
        state: Estado con historial de mensajes

    Returns:
        Diccionario con el nuevo mensaje del agente
    """
    print("\n🤖 Agente pensando...")

    # TODO: Implementar el nodo del agente
    #
    # Pasos:
    # 1. Obtener los mensajes del estado
    # 2. Agregar el system prompt si es el primer mensaje
    # 3. Invocar llm_with_tools con los mensajes
    # 4. Retornar el mensaje de respuesta
    #
    # Pistas:
    # - state["messages"] contiene el historial
    # - SystemMessage(...) para el prompt del sistema
    # - llm_with_tools.invoke([messages]) para invocar el LLM
    # - Retornar {"messages": [response]}

    messages = state["messages"]

    # Agregar system prompt si es el primer mensaje del usuario
    if len(messages) == 1:
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # Tu código aquí:
    # response = llm_with_tools.invoke(...)

    # Retornar el mensaje de respuesta
    return {"messages": []}  # TODO: Reemplazar con la respuesta real


def should_continue(state: AgentState) -> Literal["continue", "end"]:
    """
    Función de routing: decide si el agente debe continuar o terminar.

    Esta función determina el siguiente paso en el grafo:
    - Si el último mensaje tiene tool_calls → "continue" (ejecutar herramientas)
    - Si no hay tool_calls → "end" (el agente respondió, terminar)

    Args:
        state: Estado actual

    Returns:
        "continue" si hay herramientas por ejecutar, "end" si debe terminar
    """
    # TODO: Implementar la lógica de routing
    #
    # Pasos:
    # 1. Obtener el último mensaje: state["messages"][-1]
    # 2. Verificar si tiene tool_calls
    # 3. Si tiene tool_calls y no está vacío → retornar "continue"
    # 4. Si no → retornar "end"
    #
    # Pistas:
    # - Los AIMessage con tool calling tienen el atributo tool_calls
    # - tool_calls es una lista de diccionarios con las herramientas a ejecutar
    # - hasattr(mensaje, "tool_calls") verifica si existe el atributo

    last_message = state["messages"][-1]

    # Tu código aquí:
    # Verificar si hay tool_calls

    return "end"  # TODO: Implementar lógica real


# =============================================================================
# PASO 5: CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo del agente con ciclo de razonamiento.

    Este grafo es diferente al Ejercicio 1.1:
    - Usa conditional edges (decisiones dinámicas)
    - Tiene un CICLO: agent → tools → agent
    - No sabemos cuántas iteraciones tomará

    Flujo:
    START → agent → [¿tool_calls?]
                       ↓ sí
                    tools → agent (ciclo)
                       ↓ no
                      END

    Returns:
        Grafo compilado
    """
    # Crear el grafo
    workflow = StateGraph(AgentState)

    # TODO: Agregar nodos
    #
    # 1. Nodo "agent" que ejecuta agent_node
    # 2. Nodo "tools" que ejecuta las herramientas
    #
    # Para el nodo de herramientas, usa ToolNode:
    # - ToolNode es una clase de LangGraph que automáticamente:
    #   * Extrae tool_calls del último mensaje
    #   * Ejecuta las herramientas correspondientes
    #   * Retorna ToolMessages con los resultados
    #
    # Sintaxis:
    # tool_node = ToolNode(tools=tools)
    # workflow.add_node("tools", tool_node)

    # Tu código aquí:
    # workflow.add_node("agent", ...)
    # workflow.add_node("tools", ...)


    # TODO: Configurar el flujo
    #
    # 1. Establecer "agent" como punto de entrada
    # 2. Agregar conditional edge desde "agent":
    #    - Si should_continue retorna "continue" → ir a "tools"
    #    - Si should_continue retorna "end" → ir a END
    # 3. Agregar edge desde "tools" de vuelta a "agent" (¡ciclo!)
    #
    # Sintaxis para conditional edges:
    # workflow.add_conditional_edges(
    #     "nodo_origen",
    #     funcion_decision,
    #     {
    #         "continue": "nodo_destino_1",
    #         "end": END
    #     }
    # )

    # Tu código aquí:
    # workflow.set_entry_point(...)
    # workflow.add_conditional_edges(...)
    # workflow.add_edge(...)


    # Compilar el grafo
    return workflow.compile()


# =============================================================================
# PASO 6: EJECUCIÓN DEL AGENTE
# =============================================================================

def main():
    """
    Función principal que ejecuta el agente con diferentes consultas.
    """
    print("\n" + "="*70)
    print("🚀 AGENTE AUTÓNOMO CON HERRAMIENTAS")
    print("="*70)

    # Construir el grafo
    app = build_graph()

    # Ejemplos de consultas que requieren diferentes herramientas
    queries = [
        "¿Cuánto es 15% de 250?",
        "¿Cuál es el precio del producto X?",
        "Calcula el 20% de 450 y súmale el precio del producto Y",
        "¿Cuál es el horario de la tienda?",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"📝 CONSULTA {i}: {query}")
        print('='*70)

        # Crear estado inicial con la consulta del usuario
        initial_state = {
            "messages": [HumanMessage(content=query)]
        }

        # Ejecutar el agente
        # El agente puede hacer múltiples iteraciones:
        # agent → tools → agent → tools → ... → agent → END
        final_state = app.invoke(initial_state)

        # Mostrar la respuesta final
        final_message = final_state["messages"][-1]
        print(f"\n✅ RESPUESTA FINAL:")
        print(f"{final_message.content}")
        print()

        # Mostrar el número de pasos (mensajes)
        num_steps = len(final_state["messages"])
        print(f"📊 Pasos totales: {num_steps}")

        # Pequeña separación entre consultas
        if i < len(queries):
            input("\nPresiona Enter para continuar con la siguiente consulta...")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado! Has creado tu primer agente autónomo.")
    print("="*70)


if __name__ == "__main__":
    main()
