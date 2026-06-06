"""
URL configuration for npm24782092_iet_2026 project.
"""
from django.contrib import admin
from django.urls import path, include
from main_app import views
from usermanagement_24782092.views import RegisterView, CustomLoginView, custom_logout

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usermanagement_24782092.api_views import RegisterAPIView

urlpatterns = [
    # API ROUTES 🌐
    # 🔴 BERI TANDA PAGAR DI BAWAH INI UNTUK MEMATIKAN API JADUL LAB 9!
    # path('api/', include('main_app.api_urls')), 
    
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),

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