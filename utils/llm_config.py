"""
Configuración centralizada de LLMs para el tutorial.

Este módulo proporciona funciones helper para inicializar y configurar
modelos de lenguaje de diferentes proveedores.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Cargar variables de entorno
load_dotenv()


def get_openai_llm(
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    **kwargs
) -> ChatOpenAI:
    """
    Inicializa un modelo de OpenAI.

    Args:
        model: Nombre del modelo (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)
        temperature: Nivel de aleatoriedad (0 = determinista, 1 = creativo)
        max_tokens: Límite de tokens en la respuesta (None = sin límite)
        **kwargs: Argumentos adicionales para ChatOpenAI

    Returns:
        Instancia configurada de ChatOpenAI

    Ejemplos:
        >>> llm = get_openai_llm()  # Usa defaults
        >>> llm = get_openai_llm(model="gpt-4o", temperature=0)  # Determinista
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY no encontrada. "
            "Copia .env.example a .env y agrega tu API key."
        )

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )


def get_anthropic_llm(
    model: str = "claude-3-5-sonnet-20241022",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    **kwargs
) -> ChatAnthropic:
    """
    Inicializa un modelo de Anthropic (Claude).

    Args:
        model: Nombre del modelo (claude-3-opus, claude-3-sonnet, claude-3-haiku)
        temperature: Nivel de aleatoriedad (0 = determinista, 1 = creativo)
        max_tokens: Límite de tokens en la respuesta (None = sin límite)
        **kwargs: Argumentos adicionales para ChatAnthropic

    Returns:
        Instancia configurada de ChatAnthropic

    Ejemplos:
        >>> llm = get_anthropic_llm()  # Usa defaults
        >>> llm = get_anthropic_llm(model="claude-3-opus-20240229")
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY no encontrada. "
            "Copia .env.example a .env y agrega tu API key."
        )

    return ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )


def get_llm(
    provider: str = "openai",
    **kwargs
):
    """
    Factory function para obtener un LLM de cualquier proveedor.

    Args:
        provider: Proveedor del LLM ("openai" o "anthropic")
        **kwargs: Argumentos pasados al constructor específico

    Returns:
        Instancia del LLM configurado

    Ejemplos:
        >>> llm = get_llm("openai", model="gpt-4o")
        >>> llm = get_llm("anthropic", model="claude-3-sonnet-20240229")
    """
    provider = provider.lower()

    if provider == "openai":
        return get_openai_llm(**kwargs)
    elif provider == "anthropic":
        return get_anthropic_llm(**kwargs)
    else:
        raise ValueError(
            f"Proveedor '{provider}' no soportado. "
            "Usa 'openai' o 'anthropic'."
        )


# Configuraciones recomendadas para diferentes casos de uso

# Para razonamiento y análisis (temperatura baja)
def get_reasoning_llm(provider: str = "openai"):
    """LLM optimizado para razonamiento lógico y análisis."""
    return get_llm(provider, temperature=0, max_tokens=2000)


# Para generación creativa (temperatura alta)
def get_creative_llm(provider: str = "openai"):
    """LLM optimizado para generación creativa."""
    return get_llm(provider, temperature=0.9, max_tokens=2000)


# Para balance entre creatividad y coherencia
def get_balanced_llm(provider: str = "openai"):
    """LLM con balance entre creatividad y coherencia."""
    return get_llm(provider, temperature=0.7, max_tokens=2000)


# Para respuestas rápidas y económicas
def get_fast_llm():
    """LLM rápido y económico para tareas simples."""
    return get_openai_llm(model="gpt-4o-mini", temperature=0.5, max_tokens=1000)


# Para tareas complejas que requieren el mejor modelo
def get_powerful_llm(provider: str = "openai"):
    """LLM más potente para tareas complejas."""
    if provider == "openai":
        return get_openai_llm(model="gpt-4o", temperature=0.7)
    elif provider == "anthropic":
        return get_anthropic_llm(model="claude-3-5-sonnet-20241022", temperature=0.7)
    else:
        raise ValueError(f"Proveedor '{provider}' no soportado.")
