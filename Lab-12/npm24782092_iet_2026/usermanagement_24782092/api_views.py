from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import RegisterSerializer # Mengambil serializer yang kita buat di atas

class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    # Mengizinkan akses publik agar semua orang bisa mendaftar akun warga baru
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer