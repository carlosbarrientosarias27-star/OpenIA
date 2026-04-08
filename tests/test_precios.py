import pytest
from calculadora.precios import GestorPrecios, ModelNotFoundError

def test_calculo_correcto_gpt4o_mini():
    """
    Valida el CASO FELIZ: cálculo exacto para gpt-4o-mini con tokens reales.
    Input: 1.000.000 tokens ($0.15) | Output: 2.000.000 tokens ($1.20) | Total: $1.35
    """
    gestor = GestorPrecios("gpt-4o-mini")
    resultado = gestor.calcular_coste_llamada(1_000_000, 2_000_000)
    
    assert resultado["coste_total_usd"] == pytest.approx(1.35)

def test_calculo_con_tokens_cero():
    """
    Valida el CASO FELIZ: si los tokens son 0, el coste debe ser exactamente 0.0.
    """
    gestor = GestorPrecios("gpt-4o")
    resultado = gestor.calcular_coste_llamada(0, 0)
    
    assert resultado["coste_total_usd"] == pytest.approx(0.0)

def test_no_negatividad_gemini_flash():
    """
    Valida CASO BORDE: un modelo con precios muy bajos (gemini-1.5-flash) 
    no produce costes negativos.
    """
    gestor = GestorPrecios("gemini-1.5-flash")
    resultado = gestor.calcular_coste_llamada(1, 1)
    
    assert resultado["coste_total_usd"] >= 0

def test_error_tokens_negativos():
    """
    Valida CASO ERROR: el sistema debería lanzar ValueError ante tokens negativos.
    Nota: La implementación actual no lo valida, este test fallará (TDD Red step).
    """
    gestor = GestorPrecios("gpt-4o")
    
    with pytest.raises(ValueError):
        gestor.calcular_coste_llamada(-100, 200)

def test_error_modelo_desconocido():
    """
    Valida CASO ERROR: el __init__ lanza ModelNotFoundError si el modelo no existe.
    Nota: Ajustado de ValueError a ModelNotFoundError según la implementación del archivo.
    """
    with pytest.raises(ModelNotFoundError):
        GestorPrecios("modelo-inexistente-2024")