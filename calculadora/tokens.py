# calculadora/tokens.py
import tiktoken

class EstimadorTokens:
    """Encapsula la lógica de conteo de tokens para diferentes modelos."""

    def __init__(self, modelo: str):
        """
        Inicializa el estimador.
        
        Args:
            modelo: Nombre del modelo para determinar el encoding.
        """
        try:
            self.encoding = tiktoken.encoding_for_model(modelo)
        except KeyError:
            # Fallback a o200k_base si el modelo es muy reciente o desconocido por tiktoken
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def contar(self, texto: str) -> int:
        """
        Calcula el número exacto de tokens de un texto.
        
        Args:
            texto: Cadena de texto a procesar.
            
        Returns:
            Número entero de tokens.
        """
        return len(self.encoding.encode(texto))

if __name__ == "__main__":
    # Este bloque solo se ejecuta si corres este archivo directamente
    estimador = EstimadorTokens("gpt-4")
    texto_ejemplo = "Hola, ¿cuántos tokens tiene esta frase?"
    n_tokens = estimador.contar(texto_ejemplo)
    print(f"El texto tiene {n_tokens} tokens.")