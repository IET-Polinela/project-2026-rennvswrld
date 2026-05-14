from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    # Mengizinkan akses publik untuk pengujian
    permission_classes = [permissions.AllowAny]
    
    # Mengambil semua data dari model Report
    queryset = Report.objects.all()
    
    # Menggunakan serializer yang sudah kita buat
    serializer_class = ReportSerializer