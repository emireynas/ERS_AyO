import random
import math
import csv
import time

def distancia(a, b):

    return math.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2
    )

def costo(ruta, matriz):

    total = 0

    for i in range(len(ruta)):

        total += matriz[
            ruta[i]
        ][
            ruta[(i+1) % len(ruta)]
        ]

    return total

def simulated_annealing(matriz, enfriamiento):

    n = len(matriz)

    ruta = list(range(n))

    random.shuffle(ruta)

    actual = costo(ruta, matriz)

    mejor = actual

    temperatura = 1000

    inicio = time.time()

    while temperatura > 0.01:

        i, j = sorted(
            random.sample(range(n), 2)
        )

        nueva = (
            ruta[:i]
            + ruta[i:j][::-1]
            + ruta[j:]
        )

        nuevo = costo(
            nueva,
            matriz
        )

        delta = nuevo - actual

        if delta < 0 or random.random() < math.exp(-delta/temperatura):

            ruta = nueva
            actual = nuevo

            mejor = min(
                mejor,
                actual
            )

        if enfriamiento == "Exponencial":
            temperatura *= 0.99
        else:
            temperatura -= 2

    tiempo = time.time() - inicio

    return mejor, tiempo

def main():

    print("--- Ejercicio 4 ---")

    ciudades = 10

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

    costo_e, tiempo_e = simulated_annealing(
        matriz,
        "Exponencial"
    )

    costo_l, tiempo_l = simulated_annealing(
        matriz,
        "Lineal"
    )

    with open(
        "ejercicio_4_data.csv",
        "w",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Enfriamiento",
            "Costo_Final",
            "Tiempo_Seg"
        ])

        writer.writerow([
            "Exponencial",
            costo_e,
            tiempo_e
        ])

        writer.writerow([
            "Lineal",
            costo_l,
            tiempo_l
        ])

    print("CSV generado.")

if __name__ == "__main__":
    main()