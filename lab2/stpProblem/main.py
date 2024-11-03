import random
import math


#se genereaza o soluție inițială aleatorie
def genereaza_solutie_initiala(noduri):
    solutie_initiala = list(noduri.keys())
    random.shuffle(solutie_initiala)
    return solutie_initiala


#alege două poziții aleatorii în soluție și le schimbă între ele pentru a obține un vecin
def genereaza_vecin(solutie_curenta):
    i, j = sorted(random.sample(range(len(solutie_curenta)), 2))
    vecin = solutie_curenta[:i] + solutie_curenta[j:j+1] + solutie_curenta[i+1:j] +\
            solutie_curenta[i:i+1] + solutie_curenta[j+1:]
    return vecin

#calculează distanța Euclidiană între 2 puncte
def distanta(punct1, punct2):
    x1, y1 = punct1
    x2, y2 = punct2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


#dacă vecinul are o distanță mai mică sau are o probabilitate dată de formula lui Metropolis, atunci acceptă vecinul
#la fiecare iterație, temperatura este multiplicată cu rata de răcire pentru a simula procesul de răcire.
def simulated_annealing(noduri, temperatura_initiala, rata_racire, nr_iteratii):
    solutie_curenta = genereaza_solutie_initiala(noduri)
    distanta_curenta = sum(distanta(noduri[solutie_curenta[i]], noduri[solutie_curenta[i-1]])
                           for i in range(len(solutie_curenta)))
    solutie_optima = solutie_curenta
    distanta_optima = distanta_curenta

    for _ in range(nr_iteratii):
        vecin = genereaza_vecin(solutie_curenta)
        distanta_vecin = sum(distanta(noduri[vecin[i]], noduri[vecin[i-1]]) for i in range(len(vecin)))

        if distanta_vecin < distanta_curenta or random.random() < math.exp((distanta_curenta
                                                            - distanta_vecin) / temperatura_initiala):
            solutie_curenta = vecin
            distanta_curenta = distanta_vecin

            if distanta_curenta < distanta_optima:
                solutie_optima = solutie_curenta
                distanta_optima = distanta_curenta

        temperatura_initiala *= rata_racire

    return solutie_optima, distanta_optima

# Citirea coordonatelor nodurilor din fișier
def citeste_date_din_fisier(nume_fisier):
    with open(nume_fisier, 'r') as file:
        noduri = {}
        for linie in file:
            if linie.strip() == "NODE_COORD_SECTION":
                break
        for linie in file:
            if linie.strip() == "EOF":
                break
            valori = linie.strip().split()
            try:
                index, x, y = map(float, valori)
                noduri[int(index)] = (x, y)
            except ValueError:
                print("Linie invalidă:", linie.strip())
    return noduri

if __name__ == "__main__":
    noduri = citeste_date_din_fisier("st70.stp")
    temperatura_initiala = 100
    rata_racire = 0.999
    nr_iteratii = 1000

    solutie_optima, distanta_optima = simulated_annealing(noduri, temperatura_initiala, rata_racire, nr_iteratii)
    print("Solutie optima:", solutie_optima)
    print("Distanta optima:", distanta_optima)
