from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_admin = False   # 🔥 sesuai soal
        user.is_member = True
        user.save()
        return super().form_valid(form)
    

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, "Login berhasil! Selamat datang 👋")
        return super().form_valid(form)
    

def custom_logout(request):
    logout(request)
    messages.success(request, "Logout berhasil. Sampai jumpa 👋")
    return redirect('login')