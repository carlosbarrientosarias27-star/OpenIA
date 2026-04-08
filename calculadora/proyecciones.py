"""Módulo para el cálculo de costes y proyecciones financieras de API."""
from typing import Dict
from calculadora.precios import PRECIOS_MODELS, DEFAULT_MODEL

class CalculadoraFinanciera:
    """Motor de cálculo de costes operativos para APIs de IA."""

    def __init__(self, modelo: str = DEFAULT_MODEL):
        """Inicializa la calculadora con las tarifas del modelo elegido.

        Args:
            modelo: Nombre del modelo (ej. 'gpt-4o').
        """
        self.modelo = modelo
        self.tarifas = PRECIOS_MODELS.get(modelo, PRECIOS_MODELS[DEFAULT_MODEL])

    def calcular_llamada_unica(self, tokens_in: int, tokens_out: int) -> Dict[str, float]:
        """Calcula el coste de una única transacción.

        Args:
            tokens_in: Tokens de entrada.
            tokens_out: Tokens de salida.

        Returns:
            Dict con el desglose de costes en USD y céntimos.
        """
        coste_in = (tokens_in / 1_000_000) * self.tarifas["input"]
        coste_out = (tokens_out / 1_000_000) * self.tarifas["output"]
        total = coste_in + coste_out

        return {
            "usd_total": total,
            "cent_total": total * 100,
            "desglose_in": coste_in,
            "desglose_out": coste_out
        }

    def proyectar_mensual(self, 
                          llamadas_dia: int, 
                          tokens_in: int, 
                          tokens_out: int, 
                          dias: int = 30) -> Dict[str, float]:
        """Realiza una proyección de gastos a 30 días.

        Args:
            llamadas_dia: Volumen diario de peticiones.
            tokens_in: Promedio de tokens de entrada por petición.
            tokens_out: Promedio de tokens de salida por petición.
            dias: Duración del periodo a calcular.

        Returns:
            Dict con la proyección mensual detallada.
        """
        total_llamadas = llamadas_dia * dias
        coste_unidad = self.calcular_llamada_unica(tokens_in, tokens_out)
        coste_mensual = coste_unidad["usd_total"] * total_llamadas

        return {
            "llamadas_totales": float(total_llamadas),
            "coste_mensual_usd": coste_mensual,
            "coste_por_llamada": coste_unidad["usd_total"]
        }

if __name__ == "__main__":
    # Ejemplo de ejecución aislada para pruebas de desarrollo
    calc = CalculadoraFinanciera("gpt-4o")
    print(f"Proyección GPT-4o: {calc.proyectar_mensual(100, 500, 500)}")