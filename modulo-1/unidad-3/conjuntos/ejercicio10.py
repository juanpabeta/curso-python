"""Tienes un conjunto con IDs de sensores activos y otro con IDs defectuosos. Elimina los defectuosos y conserva solo los operativos.

sensores_activos = {101, 102, 103, 104, 105}
sensores_defectuosos = {102, 105}
"""

sensores_activos = {101, 102, 103, 104, 105}
sensores_defectuosos = {102, 105}

sensores_operativos = sensores_activos.difference(sensores_defectuosos)
print(f"Los sensores que están funcionando son: {sensores_operativos}")