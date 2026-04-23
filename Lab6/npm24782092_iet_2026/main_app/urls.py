from django.urls import path
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportDetailView,
    update_status,
    verify_report,
    process_report,
    resolve_report
)

urlpatterns = [
    # =========================
    # HOME / LIST
    # =========================
    path('', ReportListView.as_view(), name='home'),

    # =========================
    # CRUD (ADMIN ONLY)
    # =========================
    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='edit_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),

    # =========================
    # DETAIL (SEMUA USER)
    # =========================
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='detail_report'),

    # =========================
    # STATUS (ADMIN ONLY)
    # =========================
    path('update-status/<int:pk>/', update_status, name='update_status'),
    path('verify/<int:pk>/', verify_report, name='verify'),
    path('process/<int:pk>/', process_report, name='process'),
    path('resolve/<int:pk>/', resolve_report, name='resolve'),
]