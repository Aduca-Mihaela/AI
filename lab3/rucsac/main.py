import random

class Object:
    def __init__(self, name, profit, weight):
        self.name = name
        self.profit = profit
        self.weight = weight

def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        num_objects = int(lines[0].strip())
        capacity = int(lines[-1].strip())
        objects = []
        for line in lines[1:-1]:
            parts = line.split()
            name = parts[0]
            profit = int(parts[1])
            weight = int(parts[2])
            objects.append(Object(name, profit, weight))
    return num_objects, capacity, objects

def generate_individual(length):
    return [random.randint(0, 1) for _ in range(length)]

def fitness(individual, objects, max_weight):
    total_profit = 0
    total_weight = 0
    for i in range(len(objects)):
        if individual[i] == 1:
            total_profit += objects[i].profit
            total_weight += objects[i].weight
    if total_weight > max_weight:
        return 0
    return total_profit

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

def evolve(population, objects, max_weight, mutation_rate, elite_size):
    graded = [(fitness(ind, objects, max_weight), ind) for ind in population]
    graded = sorted(graded, key=lambda x: x[0], reverse=True)
    elites = [ind for _, ind in graded[:elite_size]]
    next_generation = elites

    while len(next_generation) < len(population):
        parent1, parent2 = random.choices(population, k=2)
        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)
        next_generation.extend([child1, child2])

    return next_generation

def genetic_algorithm(objects, max_weight, pop_size, elite_size, mutation_rate, generations):
    population = [generate_individual(len(objects)) for _ in range(pop_size)]
    for _ in range(generations):
        population = evolve(population, objects, max_weight, mutation_rate, elite_size)
    best_individual = max(population, key=lambda ind: fitness(ind, objects, max_weight))
    best_fitness = fitness(best_individual, objects, max_weight)
    return best_individual, best_fitness

# Exemplu de utilizare
num_objects, max_weight, objects = read_input("rucsac.txt")
pop_size = 50
elite_size = 10
mutation_rate = 0.1
generations = 100

best_solution, best_fitness = genetic_algorithm(objects, max_weight, pop_size, elite_size, mutation_rate, generations)
print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)