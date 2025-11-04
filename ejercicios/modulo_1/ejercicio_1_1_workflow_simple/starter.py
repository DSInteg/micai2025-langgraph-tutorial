"""
Ejercicio 1.1: Workflow Simple con Prompt Chaining

Este módulo implementa un pipeline determinístico de procesamiento de texto
que extrae ideas clave, resume y traduce artículos.

Conceptos clave:
- StateGraph: Grafo de estados para workflows
- TypedDict: Definición de estructura de estado
- Nodos: Funciones que transforman el estado
- Edges: Conexiones entre nodos
"""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# Cargar variables de entorno (API keys)
load_dotenv()

# =============================================================================
# PASO 1: DEFINICIÓN DEL ESTADO
# =============================================================================

class WorkflowState(TypedDict):
    """
    Estado compartido entre todos los nodos del workflow.

    Este diccionario fluye a través del grafo y cada nodo puede:
    - Leer cualquier campo
    - Actualizar campos retornando un diccionario parcial

    Campos:
        article: Artículo original en español (input del usuario)
        key_points: Puntos clave extraídos del artículo
        summary: Resumen del artículo basado en los puntos clave
        translation: Traducción del resumen al inglés
    """
    article: str
    key_points: str
    summary: str
    translation: str


# =============================================================================
# PASO 2: CONFIGURACIÓN DEL LLM
# =============================================================================

# Inicializar el modelo de lenguaje
# Usamos GPT-4o-mini por su balance entre costo y calidad
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,  # Creatividad moderada
)


# =============================================================================
# PASO 3: DEFINICIÓN DE NODOS
# =============================================================================

def extract_key_points(state: WorkflowState) -> dict:
    """
    Nodo 1: Extrae las ideas principales del artículo.

    Este nodo:
    1. Lee el artículo del estado
    2. Usa el LLM para identificar 3-5 puntos clave
    3. Retorna los puntos clave para actualizar el estado

    Args:
        state: Estado actual del workflow con el artículo original

    Returns:
        Diccionario con la clave 'key_points' actualizada

    Ejemplo de retorno:
        {"key_points": "1. Primera idea\n2. Segunda idea\n3. Tercera idea"}
    """
    print("\n" + "="*70)
    print("🔍 PASO 1: Extrayendo puntos clave del artículo...")
    print("="*70)

    # TODO: Implementar la extracción de puntos clave
    #
    # Pasos sugeridos:
    # 1. Obtener el artículo del estado: state["article"]
    # 2. Crear un prompt que pida al LLM extraer 3-5 ideas principales
    # 3. Invocar el LLM con el prompt
    # 4. Retornar un diccionario con la clave "key_points"
    #
    # Pista: Usa HumanMessage para crear el mensaje y llm.invoke() para llamar al modelo

    # Ejemplo de estructura del prompt:
    # prompt = f"""Analiza el siguiente artículo y extrae las 3-5 ideas principales.
    #
    # Artículo:
    # {state["article"]}
    #
    # Responde solo con una lista numerada de los puntos clave."""

    # Tu código aquí:
    key_points = "TODO: Implementar extracción de puntos clave"

    print(f"\n📌 Puntos clave extraídos:\n{key_points}\n")

    return {"key_points": key_points}


def summarize_content(state: WorkflowState) -> dict:
    """
    Nodo 2: Crea un resumen estructurado basado en los puntos clave.

    Este nodo:
    1. Lee los puntos clave del estado (generados por el nodo anterior)
    2. Usa el LLM para crear un resumen coherente de 3 párrafos
    3. Retorna el resumen para actualizar el estado

    Args:
        state: Estado actual con key_points ya extraídos

    Returns:
        Diccionario con la clave 'summary' actualizada

    Nota: Este nodo NO necesita acceder al artículo original, solo a key_points
    """
    print("\n" + "="*70)
    print("📝 PASO 2: Creando resumen del contenido...")
    print("="*70)

    # TODO: Implementar la generación del resumen
    #
    # Pasos sugeridos:
    # 1. Obtener los puntos clave del estado: state["key_points"]
    # 2. Crear un prompt que pida un resumen de 3 párrafos basado en esos puntos
    # 3. Invocar el LLM
    # 4. Retornar un diccionario con la clave "summary"
    #
    # Pista: El resumen debe ser coherente y fluido, no solo una lista

    # Ejemplo de estructura del prompt:
    # prompt = f"""Basándote en los siguientes puntos clave, escribe un resumen
    # coherente de aproximadamente 3 párrafos.
    #
    # Puntos clave:
    # {state["key_points"]}
    #
    # Resumen:"""

    # Tu código aquí:
    summary = "TODO: Implementar generación de resumen"

    print(f"\n📄 Resumen generado:\n{summary}\n")

    return {"summary": summary}


