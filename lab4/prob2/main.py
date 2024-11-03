import numpy as np

#ALGORITM PSO
# Definirea funcției Goldstein-Price
def goldstein_price(x):
    x_ = x[0]
    y_ = x[1]
    term1 = 1 + ((x_ + y_ + 1)**2) * (19 - 14*x_ + 3*x_**2 - 14*y_ + 6*x_*y_ + 3*y_**2)
    term2 = 30 + ((2*x_ - 3*y_)**2) * (18 - 32*x_ + 12*x_**2 + 48*y_ - 36*x_*y_ + 27*y_**2)
    return term1 * term2

# Funcția de actualizare a vitezei particulelor
def update_velocity(position, velocity, best_position, global_best_position, cognitive_param, social_param):
    inertia_weight = 0.5
    new_velocity = (inertia_weight * velocity +
                    cognitive_param * np.random.rand() * (best_position - position) +
                    social_param * np.random.rand() * (global_best_position - position))
    return new_velocity

# Funcția de actualizare a pozițiilor particulelor
def update_position(position, velocity):
    new_position = position + velocity
    new_position = np.clip(new_position, -2, 2)  # Se asigură că noile poziții sunt în intervalul [-2, 2]
    return new_position

# Funcția principală pentru optimizarea PSO
def optimize_pso(num_particles, dim, num_iterations, cognitive_param, social_param):
    global_best_position = None
    global_best_fitness = float('inf')

    # Inițializarea particulelor și a vitezelor
    particles = [np.random.uniform(-2, 2, dim) for _ in range(num_particles)]
    velocities = [np.random.uniform(-0.1, 0.1, dim) for _ in range(num_particles)]
    best_positions = np.copy(particles)
    best_fitnesses = [goldstein_price(p) for p in particles]

    # Iterarea prin numărul specificat de iterații
    for _ in range(num_iterations):
        # Actualizarea celei mai bune poziții globale și a fitnessului globale
        for i in range(num_particles):
            if best_fitnesses[i] < global_best_fitness:
                global_best_fitness = best_fitnesses[i]
                global_best_position = np.copy(best_positions[i])

        # Actualizarea vitezelor și a pozițiilor particulelor
        for i in range(num_particles):
            velocities[i] = update_velocity(particles[i], velocities[i], best_positions[i],
                                            global_best_position, cognitive_param, social_param)
            particles[i] = update_position(particles[i], velocities[i])

            # Actualizarea celei mai bune poziții și fitnessului pentru fiecare particulă
            current_fitness = goldstein_price(particles[i])
            if current_fitness < best_fitnesses[i]:
                best_fitnesses[i] = current_fitness
                best_positions[i] = np.copy(particles[i])

    return global_best_position, global_best_fitness

# Funcția pentru rularea algoritmului de mai multe ori
def run_multiple_pso(num_runs, num_particles, dim, num_iterations, cognitive_param, social_param):
    results = []
    for _ in range(num_runs):
        best_position, best_fitness = optimize_pso(num_particles, dim, num_iterations, cognitive_param, social_param)
        results.append((best_position, best_fitness))
    return results

# Parametrii algoritmului pentru rulările multiple
num_runs = 10
num_particles = 50
dim = 2
num_iterations = 100
cognitive_param = 2.0
social_param = 2.0

# Rularea algoritmului PSO de mai multe ori și afișarea rezultatelor
multiple_results = run_multiple_pso(num_runs, num_particles, dim, num_iterations, cognitive_param, social_param)
for i, (best_position, best_fitness) in enumerate(multiple_results):
    print(f"Rularea {i + 1}: Cel mai bun rezultat (poziție): {best_position}, Cel mai bun rezultat (fitness): {best_fitness}")
