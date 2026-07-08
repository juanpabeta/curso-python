"""f = open("datos.txt","r")
file1 = open("datos.txt","w")
file2 = open("datos.txt","a")
file3 = open("datos.txt","r+")

with open("datos.txt","r", encoding= "utf-8") as f:
    contenido = f.read()
"""  
#Metodo de lectura
with open("letras.txt","w",encoding= "utf-8") as f:
    f.write("A \n")
    f.write("B \n")
    f.write("C \n")
    f.write("D \n")

#Metodo de lectura .read()
with open("letras.txt","r",encoding= "utf-8")as f:
    print(f.read())

#Metodo .readlines() imprime una lista con los elementos que estan en el archivo 
with open("letras.txt","r",encoding= "utf-8")as f:
    print(f.readlines())

#convención de para separar texto en un archivo plano(txt,json)
#Nombre|Apellido
    
