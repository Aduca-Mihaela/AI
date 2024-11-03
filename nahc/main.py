import random
import numpy as np

def citeste_date_din_fisier(nume_fisier):
    with open(nume_fisier, 'r') as file:
        linii = file.readlines()
        dimensiune_rucsac = int(linii[0].strip())
        obiecte = [tuple(map(int, linie.strip().split())) for linie in linii[1:-1]]
        capacitate_rucsac = int(linii[-1].strip())
    return dimensiune_rucsac, obiecte, capacitate_rucsac

def generare_sol_aleatoare(dimensiune_rucsac):
    return [random.choice([0, 1]) for _ in range(dimensiune_rucsac)]

def validare_sol(solutie, obiecte, capacitate_rucsac):
    greutate_totala = sum(sol * ob[1] for sol, ob in zip(solutie, obiecte))
    return greutate_totala <= capacitate_rucsac

def evaluare_sol(solutie, obiecte):
    valoare_totala = sum(sol * ob[0] for sol, ob in zip(solutie, obiecte))
    return valoare_totala

def get_neighbors(current_solution):
    neighbors = []
    for i in range(len(current_solution)):
        neighbor = current_solution.copy()
        neighbor[i] = 1 - neighbor[i]  # Flip the bit
        neighbors.append(neighbor)
    return neighbors

def next_ascent_hill_climbing(values, weights, capacity, max_evaluations):
    item_count = len(values)
    current_solution = generare_sol_aleatoare(item_count)
    best_solution = current_solution
    evaluations = 0

    while evaluations < max_evaluations:
        neighbors = get_neighbors(current_solution)
        improved = False

        for neighbor in neighbors:
            neighbor_evaluation = evaluare_sol(neighbor, obiecte)
            current_evaluation = evaluare_sol(current_solution, obiecte)

            if neighbor_evaluation > current_evaluation:
                current_solution = neighbor
                improved = True
                break

        if not improved:
            # No neighbor led to improvement, return the best solution found so far
            return best_solution

        # Update the best solution if the current one is better
        if evaluare_sol(current_solution, obiecte) > evaluare_sol(best_solution, obiecte):
            best_solution = current_solution

        evaluations += 1

    return best_solution

# Exemplu de folosire:
optiune = input("Doriți să introduceți datele manual sau să le citiți dintr-un fișier? (manual/fisier): ").lower()

if optiune == "manual":
    dimensiune_rucsac = int(input("Introduceți dimensiunea rucsacului: "))
    obiecte = [tuple(map(int, input("Introduceți valoarea și greutatea obiectului {}: ".format(i + 1)).split())) for i
               in range(dimensiune_rucsac)]
    capacitate_rucsac = int(input("Introduceți capacitatea rucsacului: "))
elif optiune == "fisier":
    nume_fisier = input("Introduceți numele fișierului de intrare: ")
    dimensiune_rucsac, obiecte, capacitate_rucsac = citeste_date_din_fisier(nume_fisier)
else:
    print("Opțiune invalidă. Vă rugăm să introduceți 'manual' sau 'fisier'.")

numar_rulari_experiment = 20
rezultate_experimente = experimente_rucsac(numar_rulari_experiment, dimensiune_rucsac, obiecte, capacitate_rucsac)

# Aplică algoritmul Next Ascent Hill-Climbing
cel_mai_bun_hilltop = next_ascent_hill_climbing([ob[0] for ob in obiecte], [ob[1] for ob in obiecte], capacitate_rucsac, 1000)
print("Cel mai bun hilltop folosind Next Ascent Hill-Climbing:", cel_mai_bun_hilltop)
print("Valoare hilltop:", evaluare_sol(cel_mai_bun_hilltop, obiecte))
