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

# Asignar valores + y - segun sentido del bobinado y direccion de la corriente.
# Falta asignar esta parte
for k in range(0, 361):
    i_a[k] = 2
    i_b[k] = 2
    i_c[k] = 2
    i_d[k] = 2
    i_e[k] = 2

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

with open("Resultados.txt", "a") as f:
    for valor in resultado:
        print(valor, file = f)