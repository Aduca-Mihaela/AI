import random

class Intersection:
    def __init__(self, id, green_duration, red_duration):
        self.id = id
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.state = 0  # 0 pentru roșu, 1 pentru verde
        self.time_elapsed = 0
        self.queue = []

    def update(self):
        self.time_elapsed += 1
        if self.state == 1:
            self.queue = [vehicle for vehicle in self.queue if vehicle.wait_time < self.green_duration]
            for vehicle in self.queue:
                vehicle.wait_time += 1

class Vehicle:
    def __init__(self, id, intersection_id):
        self.id = id
        self.intersection_id = intersection_id
        self.wait_time = 0

class TrafficLightConfiguration:
    def __init__(self, intersections):
        self.intersections = intersections

    def apply(self):
        total_wait_time = sum(intersection.time_elapsed for intersection in self.intersections)
        return total_wait_time / len(self.intersections)  # Returnăm media timpului total de așteptare

def fitness_function(configuration):
    total_wait_time = 0
    total_travel_time = 0
    vehicles = [Vehicle(i, random.randint(0, len(configuration.intersections) - 1)) for i in range(100)]

    for vehicle in vehicles:
        current_intersection = configuration.intersections[vehicle.intersection_id]
        total_travel_time += current_intersection.green_duration
        vehicle.wait_time = current_intersection.time_elapsed
        current_intersection.queue.append(vehicle)

    for intersection in configuration.intersections:
        intersection.update()

    total_wait_time = sum(vehicle.wait_time for vehicle in vehicles)
    return total_wait_time + total_travel_time

def selection(population, fitness_values):
    idx = random.choices(range(len(population)), weights=[1 / (fitness + 1) for fitness in fitness_values])[0]
    return population[idx]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1.intersections) - 1)
    child_intersections = parent1.intersections[:crossover_point] + parent2.intersections[crossover_point:]
    return TrafficLightConfiguration(child_intersections)

def mutation(configuration, mutation_rate):
    for intersection in configuration.intersections:
        if random.random() < mutation_rate:
            intersection.green_duration = random.randint(5, 15)
            intersection.red_duration = random.randint(5, 15)
    return configuration

def generate_initial_population(population_size, num_intersections):
    return [TrafficLightConfiguration([Intersection(i, random.randint(5, 15), random.randint(5, 15))
                                       for i in range(num_intersections)]) for _ in range(population_size)]

def genetic_algorithm(population_size, generations, mutation_rate, num_intersections):
    population = generate_initial_population(population_size, num_intersections)
    for _ in range(generations):
        fitness_values = [fitness_function(configuration) for configuration in population]
        new_population = []
        for _ in range(population_size):
            parent1 = selection(population, fitness_values)
            parent2 = selection(population, fitness_values)
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            new_population.append(child)
        population = new_population
    best_solution_idx = min(range(len(population)), key=lambda x: fitness_function(population[x]))
    best_solution = population[best_solution_idx]
    return best_solution

population_size = 100
generations = 50
mutation_rate = 0.1
num_intersections = 5

best_solution = genetic_algorithm(population_size, generations, mutation_rate, num_intersections)
print("Configurația optimă a semafoarelor:")
for intersection in best_solution.intersections:
    print(f"Intersecția {intersection.id}: Durata verde = {intersection.green_duration} min, "
          f"Durata roșu = {intersection.red_duration} min")
print("Fitness:", fitness_function(best_solution))
