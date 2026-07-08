frutas = {"pera","manzana","uva","banano"}
frutas.add("mango")
print(frutas)


frutas.discard("manzana")
print(frutas)

a = {1,2,3}
b = {3,4,5}

# union
print(a | b) # {1, 2, 3, 4, 5}
#intersección
print(a & b) # {3}
# diferencia
print(a - b) # {1, 2}
print(a ^ b) # {1, 2, 4, 5}