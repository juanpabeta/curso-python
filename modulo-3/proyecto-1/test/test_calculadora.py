import pytest
from app.calculadora import sumar

def test_sumar():
    a = 5
    b = 5

    resultado = sumar(a, b)

    assert resultado == 10

    