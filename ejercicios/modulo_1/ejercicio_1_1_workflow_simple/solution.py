"""
Ejercicio 1.1: Workflow Simple con Prompt Chaining - SOLUCIÓN COMPLETA

Este módulo implementa un pipeline determinístico de procesamiento de texto
que extrae ideas clave, resume y traduce artículos.

Conceptos implementados:
- StateGraph: Grafo de estados para workflows
- TypedDict: Definición de estructura de estado
- Nodos: Funciones que transforman el estado
- Edges: Conexiones entre nodos
- Prompt engineering: Construcción de prompts efectivos
"""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# Cargar variables de entorno (API keys)
load_dotenv()

# =============================================================================
# DEFINICIÓN DEL ESTADO
# =============================================================================

class WorkflowState(TypedDict):
    """
    Estado compartido entre todos los nodos del workflow.

    Este diccionario fluye a través del grafo y cada nodo puede:
    - Leer cualquier campo
    - Actualizar campos retornando un diccionario parcial

    Importante: LangGraph automáticamente fusiona (merge) el diccionario
    retornado con el estado existente, por lo que solo necesitas retornar
    los campos que quieres actualizar.

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
# CONFIGURACIÓN DEL LLM
# =============================================================================

# Inicializar el modelo de lenguaje
# Usamos GPT-4o-mini por su balance entre costo y calidad
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,  # Creatividad moderada para textos más naturales
)


# =============================================================================
# DEFINICIÓN DE NODOS
# =============================================================================

def extract_key_points(state: WorkflowState) -> dict:
    """
    Nodo 1: Extrae las ideas principales del artículo.

    Este nodo demuestra:
    - Cómo acceder al estado con state["campo"]
    - Cómo construir un prompt claro y específico
    - Cómo invocar el LLM usando HumanMessage
    - Cómo retornar solo los campos actualizados

    Args:
        state: Estado actual del workflow con el artículo original

    Returns:
        Diccionario con la clave 'key_points' actualizada
    """
    print("\n" + "="*70)
    print("🔍 PASO 1: Extrayendo puntos clave del artículo...")
    print("="*70)

    # 1. Acceder al artículo del estado
    article = state["article"]

    # 2. Construir un prompt claro y específico
    # Nota: Un buen prompt debe ser:
    # - Claro sobre la tarea
    # - Específico sobre el formato deseado
    # - Conciso pero completo
    prompt = f"""Analiza el siguiente artículo y extrae las 3-5 ideas principales.

Artículo:
{article}

Por favor, responde solo con una lista numerada de los puntos clave más importantes.
Cada punto debe ser conciso pero completo."""

    # 3. Invocar el LLM
    # HumanMessage representa un mensaje del usuario
    message = HumanMessage(content=prompt)

    # invoke() envía el mensaje al LLM y espera la respuesta
    # Pasamos una lista de mensajes (aunque solo tengamos uno)
    response = llm.invoke([message])

    # 4. Extraer el contenido de la respuesta
    key_points = response.content

    # Mostrar resultado para seguimiento
    print(f"\n📌 Puntos clave extraídos:\n{key_points}\n")

    # 5. Retornar solo el campo que actualizamos
    # LangGraph automáticamente fusionará esto con el estado existente
    return {"key_points": key_points}


def summarize_content(state: WorkflowState) -> dict:
    """
    Nodo 2: Crea un resumen estructurado basado en los puntos clave.

    Este nodo demuestra:
    - Cómo un nodo puede depender de la salida del nodo anterior
    - Cómo pedir al LLM que genere texto con estructura específica
    - La importancia de prompts que guíen el estilo del output

    Args:
        state: Estado actual con key_points ya extraídos

    Returns:
        Diccionario con la clave 'summary' actualizada
    """
    print("\n" + "="*70)
    print("📝 PASO 2: Creando resumen del contenido...")
    print("="*70)

    # 1. Obtener los puntos clave del estado
    # Nota: Este nodo NO necesita el artículo original,
    # solo los puntos clave generados por el nodo anterior
    key_points = state["key_points"]

    # 2. Construir prompt para generar resumen coherente
    # Especificamos:
    # - La tarea (crear resumen)
    # - El formato deseado (3 párrafos)
    # - El estilo (coherente y fluido)
    prompt = f"""Basándote en los siguientes puntos clave, escribe un resumen
coherente y fluido de aproximadamente 3 párrafos.

