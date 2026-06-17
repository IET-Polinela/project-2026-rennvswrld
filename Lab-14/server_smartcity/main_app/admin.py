from django.contrib import admin
from .models import Report

# Mendaftarkan model Report agar bisa dikelola di Django Admin Panel
admin.site.register(Report)