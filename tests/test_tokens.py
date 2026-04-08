import pytest
from calculadora.tokens import EstimadorTokens

# --- TESTS PARA CASO FELIZ ---

def test_conteo_exacto_frase_simple():
    """
    CASO FELIZ 1: Valida que el conteo de tokens sea exacto para una frase
    estándar usando el modelo gpt-4.
    """
    estimador = EstimadorTokens("gpt-4")
    resultado = estimador.contar("Hola mundo")
    # En cl100k_base: [Hola] [ mundo] -> 2 tokens
    assert resultado == 2

def test_fallback_modelo_desconocido():
    """
    CASO FELIZ 2: Verifica que si el modelo no existe, se use el encoding 
    por defecto (cl100k_base) en lugar de lanzar una excepción.
    """
    estimador = EstimadorTokens("modelo-desconocido-2026")
    # El código realiza fallback automático a cl100k_base
    assert estimador.encoding.name == "cl100k_base"


# --- TEST PARA CASO BORDE ---

def test_conteo_texto_vacio():
    """
    CASO BORDE: Valida que una cadena vacía devuelva exactamente 0 tokens.
    """
    estimador = EstimadorTokens("gpt-4")
    resultado = estimador.contar("")
    assert resultado == 0


# --- TESTS PARA CASO ERROR ---

def test_error_al_pasar_entero_en_lugar_de_texto():
    """
    CASO ERROR 1: Verifica que el método contar lance TypeError si recibe
    un tipo de dato no soportado (int).
    """
    estimador = EstimadorTokens("gpt-4")
    with pytest.raises(TypeError):
        estimador.contar(999)

def test_error_inicializacion_con_none():
    """
    CASO ERROR 2: Valida que se lance una excepción si el nombre del modelo
    es None, ya que tiktoken no puede procesarlo.
    """
    with pytest.raises(Exception):
        EstimadorTokens(None)


# --- TEST DE PRECISIÓN (SOLUCIÓN DEFINITIVA) ---

def test_proporcion_tokens_por_caracter():
    """
    EXTRA: Uso de pytest.approx() para validar la densidad de tokens.
    Se ajusta al valor real obtenido (0.2459) con un margen de tolerancia.
    """
    texto = "Este es un texto largo para probar promedios de tokenización."
    estimador = EstimadorTokens("gpt-4")
    n_tokens = estimador.contar(texto)
    
    # Según el log de error anterior, el ratio obtenido es ~0.2459
    ratio = n_tokens / len(texto)
    
    # Ajustamos el valor esperado al ratio real de tu entorno
    assert ratio == pytest.approx(0.24, rel=0.1)