El resumen debe:
- Ser natural y fácil de leer
- Conectar las ideas de manera lógica
- Mantener la información importante

Puntos clave:
{key_points}

Resumen:"""

    # 3. Invocar el LLM
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    summary = response.content

    # Mostrar resultado
    print(f"\n📄 Resumen generado:\n{summary}\n")

    # 4. Retornar campo actualizado
    return {"summary": summary}


def translate_summary(state: WorkflowState) -> dict:
    """
    Nodo 3: Traduce el resumen al inglés.

    Este nodo demuestra:
    - Tareas de transformación de lenguaje
    - Cómo pedir traducciones naturales (no literales)
    - El último paso en un pipeline secuencial

    Args:
        state: Estado actual con summary ya generado

    Returns:
        Diccionario con la clave 'translation' actualizada
    """
    print("\n" + "="*70)
    print("🌐 PASO 3: Traduciendo resumen al inglés...")
    print("="*70)

    # 1. Obtener el resumen del estado
    summary = state["summary"]

    # 2. Construir prompt para traducción natural
    # Importante: Pedimos traducción "natural y fluida"
    # para evitar traducciones demasiado literales
    prompt = f"""Traduce el siguiente texto al inglés de manera natural y fluida.
Mantén el tono profesional pero accesible.

Texto en español:
{summary}

Traducción al inglés:"""

    # 3. Invocar el LLM
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    translation = response.content

    # Mostrar resultado
    print(f"\n🌍 Traducción completada:\n{translation}\n")

    # 4. Retornar campo actualizado
    return {"translation": translation}


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph() -> StateGraph:
    """
    Construye el grafo del workflow conectando los nodos.

    Este grafo representa un workflow DETERMINÍSTICO:
    - Siempre ejecuta los mismos nodos en el mismo orden
    - No hay decisiones condicionales
    - Ideal para pipelines predecibles

    El flujo es:
    START → extract_key_points → summarize_content → translate_summary → END

    Returns:
        Grafo compilado listo para ejecutar
    """
    # 1. Crear el grafo especificando el tipo de estado
    # Esto permite a LangGraph validar y proporcionar type hints
    workflow = StateGraph(WorkflowState)

    # 2. Agregar los nodos al grafo
    # Sintaxis: add_node(nombre_string, función_a_ejecutar)
    # El nombre es cómo referenciamos el nodo en los edges
    workflow.add_node("extract", extract_key_points)
    workflow.add_node("summarize", summarize_content)
    workflow.add_node("translate", translate_summary)

    # 3. Definir el punto de entrada
    # Este es el primer nodo que se ejecutará
    workflow.set_entry_point("extract")

    # 4. Conectar los nodos con edges (conexiones)
    # add_edge(origen, destino) significa: "después de origen, ejecutar destino"
    workflow.add_edge("extract", "summarize")
    workflow.add_edge("summarize", "translate")

    # 5. Conectar el último nodo con END
    # END es una constante especial que marca el final del workflow
    workflow.add_edge("translate", END)

    # 6. Compilar el grafo
    # compile() valida el grafo y lo prepara para ejecución
    # Retorna un objeto ejecutable
    return workflow.compile()


# =============================================================================
# EJECUCIÓN DEL WORKFLOW
# =============================================================================

def main():
    """
    Función principal que ejecuta el workflow completo.

    Flujo de ejecución:
    1. Definir el artículo de entrada
    2. Construir el grafo
    3. Crear el estado inicial
    4. Ejecutar el workflow con invoke()
    5. Mostrar resultados
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
    # Esta función retorna un grafo compilado listo para ejecutar
    app = build_graph()

    # Crear el estado inicial
    # Debemos proporcionar todos los campos definidos en WorkflowState
    # Los campos vacíos serán llenados por los nodos durante la ejecución
    initial_state = {
        "article": article.strip(),
        "key_points": "",
        "summary": "",
        "translation": ""
    }

    # Ejecutar el workflow
    # invoke() es el método principal para ejecutar un grafo
    # - Toma el estado inicial
    # - Ejecuta cada nodo en orden
    # - Retorna el estado final con todos los campos actualizados
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

    # Nota sobre el estado final:
    # final_state contiene TODOS los campos del estado:
    # - article: El artículo original (sin cambios)
    # - key_points: Generado por extract_key_points()
    # - summary: Generado por summarize_content()
    # - translation: Generado por translate_summary()


if __name__ == "__main__":
    main()
