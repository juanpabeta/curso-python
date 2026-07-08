
temperatura = int(input("Ingrese la temperatura en grados celcius: "))

if temperatura < 0:
    print("Esta muy helado 🥶")
elif temperatura > 0 and temperatura <=21:
    print("Clima templado 🌤️")
elif temperatura >21 and temperatura <= 30:
    print("Clima agradable 🌞 ")
elif temperatura > 30:
    print("Es un infierno 🥵 ")
    