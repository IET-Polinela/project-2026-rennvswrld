from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # 💡 Sesuai standar Django, password1 dan password2 otomatis diurus oleh UserCreationForm.
        # Kita hanya perlu mendaftarkan field tambahan yang ingin ditampilkan.
        fields = ['username', 'email']