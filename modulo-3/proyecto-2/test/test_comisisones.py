import pytest

from app.comisiones import calculo_comisiones

def test_ventas_negativas():
    #Arrange
    ventas = -100

    #Act y Assert
    with pytest.raises(ValueError):
        calculo_comisiones(ventas)

def test_ventas_sin_comision():
    #Arrange
    ventas = 800

    #Act
    resultado = calculo_comisiones(ventas)

    #Assert
    assert resultado == 0


def test_comision_media():
    #Arrange
    ventas = 2000

    #Act
    resultado = calculo_comisiones(ventas)
    
def test_comision_alta():
    #Arrange
    ventas = 6000

    #Act 
    resultado = calculo_comisiones(ventas)

    #Assert
    assert resultado == ventas * 0.10
