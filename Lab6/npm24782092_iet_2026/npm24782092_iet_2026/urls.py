"""
URL configuration for npm24782092_iet_2026 project.
"""

from django.contrib import admin
from django.urls import path, include
from main_app import views
from django.contrib.auth import views as auth_views   
from usermanagement_24782092.views import RegisterView
from django.contrib.auth import views as auth_views
from usermanagement_24782092.views import CustomLoginView
from usermanagement_24782092.views import custom_logout

urlpatterns = [
    # MAIN ROUTES
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('register/', RegisterView.as_view(), name='register'),

    # ADMIN
    path('admin/', admin.site.urls),

    # STATUS UPDATE
    path('update-status/<int:pk>/', views.update_status, name='update_status'),

    # AUTH 🔐
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]