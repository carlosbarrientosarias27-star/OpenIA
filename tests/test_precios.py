import pytest
from typing import Dict
import calculadora.precios

class TestPreciosConfig:
    """Suite de pruebas para validar la configuración de tarifas de modelos de IA."""

    # --- Fixtures ---
    
    @pytest.fixture
    def expected_models(self):
        """Proporciona la lista de modelos mínimos que deben existir en la config."""
        return ["gpt-4o", "gpt-4o-mini", "gemini-1.5-flash", "gemini-1.5-pro"]

    # --- Happy Path ---

    def test_precios_structure_is_correct(self):
        """Valida que PRECIOS_MODELS sea un diccionario con el formato {modelo: {input, output}}."""
        assert isinstance(calculadora.precios.PRECIOS_MODELS, dict)
        for model, rates in calculadora.precios.PRECIOS_MODELS.items():
            assert "input" in rates
            assert "output" in rates
            assert isinstance(rates["input"], (float, int))
            assert isinstance(rates["output"], (float, int))

    def test_specific_model_rates(self):
        """Verifica que las tarifas de un modelo específico (ej. GPT-4o) sean las correctas según contrato."""
        gpt_4o_rates = calculadora.precios.PRECIOS_MODELS.get("gpt-4o")
        assert gpt_4o_rates["input"] == 2.50
        assert gpt_4o_rates["output"] == 10.00

    def test_default_model_exists_in_dict(self):
        """Asegura que el modelo por defecto definido exista en el diccionario de precios."""
        assert calculadora.precios.DEFAULT_MODEL in calculadora.precios.PRECIOS_MODELS

    # --- Edge Cases ---

    def test_prices_are_positive(self):
        """Valida que no existan tarifas negativas o iguales a cero (caso borde de gratuidad)."""
        for model, rates in calculadora.precios.PRECIOS_MODELS.items():
            assert rates["input"] > 0, f"El input de {model} debe ser mayor a 0"
            assert rates["output"] > 0, f"El output de {model} debe ser mayor a 0"

    def test_high_precision_decimals(self):
        """Valida modelos con precisión decimal alta, como Gemini 1.5 Flash."""
        flash_input = calculadora.precios.PRECIOS_MODELS["gemini-1.5-flash"]["input"]
        # Verificamos que se mantenga la precisión de 3 decimales (0.075)
        assert flash_input == 0.075
        assert isinstance(flash_input, float)

    # --- Negative Testing ---

    @pytest.mark.parametrize("invalid_model", ["claude-2", "llama-3", "gpt-3.5-turbo"])
    def test_unsupported_models_not_present(self, invalid_model):
        """Verifica que modelos obsoletos o no definidos no estén en la configuración actual."""
        assert invalid_model not in calculadora.precios.PRECIOS_MODELS

    def test_config_immutability_check(self):
        """
        Validación de integridad: Verifica que los valores clave no sean None o tipos erróneos.
        Nota: En Python los dicts son mutables, este test previene errores de definición manual.
        """
        for model in calculadora.precios.PRECIOS_MODELS:
            rates = calculadora.precios.PRECIOS_MODELS[model]
            assert isinstance(rates, dict), f"Las tarifas de {model} deben ser un diccionario"
            assert len(rates) == 2, f"{model} tiene una cantidad de parámetros de precio incorrecta"

    def test_default_model_type(self):
        """Valida que el nombre del modelo por defecto sea estrictamente un string."""
        assert isinstance(calculadora.precios.DEFAULT_MODEL, str)