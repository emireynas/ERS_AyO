import csv

class Item:

    def __init__(self, id, peso, valor):
        self.id = id
        self.peso = peso
        self.valor = valor
        self.ratio = valor / peso


def greedy_knapsack(items, capacidad, criterio):

    if criterio == "ratio":
        items = sorted(
            items,
            key=lambda x: x.ratio,
            reverse=True
        )

    else:
        items = sorted(
            items,
            key=lambda x: x.peso
        )

    peso_total = 0
    valor_total = 0
    seleccionados = []

    for item in items:

        if peso_total + item.peso <= capacidad:

            seleccionados.append(item.id)

            peso_total += item.peso
            valor_total += item.valor

    return seleccionados, peso_total, valor_total


def main():

    print("--- Ejercicio 2: Greedy Knapsack ---")

    capacidad = 5

    items = [
        Item(1, 1, 1),
        Item(2, 2, 2),
        Item(3, 5, 20)
    ]

    s1, p1, v1 = greedy_knapsack(
        items,
        capacidad,
        "ratio"
    )

    s2, p2, v2 = greedy_knapsack(
        items,
        capacidad,
        "weight"
    )

    print("Valor/Peso:", v1)
    print("Menor Peso:", v2)

    with open("ejercicio_2_data.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Metodo",
            "Objetos",
            "Capacidad_Usada",
            "Valor_Total"
        ])

        writer.writerow([
            "Valor/Peso",
            s1,
            p1,
            v1
        ])

        writer.writerow([
            "Menor Peso",
            s2,
            p2,
            v2
        ])

    print("CSV generado.")

if __name__ == "__main__":
    main()