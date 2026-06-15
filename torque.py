import numpy as np
import femm as fe

archivo = "simulacion.fem"

resultado = []

fe.openfemm()
fe.opendocument(archivo)
fe.main_resize(1920, 1080)

# Corrientes para las 361 posiciones del rotor.
i_a = np.zeros(361)
i_b = np.zeros(361)
i_c = np.zeros(361)
i_d = np.zeros(361)
i_e = np.zeros(361)

# Conmutacion: cada bobina invierte el signo de su corriente cada vez que su
# centro cruza el eje de los imanes (0 y 180 grados), igual que el colector de
# un motor DC real. El torque de cada bobina es ~ I*sin(theta); sin conmutar,
# la suma de las 5 bobinas (separadas 72 grados) se cancela y el torque es ~0.

I0 = 2.0  # corriente por bobina [A]

# Angulo (grados) del centro de cada bobina en k=0, medido desde el eje de los
# imanes (eje x), obtenido de la geometria del .fem (bisectriz de sus 2 lados).
phi0_a = 1.75
phi0_b = 74.4
phi0_c = 145.05
phi0_d = 218.5
phi0_e = 290.0

# El rotor (grupo 1) gira -1 grado por paso, asi que el centro de la bobina en
# el paso k esta en theta = phi0 - k.
for k in range(0, 361):
    i_a[k] = I0 * np.sign(np.sin(np.deg2rad(phi0_a - k)))
    i_b[k] = I0 * np.sign(np.sin(np.deg2rad(phi0_b - k)))
    i_c[k] = I0 * np.sign(np.sin(np.deg2rad(phi0_c - k)))
    i_d[k] = I0 * np.sign(np.sin(np.deg2rad(phi0_d - k)))
    i_e[k] = I0 * np.sign(np.sin(np.deg2rad(phi0_e - k)))

#

for k in range(0, 360):
    fe.mi_setcurrent("Ia", i_a[k])
    fe.mi_setcurrent("Ib", i_b[k])
    fe.mi_setcurrent("Ic", i_c[k])
    fe.mi_setcurrent("Id", i_d[k])
    fe.mi_setcurrent("Ie", i_e[k])

    fe.mi_analyze()
    fe.mi_loadsolution()
    fe.mo_zoomnatural()

    fe.mo_groupselectblock(1)
    torque = fe.mo_blockintegral(22)
    resultado.append(torque)
    fe.mo_savebitmap(f"./imagenes/Angulo_{k}.bmp")
    fe.mo_clearblock()

    fe.mi_seteditmode("group")
    fe.mi_selectgroup(1)
    fe.mi_moverotate(0, 0, -1)

fe.closefemm()

with open("Resultados.txt", "w") as f:
    for valor in resultado:
        print(valor, file = f)