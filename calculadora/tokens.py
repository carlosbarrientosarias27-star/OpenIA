"""Módulo para la gestión y conteo de tokens."""
import tiktoken
import logging

def estimar_tokens(texto: str, modelo: str) -> int:
    """Calcula la cantidad de tokens de una cadena de texto.

    Args:
        texto: El contenido a procesar.
        modelo: El nombre del modelo para determinar el encoding.

    Returns:
        int: Cantidad de tokens estimados.

    Raises:
        ValueError: Si el modelo no es reconocido por tiktoken.
    """
    try:
        encoding = tiktoken.encoding_for_model(modelo)
        return len(encoding.encode(texto))
    except KeyError:
        logging.warning(f"Modelo {modelo} no encontrado en tiktoken. Usando cl100k_base por defecto.")
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(texto))
    except Exception as e:
        raise ValueError(f"Error al procesar tokens: {e}")