import random

class City:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

def read_input(filename):
    cities = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[6:]:
            if line.strip() == "EOF":
                break
            parts = line.split()
            index = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            cities.append(City(index, x, y))
    return cities

def generate_individual(cities):
    return random.sample(cities, len(cities))

def calculate_distance(city1, city2):
    return ((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2) ** 0.5

def total_distance(route):
    total = 0
    for i in range(len(route)):
        total += calculate_distance(route[i], route[(i + 1) % len(route)])
    return total

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start = random.randint(0, size - 1)
    end = random.randint(start, size - 1)
    child = [None] * size
    for i in range(start, end + 1):
        child[i] = parent1[i]
    remaining = [city for city in parent2 if city not in child]
    index = 0
    for i in range(size):
        if child[i] is None:
            child[i] = remaining[index]
            index += 1
    return child

def mutate(route):
    start = random.randint(0, len(route) - 1)
    end = random.randint(start, len(route) - 1)
    route[start:end + 1] = reversed(route[start:end + 1])
    return route

def evolve(population, mutation_rate):
    graded = [(total_distance(ind), ind) for ind in population]
    graded = sorted(graded, key=lambda x: x[0])
    next_generation = []

    elite_size = int(0.1 * len(population))
    next_generation.extend([ind for _, ind in graded[:elite_size]])

    while len(next_generation) < len(population):
        parent1, parent2 = random.choices(population, k=2)
        child = ordered_crossover(parent1, parent2)
        if random.random() < mutation_rate:
            child = mutate(child)
        next_generation.append(child)

    return next_generation

def genetic_algorithm(cities, pop_size, mutation_rate, generations):
    population = [generate_individual(cities) for _ in range(pop_size)]
    for _ in range(generations):
        population = evolve(population, mutation_rate)
    best_route = min(population, key=total_distance)
    return best_route, total_distance(best_route)

# Exemplu de utilizare
filename = "st70.stp"
cities = read_input(filename)
pop_size = 50
mutation_rate = 0.1
generations = 1000

best_route, best_distance = genetic_algorithm(cities, pop_size, mutation_rate, generations)
print("Best Route:", [city.index for city in best_route])
print("Best Distance:", best_distance)
