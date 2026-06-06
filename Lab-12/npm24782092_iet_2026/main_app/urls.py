from django.urls import path, include  # 🌟 TAMBAHAN: import include
from rest_framework.routers import DefaultRouter  # 🌟 TAMBAHAN: import DefaultRouter
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportDetailView,
    update_status,
    verify_report,
    process_report,
    resolve_report,
    search_reports,
    report_detail_api,
    ReportViewSet,  # 🌟 TAMBAHAN: import ReportViewSet kita!
)

# ==============================================================================
# 🚀 1. KONFIGURASI ROUTER DRF (UNTUK SPA LAB 12)
# Router ini akan otomatis membuat endpoint GET, POST, PUT untuk /api/report/
# ==============================================================================
router = DefaultRouter()
router.register(r'report', ReportViewSet, basename='report')

urlpatterns = [
    # =========================
    # 🌐 API ENDPOINTS (SPA)
    # =========================
    path('api/', include(router.urls)), # 🌟 Menyambungkan /api/report/ ke ReportViewSet

    # =========================
    # 🏠 HOME / LIST
    # =========================
    path('', ReportListView.as_view(), name='home'),

    # =========================
    # 📝 CRUD (ADMIN ONLY)
    # =========================
    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='edit_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),

    # =========================
    # 🔍 DETAIL (SEMUA USER)
    # =========================
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='detail_report'),

    # =========================
    # ⚙️ STATUS (ADMIN ONLY)
    # =========================
    path('update-status/<int:pk>/', update_status, name='update_status'),
    path('verify/<int:pk>/', verify_report, name='verify'),
    path('process/<int:pk>/', process_report, name='process'),
    path('resolve/<int:pk>/', resolve_report, name='resolve'),
    path('search/', search_reports, name='search_reports'),
    
    # Endpoint jadul Lab 11 (Tetap dibiarkan agar kodingan lama tidak error)
    path('api/detail/<int:pk>/', report_detail_api, name='report_detail_api'),
]