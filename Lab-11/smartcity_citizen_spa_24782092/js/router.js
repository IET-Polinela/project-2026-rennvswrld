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

    // 📊 2. TEMPLATE HALAMAN DASHBOARD (LAYOUT RESPONSIF 3 KOLOM)
    '#dashboard': `
        <div class="row g-4 animate-fade-in">
            
            <aside class="col-12 col-lg-3">
                <div class="card card-custom p-3 sticky-top" style="top: 20px; z-index: 10;">
                    <button class="btn btn-info text-white btn-lg w-100 fw-bold py-2.5 rounded-3 shadow-sm border-0 d-flex align-items-center justify-content-center gap-2" style="background: linear-gradient(135deg, #4da3ff 0%, #2575fc 100%); font-size: 1rem;">
                        <i class="bi bi-plus-circle-fill"></i> Laporan Baru
                    </button>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card card-custom p-5 text-center text-muted border-dashed-custom bg-white">
                    <div class="d-inline-flex align-items-center justify-content-center bg-light rounded-circle mb-3 mx-auto" style="width: 70px; height: 70px; color: #b0c4de;">
                        <i class="bi bi-inbox-fill display-6"></i>
                    </div>
                    <h4 class="fw-bold text-dark mb-2">Selamat Datang!</h4>
                    <p class="small text-secondary mx-auto mb-0" style="max-width: 400px;">
                        Koneksi API untuk manajemen data laporan warga secara penuh akan diimplementasikan secara dinamis pada materi Lab Session 12.
                    </p>
                </div>
            </section>

            <aside class="col-12 col-lg-3 d-none d-lg-block">
                <div class="card card-custom p-3 sticky-top" style="top: 20px; z-index: 10;">
                    <h6 class="fw-bold text-dark mb-3 pb-2 border-bottom d-flex align-items-center gap-2">
                        <i class="bi bi-info-circle-fill text-primary" style="color: #4da3ff !important;"></i> Papan Pengumuman
                    </h6>
                    <p class="small text-muted mb-0">Belum ada pengumuman berkala dari administrasi kelurahan saat ini.</p>
                </div>
            </aside>

        </div>
    `
};

// 🔥 PROSES AUTH LOGIN ANTI-SPAM & LOADING EFFECT
async function handleLoginProcess(event) {
    event.preventDefault(); // [cite: 119]

    const submitBtn = document.getElementById('submitLoginBtn');
    const usernameInput = document.getElementById('loginUsername').value;
    const passwordInput = document.getElementById('loginPassword').value;

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Memverifikasi...`;
    }

    const payload = {
        username: usernameInput,
        password: passwordInput
    };

    try {
        // Kirim payload ke endpoint token backend menggunakan requestAPI [cite: 120]
        const result = await requestAPI('/api/token/', 'POST', payload); // [cite: 120]

        if (result.status === 200) { // [cite: 121]
            // Simpan access dan refresh token ke dalam localStorage [cite: 121]
            localStorage.setItem('access_token', result.data.access); // [cite: 121]
            localStorage.setItem('refresh_token', result.data.refresh); // [cite: 121]

            // ✨ COMBINATION SAKTI: TOMBOL "OK" TETAP ADA + COUNTDOWN PROGRESS BAR JALAN SEMPURNA
            Swal.fire({
                icon: 'success',
                title: 'Login Berhasil!',
                text: 'Selamat Datang di Portal Warga.',
                confirmButtonColor: '#2980b9', // Warna Biru Khas TRI
                confirmButtonText: 'OK',       // Memaksa teks tombol OK manual muncul
                showConfirmButton: true,       // Memastikan tombol konfirmasi terkunci aktif
                timer: 3000,                   // Garis waktu countdown berjalan selama 3 detik sebelum auto-redirect
                timerProgressBar: true,        // Memunculkan garis animasi loading countdown di bawah modal
                allowOutsideClick: false       // Mengunci layar dari misklik luar area popup
            }).then((res) => {
                // Mau diklik OK manual atau ditunggu timer habis, rute otomatis pindah dengan aman
                window.location.hash = '#dashboard'; // [cite: 121]
                handleRouting(); // Paksa router langsung merombak navbar
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Login Gagal',
                text: result.data.detail || 'Username atau password salah!',
                confirmButtonColor: '#e74c3c'
            });
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = `<i class="bi bi-box-arrow-in-right me-1"></i> Masuk`;
            }
        }
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Koneksi Terputus',
            text: 'Gagal terhubung ke server backend Django Anda.',
            confirmButtonColor: '#e74c3c'
        });
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<i class="bi bi-box-arrow-in-right me-1"></i> Masuk`;
        }
    }
}

// ⚙️ FUNGSI HANDLER ROUTING INTERNAL SPA
function handleRouting() {
    const hash = window.location.hash || '#login';
    const contentDiv = document.getElementById('app-content');
    const navMenus = document.getElementById('nav-menus');
    
    if (contentDiv) {
        contentDiv.innerHTML = routes[hash] || routes['#login'];
    }

    // 🎛️ MANAJEMEN NAVBAR SAKTI (Langsung dikunci di dalam routing engine)
    if (hash === '#dashboard' && navMenus) {
        navMenus.innerHTML = `
            <button class="btn btn-outline-light fw-bold btn-sm d-inline-flex align-items-center gap-1" id="logoutBtn">
                <i class="bi bi-box-arrow-right"></i> Logout
            </button>
        `;

        // Trigger aksi klik tombol logout
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.onclick = function() {
                Swal.fire({
                    title: 'Apakah Anda ingin keluar?',
                    text: "Sesi Anda di portal warga akan segera diakhiri.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#2980b9',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Ya, Keluar',
                    cancelButtonText: 'Batal'
                }).then((res) => {
                    if (res.isConfirmed) {
                        localStorage.removeItem('access_token');
                        localStorage.removeItem('refresh_token');
                        window.location.hash = '#login';
                        handleRouting();
                    }
                });
            };
        }
    } else if (navMenus) {
        navMenus.innerHTML = `<span class="text-light small fw-semibold">Gunakan Akun Warga</span>`;
    }
}

// 🎛️ MENGIKAT EVENT NAVIGASI BROWSER
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);