def translate_summary(state: WorkflowState) -> dict:
    """
    Nodo 3: Traduce el resumen al inglés.

    Este nodo:
    1. Lee el resumen del estado (generado por el nodo anterior)
    2. Usa el LLM para traducir el texto al inglés
    3. Retorna la traducción para actualizar el estado

    Args:
        state: Estado actual con summary ya generado

    Returns:
        Diccionario con la clave 'translation' actualizada
    """
    print("\n" + "="*70)
    print("🌐 PASO 3: Traduciendo resumen al inglés...")
    print("="*70)

    # TODO: Implementar la traducción
    #
    # Pasos sugeridos:
    # 1. Obtener el resumen del estado: state["summary"]
    # 2. Crear un prompt que pida traducir al inglés
    # 3. Invocar el LLM
    # 4. Retornar un diccionario con la clave "translation"
    #
    # Pista: Pide una traducción natural y fluida, no literal

    # Ejemplo de estructura del prompt:
    # prompt = f"""Traduce el siguiente texto al inglés de manera natural y fluida.
    #
    # Texto en español:
    # {state["summary"]}
    #
    # Traducción al inglés:"""

    # Tu código aquí:
    translation = "TODO: Implementar traducción"

    print(f"\n🌍 Traducción completada:\n{translation}\n")

    return {"translation": translation}


# =============================================================================
# PASO 4: CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph() -> StateGraph:
    """
    Construye el grafo del workflow conectando los nodos.

    El flujo del workflow es:
    START → extract_key_points → summarize_content → translate_summary → END

    Pasos para construir el grafo:
    1. Crear una instancia de StateGraph con el tipo de estado
    2. Agregar los nodos con add_node(nombre, función)
    3. Definir el punto de entrada con set_entry_point(nombre)
    4. Conectar nodos con add_edge(origen, destino)
    5. Compilar el grafo con compile()

    Returns:
        Grafo compilado listo para ejecutar
    """
    # Crear el grafo con nuestro tipo de estado
    workflow = StateGraph(WorkflowState)

    # TODO: Agregar los tres nodos al workflow
    #
    # Sintaxis: workflow.add_node("nombre_del_nodo", funcion_del_nodo)
    #
    # Debes agregar:
    # - Nodo "extract" que ejecuta extract_key_points
    # - Nodo "summarize" que ejecuta summarize_content
    # - Nodo "translate" que ejecuta translate_summary

    # Tu código aquí:
    # workflow.add_node(...)


    # TODO: Definir el flujo del workflow
    #
    # Pasos:
    # 1. Establecer "extract" como punto de entrada
    # 2. Conectar "extract" → "summarize"
    # 3. Conectar "summarize" → "translate"
    # 4. Conectar "translate" → END
    #
    # Sintaxis:
    # - workflow.set_entry_point("nombre_primer_nodo")
    # - workflow.add_edge("nodo_origen", "nodo_destino")
    # - workflow.add_edge("ultimo_nodo", END)

    # Tu código aquí:
    # workflow.set_entry_point(...)
    # workflow.add_edge(...)


    # Compilar y retornar el grafo
    return workflow.compile()


# =============================================================================
# PASO 5: EJECUCIÓN DEL WORKFLOW
# =============================================================================

def main():
    """
    Función principal que ejecuta el workflow completo.
    """
    print("\n" + "="*70)
    print("🚀 INICIANDO WORKFLOW DE PROCESAMIENTO DE ARTÍCULOS")
    print("="*70)

    # Artículo de ejemplo sobre inteligencia artificial
    article = """
    La inteligencia artificial está transformando radicalmente la forma en que
    trabajamos y vivimos. Los sistemas de IA modernos pueden procesar grandes
    cantidades de información en segundos, identificar patrones complejos y
    hacer predicciones con una precisión sorprendente.

    En el ámbito empresarial, las compañías están implementando agentes
    autónomos para automatizar tareas repetitivas, mejorar la atención al
    cliente y optimizar procesos de negocio. Estos sistemas multi-agente pueden
    colaborar entre sí para resolver problemas complejos que antes requerían
    intervención humana constante.

    Sin embargo, con estos avances vienen importantes desafíos éticos y
    técnicos. Es crucial desarrollar sistemas de IA que sean transparentes,
    explicables y alineados con valores humanos. La comunidad científica está
    trabajando activamente en frameworks y mejores prácticas para el desarrollo
    responsable de IA.
    """

    # Construir el grafo
    app = build_graph()

    # Estado inicial con el artículo
    initial_state = {
        "article": article.strip(),
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    # Ejecutar el workflow
    # El método invoke() procesa el estado a través de todos los nodos
    print("\n⚙️  Ejecutando workflow...\n")
    final_state = app.invoke(initial_state)

    # Mostrar resultados finales
    print("\n" + "="*70)
    print("✅ WORKFLOW COMPLETADO - RESULTADOS FINALES")
    print("="*70)

    print("\n📌 PUNTOS CLAVE:")
    print("-" * 70)
    print(final_state["key_points"])

    print("\n📄 RESUMEN (ESPAÑOL):")
    print("-" * 70)
    print(final_state["summary"])

    print("\n🌍 TRADUCCIÓN (INGLÉS):")
    print("-" * 70)
    print(final_state["translation"])

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado exitosamente!")
    print("="*70)


if __name__ == "__main__":
    main()
