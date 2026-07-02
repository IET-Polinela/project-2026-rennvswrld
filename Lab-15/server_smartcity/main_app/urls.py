from django.urls import path, include
from .views import (
    home_view,
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
)

urlpatterns = [
    # 🏠 HOME PUBLIC — render home.html tanpa auth
    path('', home_view, name='home'),

    # 📋 REPORTS LIST — butuh login admin
    path('reports/', ReportListView.as_view(), name='report_list'),

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
    path('dashboard/search/', search_reports, name='search_reports'),
    
    # Endpoint jadul Lab 11 (Tetap dibiarkan agar kodingan lama tidak error)
    path('api/detail/<int:pk>/', report_detail_api, name='report_detail_api'),
]