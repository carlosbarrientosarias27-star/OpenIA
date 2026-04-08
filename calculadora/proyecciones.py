# calculadora/proyecciones.py
from typing import Dict
from calculadora.precios import GestorPrecios

class ProyectorUso:
    """Realiza estimaciones de costes a largo plazo basadas en volumen."""

    def __init__(self, gestor_precios: GestorPrecios):
        """
        Inicializa el proyector.
        
        Args:
            gestor_precios: Instancia de GestorPrecios configurada.
        """
        self.gestor = gestor_precios

    def calcular_mensual(self, 
                         llamadas_dia: int, 
                         input_promedio: int, 
                         output_promedio: int, 
                         dias: int = 30) -> Dict[str, float]:
        """
        Proyecta el coste mensual basado en promedios de uso.
        
        Args:
            llamadas_dia: Número de llamadas diarias estimadas.
            input_promedio: Media de tokens de entrada por llamada.
            output_promedio: Media de tokens de salida por llamada.
            dias: Duración del periodo en días.
            
        Returns:
            Diccionario con métricas de volumen y costes proyectados.
        """
        total_llamadas = llamadas_dia * dias
        total_input = total_llamadas * input_promedio
        total_output = total_llamadas * output_promedio
        
        costes = self.gestor.calcular_coste_llamada(total_input, total_output)
        
        return {
            "total_llamadas": float(total_llamadas),
            "total_tokens_input": float(total_input),
            "total_tokens_output": float(total_output),
            "coste_mensual_usd": costes["coste_total_usd"],
            "coste_por_llamada": costes["coste_total_usd"] / total_llamadas if total_llamadas > 0 else 0.0
        }