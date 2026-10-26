import random
import math
import csv

random.seed(42)

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

def two_opt(ruta, matriz):

    mejor = ruta[:]

    mejor_costo = costo(mejor, matriz)

    mejoras = 0

    cambio = True

    while cambio:

        cambio = False

        for i in range(len(mejor)-1):

            for j in range(i+2, len(mejor)+1):

                nueva = (
                    mejor[:i]
                    + mejor[i:j][::-1]
                    + mejor[j:]
                )

                nuevo_costo = costo(
                    nueva,
                    matriz
                )

                if nuevo_costo < mejor_costo:

                    mejor = nueva
                    mejor_costo = nuevo_costo

                    mejoras += 1

                    cambio = True
                    break

            if cambio:
                break

    return mejor_costo, mejoras

def vecino_cercano(matriz):

    n = len(matriz)

    actual = 0

    sin_visitar = set(range(n))

    ruta = [actual]

    sin_visitar.remove(actual)

    while sin_visitar:

        sig = min(
            sin_visitar,
            key=lambda x:
            matriz[actual][x]
        )

        ruta.append(sig)

        sin_visitar.remove(sig)

        actual = sig

    return ruta

def main():

    print("--- Ejercicio 3 ---")

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

    aleatoria = list(range(ciudades))

    random.shuffle(aleatoria)

    costo_a, mejoras_a = two_opt(
        aleatoria,
        matriz
    )

    nn = vecino_cercano(matriz)

    costo_n, mejoras_n = two_opt(
        nn,
        matriz
    )

    with open("ejercicio_3_data.csv",
              "w",
              newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Metodo",
            "Mejoras",
            "Costo_Final"
        ])

        writer.writerow([
            "Aleatorio",
            mejoras_a,
            costo_a
        ])

        writer.writerow([
            "Vecino Mas Cercano",
            mejoras_n,
            costo_n
        ])

    print("CSV generado.")

if __name__ == "__main__":
    main()