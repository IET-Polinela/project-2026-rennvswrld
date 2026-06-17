from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import RegisterSerializer # Mengambil serializer yang kita buat di at

# ==============================================================================
# # Library Imports Khusus Lab Session 14
# ==============================================================================
from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True) # Tambahkan ini untuk menyembunyikan endpoint dari dokumen publik!
class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    # Mengizinkan akses publik agar semua orang bisa mendaftar akun warga baru
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer