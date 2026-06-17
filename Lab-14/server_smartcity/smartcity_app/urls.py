"""
URL configuration for npm24782092_iet_2026 project.
"""
from django.contrib import admin
from django.urls import path, include
from main_app import views
from usermanagement_24782092.views import RegisterView, CustomLoginView, custom_logout

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usermanagement_24782092.api_views import RegisterAPIView

# ==============================================================================
# # Library Imports Khusus Lab Session 14
# ==============================================================================
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer

urlpatterns = [
    # API ROUTES 🌐
    # 🔴 BERI TANDA PAGAR DI BAWAH INI UNTUK MEMATIKAN API JADUL LAB 9!
    # path('api/', include('main_app.api_urls')), 
    
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),

    # 🚀 JALUR BARU: Halaman Pembuka / Landing Page di root (/)
    path('', views.landing_page, name='landing'),

    # 🚀 JALUR BARU: Halaman Utama Daftar Laporan Warga (/reports/)
    # Menggunakan name='home' agar seluruh tag {% url 'home' %} otomatis lari ke /reports/
    path('reports/', views.ReportListView.as_view(), name='home'),

    # MAIN ROUTES WEB (Monolitik)
    # 🟢 KARENA YANG ATAS DIMATIKAN, DJANGO AKAN MEMBACA API BARU KITA DI DALAM SINI:
    path('', include('main_app.urls')), 
    
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', include('dashboard_24782092.urls')),

    # ADMIN
    path('admin/', admin.site.urls),

    # STATUS UPDATE
    path('update-status/<int:pk>/', views.update_status, name='update_status'),

    # AUTH WEB 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]

# Endpoint token JWT
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# ==============================================================================
# # Endpoint Dokumentasi API OpenAPI 3.0 (Lab Session 14)
# ==============================================================================
urlpatterns += [
    # 1. Endpoint untuk meng-generate file skema mentah (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Endpoint Swagger UI
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Endpoint Scalar UI
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),
]