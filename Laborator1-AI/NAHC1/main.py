import random

def citeste_date_din_fisier(nume_fisier):
    with open(nume_fisier, 'r') as f:
        n = int(f.readline().strip())
        obiecte = [list(map(int, line.split())) for line in f]

    return n, obiecte

def eval(c, obiecte):
    suma_valori = 0
    suma_greutati = 0

    for i in range(len(c)):
        suma_valori += c[i] * obiecte[i][1]
        suma_greutati += c[i] * obiecte[i][2]

    return suma_valori, suma_greutati

def hill_climbing(n, obiecte, capacitate_maxima, max_evaluari):
    cea_mai_buna_solutie = []
    cea_mai_buna_valoare = 0

    for _ in range(10):  # încercați 10 runde diferite de pornire aleatorie
        c = [random.randint(0, 1) for _ in range(n)]
        evaluari = 0

        while evaluari < max_evaluari:
            vecini = []
            for i in range(n):
                vecin = c.copy()
                vecin[i] = 1 - vecin[i]
                vecini.append(vecin)

            evaluare_curenta, greutate_curenta = eval(c, obiecte)

            for vecin in vecini:
                evaluare_vecin, greutate_vecin = eval(vecin, obiecte)
                if evaluare_vecin > evaluare_curenta and greutate_vecin <= capacitate_maxima:
                    c = vecin
                    evaluari += 1
                    break

            if evaluare_curenta == eval(c, obiecte)[0]:
                break

        valoare_curenta, _ = eval(c, obiecte)
        if valoare_curenta > cea_mai_buna_valoare and greutate_curenta <= capacitate_maxima:
            cea_mai_buna_valoare = valoare_curenta
            cea_mai_buna_solutie = c

    return cea_mai_buna_solutie

if __name__ == "__main__":
    nume_fisier = "rucsac2.txt"  # înlocuiți cu numele fișierului dvs.
    capacitate_maxima =112648  # specificați capacitatea maximă a rucsacului
    max_evaluari = 1000  # specificați numărul maxim de evaluări

    n, obiecte = citeste_date_din_fisier(nume_fisier)
    dimensiune = 17
    obiect = [(1, 91, 29), (2, 60, 65), (3, 61, 71), (4, 9, 60), (5, 79, 45),
              (6, 46, 71), (7, 19, 22), (8, 57, 97), (9, 8, 6), (10, 84, 91),
              (11, 20, 57), (12, 72, 60), (13, 32, 49), (14, 31, 89), (15, 28, 2),
              (16, 81, 30), (17, 55, 90)]
    capacitate = 378

    solutie_finala = hill_climbing(n, obiecte, capacitate_maxima, max_evaluari)

    print("Solutia gasita:", solutie_finala)
    valoare, greutate = eval(solutie_finala, obiecte)
    print("Valoare:", valoare)
    print("Greutate:", greutate)
