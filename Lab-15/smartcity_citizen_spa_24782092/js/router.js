// 🧭 KONFIGURASI ROUTING HASH-BASED SPA PORTAL CITIZEN
const routes = {
    // 🔒 1. TEMPLATE HALAMAN LOGIN
    '#login': `
        <div class="row justify-content-center align-items-center mt-5 animate-fade-in">
            <div class="col-md-5 col-lg-4">
                <div class="card card-custom p-4 p-md-5">
                    
                    <div class="text-center mb-4">
                        <div class="d-inline-flex align-items-center justify-content-center bg-info bg-opacity-10 p-3 rounded-circle mb-3" style="color: #2980b9; width: 60px; height: 60px;">
                            <i class="bi bi-shield-lock-fill fs-2"></i>
                        </div>
                        <h4 class="fw-bold text-dark mb-1">Login Warga</h4>
                        <p class="text-muted small mb-0">Citizen Single Page Application</p>
                    </div>

                    <form id="loginForm" onsubmit="handleLoginProcess(event)">
                        <div class="mb-3">
                            <label class="form-label small fw-bold text-secondary">Username</label>
                            <div class="input-group shadow-sm rounded-3 overflow-hidden">
                                <span class="input-group-text bg-light border-end-0 text-muted ps-3"><i class="bi bi-person-fill"></i></span>
                                <input type="text" id="loginUsername" class="form-control bg-light border-start-0 py-2 shadow-none text-secondary small" placeholder="Username" required>
                            </div>
                        </div>
                        <div class="mb-4">
                            <label class="form-label small fw-bold text-secondary">Password</label>
                            <div class="input-group shadow-sm rounded-3 overflow-hidden">
                                <span class="input-group-text bg-light border-end-0 text-muted ps-3"><i class="bi bi-key-fill"></i></span>
                                <input type="password" id="loginPassword" class="form-control bg-light border-start-0 py-2 shadow-none text-secondary small" placeholder="Password" required>
                            </div>
                        </div>
                        <button type="submit" id="submitLoginBtn" class="btn btn-info text-white w-100 py-2.5 rounded-3 fw-bold shadow-sm border-0" style="background: linear-gradient(135deg, #4da3ff 0%, #2575fc 100%);">
                            <i class="bi bi-box-arrow-in-right me-1"></i> Masuk
                        </button>
                    </form>

                </div>
            </div>
        </div>
    `,

    // 📊 2. TEMPLATE HALAMAN DASHBOARD
    '#dashboard': `
        <div class="row g-4 animate-fade-in">
            
            <aside class="col-12 col-lg-3">
                <div class="card border-0 shadow-sm mb-4 rounded-3" style="background-color: transparent;">
                    <button id="btnBukaModal" onclick="openNewReportModal()" class="btn btn-primary btn-lg w-100 fw-bold py-4 rounded-3 d-flex flex-column align-items-center justify-content-center gap-2 shadow-sm" style="font-size: 1.15rem; min-height: 140px;">
                        <i class="bi bi-plus-circle fs-2"></i> Buat Laporan<br>Baru
                    </button>
                </div>

                <div class="card border-0 shadow-sm rounded-3">
                    <div class="card-header bg-white border-0 pt-4 pb-2 px-4">
                        <h6 class="fw-bold text-secondary mb-0" style="font-size: 0.8rem; letter-spacing: 0.5px;">
                            <i class="bi bi-activity me-1"></i> STATUS LAPORAN ANDA
                        </h6>
                    </div>
                    <div class="card-body px-4 pb-4" id="summaryStats">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="text-secondary small"><i class="bi bi-pencil-square me-2"></i> Draf</span>
                            <span class="badge bg-secondary rounded-pill px-2.5 py-1" id="countDraft">0</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="text-secondary small"><i class="bi bi-send-fill text-warning me-2"></i> Diajukan</span>
                            <span class="badge bg-warning text-dark rounded-pill px-2.5 py-1" id="countReported">0</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="text-secondary small"><i class="bi bi-gear-fill text-info me-2"></i> Diproses</span>
                            <span class="badge bg-info text-dark rounded-pill px-2.5 py-1" id="countInProgress">0</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="text-secondary small"><i class="bi bi-check-circle-fill text-success me-2"></i> Selesai</span>
                            <span class="badge bg-success rounded-pill px-2.5 py-1" id="countResolved">0</span>
                        </div>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-9">
                <ul class="nav nav-tabs mb-4 border-bottom-0 gap-2" id="dashboardTabs" role="tablist">
                    <li class="nav-item">
                        <button class="nav-link text-secondary fw-bold border-0 bg-transparent px-4 py-2" id="tabMyReports" onclick="switchTab('my_reports')">
                            <i class="bi bi-folder-fill me-2"></i>Laporan Saya
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link text-secondary fw-bold border-0 bg-transparent px-4 py-2" id="tabFeedKota" onclick="switchTab('feed')">
                            <i class="bi bi-globe me-2"></i>Feed Kota (Publik)
                        </button>
                    </li>
                </ul>

                <div class="row g-4" id="listContainer">
                    <div class="col-12 text-center p-5">
                        <div class="spinner-border text-primary" role="status"></div>
                        <p class="mt-2 text-muted small">Menyelaraskan data...</p>
                    </div>
                </div>

                <div id="paginationContainer" class="d-flex justify-content-center mt-4 mb-5"></div>
            </section>
        </div>
    `
};

