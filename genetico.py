from typing import Sequence, Tuple
from bitarray import bitarray

import matplotlib
import matplotlib.pyplot as plt
import random

# Parametros del problema
_CAPACIDAD_MOCHILA = 4
_PESO_MAX = 1
_VALOR_MAX = 200
_NO_OBJETOS = 22

# Parametros del algoritmo genetico
_TAMANO_POBLACION = 100
_GENERACIONES_MAX = 300
_PORCENTAJE_RETENCION = 0.3
_MU = 0.2 #Porcentaje de mutacion

# Genera una lista de tuplas donde cada elemento es la representacion de un objeto
# El primer elemento de cada tupla representa el peso del objeto, generado de manera aleatoria
# El segundo elemento de cada tupla representa el valor del objeto, generado de manera aleatoria

_OBJETOS = [
        (random.randint(1, _PESO_MAX), random.randint(1, _VALOR_MAX))
        for i in range(0, _NO_OBJETOS)
]

# Funcion objetivo
# Evalua un individuo (bitarray) y regresa un escalar que representa la aptitud del individuo
def f(individuo: bitarray):
    peso = 0
    valor = 0

    for i in range(0, len(individuo)):
        if individuo[i]:
            peso += _OBJETOS[i][0]
            valor += _OBJETOS[i][1]

    if peso <= _CAPACIDAD_MOCHILA:
        return valor
    else:
        return valor/peso

# Extraer estadisticas
def calcula_estadisticas(poblacion: Sequence[Tuple[bitarray, float]]) -> Tuple[float, float]:
    mejor_aptitud = max([individuo[1] for individuo in poblacion])
    aptitud_promedio = sum(individuo[1] for individuo in poblacion)/_TAMANO_POBLACION
    return mejor_aptitud, aptitud_promedio

# Mejor individuo
def seleccionar_mejor(poblacion: Sequence[Tuple[bitarray, float]]) -> Tuple[bitarray, float]:
    mejor_aptitud = max([individuo[1] for individuo in poblacion])

    for individuo in poblacion:
        if individuo[1] == mejor_aptitud:
            return individuo

# Seleccion por ruleta
def ruleta(poblacion: Sequence[Tuple[bitarray, float]]) -> int:
    aptitud_total = sum(individuo[1] for individuo in poblacion)
    suma = 0

    for i in range(0, len(poblacion)):
        individuo = poblacion[i]
        suma += individuo[1]

        if random.random() < suma:
            return i

    return i


# Cruza uniforme
# Por cada uno de los genes, con una probabilidad aleatoria
# Tomamos el gen de un padre u otro
def cruza(padre_a: bitarray, padre_b: bitarray) -> bitarray:
    hijo = bitarray(_NO_OBJETOS)

    for i in range(0, len(hijo)):
        hijo[i] = padre_a[i] if random.random() >= 0.5 else padre_b[i]

    return hijo

# Mutacion
# Elegimos un gen de manera aleatoria e invertimos su valor
def mutar(individuo: bitarray) -> bitarray:
    gen_mutante = random.randint(0, len(individuo) - 1)
    individuo[gen_mutante] = not individuo[gen_mutante]
    return individuo


# Generamos los individuos de la poblacion inicial
# El valor de cada posicion de la cadena de bits, significa si se selecciona o no el objeto en la posicion
# 0 significa no seleccion, 1 significa seleccion
poblacion = []

for i in range(0, _TAMANO_POBLACION):
    individuo = bitarray(_NO_OBJETOS)
    poblacion.append((individuo, f(individuo)))

# Evolucion
# Guardamos la mejor aptitud y la aptitud promedio
estadisticas = []
estadisticas.append(calcula_estadisticas(poblacion))

numero_retenidos = int(_TAMANO_POBLACION*_PORCENTAJE_RETENCION)

for g in range(0, _GENERACIONES_MAX):
    # Seleccion por ruleta
    individuos_retenidos = []
    mejor_individuo = seleccionar_mejor(poblacion)
    individuos_retenidos.append(mejor_individuo)
    poblacion.remove(mejor_individuo)

    for i in range(0, numero_retenidos - 1):
        seleccionado = poblacion[ruleta(poblacion)]
        individuos_retenidos.append(seleccionado)
        poblacion.remove(seleccionado)

    # Copiamos los individuos retenidos a la siguiente generacion
    siguiente_generacion = individuos_retenidos[:]

    # Para el resto de la poblacion cruzamos los individuos
    padres = poblacion + individuos_retenidos

    for i in range(0, _TAMANO_POBLACION - numero_retenidos):
        padre_a = padres[i]
        indices_parejas = [i for i in range(0, len(padres))]
        indices_parejas.remove(i)
        padre_b = padres[random.choice(indices_parejas)]
        # Cruza
        hijo = cruza(padre_a[0], padre_b[0])

        # Mutacion
        if random.random() < _MU:
            hijo = mutar(hijo)

        siguiente_generacion.append((hijo, f(hijo)))

    poblacion = siguiente_generacion
    estadisticas.append(calcula_estadisticas(poblacion))


# Mostrar resultados
x = [i for i in range(0, len(estadisticas))]
y = [p[0] for p in estadisticas]

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set(xlabel='Generacion', ylabel='Mejor aptitud', title='Algoritmo genetico')
ax.grid()
fig.savefig("test.png")
plt.show()

for g in range(1, len(estadisticas)):
    print('G[%d]: mejor: %f, promedio: %f' % (g, estadisticas[g][0], estadisticas[g][1]))




