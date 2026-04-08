import pytest

# Asumiendo una estructura donde 'app.tokens' contiene la lógica
# de cálculo de valor y validación de tokens.
def calculate_token_value(amount, rate):
    if amount < 0 or rate < 0:
        raise ValueError("Los valores no pueden ser negativos")
    return amount * rate

def validate_token_format(token_id):
    if not token_id.startswith("TK-"):
        raise ValueError("Formato de ID inválido")
    return True

# --- TESTS ---

def test_calculate_value_standard_input():
    """
    CASO FELIZ 1: Valida que el cálculo del valor total sea correcto
    con entradas estándar de tipo float.
    """
    result = calculate_token_value(10.5, 1.5)
    assert result == pytest.approx(15.75)

def test_token_id_prefix_validation():
    """
    CASO FELIZ 2: Verifica que un ID de token correctamente formado
    sea validado como exitoso.
    """
    result = validate_token_format("TK-12345")
    assert result is True

def test_calculate_value_at_zero_boundary():
    """
    CASO BORDE: Valida el comportamiento del sistema cuando el
    monto es exactamente cero (límite inferior permitido).
    """
    result = calculate_token_value(0, 1.5)
    assert result == pytest.approx(0.0)

def test_error_on_negative_amount():
    """
    CASO ERROR 1: Asegura que el sistema lance una excepción ValueError
    si se intenta calcular un valor con un monto negativo.
    """
    with pytest.raises(ValueError, match="Los valores no pueden ser negativos"):
        calculate_token_value(-1, 1.5)

def test_error_on_invalid_id_format():
    """
    CASO ERROR 2: Verifica que se lance un ValueError si el ID del
    token no cumple con el prefijo obligatorio 'TK-'.
    """
    with pytest.raises(ValueError, match="Formato de ID inválido"):
        validate_token_format("BAD-99")