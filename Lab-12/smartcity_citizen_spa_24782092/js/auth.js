// 🔥 FUNGSI JEMBATAN AUTH LOGIN ANTI-SPAM & LOADING EFFECT
// Fungsi ini dipanggil langsung secara inline lewat atribut onsubmit="handleLoginProcess(event)" di router.js
async function handleLoginProcess(event) {
    event.preventDefault(); // ⚠️ Wajib digunakan agar halaman tidak melakukan reload bawaan HTML

    const submitBtn = document.getElementById('submitLoginBtn');
    const usernameInput = document.getElementById('loginUsername').value;
    const passwordInput = document.getElementById('loginPassword').value;

    // ⏳ Kunci tombol dan pasang animasi spinner loading agar tidak bisa di-spam klik ganda
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Memverifikasi...`;
    }

    const payload = {
        username: usernameInput,
        password: passwordInput
    };

    try {
        // Kirim payload username & password ke endpoint token backend menggunakan requestAPI
        const result = await requestAPI('/api/token/', 'POST', payload);

        if (result.status === 200) {
            // Jika respons berstatus 200, simpan access dan refresh token ke dalam localStorage
            localStorage.setItem('access_token', result.data.access);
            localStorage.setItem('refresh_token', result.data.refresh);

            // ✨ NOTIFIKASI SUKSES PREMIUM SWEETALERT2
            Swal.fire({
                icon: 'success',
                title: 'Login Berhasil!',
                text: 'Selamat Datang di Portal Warga.',
                confirmButtonColor: '#2980b9', // Warna Biru Khas TRI
                timer: 1500,
                timerProgressBar: true,
                showConfirmButton: false,
                willClose: () => {
                    // Ubah rute halaman secara instan ke #dashboard tanpa reload
                    window.location.hash = '#dashboard';
                    // Sinkronisasi paksa perubahan menu navbar atas
                    updateNavbar();
                }
            });
        } else {
            // ❌ NOTIFIKASI ERROR GAGAL OTENTIKASI KREDENSIAL
            Swal.fire({
                icon: 'error',
                title: 'Login Gagal',
                text: result.data.detail || 'Username atau password salah!',
                confirmButtonColor: '#e74c3c'
            });

            // Kembalikan tombol ke kondisi aktif semula jika verifikasi ditolak
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = `<i class="bi bi-box-arrow-in-right me-1"></i> Masuk`;
            }
        }
    } catch (error) {
        // ❌ NOTIFIKASI ERROR JIKA BACKEND DJANGO MATI
        Swal.fire({
            icon: 'error',
            title: 'Koneksi Terputus',
            text: 'Gagal melakukan komunikasi dengan server backend Django (Port 8000).',
            confirmButtonColor: '#e74c3c'
        });

        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<i class="bi bi-box-arrow-in-right me-1"></i> Masuk`;
        }
    }
}

// ⚙️ FUNGSI LAMA (COMPATIBILITY BACKWARD FOR ROUTER INITIALIZATION)
// Tetap dipertahankan agar tidak memicu error undefined di file js lainnya
function setupLoginForm() {
    // Penanganan event submit sekarang dialihkan secara inline ke handleLoginProcess demi stabilitas DOM
}

// 🎛️ FUNGSI DINAMIS UNTUK MEMPERBARUI TOMBOL MENU NAVBAR ATAS (LOGIN / LOGOUT)
function updateNavbar() {
    const navMenus = document.getElementById('nav-menus');
    if (!navMenus) return;

    const token = localStorage.getItem('access_token');

    if (token) {
        // Jika user sudah login dan sedang di #dashboard, render tombol Logout premium
        navMenus.innerHTML = `
            <button class="btn btn-outline-light fw-bold btn-sm d-inline-flex align-items-center gap-1" id="logoutBtn">
                <i class="bi bi-box-arrow-right"></i> Logout
            </button>
        `;

        // Amankan penangkapan elemen tombol logout dari resiko nilai null
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function() {
                // 🌟 KONFIRMASI LOGOUT MODEREN SWEETALERT2
                Swal.fire({
                    title: 'Apakah Anda ingin keluar?',
                    text: "Sesi Anda di portal warga akan segera diakhiri.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#2980b9',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Ya, Keluar',
                    cancelButtonText: 'Batal'
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Bersihkan penyimpanan token dari memori browser
                        localStorage.removeItem('access_token');
                        localStorage.removeItem('refresh_token');
                        
                        Swal.fire({
                            icon: 'success',
                            title: 'Logged Out',
                            text: 'Anda telah keluar dari sistem.',
                            confirmButtonColor: '#2980b9',
                            timer: 1500,
                            showConfirmButton: false,
                            willClose: () => {
                                // Kembalikan rute ke halaman login
                                window.location.hash = '#login';
                                updateNavbar();
                            }
                        });
                    }
                });
            });
        }
    } else {
        // Jika belum login, render teks instruksi standar bawaan modul
        navMenus.innerHTML = `<span class="text-light small fw-semibold">Gunakan Akun Warga</span>`;
    }
}