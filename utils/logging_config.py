"""
Configuración de logging para el tutorial.

Proporciona loggers configurados para diferentes niveles de verbosidad
y formatos útiles para debugging de sistemas multi-agente.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Colores para terminal (ANSI escape codes)
class Colors:
    """Códigos de color ANSI para terminal."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"


class ColoredFormatter(logging.Formatter):
    """
    Formatter que agrega colores a los logs en terminal.
    """

    COLORS = {
        "DEBUG": Colors.GRAY,
        "INFO": Colors.BLUE,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.RED + Colors.BOLD,
    }

    def format(self, record):
        # Agregar color según el nivel
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{levelname}{Colors.RESET}"
            )

        # Agregar color al nombre del logger
        record.name = f"{Colors.CYAN}{record.name}{Colors.RESET}"

        return super().format(record)


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    colored: bool = True
) -> logging.Logger:
    """
    Configura un logger con formato consistente.

    Args:
        name: Nombre del logger (típicamente __name__ del módulo)
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Ruta opcional para guardar logs en archivo
        colored: Si True, usa colores en la consola

    Returns:
        Logger configurado

    Ejemplos:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Mensaje de información")
        >>> logger.debug("Mensaje de debug (no se muestra con level=INFO)")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers si el logger ya existe
    if logger.handlers:
        return logger

    # Formato del mensaje
    format_string = (
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    date_format = "%H:%M:%S"

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    if colored:
        console_formatter = ColoredFormatter(format_string, datefmt=date_format)
    else:
        console_formatter = logging.Formatter(format_string, datefmt=date_format)

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Handler opcional para archivo
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(format_string, datefmt=date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def setup_tutorial_logging(
    level: int = logging.INFO,
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """
    Configura logging para el tutorial completo.

    Args:
        level: Nivel de logging para todos los loggers
        log_dir: Directorio opcional para guardar logs

    Returns:
        Logger principal del tutorial

    Ejemplos:
        >>> logger = setup_tutorial_logging(level=logging.DEBUG)
        >>> logger.info("Tutorial iniciado")
    """
    # Crear directorio de logs si se especifica
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"tutorial_{timestamp}.log"
    else:
        log_file = None

    # Logger principal
    main_logger = setup_logger(
        "tutorial",
        level=level,
        log_file=log_file,
        colored=True
    )

    return main_logger


# Logger específicos para diferentes componentes

def get_agent_logger(agent_name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Logger para un agente específico.

    Args:
        agent_name: Nombre del agente
        level: Nivel de logging

    Returns:
        Logger configurado para el agente
    """
    return setup_logger(f"agent.{agent_name}", level=level)


def get_tool_logger(tool_name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Logger para una herramienta específica.

    Args:
        tool_name: Nombre de la herramienta
        level: Nivel de logging

    Returns:
        Logger configurado para la herramienta
    """
    return setup_logger(f"tool.{tool_name}", level=level)


def get_workflow_logger(workflow_name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Logger para un workflow específico.

    Args:
        workflow_name: Nombre del workflow
        level: Nivel de logging

    Returns:
        Logger configurado para el workflow
    """
    return setup_logger(f"workflow.{workflow_name}", level=level)


# Funciones helper para logging estructurado

def log_llm_call(logger: logging.Logger, model: str, prompt_length: int):
    """
    Loggea una llamada a un LLM.

    Args:
        logger: Logger a usar
        model: Nombre del modelo
        prompt_length: Longitud del prompt en caracteres
    """
    logger.debug(f"LLM call: model={model}, prompt_length={prompt_length}")


def log_tool_execution(
    logger: logging.Logger,
    tool_name: str,
    args: dict,
    result: str,
    duration_ms: float
):
    """
    Loggea la ejecución de una herramienta.

    Args:
        logger: Logger a usar
        tool_name: Nombre de la herramienta
        args: Argumentos pasados
        result: Resultado retornado (truncado si es muy largo)
        duration_ms: Duración en milisegundos
    """
    result_preview = result[:100] + "..." if len(result) > 100 else result
    logger.info(
        f"Tool executed: {tool_name} | "
        f"args={args} | "
        f"result='{result_preview}' | "
        f"duration={duration_ms:.2f}ms"
    )


def log_state_update(logger: logging.Logger, field: str, value_preview: str):
    """
    Loggea una actualización de estado.

    Args:
        logger: Logger a usar
        field: Campo del estado actualizado
        value_preview: Preview del nuevo valor
    """
    logger.debug(f"State updated: {field} = '{value_preview}'")


def log_graph_step(logger: logging.Logger, node_name: str, step_number: int):
    """
    Loggea un paso en la ejecución del grafo.

    Args:
        logger: Logger a usar
        node_name: Nombre del nodo ejecutado
        step_number: Número del paso
    """
    logger.info(f"Step {step_number}: Executing node '{node_name}'")


# Ejemplo de uso en un módulo
if __name__ == "__main__":
    # Setup básico
    logger = setup_tutorial_logging(level=logging.DEBUG)

    # Ejemplos de logs
    logger.debug("Este es un mensaje de debug")
    logger.info("Este es un mensaje informativo")
    logger.warning("Esta es una advertencia")
    logger.error("Este es un error")

    # Logger específico para un agente
    agent_logger = get_agent_logger("research_agent")
    agent_logger.info("Agente de investigación iniciado")

    # Logging estructurado
    log_llm_call(logger, "gpt-4o-mini", 1500)
    log_tool_execution(
        logger,
        "calculator",
        {"expression": "2 + 2"},
        "4",
        15.5
    )
