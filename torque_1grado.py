import shutil
import numpy as np
import femm as fe

archivo = "simulacion_final.fem"
tmp = "_run_tmp_1.fem"   # se trabaja sobre una copia: el original NUNCA se modifica

resultado = []


# Lee del .fem el angulo real del centro de cada bobina (circuitos 1..5 = Ia..Ie).
# Asi la conmutacion funciona sin importar en que posicion quedo guardado el rotor
# (mi_analyze guarda el .fem rotado; esto nos hace inmunes a eso).
def leer_centros(path):
    lineas = open(path).read().splitlines()
    start = n = None
    for i, l in enumerate(lineas):
        if l.startswith('[NumBlockLabels]'):
            n = int(l.split('=')[1]); start = i + 1; break
    lados = {1: [], 2: [], 3: [], 4: [], 5: []}
    for l in lineas[start:start + n]:
        p = l.split()
        mat = int(p[2]); incirc = int(p[4])
        if mat == 4 and incirc in lados:          # material 4 = 22 AWG (bobinas)
            ang = np.degrees(np.arctan2(float(p[1]), float(p[0]))) % 360
            lados[incirc].append(ang)
    centros = {}
    for c, a in lados.items():
        a = sorted(a)
        if a[1] - a[0] > 180:                      # corrige el cruce por 0 grados
            a = [a[1], a[0] + 360]
        centros[c] = (a[0] + a[1]) / 2.0 % 360
    return centros


I0 = 2.0
centros = leer_centros(archivo)   # {1:Ia, 2:Ib, 3:Ic, 4:Id, 5:Ie}

# Corrientes para las 361 posiciones del rotor.
i_a = np.zeros(361)
i_b = np.zeros(361)
i_c = np.zeros(361)
i_d = np.zeros(361)
i_e = np.zeros(361)

# Conmutacion: cada bobina invierte su signo de corriente al cruzar el eje de los
# imanes, partiendo del angulo real de cada bobina leido del archivo.
arr = {1: i_a, 2: i_b, 3: i_c, 4: i_d, 5: i_e}
for c in range(1, 6):
    for k in range(0, 361):
        arr[c][k] = I0 * np.sign(np.sin(np.deg2rad(k - centros[c])))

shutil.copyfile(archivo, tmp)

fe.openfemm()
fe.opendocument(tmp)
fe.main_resize(1920, 1080)

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

with open("Resultados.txt", "w") as f:
    for valor in resultado:
        print(valor, file = f)
