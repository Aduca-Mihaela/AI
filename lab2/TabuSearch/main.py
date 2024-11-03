import random

#am definit o clasa pentru obiectele din rucsac
class Obiect:
    def __init__(self, index, greutate, valoare):
        self.index = index
        self.greutate = greutate
        self.valoare = valoare

def citeste_date_din_fisier(nume_fisier):
    with open(nume_fisier, 'r') as file:
        linii = file.readlines()
        dimensiune_rucsac = int(linii[0].strip())
        obiecte = [Obiect(*map(int, linie.strip().split())) for linie in linii[1:-1]]
        capacitate_rucsac = int(linii[-1].strip())

    return dimensiune_rucsac, obiecte, capacitate_rucsac

#genereaza o solutie atâta timp cât greutatea totală a obiectelor adăugate este mai mică sau egală cu capacitatea rucsacului
def genereaza_solutie_initiala(obiecte, capacitate_rucsac):
    solutie = [0] * len(obiecte)
    greutate_totala = 0
    index = 0
    while index < len(obiecte) and greutate_totala + obiecte[index].greutate <= capacitate_rucsac:
        solutie[index] = 1
        greutate_totala += obiecte[index].greutate
        index += 1
    return solutie, greutate_totala


#alege aleatoriu un indice din soluție și inversează valoarea (0 devine 1 și invers)
def genereaza_vecin(solutie):
    vecin = solutie[:]
    index = random.randint(0, len(vecin) - 1)
    vecin[index] = 1 - vecin[index]  # Inversăm valoarea obiectului selectat
    return vecin


#dacă greutatea totală depășește capacitatea rucsacului, soluția primeste o valoare negativă
def evalueaza_solutie(solutie, obiecte, capacitate_rucsac):
    valoare_totala = sum(solutie[i] * obiecte[i].valoare for i in range(len(solutie)))
    greutate_totala = sum(solutie[i] * obiecte[i].greutate for i in range(len(solutie)))
    if greutate_totala > capacitate_rucsac:
        return -1, greutate_totala  # Penalizăm soluțiile care depășesc capacitatea rucsacului
    return valoare_totala, greutate_totala


#generează vecini și alege cel mai bun vecin care nu se află în lista tabu si actualizeaza solutia curenta si lista tabu si restul
def cautare_tabu(obiecte, capacitate_rucsac, durata_tabu, max_iteratii):
    solutie_curenta, greutate_curenta = genereaza_solutie_initiala(obiecte, capacitate_rucsac)
    cea_mai_buna_solutie = solutie_curenta[:]
    cea_mai_buna_valoare, _ = evalueaza_solutie(cea_mai_buna_solutie, obiecte, capacitate_rucsac)
    lista_tabu = []
    iteratie = 0
    while iteratie < max_iteratii:
        vecini = [genereaza_vecin(solutie_curenta) for _ in range(len(obiecte))]
        vecini = [vecin for vecin in vecini if vecin not in lista_tabu]
        if not vecini:
            break
        valori_vecini = [evalueaza_solutie(vecin, obiecte, capacitate_rucsac)[0] for vecin in vecini]
        cea_mai_buna_valoare_vecin = max(valori_vecini)
        index_cea_mai_buna_vecin = valori_vecini.index(cea_mai_buna_valoare_vecin)
        if cea_mai_buna_valoare_vecin > cea_mai_buna_valoare:
            cea_mai_buna_solutie = vecini[index_cea_mai_buna_vecin][:]
            cea_mai_buna_valoare = cea_mai_buna_valoare_vecin
        solutie_curenta = vecini[index_cea_mai_buna_vecin][:]
        lista_tabu.append(solutie_curenta)
        if len(lista_tabu) > durata_tabu:
            lista_tabu.pop(0)  # Eliminăm cea mai veche soluție din lista tabu
        iteratie += 1
    return cea_mai_buna_solutie, cea_mai_buna_valoare



dimensiune_rucsac, obiecte, capacitate_rucsac = citeste_date_din_fisier("rucsac2.txt")
durata_tabu = 5

max_iteratii = 100


cea_mai_buna_solutie, cea_mai_buna_valoare = cautare_tabu(obiecte, capacitate_rucsac, durata_tabu, max_iteratii)
print("Cea mai bună soluție:", cea_mai_buna_solutie)
print("Cea mai bună valoare:", cea_mai_buna_valoare)
