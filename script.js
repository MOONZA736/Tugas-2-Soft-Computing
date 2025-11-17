let isTugas2Loaded = false;

function updateActiveButton(activeAlgoritma) {
    const buttons = document.querySelectorAll('.alg-button');
    buttons.forEach(button => {
        button.classList.remove('active-alg');

        if (button.textContent.toLowerCase().includes(activeAlgoritma.toLowerCase())) {
            button.classList.add('active-alg');
        }
    });
}

function loadMateri(algoritma) {
    const contentArea = document.getElementById('content-area');
    contentArea.innerHTML = '<h2>Memuat...</h2>'; 

    fetch(`/api/materi/${algoritma}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Gagal memuat data dari backend.');
            }
            return response.json();
        })
        .then(data => {
            let htmlContent = '<h3><span style="color: #007BFF;">♦</span> ' + data.judul + '</h3>'; // Icon diamond
            
            htmlContent += '<h4>Pengertian:</h4>';
            htmlContent += `<p>${data.pengertian}</p>`;

            htmlContent += '<h4>Kelebihan:</h4><ul>';
            data.kelebihan.forEach(item => {
                htmlContent += `<li>${item}</li>`;
            });
            htmlContent += '</ul>';

            htmlContent += '<h4>Kekurangan:</h4><ul>';
            data.kekurangan.forEach(item => {
                htmlContent += `<li>${item}</li>`;
            });
            htmlContent += '</ul>';

            contentArea.innerHTML = htmlContent;

            updateActiveButton(algoritma);
        })
        .catch(error => {
            console.error('Error:', error);
            contentArea.innerHTML = `<h2>Error</h2><p>Gagal memuat data algoritma. (${error.message})</p>`;
        });
}

function loadTugas2Content() {
    if (isTugas2Loaded) return; 

    const container = document.getElementById('tugas2-container');
    container.innerHTML = `<h2 class="text-center text-muted">Mengambil data dari server...</h2>`;
    
    fetch('/api/tugas2_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Gagal koneksi ke API Tugas 2. Pastikan Flask berjalan.');
            }
            return response.json();
        })
        .then(data => {
            container.innerHTML = `
                <h2>Tugas 2 — Hasil Implementasi Algoritma Genetika (Knapsack)</h2>
                
                <h4 class="mt-4">Source Code Algoritma Genetika</h4>
                <pre class="code-block">${data.source_code}</pre>

                <h4 class="mt-4">Output Algoritma Genetika</h4>
                <pre class="output-block">${data.output}</pre>
            `;
            isTugas2Loaded = true;
        })
        .catch(error => {
            container.innerHTML = `<h2 class="error">Gagal memuat Tugas 2</h2><p>${error.message}</p>`;
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-button'); 
    
    const tabPanes = document.querySelectorAll('.tab-pane'); 

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            tabPanes.forEach(pane => pane.classList.remove('active-content'));
            const activePane = document.querySelector(`[data-tab-content="${targetTab}"]`);
            if (activePane) {
                activePane.classList.add('active-content');
            }

            if (targetTab === 'tugas2') {
                loadTugas2Content();
            }
        });
    });
});
