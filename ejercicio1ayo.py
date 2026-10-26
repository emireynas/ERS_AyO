import time
import random
import multiprocessing
import csv

def monte_carlo_pi_chunk(num_samples):
    inside = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()

        if x*x + y*y <= 1:
            inside += 1

    return inside

def main():

    print("--- Ejercicio 1: Aceleración Paralela ---")

    total_samples = 5000000
    process_counts = [1, 2, 4, 8]

    times = []

    start = time.time()
    monte_carlo_pi_chunk(total_samples)
    t1 = time.time() - start

    times.append(t1)

    print(f"Procesos: 1 | Tiempo: {t1:.4f}s")

    for p in process_counts[1:]:

        chunk = total_samples // p

        start = time.time()

        with multiprocessing.Pool(processes=p) as pool:
            pool.map(monte_carlo_pi_chunk, [chunk] * p)

        tp = time.time() - start

        times.append(tp)

        print(f"Procesos: {p} | Tiempo: {tp:.4f}s")

    with open("ejercicio_1_data.csv", "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Procesos",
            "Tiempo",
            "Speedup",
            "Speedup_Ideal"
        ])

        for p, t in zip(process_counts, times):

            speedup = t1 / t

            writer.writerow([
                p,
                t,
                speedup,
                p
            ])

    print("CSV generado.")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()