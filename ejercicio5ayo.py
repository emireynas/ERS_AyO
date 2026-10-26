import random
import math
import csv
from itertools import permutations

def distancia(a, b):

    return math.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2
    )

def costo(ruta, matriz):

    total = 0

    n = len(ruta)

    for i in range(n):

        total += matriz[
            ruta[i]
        ][
            ruta[(i+1) % n]
        ]

    return total

def tsp_optimo(matriz):

    mejor = float("inf")

    n = len(matriz)

    for perm in permutations(range(1, n)):

        ruta = [0] + list(perm)

        mejor = min(
            mejor,
            costo(ruta, matriz)
        )

    return mejor

def mst_aprox(matriz):

    n = len(matriz)

    visitados = {0}

    ruta = [0]

    while len(visitados) < n:

        actual = ruta[-1]

        siguiente = min(
            [
                i for i in range(n)
                if i not in visitados
            ],
            key=lambda x:
            matriz[actual][x]
        )

        ruta.append(siguiente)

        visitados.add(siguiente)

    return ruta

def main():

    print("--- Ejercicio 5 ---")

    ratios = []

    for instancia in range(10):

        ciudades = 7

        coord = [
            (
                random.random(),
                random.random()
            )
            for _ in range(ciudades)
        ]

        matriz = [
            [
                distancia(coord[i], coord[j])
                for j in range(ciudades)
            ]
            for i in range(ciudades)
        ]

        optimo = tsp_optimo(matriz)

        mst = mst_aprox(matriz)

        costo_mst = costo(
            mst,
            matriz
        )

        ratios.append(
            costo_mst / optimo
        )

    with open(
        "ejercicio_5_data.csv",
        "w",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Instancia",
            "Razon_MST_Optimo"
        ])

        for i, r in enumerate(ratios, 1):

            writer.writerow([
                i,
                r
            ])

    print("CSV generado.")

if __name__ == "__main__":
    main()