"""
LangSmith Configuration Utilities

Este módulo proporciona utilidades para configurar y usar LangSmith para
debugging, tracing y observabilidad de agentes LangGraph.

LangSmith es una plataforma de observabilidad que permite:
- Rastrear automáticamente todas las llamadas a LLMs
- Visualizar flujos de ejecución de agentes
- Medir latencia, tokens y costos
- Debuggear comportamientos inesperados
- Comparar diferentes versiones de prompts
"""

import os
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from datetime import datetime
import functools

# LangSmith está incluido en langchain-core
from langsmith import Client, traceable, get_current_run_tree
from langchain_core.runnables import RunnableConfig


class LangSmithConfig:
    """
    Clase para gestionar la configuración de LangSmith.

    Permite activar/desactivar tracing dinámicamente y gestionar
    proyectos, tags y metadata de forma centralizada.
    """

    def __init__(
        self,
        project_name: Optional[str] = None,
        enabled: Optional[bool] = None
    ):
        """
        Inicializa la configuración de LangSmith.

        Args:
            project_name: Nombre del proyecto en LangSmith (ej: "micai-tutorial")
            enabled: Si es True, fuerza el tracing. Si es False, lo desactiva.
                    Si es None, usa la variable de entorno LANGCHAIN_TRACING_V2
        """
        # Determinar si el tracing está habilitado
        if enabled is not None:
            self.enabled = enabled
        else:
            self.enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

        # Configurar nombre del proyecto
        if project_name:
            os.environ["LANGCHAIN_PROJECT"] = project_name

        self.project_name = os.getenv("LANGCHAIN_PROJECT", "default")

        # Inicializar cliente si está habilitado
        self.client = None
        if self.enabled:
            try:
                self.client = Client()
            except Exception as e:
                print(f"⚠️ Warning: No se pudo inicializar LangSmith client: {e}")
                self.enabled = False

    def is_enabled(self) -> bool:
        """Verifica si LangSmith está habilitado."""
        return self.enabled

    def get_client(self) -> Optional[Client]:
        """Retorna el cliente de LangSmith si está disponible."""
        return self.client

    def get_project_url(self) -> str:
        """Retorna la URL del proyecto en LangSmith."""
        if not self.enabled:
            return "LangSmith no está habilitado"

        # La URL sigue el formato: https://smith.langchain.com/o/[org]/projects/p/[project]
        return f"https://smith.langchain.com (Proyecto: {self.project_name})"

    def print_status(self):
        """Imprime el estado actual de LangSmith."""
        print("\n" + "="*60)
        print("🔍 LangSmith Configuration Status")
        print("="*60)
        print(f"Enabled: {self.enabled}")
        print(f"Project: {self.project_name}")

        if self.enabled:
            print(f"API Key: {'✓ Configured' if os.getenv('LANGCHAIN_API_KEY') else '✗ Missing'}")
            print(f"Endpoint: {os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')}")
            print(f"URL: {self.get_project_url()}")
        else:
            print("\nPara habilitar LangSmith:")
            print("1. Crea una cuenta en https://smith.langchain.com")
            print("2. Configura las variables de entorno:")
            print("   LANGCHAIN_TRACING_V2=true")
            print("   LANGCHAIN_API_KEY=ls__your_key")
            print("   LANGCHAIN_PROJECT=your_project")

        print("="*60 + "\n")


def get_runnable_config(
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    run_name: Optional[str] = None,
    **kwargs
) -> RunnableConfig:
    """
    Crea una configuración para runnables con tags y metadata para LangSmith.

    Esta función es útil cuando invocas chains, agents o graphs y quieres
    añadir contexto adicional al trace.

    Args:
        tags: Lista de tags para categorizar el run (ej: ["production", "v1.0"])
        metadata: Diccionario con metadata adicional (ej: {"user_id": "123"})
        run_name: Nombre descriptivo para el run
        **kwargs: Otros parámetros de configuración

    Returns:
        RunnableConfig con la configuración especificada

    Ejemplo:
        >>> config = get_runnable_config(
        ...     tags=["production", "customer-support"],
        ...     metadata={"user_id": "123", "session_id": "abc"},
        ...     run_name="HandleSupportTicket"
        ... )
        >>> result = agent.invoke(input, config=config)
    """
    config: RunnableConfig = {}

    if tags:
        config["tags"] = tags

    if metadata:
        config["metadata"] = metadata

    if run_name:
        config["run_name"] = run_name

    # Añadir otros kwargs
    config.update(kwargs)

    return config


