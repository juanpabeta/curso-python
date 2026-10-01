def calculo_comisiones(ventas:float) -> float:
    if ventas < 0:
        raise ValueError("Las ventas no pueden ser negativas")
    if ventas < 1000:
        return 0
    if ventas < 5000:
        return ventas * 0.05
    return ventas * 0.10
    
    	