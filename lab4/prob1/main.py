import numpy as np
#ALGORITM EVOLUTIV

# Definirea funcției Goldstein-Price
def goldstein_price(x):
    x_ = x[0]
    y_ = x[1]
    term1 = 1 + ((x_ + y_ + 1)**2) * (19 - 14*x_ + 3*x_**2 - 14*y_ + 6*x_*y_ + 3*y_**2)
    term2 = 30 + ((2*x_ - 3*y_)**2) * (18 - 32*x_ + 12*x_**2 + 48*y_ - 36*x_*y_ + 27*y_**2)
    return term1 * term2

# Inițializarea populației inițiale cu valori aleatoare
def initialize_population(pop_size, dim):
    return np.random.uniform(-2, 2, (pop_size, dim))

# Selecția părinților folosind metoda turneului
def selection(population, fitness_values, tournament_size):
    selected_solutions = np.empty_like(population)
    for i in range(len(population)):
        tournament_idxs = np.random.choice(len(population), size=tournament_size, replace=False)
        tournament_fitness = fitness_values[tournament_idxs]
        winner_idx = tournament_idxs[np.argmin(tournament_fitness)]
        selected_solutions[i] = population[winner_idx]
    return selected_solutions

# Realizarea încrucișării între două soluții
def crossover(solution1, solution2):
    crossover_point = np.random.randint(1, len(solution1))
    child1 = np.concatenate((solution1[:crossover_point], solution2[crossover_point:]))
    child2 = np.concatenate((solution2[:crossover_point], solution1[crossover_point:]))
    return child1, child2

# Aplicarea mutației asupra unei soluții cu o anumită rată
def mutation(solution, mutation_rate):
    mutated_solution = solution + np.random.normal(0, mutation_rate, solution.shape)
    return mutated_solution

# Analiza evoluției celei mai bune soluții în fiecare generație
def track_best_solution(population, fitness_values):
    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx]
    best_fitness = fitness_values[best_idx]
    return best_solution, best_fitness

# Algoritmul evoluționar propriu-zis
def evolutionary_algorithm(pop_size, dim, num_generations, tournament_size, crossover_rate, mutation_rate):
    population = initialize_population(pop_size, dim)
    best_per_generation = []

    for gen in range(num_generations):
        # Evaluarea fiecărei soluții din populație
        fitness_values = np.array([goldstein_price(solution) for solution in population])

        # Salvarea celei mai bune soluții din această generație
        best_solution, best_fitness = track_best_solution(population, fitness_values)
        best_per_generation.append((best_solution, best_fitness))

        # Selecția părinților
        selected_parents = selection(population, fitness_values, tournament_size)

        # Realizarea încrucișării
        children = []
        for i in range(0, pop_size, 2):
            if np.random.rand() < crossover_rate:
                child1, child2 = crossover(selected_parents[i], selected_parents[i+1])
            else:
                child1, child2 = selected_parents[i], selected_parents[i+1]
            children.append(child1)
            children.append(child2)

        # Realizarea mutației
        mutated_children = [mutation(child, mutation_rate) for child in children]

        # Înlocuirea populației vechi cu noua populație
        population = np.array(mutated_children)

        # Afișarea celei mai bune soluții din populație
        print(f"Generația {gen + 1}: Cea mai bună soluție: {best_solution}, Fitness: {best_fitness}")

    return best_per_generation


pop_size = 50
dim = 2
num_generations = 10
tournament_size = 3
crossover_rate = 0.7
mutation_rate = 0.1

# Apelarea algoritmului evoluționar
best_per_generation = evolutionary_algorithm(pop_size, dim, num_generations, tournament_size, crossover_rate, mutation_rate)

# Afișarea celei mai bune soluții din fiecare generație
for gen, (best_solution, best_fitness) in enumerate(best_per_generation):
    print(f"Generația {gen + 1}: Cea mai bună soluție: {best_solution}, Fitness: {best_fitness}")
