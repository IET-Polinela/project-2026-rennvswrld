from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # 🔐 Mengamankan data (Password sudah otomatis di-hash oleh UserCreationForm)
        user = form.save(commit=False)
        user.is_admin = False   # 🔥 Sesuai ketentuan soal
        user.is_member = True
        user.is_active = True   # 🔥 Memastikan akun langsung aktif
        user.save()
        
        self.object = user
        messages.success(self.request, "Pendaftaran warga berhasil! Silakan masuk 👋")
        
        # ✅ WAJIB ADA: Mengembalikan objek HttpResponseRedirect agar tidak memicu ValueError None
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("\n❌ BOLO, REGISTRASI WEB GAGAL KARENA:")
        print(form.errors.as_data())
        print("======================================\n")
        # ✅ WAJIB ADA: Mengembalikan template kembali jika form gagal
        return super().form_invalid(form)
    

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, "Login berhasil! Selamat datang 👋")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("\n🔍 ===== INVESTIGASI LOGIN BOLO =====")
        print("1. Data yang dikirim Browser:", self.request.POST)
        print("2. Alasan Django Menolak:", form.errors.as_data())
        print("======================================\n")
        messages.error(self.request, "Username atau password salah!")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')
    

def custom_logout(request):
    logout(request)
    messages.success(request, "Logout berhasil. Sampai jumpa 👋")
    return redirect('login')