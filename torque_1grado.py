import numpy as np
import femm as fe

archivo = "simulacion_final.fem"

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

# Conmutacion pre-fijada (OFFSET = 30 grados): es la que dio el buen resultado
# (~0.13 Nm promedio, todo positivo). Cada bobina lleva el signo de corriente
# que hace que su aporte de torque sea siempre del mismo sentido:
#     i = I0 * sign( sin( ang - phi0 - OFFSET ) )
I0 = 2.0
OFFSET = 30.0
phi0_a = 1.75
phi0_b = 74.4
phi0_c = 145.05
phi0_d = 218.5
phi0_e = 290.0

for k in range(0, 361):
    i_a[k] = I0 * np.sign(np.sin(np.deg2rad(k - phi0_a - OFFSET)))
    i_b[k] = I0 * np.sign(np.sin(np.deg2rad(k - phi0_b - OFFSET)))
    i_c[k] = I0 * np.sign(np.sin(np.deg2rad(k - phi0_c - OFFSET)))
    i_d[k] = I0 * np.sign(np.sin(np.deg2rad(k - phi0_d - OFFSET)))
    i_e[k] = I0 * np.sign(np.sin(np.deg2rad(k - phi0_e - OFFSET)))


for k in range(0, 360):
    print(f"ITERACIÓN: {k}° con valores de corriente: A: {i_a[k]}, B: {i_b[k]}, C: {i_c[k]}, D: {i_d[k]}, E: {i_e[k]}")
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

with open("Resultados.txt", "a") as f:
    for valor in resultado:
        print(valor, file = f)
