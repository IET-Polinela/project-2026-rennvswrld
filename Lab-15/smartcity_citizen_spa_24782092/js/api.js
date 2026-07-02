const BASE_URL = 'http://103.151.63.88:8009'; // URL Server Backend Django

// Fungsi global requestAPI untuk membungkus Fetch API
async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    // Otomatis mengambil access_token dari localStorage jika ada
    const token = localStorage.getItem('access_token');
    
    // Konfigurasi Header Standar
    const headers = {
        'Content-Type': 'application/json'
    };

    // Jika token ditemukan, sisipkan pada Headers Authorization dengan format Bearer
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers
    };

    // Jika ada data payload yang dikirim (POST, PUT, PATCH), ubah ke string JSON
    if (bodyData && ['POST', 'PUT', 'PATCH'].includes(method)) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);
        const data = await response.json();

        // 🔒 INTERCEPTOR 401: Jika token expired/invalid, bersihkan sesi dan redirect ke login
        // Diperlukan untuk AUTH-05 dan AUTH-06
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('username');
            window.location.hash = '#login';
            if (typeof handleRouting === 'function') handleRouting();
            return { status: 401, data: data };
        }

        return { status: response.status, data: data };
    } catch (error) {
        console.error('API Request Error:', error);
        return { status: 500, data: { detail: 'Koneksi ke server backend gagal!' } };
    }
}