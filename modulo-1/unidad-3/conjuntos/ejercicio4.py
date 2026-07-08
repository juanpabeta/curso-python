"""Ejercicio 2 — Verificar acceso (operador in)
Un sistema tiene usuarios autorizados:
usuarios_autorizados = {"ana", "carlos", "maria", "pedro"}
El programa debe pedir un nombre y decir si puede entrar o no.
Actividad
•	Solicitar un nombre con input
•	Indicar si pertenece al conjunto
Qué debe aprender el estudiante: Los sets permiten búsquedas extremadamente rápidas (mejor que lista)"""
usuarios_autorizados = {"ana", "carlos", "maria", "pedro"}
nombre = input("Ingrese su nombre de usuario para verificar si puede entrar: ").strip().lower()


if nombre in usuarios_autorizados:
    print(f"{nombre} puedes pasar")
else:
    print(f"{nombre} no puedes pasar")
