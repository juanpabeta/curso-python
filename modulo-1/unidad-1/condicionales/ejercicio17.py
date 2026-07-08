### Cálculo de impuesto según salario**
"""
**Descripción:**
El usuario ingresa su salario mensual. Se aplica impuesto según rango:

| Rango               | Impuesto |
| ------------------- | -------- |
| ≤ 2.000.000         | 0%       |
| 2.000.001–5.000.000 | 10%      |
| > 5.000.000         | 20%      |
"""



while True:
    try:
        salario_Mensual = float(input("Ingresa tu salario mensual: $ "))

        if salario_Mensual < 0:
            print("No se puede poner salario negativo")
            continue        
        break
    except ValueError:
        print("\n\nIngresa solo numeros\n\n")

if salario_Mensual <= 2000000:
    impuesto = 0.0
elif salario_Mensual >= 2000001 and salario_Mensual <=  5000000:
    impuesto = 0.10
elif salario_Mensual > 5000000:
    impuesto = 0.20

total_Salario = salario_Mensual*(1-impuesto)

print(f"EL impuesto aplicado a su salario es de:{impuesto * 100:.0f}% ") 
print(f"Su salario total es de: {total_Salario:,.0f}")    