from flask import Flask, render_template, jsonify
import os
import textwrap
from genetic_output import run_genetic_algorithm 

SOURCE_CODE_GENETIKA = textwrap.dedent(r'''
import random

# ---------------------------
# 1. Data Masalah Knapsack
# ---------------------------
items = {
    'A': {'weight': 7, 'value': 5},
    'B': {'weight': 2, 'value': 4},
    'C': {'weight': 1, 'value': 7},
    'D': {'weight': 9, 'value': 2},
}
capacity = 15
item_list = list(items.keys())
n_items = len(item_list)

# ---------------------------
# 2. Fungsi bantu
# ---------------------------

def decode(chromosome):
    """Mengembalikan list item, total berat, total nilai"""
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
    """Fungsi fitness dengan penalti berat"""
    chosen_items, total_weight, total_value = decode(chromosome)
    
    if total_weight <= capacity:
        return total_value
    else:
        # Penalti berat berlebihan 
        return 0

def roulette_selection(population, fitnesses):
    """Seleksi roulette wheel"""
    total_fit = sum(fitnesses)
    
    if total_fit == 0:
        return random.choice(population)
        
    pick = random.uniform(0, total_fit)
    current = 0
    
    for chrom, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return chrom
    
    return population[-1]

def crossover(p1, p2):
    """Single-point crossover"""
    if len(p1) != len(p2):
        raise ValueError("Parent length mismatch")
        
    point = random.randint(1, len(p1) - 1)
    
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    
    return child1, child2

def mutate(chromosome, mutation_rate=0.1):
    """Flip bit dengan probabilitas mutation_rate"""
    return [1 - g if random.random() < mutation_rate else g for g in chromosome]

# ------------------------------
# 3. Algoritma Genetika Utama
# ------------------------------

def genetic_algorithm(pop_size=10, generations=10, crossover_rate=0.8, mutation_rate=0.1, elitism=True):
    # 1. Inisialisasi populasi acak
    population = [[random.randint(0, 1) for _ in range(n_items)] for _ in range(pop_size)]

    for gen in range(generations):
        # Hitung fitness
        fitnesses = [fitness(ch) for ch in population]
        
        # Catat individu terbaik
        best_index = fitnesses.index(max(fitnesses))
        best_chrom = population[best_index]
        best_fit = fitnesses[best_index]
        best_items, w, v = decode(best_chrom)
        
        print(f'Generasi {gen+1}:')
        print(f"Terbaik: {best_chrom} | Item: {best_items} | Berat: {w} | Nilai: {v} | Fitness: {best_fit}")
        
        # Buat generasi baru
        new_population = []
        
        # Elitism: pertahankan individu terbaik
        if elitism:
            new_population.append(best_chrom)

        while len(new_population) < pop_size:
            # Seleksi orang tua
            parent1 = roulette_selection(population, fitnesses)
            parent2 = roulette_selection(population, fitnesses)

            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]
                
            # Mutasi
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            # Tambah ke populasi baru
            new_population.extend([child1, child2])

        # Batasi ukuran populasi
        population = new_population[:pop_size]

    # Ambil hasil akhir
    fitnesses = [fitness(ch) for ch in population]
    best_index = fitnesses.index(max(fitnesses))
    best_chrom = population[best_index]
    best_items, w, v = decode(best_chrom)
    
    print('\n' + "="*20 + " HASIL AKHIR " + "="*20)
    print(f'Kromosom terbaik: {best_chrom}')
    print(f'Item terpilih: {best_items}')
    print(f'Total berat: {w} kg')
    print(f'Total nilai: ${v}')
    print(f'Fitness akhir: {fitness(best_chrom)}')
    print("="*53)


# ---------------------
# 4. Jalankan Program
# ---------------------

if __name__ == '__main__':
    random.seed(43) # agar hasil replikasi konsisten

    # Contoh menjalankan algoritma:
    genetic_algorithm(pop_size=8, generations=7, crossover_rate=0.8, mutation_rate=0.1)
''')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

ALGORITMA_DATA = {
    "fuzzy": {
        "judul": "Algoritma Fuzzy Logic",
        "pengertian": "Logika Fuzzy memperluas logika klasik dengan derajat kebenaran antara 0 dan 1, sehingga cocok untuk memodelkan ketidakpastian atau data samar.",
        "kelebihan": ["Mampu menangani ketidakpastian dan ambiguitas data.", "Mudah diinterpretasikan dengan aturan IF-THEN.", "Tidak butuh model matematis yang rumit."],
        "kekurangan": ["Akurasi bergantung pada pakar untuk rule base.", "Membutuhkan banyak validasi dan verifikasi."]
    },
    "jst": {
        "judul": "Jaringan Syaraf Tiruan (JST)",
        "pengertian": "JST adalah model komputasi yang terinspirasi dari struktur dan fungsi jaringan saraf biologis di otak manusia. JST belajar dari data untuk mengenali pola.",
        "kelebihan": ["Kemampuan belajar dan beradaptasi.", "Mampu memproses data secara paralel.", "Memiliki toleransi kesalahan."],
        "kekurangan": ["Bersifat Black Box (Sulit diinterpretasi).", "Membutuhkan data pelatihan besar.", "Membutuhkan sumber daya komputasi tinggi."]
    },
    "genetika": {
        "judul": "Algoritma Genetika",
        "pengertian": "Algoritma pencarian adaptif yang meniru proses seleksi alam dan evolusi biologis untuk mencari solusi optimal melalui operator seleksi, crossover, dan mutasi.",
        "kelebihan": ["Mampu menangani masalah optimasi yang kompleks.", "Cocok untuk masalah multi-kriteria.", "Sangat robust."],
        "kekurangan": ["Bersifat stokastik (tidak ada jaminan optimal).", "Membutuhkan banyak iterasi (waktu konvergen lama).", "Sensitif terhadap pemilihan parameter."]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/materi/<algoritma_name>')
def get_materi(algoritma_name):
    data = ALGORITMA_DATA.get(algoritma_name.lower())
    if data:
        return jsonify(data)
    return jsonify({"error": "Algoritma tidak ditemukan"}), 404

@app.route('/api/tugas2_data')
def get_tugas2_data():
    output = run_genetic_algorithm()
    
    return jsonify({
        "source_code": SOURCE_CODE_GENETIKA,
        "output": output
    })

def list_routes():
    """Mencetak semua rute yang tersedia di console."""
    print("\n" + "="*50)
    print("✅ APPLICATION ROUTES")
    print("="*50)
    
    base_url = "http://127.0.0.1:5000"
    print(f"🔗 URL Utama (Tugas 1 & 2): {base_url}/")
    print("="*50)

if __name__ == '__main__':
    list_routes()
    app.run(debug=True, host='127.0.0.1')
