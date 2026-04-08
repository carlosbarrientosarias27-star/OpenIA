# calculadora/precios.py
from typing import Dict

class ModelNotFoundError(Exception):
    """Excepción lanzada cuando se solicita un modelo no configurado."""
    pass

class GestorPrecios:
    """Gestiona los precios por millón de tokens y calcula costes base."""

    PRECIOS: Dict[str, Dict[str, float]] = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "claude-3-sonnet": {"input": 3.00, "output": 15.00},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    }

    def __init__(self, modelo: str):
        """
        Inicializa el gestor con un modelo específico.
        
        Args:
            modelo: Nombre del modelo de IA.
        Raises:
            ModelNotFoundError: Si el modelo no existe en el diccionario de precios.
        """
        if modelo not in self.PRECIOS:
            raise ModelNotFoundError(f"El modelo '{modelo}' no está soportado.")
        
        self.modelo = modelo
        self.tarifas = self.PRECIOS[modelo]

    def calcular_coste_llamada(self, tokens_input: int, tokens_output: int) -> Dict[str, float]:
        """
        Calcula el desglose de costes para una cantidad de tokens.
        
        Args:
            tokens_input: Cantidad de tokens de entrada.
            tokens_output: Cantidad de tokens de salida.
            
        Returns:
            Diccionario con costes en USD y céntimos.
        """
        coste_input = (tokens_input / 1_000_000) * self.tarifas["input"]
        coste_output = (tokens_output / 1_000_000) * self.tarifas["output"]
        total = coste_input + coste_output

        return {
            "coste_input_usd": coste_input,
            "coste_output_usd": coste_output,
            "coste_total_usd": total,
            "coste_total_cent": total * 100
        }