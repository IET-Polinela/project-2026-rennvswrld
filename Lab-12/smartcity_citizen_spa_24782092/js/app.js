// =====================================================================
// 🌍 VARIABEL GLOBAL (STATE MANAGEMENT SPA - LAB SESSION 12)
// =====================================================================
let currentTab = 'feed'; 
let currentPage = 1;     
let allReports = [];     
let totalPages = 1;     
let editingReportId = null; 

// =====================================================================
// 🚀 EVENT LISTENER UTAMA (SINKRONISASI TOMBOL MODAL FORM)
// =====================================================================
document.addEventListener('DOMContentLoaded', function() {
    if (typeof updateNavbar === 'function') updateNavbar();
    
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    if (btnDraft) {
        btnDraft.addEventListener('click', function() {
            handleReportSubmit('DRAFT');
        });
    }

    if (btnSubmit) {
        btnSubmit.addEventListener('click', function() {
            handleReportSubmit('REPORTED'); 
        });
    }
});

// =====================================================================
// 🌟 3. FETCHING PAGINATED LIST & RENDER PROGRESS BAR (LAB 12 - STEP 3)
// =====================================================================
async function loadDashboardData(tab = currentTab, page = currentPage) {
    currentTab = tab;
    currentPage = page;

    // Sinkronisasi kelas aktif pada tombol tab di UI
    if(document.getElementById('tab-feed') && document.getElementById('tab-my_reports')) {
        document.getElementById('tab-feed').className = tab === 'feed' ? 'nav-link active text-primary fw-bold bg-white shadow-sm rounded-pill px-4' : 'nav-link text-secondary fw-bold border-0 bg-transparent px-4';
        document.getElementById('tab-my_reports').className = tab === 'my_reports' ? 'nav-link active text-primary fw-bold bg-white shadow-sm rounded-pill px-4' : 'nav-link text-secondary fw-bold border-0 bg-transparent px-4';
    }

    // 🛡️ BUNGKUS DENGAN TRY...CATCH AGAR APLIKASI TIDAK AKAN PERNAH STUCK MUTER-MUTER
    try {
        const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`, 'GET');

        if (response && response.status === 200) {
            // 🌟 LOGIKA KEBAL PELURU: Deteksi otomatis format data DRF
            if (response.data.results !== undefined) {
                // Jika backend memakai Paginasi (ada kotak 'results')
                allReports = response.data.results;
                const totalItems = response.data.count || 0;
                totalPages = Math.ceil(totalItems / 10);
            } else if (Array.isArray(response.data)) {
                // Jika backend mengirim data telanjang (Array Flat)
                allReports = response.data;
                totalPages = Math.ceil(allReports.length / 10) || 1;
            } else {
                // Jika data benar-benar kosong
                allReports = [];
                totalPages = 1;
            }

            // Pemicu Perbaruan UI (Sinkronisasi Antarmuka)
            if (typeof renderList === 'function') renderList();            
            if (typeof renderPagination === 'function') renderPagination();
            
            loadSummaryStats();
        } else {
            showErrorLayout();
        }
    } catch (error) {
        console.error("Terjadi crash pembacaan API, dialihkan ke layout eror:", error);
        showErrorLayout();
    }
}

// Fungsi pembantu menggambar layout eror jika token mati / server putus
function showErrorLayout() {
    const listContainer = document.getElementById('listContainer');
    if (listContainer) {
        listContainer.innerHTML = `
            <div class="col-12 text-center text-muted p-5 bg-white shadow-sm rounded-4 mt-2">
                <i class="bi bi-exclamation-triangle fs-1 text-danger"></i>
                <p class="mt-2 fw-bold text-dark">Sesi Berakhir / Gagal Memuat Data</p>
                <p class="small text-secondary">Token keamanan Anda kedaluwarsa. Silakan klik tombol keluar di kanan atas lalu login kembali.</p>
            </div>
        `;
    }
    const paginationContainer = document.getElementById('paginationContainer');
    if (paginationContainer) paginationContainer.innerHTML = '';
}

// Fungsi pembantu perpindahan tab linimasa
function switchTab(tabName) {
    loadDashboardData(tabName, 1);
}

// =====================================================================
// 📊 4. KALKULASI REKAP STATUS DI SIDEBAR (LAB 12 - STEP 4)
// =====================================================================
async function loadSummaryStats() {
    try {
        const response = await requestAPI('/api/report/?tab=my_reports&page_size=1000', 'GET');
        if (response && response.status === 200) {
            
            // 🌟 LOGIKA KEBAL PELURU UNTUK SIDEBAR
            let allMyReports = [];
            if (response.data.results !== undefined) {
                allMyReports = response.data.results;
            } else if (Array.isArray(response.data)) {
                allMyReports = response.data;
            }

            const countDraft = allMyReports.filter(report => report.status === 'DRAFT').length;
            const countReported = allMyReports.filter(report => report.status === 'REPORTED').length;
            const countInProgress = allMyReports.filter(report => report.status === 'IN_PROGRESS').length;
            const countResolved = allMyReports.filter(report => report.status === 'RESOLVED').length;

            const elDraft = document.getElementById('countDraft');
            const elReported = document.getElementById('countReported');
            const elInProgress = document.getElementById('countInProgress');
            const elResolved = document.getElementById('countResolved');

            if (elDraft) elDraft.innerText = countDraft;
            if (elReported) elReported.innerText = countReported;
            if (elInProgress) elInProgress.innerText = countInProgress;
            if (elResolved) elResolved.innerText = countResolved;
        }
    } catch (e) {
        console.log("Gagal memuat statistik sidebar:", e);
    }
}

// =====================================================================
// 📝 5. REPORT MANAGEMENT VIA MODAL FORM (LAB 12 - STEP 5)
// =====================================================================
async function editDraft(id) {
    try {
        const response = await requestAPI(`/api/report/${id}/`, 'GET');
        if (response && response.status === 200) {
            const report = response.data;
            document.getElementById('reportTitle').value = report.title;
            document.getElementById('reportCategory').value = report.category;
            document.getElementById('reportLocation').value = report.location;
            document.getElementById('reportDescription').value = report.description;
            
            editingReportId = id;
            
            // 🌟 PERBAIKAN: Ubah Judul Modal Menjadi Mode Edit
            const modalTitle = document.querySelector('#reportModal .modal-title');
            if (modalTitle) modalTitle.innerText = 'Edit Draft Laporan';
            
            const modalElement = document.getElementById('reportModal');
            const reportModal = new bootstrap.Modal(modalElement);
            reportModal.show();
        } else {
            Swal.fire("Gagal", "Data draf tidak ditemukan.", "error");
        }
    } catch (error) {
        console.error("Error fetching detail:", error);
    }
}

async function handleReportSubmit(targetStatus) {
    const title = document.getElementById('reportTitle').value;
    const category = document.getElementById('reportCategory').value;
    const location = document.getElementById('reportLocation').value;
    const description = document.getElementById('reportDescription').value;

    if (!title || !category || !location || !description) {
        Swal.fire("Peringatan", "Harap lengkapi seluruh kolom formulir!", "warning");
        return;
    }

    const payload = {
        title: title,
        category: category,
        location: location,
        description: description,
        status: targetStatus 
    };

    const method = editingReportId === null ? 'POST' : 'PUT';
    const endpoint = editingReportId === null ? '/api/report/' : `/api/report/${editingReportId}/`;

    try {
        const response = await requestAPI(endpoint, method, payload);

        if (response && (response.status === 201 || response.status === 200)) {
            const modalElement = document.getElementById('reportModal');
            const modalInstance = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
            modalInstance.hide();
            
            document.body.classList.remove('modal-open');
            const modalBackdrop = document.querySelector('.modal-backdrop');
            if (modalBackdrop) modalBackdrop.remove();

            document.getElementById('reportForm').reset();
            editingReportId = null;

            Swal.fire({
                icon: 'success',
                title: 'Berhasil',
                text: targetStatus === 'DRAFT' ? 'Draft berhasil disimpan!' : 'Laporan berhasil diajukan!',
                timer: 2000,
                showConfirmButton: false
            });

            loadDashboardData();
        } else {
            Swal.fire("Gagal", "Terjadi kesalahan pemrosesan data di server.", "error");
        }
    } catch (err) {
        Swal.fire("Gagal", "Koneksi terputus ke server backend.", "error");
    }
}

function openNewReportModal() {
    editingReportId = null;
    document.getElementById('reportForm').reset();
    
    // 🌟 PERBAIKAN: Kembalikan Judul Modal Menjadi Mode Buat Baru
    const modalTitle = document.querySelector('#reportModal .modal-title');
    if (modalTitle) modalTitle.innerText = 'Buat Laporan Baru';

    const modalElement = document.getElementById('reportModal');
    const reportModal = new bootstrap.Modal(modalElement);
    reportModal.show();
}

// =====================================================================
// 🎨 FUNGSI MANIPULASI DOM: RENDER KARTU PERSIS GAMBAR ACUAN DOSEN
// =====================================================================
function renderList() {
    const container = document.getElementById('listContainer');
    if (!container) return;

    container.innerHTML = ''; 

    if (allReports.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center text-muted p-5 border-dashed-custom bg-white mt-2 rounded-3">
                <i class="bi bi-inbox fs-1"></i>
                <p class="mt-2 fw-bold">Belum ada laporan di tab ini.</p>
            </div>`;
        return;
    }

    let htmlContent = '';
    allReports.forEach(report => {
        let progress = 0; let barColor = ''; let statusText = '';
        
        if(report.status === 'DRAFT') { progress = 0; barColor = 'bg-secondary'; statusText = 'Draf'; }
        else if(report.status === 'REPORTED') { progress = 25; barColor = 'bg-warning'; statusText = 'Diajukan'; }
        else if(report.status === 'VERIFIED') { progress = 50; barColor = 'bg-info'; statusText = 'Diverifikasi'; }
        else if(report.status === 'IN_PROGRESS') { progress = 75; barColor = 'bg-primary'; statusText = 'Diproses'; }
        else if(report.status === 'RESOLVED') { progress = 100; barColor = 'bg-success'; statusText = 'Selesai'; }

        let categoryText = report.category;
        if(report.category === 'INFRASTRUCTURE') categoryText = 'Infrastruktur';
        else if(report.category === 'ENVIRONMENT') categoryText = 'Lingkungan';
        else if(report.category === 'CRIME') categoryText = 'Kriminalitas';
        else if(report.category === 'OTHER') categoryText = 'Lainnya';

        htmlContent += `
            <div class="col-12 col-md-6">
                <div class="card border-0 shadow-sm h-100 rounded-3 bg-white">
                    <div class="card-body p-4 d-flex flex-column">
                        
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge ${barColor} text-dark fw-bold rounded-1 px-2.5 py-1" style="font-size: 0.75rem;">${report.status}</span>
                            <span class="text-muted small">${categoryText}</span>
                        </div>
                        
                        <h4 class="card-title fw-bold text-dark mb-1" style="font-size: 1.4rem;">${report.title}</h4>
                        <p class="text-secondary small mb-3 flex-grow-1">${report.description}</p>
                        
                        <hr class="text-muted my-2">
                        <div class="mb-3 small text-dark">
                            <div class="mb-1"><strong>Lokasi:</strong> ${report.location}</div>
                            <div><strong>Oleh:</strong> ${report.reporter}</div>
                        </div>
        `;

        if (report.status === 'DRAFT') {
            htmlContent += `
                        <div class="mt-auto text-end">
                            <button class="btn btn-sm btn-outline-primary fw-bold px-3 rounded-2" onclick="editDraft(${report.id})">
                                <i class="bi bi-pencil-square"></i> Edit Draft
                            </button>
                        </div>
            `;
        } else {
            htmlContent += `
                        <div class="mt-auto">
                            <div class="d-flex justify-content-between small fw-bold mb-1" style="font-size: 0.8rem;">
                                <span class="text-secondary">Progress Laporan:</span>
                                <span class="text-primary">${statusText} (${progress}%)</span>
                            </div>
                            <div class="progress rounded-pill" style="height: 6px;">
                                <div class="progress-bar ${barColor}" style="width: ${progress}%"></div>
                            </div>
                        </div>
            `;
        }

        htmlContent += `</div></div></div>`;
    });
    
    container.innerHTML = htmlContent;
}

