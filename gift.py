import imageio.v2 as imageio
import os

fps = 120
tiempo = 1/fps

salida = "simulacion.gif"

imagenes = []

for k in range(0, 360):
    imagen = imageio.imread(f"./imagenes/Angulo_{k}.bmp")
    imagenes.append(imagen)

imageio.mimsave(
    salida,
    imagenes,
    duration = tiempo 
)

print("GIF creado:", salida)
    
