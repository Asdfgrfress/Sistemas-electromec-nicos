import matplotlib.pyplot as plt
import numpy as np

with open("Resultados.txt", "r") as f:
    datos = [float(line.strip()) for line in f.readlines()]

valores = np.array(datos)
angulos = np.zeros(len(datos))

for k in range(len(datos)):
    angulos[k] = k

print(datos)
print(angulos)

plt.plot(angulos, valores)
plt.xlabel("Ángulo del rotor (grados)")
plt.ylabel("Torque (Nm)")
plt.xlim(0, 370)
plt.ylim(0, max(valores) * 1.1)
plt.title("Torque vs Ángulo del Rotor")
plt.grid()
plt.savefig("Torque_vs_Angulo.png")
plt.show()


