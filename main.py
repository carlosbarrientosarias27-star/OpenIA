# main.py
from calculadora.precios import GestorPrecios, ModelNotFoundError
from calculadora.tokens import EstimadorTokens
from calculadora.proyecciones import ProyectorUso

def ejecutar_demo() -> None:
    """Ejecuta los ejemplos de uso de la calculadora refactorizada."""
    
    modelo_ejemplo = "gpt-4o-mini"
    
    try:
        # 1. Configuración de componentes
        gestor = GestorPrecios(modelo_ejemplo)
        estimador = EstimadorTokens(modelo_ejemplo)
        proyector = ProyectorUso(gestor)

        print("-" * 30)
        print(f"MODELO: {modelo_ejemplo}")
        print("-" * 30)

        # 2. Ejemplo de conteo y coste puntual
        prompt = "Hola, ¿podrías resumir este documento para mí?"
        tokens_in = estimador.contar(prompt)
        tokens_out = 50  # Estimación fija para el ejemplo
        
        coste_fijo = gestor.calcular_coste_llamada(tokens_in, tokens_out)
        print(f"Coste de 1 llamada ({tokens_in} in / {tokens_out} out):")
        print(f"USD: ${coste_fijo['coste_total_usd']:.6f}")

        # 3. Ejemplo de proyección mensual
        proyeccion = proyector.calcular_mensual(
            llamadas_dia=100,
            input_promedio=200,
            output_promedio=300
        )
        
        print(f"\nProyección Mensual (100 llamadas/día):")
        print(f"Total Llamadas: {proyeccion['total_llamadas']:.0f}")
        print(f"Coste Mensual: ${proyeccion['coste_mensual_usd']:.2f}")
        print(f"Coste por Llamada: ${proyeccion['coste_por_llamada']:.6f}")

    except ModelNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    ejecutar_demo()