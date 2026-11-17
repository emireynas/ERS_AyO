import random
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from statsmodels.formula.api import ols

# =====================================================
# DATOS DEL ALUMNO
# =====================================================

MATRICULA = 2145707

random.seed(MATRICULA)
r = random.random()

print("Valor r =", r)

# =====================================================
# RANGO DE TEMPERATURA
# =====================================================

TMIN = 10
TMAX = 1000

# =====================================================
# NIVELES DE TEMPERATURA
# =====================================================

f_baja = 0.3 * r
f_media = 0.3 * r + 0.3
f_alta = 0.3 * r + 0.6

TB = TMIN + f_baja * (TMAX - TMIN)
TM = TMIN + f_media * (TMAX - TMIN)
TA = TMIN + f_alta * (TMAX - TMIN)

temperaturas = {
    "Baja": TB,
    "Media": TM,
    "Alta": TA
}

print("\nTemperaturas:")

for nombre, valor in temperaturas.items():
    print(nombre, round(valor, 3))

# =====================================================
# DISTANCIA
# =====================================================

def distancia(a, b):

    return math.sqrt(
        (a[0] - b[0])**2 +
        (a[1] - b[1])**2
    )

# =====================================================
# COSTO
# =====================================================

def costo(ruta, matriz):

    total = 0

    n = len(ruta)

    for i in range(n):

        total += matriz[
            ruta[i]
        ][
            ruta[(i + 1) % n]
        ]

    return total

# =====================================================
# GENERAR TSP
# =====================================================

def generar_tsp(n, semilla):

    random.seed(semilla)

    coord = [

        (
            random.random(),
            random.random()
        )

        for _ in range(n)
    ]

    matriz = [

        [
            distancia(coord[i], coord[j])

            for j in range(n)

        ]

        for i in range(n)

    ]

    return matriz

# =====================================================
# RECOCIDO SIMULADO
# =====================================================

def simulated_annealing(
        matriz,
        temperatura_inicial):

    n = len(matriz)

    ruta = list(range(n))

    random.shuffle(ruta)

    actual = costo(
        ruta,
        matriz
    )

    mejor = actual

    temperatura = temperatura_inicial

    while temperatura > 0.01:

        i, j = sorted(
            random.sample(
                range(n),
                2
            )
        )

        nueva = (
            ruta[:i] +
            ruta[i:j][::-1] +
            ruta[j:]
        )

        nuevo = costo(
            nueva,
            matriz
        )

        delta = nuevo - actual

        if (
            delta < 0
            or
            random.random()
            <
            math.exp(
                -delta / temperatura
            )
        ):

            ruta = nueva

            actual = nuevo

            if actual < mejor:
                mejor = actual

        temperatura *= 0.99

    return mejor

# =====================================================
# BOOTSTRAP
# =====================================================

def bootstrap_mediana(
        datos,
        repeticiones=10000):

    medianas = []

    datos = np.array(datos)

    for _ in range(repeticiones):

        muestra = np.random.choice(
            datos,
            size=len(datos),
            replace=True
        )

        medianas.append(
            np.median(muestra)
        )

    mediana = np.median(datos)

    li = np.percentile(
        medianas,
        2.5
    )

    ls = np.percentile(
        medianas,
        97.5
    )

    return mediana, li, ls

# =====================================================
# INSTANCIAS
# =====================================================

instancias = {

    5: generar_tsp(5, 5),

    10: generar_tsp(10, 10),

    15: generar_tsp(15, 15)

}

# =====================================================
# DOE
# =====================================================

resultados = []

print("\nEjecutando 90 corridas...")

for tamano, matriz in instancias.items():

    for nombre_temp, valor_temp in temperaturas.items():

        for replica in range(1, 11):

            random.seed(
                tamano * 1000 +
                replica
            )

            mejor_costo = simulated_annealing(
                matriz,
                valor_temp
            )

            resultados.append([

                tamano,
                nombre_temp,
                valor_temp,
                replica,
                mejor_costo

            ])

# =====================================================
# DATAFRAME
# =====================================================

df = pd.DataFrame(

    resultados,

    columns=[
        "tamano",
        "temperatura",
        "T",
        "replica",
        "costo"
    ]
)

df.to_csv(
    "resultados_doe.csv",
    index=False
)

# =====================================================
# ANOVA
# =====================================================

print("\nANOVA")

modelo = ols(
    'costo ~ C(temperatura) * C(tamano)',
    data=df
).fit()

tabla_anova = sm.stats.anova_lm(
    modelo,
    typ=2
)

print(tabla_anova)

tabla_anova.to_csv(
    "tabla_anova.csv"
)

# =====================================================
# EFECTO TEMPERATURA
# =====================================================

plt.figure(figsize=(8,5))

df.groupby(
    'temperatura'
)['costo'].mean().plot(
    marker='o'
)

plt.title(
    'Efecto Principal Temperatura'
)

plt.ylabel(
    'Costo Promedio'
)

plt.grid(True)

plt.savefig(
    'efecto_temperatura.png'
)

plt.close()

# =====================================================
# EFECTO TAMAÑO
# =====================================================

plt.figure(figsize=(8,5))

df.groupby(
    'tamano'
)['costo'].mean().plot(
    marker='o'
)

plt.title(
    'Efecto Principal Tamaño'
)

plt.ylabel(
    'Costo Promedio'
)

plt.grid(True)

plt.savefig(
    'efecto_tamano.png'
)

plt.close()

# =====================================================
# INTERACCION
# =====================================================

plt.figure(figsize=(8,5))

sns.pointplot(

    data=df,

    x='temperatura',

    y='costo',

    hue='tamano'

)

plt.title(
    'Interaccion Temperatura x Tamaño'
)

plt.savefig(
    'interaccion.png'
)

plt.close()

# =====================================================
# TABLA RESUMEN
# =====================================================

resumen = []

for tamano in [5,10,15]:

    sub = df[
        df['tamano']
        == tamano
    ]

    mejor_temp = None
    mejor_mediana = float("inf")
    mejor_li = None
    mejor_ls = None

    for temp in [

        "Baja",
        "Media",
        "Alta"

    ]:

        datos = sub[
            sub['temperatura']
            == temp
        ]['costo']

        med, li, ls = (
            bootstrap_mediana(
                datos
            )
        )

        if med < mejor_mediana:

            mejor_mediana = med
            mejor_temp = temp
            mejor_li = li
            mejor_ls = ls

    resumen.append([

        tamano,
        mejor_temp,
        mejor_mediana,
        mejor_li,
        mejor_ls

    ])

tabla_final = pd.DataFrame(

    resumen,

    columns=[

        "Tamano",
        "MejorTemperatura",
        "MedianaBootstrap",
        "IC95_LI",
        "IC95_LS"

    ]

)

print("\nTABLA FINAL")
print(tabla_final)

tabla_final.to_csv(
    "tabla_final.csv",
    index=False
)

print("\nArchivos generados:")

print("resultados_doe.csv")
print("tabla_anova.csv")
print("tabla_final.csv")
print("efecto_temperatura.png")
print("efecto_tamano.png")
print("interaccion.png")