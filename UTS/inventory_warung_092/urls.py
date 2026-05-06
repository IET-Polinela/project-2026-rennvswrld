"""
URL configuration for inventory_warung_092 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView # Tambahkan ini
from barang_app.views import BarangListView, BarangCreateView, BarangDeleteView
from barang_app.views import (
    BarangListView, BarangCreateView, BarangDeleteView, barang_detail_json
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BarangListView.as_view(), name='barang_list'),
    path('tambah/', BarangCreateView.as_view(), name='barang_tambah'),
    path('hapus/<int:pk>/', BarangDeleteView.as_view(), name='barang_hapus'), # Path hapus dengan ID barang
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('detail-json/<int:pk>/', barang_detail_json, name='barang_detail_json')
]