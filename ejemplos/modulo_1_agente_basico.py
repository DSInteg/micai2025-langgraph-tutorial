"""
EJEMPLO: Agente Básico con ReAct Pattern (Módulo 1.2)

Este ejemplo demuestra un agente autónomo que usa herramientas.
"""

from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from operator import add

load_dotenv()

# Estado del agente
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Herramientas
@tool
def calculator(expression: str) -> str:
    """Evalúa expresiones matemáticas. Ejemplo: '2 + 2' o '10 * 5'"""
    try:
        result = eval(expression)
        return f"Resultado: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """Obtiene el clima de una ciudad (simulado)."""
    # Simulación
    weather_data = {
        "mexico city": "22°C, Parcialmente nublado",
        "guadalajara": "28°C, Soleado",
        "monterrey": "30°C, Caluroso"
    }
    return weather_data.get(city.lower(), "Ciudad no encontrada")

tools = [calculator, get_weather]
llm_with_tools = llm.bind_tools(tools)

# Nodo del agente
def agent_node(state: AgentState):
    """Agente que decide qué hacer."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Decidir si continuar o terminar
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

# Construir grafo
def build_agent():
    workflow = StateGraph(AgentState)

    # Nodos
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    # Flujo
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_agent()

    queries = [
        "¿Cuánto es 25 * 4?",
        "¿Qué clima hace en Guadalajara?",
        "Calcula 100 / 5 y luego dime el clima en Mexico City"
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"💬 Query: {query}")
        print(f"{'='*60}")

        result = app.invoke({
            "messages": [HumanMessage(content=query)]
        })

        # Mostrar respuesta final
        final_message = result["messages"][-1]
        print(f"🤖 Respuesta: {final_message.content}")
