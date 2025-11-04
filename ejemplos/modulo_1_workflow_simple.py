"""
EJEMPLO: Workflow Simple con Prompt Chaining (Módulo 1.1)

Este ejemplo demuestra un workflow determinístico básico con tres pasos secuenciales.
"""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado del workflow
class State(TypedDict):
    text: str
    key_points: str
    summary: str
    translation: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Nodo 1: Extraer puntos clave
def extract_points(state: State) -> dict:
    """Extrae puntos clave del texto."""
    prompt = f"Extract 3-5 key points from this text:\n\n{state['text']}"
    response = llm.invoke(prompt)
    return {"key_points": response.content}

# Nodo 2: Crear resumen
def create_summary(state: State) -> dict:
    """Crea un resumen basado en los puntos clave."""
    prompt = f"Create a concise summary based on these key points:\n\n{state['key_points']}"
    response = llm.invoke(prompt)
    return {"summary": response.content}

# Nodo 3: Traducir
def translate_text(state: State) -> dict:
    """Traduce el resumen al español."""
    prompt = f"Translate this summary to Spanish:\n\n{state['summary']}"
    response = llm.invoke(prompt)
    return {"translation": response.content}

# Construir grafo
def build_workflow():
    workflow = StateGraph(State)

    # Agregar nodos
    workflow.add_node("extract", extract_points)
    workflow.add_node("summarize", create_summary)
    workflow.add_node("translate", translate_text)

    # Definir flujo secuencial
    workflow.set_entry_point("extract")
    workflow.add_edge("extract", "summarize")
    workflow.add_edge("summarize", "translate")
    workflow.add_edge("translate", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_workflow()

    initial_state = {
        "text": """
        Artificial Intelligence is transforming industries worldwide.
        Machine learning models can now process vast amounts of data,
        identify patterns, and make predictions with remarkable accuracy.
        However, challenges remain in areas like explainability, bias, and ethics.
        """,
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    result = app.invoke(initial_state)

    print("🔍 Key Points:")
    print(result["key_points"])
    print("\n📝 Summary:")
    print(result["summary"])
    print("\n🌐 Translation:")
    print(result["translation"])
