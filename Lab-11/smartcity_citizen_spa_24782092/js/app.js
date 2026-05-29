// Memastikan status navbar sinkron saat aplikasi pertama kali diakses browser
document.addEventListener('DOMContentLoaded', function() {
    if (typeof updateNavbar === 'function') {
        updateNavbar();
    }
});