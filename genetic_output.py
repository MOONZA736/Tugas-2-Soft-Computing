import random
import io
import sys

# Data Masalah Knapsack
items = {
    'A': {'weight': 7, 'value': 5},
    'B': {'weight': 2, 'value': 4},
    'C': {'weight': 1, 'value': 7},
    'D': {'weight': 9, 'value': 2},
}
capacity = 15
item_list = list(items.keys())
n_items = len(item_list)

def decode(chromosome):
    total_weight = 0
    total_value = 0
    chosen_items = []
    for gene, name in zip(chromosome, item_list):
        if gene == 1:
            total_weight += items[name]['weight']
            total_value += items[name]['value']
            chosen_items.append(name)
    return chosen_items, total_weight, total_value

def fitness(chromosome):
    chosen_items, total_weight, total_value = decode(chromosome)
    # Penalti jika berat melebihi kapasitas
    return total_value if total_weight <= capacity else 0

def roulette_selection(population, fitnesses):
    total_fit = sum(fitnesses)
    if total_fit == 0:
        # Jika semua fitness 0, pilih acak
        return random.choice(population)
    pick = random.uniform(0, total_fit)
    current = 0
    for chrom, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return chrom
    return population[-1]

def crossover(p1, p2):
    # Single-point crossover
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

def mutate(chromosome, mutation_rate=0.1):
    # Flip bit dengan probabilitas mutation_rate
    return [1 - g if random.random() < mutation_rate else g for g in chromosome]

def run_genetic_algorithm(pop_size=8, generations=7, crossover_rate=0.8, mutation_rate=0.1):
    """Menjalankan algoritma genetika dan mengembalikan log output sebagai string."""
    random.seed(43) # agar hasil replikasi konsisten
    
    # Mengalihkan output stdout ke string buffer
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output

    population = [[random.randint(0, 1) for _ in range(n_items)] for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses = [fitness(ch) for ch in population]
        best_idx = fitnesses.index(max(fitnesses))
        best = population[best_idx]
        items_chosen, w, v = decode(best)

        print(f"Generasi {gen+1}:")
        print(f"Terbaik: {best} | Item: {items_chosen} | Berat: {w} | Nilai: {v} | Fitness: {fitness(best)}")
        
        new_pop = [best]  # elitism

        while len(new_pop) < pop_size:
            p1 = roulette_selection(population, fitnesses)
            p2 = roulette_selection(population, fitnesses)

            if random.random() < crossover_rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            # Mutasi
            new_pop += [mutate(c1, mutation_rate), mutate(c2, mutation_rate)]

        population = new_pop[:pop_size]

    # hasil akhir
    fitnesses = [fitness(ch) for ch in population]
    best_idx = fitnesses.index(max(fitnesses))
    best = population[best_idx]
    items_chosen, w, v = decode(best)

    print("\n" + "="*20 + " HASIL AKHIR " + "="*20)
    print(f"Kromosom terbaik: {best}")
    print(f"Item terpilih: {items_chosen}")
    print(f"Total berat: {w} kg")
    print(f"Total nilai: {v}")
    print(f"Fitness akhir: {fitness(best)}")
    print("="*53)

    # Mengembalikan stdout ke normal dan mengambil log
    sys.stdout = old_stdout
    return redirected_output.getvalue()
