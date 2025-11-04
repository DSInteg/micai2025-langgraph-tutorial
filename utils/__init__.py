"""
Utilidades compartidas para el tutorial de LangGraph Multi-Agent.

Este paquete contiene funciones y clases helper usadas en múltiples módulos:
- llm_config: Configuración de modelos de lenguaje
- logging_config: Configuración de logging
- evaluation: Métricas y evaluación (TODO)
- visualization: Visualización de grafos (TODO)
"""

from .llm_config import (
    get_openai_llm,
    get_anthropic_llm,
    get_llm,
    get_reasoning_llm,
    get_creative_llm,
    get_balanced_llm,
    get_fast_llm,
    get_powerful_llm,
)

from .logging_config import (
    setup_logger,
    setup_tutorial_logging,
    get_agent_logger,
    get_tool_logger,
    get_workflow_logger,
    log_llm_call,
    log_tool_execution,
    log_state_update,
    log_graph_step,
)

__all__ = [
    # LLM config
    "get_openai_llm",
    "get_anthropic_llm",
    "get_llm",
    "get_reasoning_llm",
    "get_creative_llm",
    "get_balanced_llm",
    "get_fast_llm",
    "get_powerful_llm",
    # Logging
    "setup_logger",
    "setup_tutorial_logging",
    "get_agent_logger",
    "get_tool_logger",
    "get_workflow_logger",
    "log_llm_call",
    "log_tool_execution",
    "log_state_update",
    "log_graph_step",
]