// 🔥 PROSES AUTH LOGIN
async function handleLoginProcess(event) {
    event.preventDefault(); 
    const submitBtn = document.getElementById('submitLoginBtn');
    const usernameInput = document.getElementById('loginUsername').value;
    const passwordInput = document.getElementById('loginPassword').value;

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Memverifikasi...`;
    }

    const payload = { username: usernameInput, password: passwordInput };

    try {
        const result = await requestAPI('/api/token/', 'POST', payload); 
        if (result.status === 200) { 
            localStorage.setItem('access_token', result.data.access); 
            localStorage.setItem('refresh_token', result.data.refresh); 
            localStorage.setItem('username', usernameInput);
            
            Swal.fire({
                icon: 'success', title: 'Login Berhasil!', text: 'Selamat Datang di Portal Warga.',
                confirmButtonColor: '#2980b9', confirmButtonText: 'OK', showConfirmButton: true, timer: 3000, timerProgressBar: true, allowOutsideClick: false      
            }).then(() => {
                window.location.hash = '#dashboard'; 
                handleRouting(); 
            });
        } else {
            Swal.fire({ icon: 'error', title: 'Login Gagal', text: result.data.detail || 'Username/password salah!', confirmButtonColor: '#e74c3c' });
            if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = `<i class="bi bi-box-arrow-in-right me-1"></i> Masuk`; }
        }
    } catch (error) {
        Swal.fire({ icon: 'error', title: 'Koneksi Terputus', text: 'Gagal terhubung ke server backend.', confirmButtonColor: '#e74c3c' });
        if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = `<i class="bi bi-box-arrow-in-right me-1"></i> Masuk`; }
    }
}

// ⚙️ FUNGSI HANDLER ROUTING INTERNAL SPA
function handleRouting() {
    const hash = window.location.hash || '#login';
    const contentDiv = document.getElementById('app-content');
    const navMenus = document.getElementById('nav-menus');

    // 🔒 AUTH GUARD — TAMBAHKAN 6 BARIS INI
    const token = localStorage.getItem('access_token');
    if (hash === '#dashboard' && !token) {
        window.location.hash = '#login';
        handleRouting();
        return;
    }
    // SAMPAI SINI — sisanya jangan diubah
    
    if (contentDiv) {
        contentDiv.innerHTML = routes[hash] || routes['#login'];
    }

    if (hash === '#dashboard' && typeof loadDashboardData === 'function') {
        loadDashboardData(typeof currentTab !== 'undefined' ? currentTab : 'feed', 1);
    }

    if (hash === '#dashboard' && navMenus) {
        navMenus.innerHTML = `
            <button class="btn btn-outline-light fw-bold btn-sm d-inline-flex align-items-center gap-1" id="logoutBtn">
                <i class="bi bi-box-arrow-right"></i> Logout
            </button>
        `;
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.onclick = function() {
                Swal.fire({
                    title: 'Apakah Anda ingin keluar?', text: "Sesi Anda akan diakhiri.", icon: 'warning',
                    showCancelButton: true, confirmButtonColor: '#2980b9', cancelButtonColor: '#d33',
                    confirmButtonText: 'Ya, Keluar', cancelButtonText: 'Batal'
                }).then((res) => {
                    if (res.isConfirmed) {
                        localStorage.removeItem('access_token'); 
                        localStorage.removeItem('refresh_token');
                        localStorage.removeItem('username');
                        
                        window.location.hash = '#login'; handleRouting();
                    }
                });
            };
        }
    } else if (navMenus) {
        navMenus.innerHTML = `<span class="text-light small fw-semibold">Gunakan Akun Warga</span>`;
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);