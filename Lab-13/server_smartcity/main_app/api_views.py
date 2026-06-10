from rest_framework import viewsets, permissions
from django.db.models import Q  # <-- Ditambahkan untuk logika penyaringan OR antar-user
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly 

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    # 🌐 MENGATUR PRIVASI VISIBILITAS DATA (LIST & DETAIL)
    def get_queryset(self):
        user = self.request.user
        
        # 1. Admin/Staff ==> Bisa melihat SEMUA laporan tanpa terkecuali (Termasuk semua DRAFT milik siapa pun)
        if user.is_staff or user.is_superuser:
            return Report.objects.all()
            
        # 2. Citizen/Warga Biasa ==> Hanya bisa melihat laporan miliknya sendiri ATAU data yang BUKAN DRAFT
        # (Mencegah sesama warga saling mengintip draf laporan lain)
        return Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))

    # 🔒 MENGATUR HAK AKSES SECARA DINAMIS BERDASARKAN AKSI
    def get_permissions(self):
        # Jika user melakukan Edit (update) atau Hapus (destroy)
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        
        # Untuk aksi melihat data (list/detail) dan membuat data baru
        return [permissions.IsAuthenticated()]

    # ✍️ OTOMATIS MENGISI FIELD REPORTER DENGAN USER YANG SEDANG LOGIN
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)