function renderPagination() {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    paginationContainer.innerHTML = '';
    if (totalPages <= 1) return; 

    let buttonsHTML = '<div class="btn-group shadow-sm">';
    buttonsHTML += `<button class="btn btn-outline-primary fw-bold" ${currentPage === 1 ? 'disabled' : ''} onclick="loadDashboardData('${currentTab}', ${currentPage - 1})">« Prev</button>`;
    
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);
    
    if (currentPage <= 3) {
        endPage = Math.min(totalPages, 5);
    }
    if (currentPage > totalPages - 2) {
        startPage = Math.max(1, totalPages - 4);
    }

    if (startPage > 1) {
        buttonsHTML += `<button class="btn btn-outline-primary fw-bold" onclick="loadDashboardData('${currentTab}', 1)">1</button>`;
        if (startPage > 2) buttonsHTML += `<button class="btn btn-outline-primary disabled" disabled>...</button>`;
    }

    for (let i = startPage; i <= endPage; i++) {
        buttonsHTML += `<button class="btn fw-bold ${i === currentPage ? 'btn-primary' : 'btn-outline-primary'}" onclick="loadDashboardData('${currentTab}', ${i})">${i}</button>`;
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) buttonsHTML += `<button class="btn btn-outline-primary disabled" disabled>...</button>`;
        buttonsHTML += `<button class="btn btn-outline-primary fw-bold" onclick="loadDashboardData('${currentTab}', ${totalPages})">${totalPages}</button>`;
    }
    
    buttonsHTML += `<button class="btn btn-outline-primary fw-bold" ${currentPage === totalPages ? 'disabled' : ''} onclick="loadDashboardData('${currentTab}', ${currentPage + 1})">Next »</button>`;
    buttonsHTML += '</div>';
    paginationContainer.innerHTML = buttonsHTML;
}