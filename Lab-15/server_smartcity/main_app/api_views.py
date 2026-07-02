from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    # 🌐 MENGATUR PRIVASI VISIBILITAS DATA (LIST & DETAIL)
    def get_queryset(self):
        user = self.request.user
        tab = self.request.query_params.get('tab', None)

        # Base queryset dengan ordering
        queryset = Report.objects.all().order_by('-updated_at')

        # 1. Admin/Staff ==> Bisa melihat SEMUA laporan
        if user.is_staff or user.is_superuser:
            if tab == 'my_reports':
                return queryset.filter(reporter=user)
            elif tab == 'feed':
                return queryset.filter(~Q(status='DRAFT'))
            return queryset

        # 2. Citizen/Warga Biasa — filter berdasarkan tab
        if tab == 'my_reports':
            # Laporan milik sendiri saja
            return queryset.filter(reporter=user)
        elif tab == 'feed':
            # Feed publik: laporan BUKAN DRAFT milik orang lain
            return queryset.filter(~Q(reporter=user) & ~Q(status='DRAFT'))
        else:
            # Default: laporan milik sendiri + laporan non-DRAFT milik orang lain
            return queryset.filter(Q(reporter=user) | ~Q(status='DRAFT'))

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