import random

def citeste_date_din_fisier(nume_fisier):
    with open(nume_fisier, 'r') as file:
        linii = file.readlines()
        dimensiune_rucsac = int(linii[0].strip())
        obiecte = [tuple(map(int, linie.strip().split())) for linie in linii[1:-1]]
        capacitate_rucsac = int(linii[-1].strip())

    return dimensiune_rucsac, obiecte, capacitate_rucsac

def generare_solutie_aleatoare(n):
    return [random.choice([0, 1]) for _ in range(n)]

def validare_solutie(solutie, obiecte, capacitate):
    greutate_totala = sum(solutie[i] * obiecte[i][1] for i in range(len(solutie)))
    return greutate_totala <= capacitate

def calcul_calitate_solutie(solutie, obiecte):
    return sum(solutie[i] * obiecte[i][2] for i in range(len(solutie)))

def calcul_greutate_solutie(solutie, obiecte):
    return sum(solutie[i] * obiecte[i][1] for i in range(len(solutie)))

def cautare_aleatoare_rucsac(dimensiune_rucsac, obiecte, capacitate, k_iteratii):
    cea_mai_buna_solutie = None
    cea_mai_buna_calitate = 0
    cea_mai_buna_greutate = float('inf')

    for _ in range(k_iteratii):
        solutie_curenta = generare_solutie_aleatoare(dimensiune_rucsac)

        if validare_solutie(solutie_curenta, obiecte, capacitate):
            calitate_curenta = calcul_calitate_solutie(solutie_curenta, obiecte)
            greutate_curenta = calcul_greutate_solutie(solutie_curenta, obiecte)

            if calitate_curenta > cea_mai_buna_calitate or (calitate_curenta == cea_mai_buna_calitate
                                                            and greutate_curenta < cea_mai_buna_greutate):
                cea_mai_buna_solutie = solutie_curenta
                cea_mai_buna_calitate = calitate_curenta
                cea_mai_buna_greutate = greutate_curenta

    return cea_mai_buna_solutie, cea_mai_buna_calitate, cea_mai_buna_greutate

if __name__ == "__main__":
    dimensiune = 17
    obiect = [(1, 91, 29), (2, 60, 65), (3, 61, 71), (4, 9, 60), (5, 79, 45),
               (6, 46, 71), (7, 19, 22), (8, 57, 97), (9, 8, 6), (10, 84, 91),
               (11, 20, 57), (12, 72, 60), (13, 32, 49), (14, 31, 89), (15, 28, 2),
               (16, 81, 30), (17, 55, 90)]
    capacitate= 378
    nume_fisier = "rucsac.txt"
    dimensiune_rucsac, obiecte, capacitate_rucsac = citeste_date_din_fisier(nume_fisier)
    k_iteratii = 1000

    rezultat = cautare_aleatoare_rucsac(dimensiune_rucsac, obiecte, capacitate_rucsac, k_iteratii)
    print("Cea mai bună soluție:", rezultat[0])
    print("Calitatea celei mai bune soluții:", rezultat[1])
    print("Greutatea celei mai bune soluții:", rezultat[2])