def add_run_metadata(metadata: Dict[str, Any]):
    """
    Añade metadata al run actual de LangSmith.

    Útil cuando quieres añadir información dinámica durante la ejecución.

    Args:
        metadata: Diccionario con metadata a añadir

    Ejemplo:
        >>> def my_agent(input: str):
        ...     result = process(input)
        ...     add_run_metadata({"steps_completed": 3, "total_cost": 0.05})
        ...     return result
    """
    run_tree = get_current_run_tree()
    if run_tree:
        if not hasattr(run_tree, "metadata"):
            run_tree.metadata = {}
        run_tree.metadata.update(metadata)


def add_run_tags(tags: List[str]):
    """
    Añade tags al run actual de LangSmith.

    Args:
        tags: Lista de tags a añadir

    Ejemplo:
        >>> def process_urgent(input: str):
        ...     add_run_tags(["urgent", "high-priority"])
        ...     return handle(input)
    """
    run_tree = get_current_run_tree()
    if run_tree:
        if not hasattr(run_tree, "tags"):
            run_tree.tags = []
        run_tree.tags.extend(tags)


@contextmanager
def trace_section(
    name: str,
    run_type: str = "chain",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Context manager para crear una sección específica en el trace.

    Permite agrupar múltiples operaciones bajo un nombre descriptivo
    en la visualización de LangSmith.

    Args:
        name: Nombre descriptivo de la sección
        run_type: Tipo de run ("chain", "tool", "llm", etc.)
        tags: Tags para esta sección
        metadata: Metadata para esta sección

    Ejemplo:
        >>> def complex_workflow(input: str):
        ...     with trace_section("Preprocessing", tags=["data-prep"]):
        ...         data = clean(input)
        ...         data = normalize(data)
        ...
        ...     with trace_section("Analysis", tags=["ml-model"]):
        ...         result = analyze(data)
        ...
        ...     return result
    """
    from langsmith import trace

    with trace(name=name, run_type=run_type) as run_tree:
        if tags:
            add_run_tags(tags)
        if metadata:
            add_run_metadata(metadata)

        yield run_tree


def trace_agent(
    name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata_fn: Optional[callable] = None
):
    """
    Decorador para trazar funciones de agentes con configuración automática.

    Args:
        name: Nombre del trace (usa el nombre de la función si no se especifica)
        tags: Tags a aplicar al trace
        metadata_fn: Función que recibe los args/kwargs y retorna metadata

    Ejemplo:
        >>> @trace_agent(
        ...     name="CustomerSupportAgent",
        ...     tags=["production", "support"],
        ...     metadata_fn=lambda *args, **kwargs: {"user_id": kwargs.get("user_id")}
        ... )
        ... def support_agent(query: str, user_id: str):
        ...     return process_support_query(query)
    """
    def decorator(func):
        @functools.wraps(func)
        @traceable(run_type="chain", name=name or func.__name__)
        def wrapper(*args, **kwargs):
            # Añadir tags si se especificaron
            if tags:
                add_run_tags(tags)

            # Añadir metadata dinámica si se especificó
            if metadata_fn:
                try:
                    metadata = metadata_fn(*args, **kwargs)
                    if metadata:
                        add_run_metadata(metadata)
                except Exception as e:
                    print(f"Warning: Error al generar metadata: {e}")

            # Ejecutar función original
            return func(*args, **kwargs)

        return wrapper
    return decorator


def create_feedback(
    run_id: str,
    score: float,
    key: str = "user_feedback",
    comment: Optional[str] = None
):
    """
    Crea feedback para un run específico en LangSmith.

    Útil para capturar feedback de usuarios o resultados de evaluaciones.

    Args:
        run_id: ID del run en LangSmith
        score: Puntuación (típicamente 0-1, donde 1 es mejor)
        key: Clave del feedback (ej: "user_feedback", "accuracy", "helpfulness")
        comment: Comentario opcional con detalles

    Ejemplo:
        >>> # Durante ejecución, guarda el run_id
        >>> run_tree = get_current_run_tree()
        >>> run_id = run_tree.id if run_tree else None
        >>>
        >>> # Después, basado en feedback del usuario
        >>> if user_clicked_thumbs_down:
        ...     create_feedback(
        ...         run_id=run_id,
        ...         score=0,
        ...         key="user_satisfaction",
        ...         comment="User reported incorrect information"
        ...     )
    """
    try:
        client = Client()
        client.create_feedback(
            run_id=run_id,
            key=key,
            score=score,
            comment=comment
        )
    except Exception as e:
        print(f"Warning: No se pudo crear feedback: {e}")


def log_agent_decision(
    agent_name: str,
    decision: str,
    reasoning: str,
    confidence: Optional[float] = None
):
    """
    Registra una decisión de agente en el trace actual.

    Útil para entender por qué un agente tomó una decisión específica.

    Args:
        agent_name: Nombre del agente que tomó la decisión
        decision: La decisión tomada (ej: "use_search_tool", "transfer_to_billing")
        reasoning: Explicación de por qué se tomó esta decisión
        confidence: Nivel de confianza en la decisión (0-1)

    Ejemplo:
        >>> def router_agent(input: str):
        ...     intent = classify_intent(input)
        ...
        ...     log_agent_decision(
        ...         agent_name="RouterAgent",
        ...         decision=f"route_to_{intent}",
        ...         reasoning=f"Input classified as {intent} with high confidence",
        ...         confidence=0.95
        ...     )
        ...
        ...     return route_to_agent(intent)
    """
    metadata = {
        f"{agent_name}_decision": decision,
        f"{agent_name}_reasoning": reasoning,
        "timestamp": datetime.now().isoformat()
    }

    if confidence is not None:
        metadata[f"{agent_name}_confidence"] = confidence

    add_run_metadata(metadata)


def compare_runs(run_ids: List[str], metric: str = "latency"):
    """
    Compara múltiples runs y retorna estadísticas.

    Útil para análisis de rendimiento y comparación de versiones.

    Args:
        run_ids: Lista de IDs de runs a comparar
        metric: Métrica a comparar ("latency", "total_tokens", "cost")

    Returns:
        Dict con estadísticas comparativas

    Ejemplo:
        >>> run_ids = ["run-1", "run-2", "run-3"]
        >>> stats = compare_runs(run_ids, metric="latency")
        >>> print(f"Average latency: {stats['average']}ms")
    """
    try:
        client = Client()
        runs = [client.read_run(run_id) for run_id in run_ids]

        values = []
        for run in runs:
            if metric == "latency":
                values.append(run.latency or 0)
            elif metric == "total_tokens":
                values.append((run.total_tokens or 0))
            elif metric == "cost":
                # El costo se calcula automáticamente por LangSmith
                values.append(getattr(run, "cost", 0))

        if not values:
            return {"error": "No values found"}

        return {
            "metric": metric,
            "values": values,
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }
    except Exception as e:
        return {"error": str(e)}


# Configuración global por defecto
_default_config = LangSmithConfig()


def get_default_config() -> LangSmithConfig:
    """Retorna la configuración global por defecto."""
    return _default_config


def set_default_config(config: LangSmithConfig):
    """Establece una nueva configuración global."""
    global _default_config
    _default_config = config


# Ejemplo de uso
if __name__ == "__main__":
    # Verificar configuración
    config = LangSmithConfig()
    config.print_status()

    # Ejemplo de uso con decorador
    @trace_agent(
        name="ExampleAgent",
        tags=["example", "demo"],
        metadata_fn=lambda query, **kw: {"query_length": len(query)}
    )
    def example_agent(query: str, user_id: str = "anonymous"):
        """Agente de ejemplo."""
        print(f"Processing: {query}")

        # Simular procesamiento
        with trace_section("Step1_Analysis", tags=["analysis"]):
            result = f"Analyzed: {query}"

        with trace_section("Step2_Synthesis", tags=["synthesis"]):
            final = f"Result for {user_id}: {result}"

        # Añadir metadata dinámica
        add_run_metadata({
            "result_length": len(final),
            "processing_complete": True
        })

        return final

    # Ejecutar ejemplo si LangSmith está habilitado
    if config.is_enabled():
        result = example_agent("Hello, world!", user_id="user123")
        print(f"\n✓ Result: {result}")
        print(f"\n📊 Ve el trace en: {config.get_project_url()}")
    else:
        print("\n⚠️ LangSmith no está habilitado. Configura las variables de entorno.")
