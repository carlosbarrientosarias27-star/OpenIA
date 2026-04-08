"""Módulo de configuración de tarifas para modelos de IA."""
from typing import Dict

# Tarifas por cada 1.000.000 de tokens (Actualizado 2025)
PRECIOS_MODELS: Dict[str, Dict[str, float]] = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
}

DEFAULT_MODEL = "gpt-4o-mini"