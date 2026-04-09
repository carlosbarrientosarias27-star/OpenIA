# calculadora/precios.py
from typing import Dict

class ModelNotFoundError(Exception):
    """Excepción lanzada cuando se solicita un modelo no configurado."""
    pass

class GestorPrecios:
    """Gestiona los precios por millón de tokens y calcula costes base."""

    # Diccionario maestro de precios por cada 1M de tokens
    PRECIOS: Dict[str, Dict[str, float]] = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "claude-3-sonnet": {"input": 3.00, "output": 15.00},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    }

    def __init__(self, modelo: str):
        if modelo not in self.PRECIOS:
            raise ModelNotFoundError(f"El modelo '{modelo}' no está soportado.")
        
        self.modelo = modelo
        # Cambiamos 'tarifas' por 'precios' para coincidir con tu lógica de cálculo
        self.precios = self.PRECIOS[modelo] 

    def calcular_coste_llamada(self, tokens_input: int, tokens_output: int) -> Dict[str, float]:
        """
        Calcula el coste de una llamada específica basado en precios por millón de tokens.
        Mantiene consistencia con la llamada en InterfazCostes.py (línea 102).
        """
        # 1. Validación de seguridad
        if tokens_input < 0 or tokens_output < 0:
            raise ValueError("Los tokens no pueden ser negativos")

        # 2. Lógica de cálculo ($/1M tokens)
        coste_input = (tokens_input / 1_000_000) * self.precios["input"]
        coste_output = (tokens_output / 1_000_000) * self.precios["output"]
        coste_total = coste_input + coste_output
        
        # 3. Retorno del diccionario completo para la UI
        return {
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "coste_input_usd": coste_input,
            "coste_output_usd": coste_output,
            "coste_total_usd": coste_total,
            "coste_total_cent": coste_total * 100
        }