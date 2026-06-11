from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Report
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.db.models import Q  # <-- WAJIB UTK LOGIKA OR PRIVASI DOSEN

# 🔑 TAMBAHAN IMPORT UNTUK REST FRAMEWORK (LAB 12 - FIGURE 1)
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import ReportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# =====================================================================
# 🔐 MIXINS PROTEKSI HAK AKSES (SESUAI ATURAN SKENARIO DOSEN)
# =====================================================================

# 1. Khusus Admin: Menolak Warga yang mencoba masuk ke menu verifikasi status Admin
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'is_admin', False)

    def handle_no_permission(self):
        messages.error(self.request, "Akses ditolak! Hanya admin yang boleh melakukan aksi ini.")
        return redirect('home')

# 2. Khusus Warga: Menolak Admin yang mencoba membuat laporan warga (Alert Merah Ala Riyan)
class CitizenRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'is_member', False)

    def handle_no_permission(self):
        messages.error(self.request, "Admin tidak diizinkan membuat laporan! Fitur ini khusus untuk warga.")
        return redirect('home')

# 3. Khusus Pemilik: Memastikan Warga hanya bisa mengedit/menghapus laporannya sendiri (Citizen1 ==> Report1)
class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        report = self.get_object()
        return self.request.user.is_authenticated and report.reporter == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Akses ditolak! Hanya pemilik laporan yang boleh melakukan aksi ini.")
        return redirect('home')


# =====================================================================
# 📋 HALAMAN UTAMA & CRUD WEB (WEB FRONTEND)
# =====================================================================

# READ (LIST) - SUDAH DIPROTEKSI PRIVASI
class ReportListView(LoginRequiredMixin, ListView):
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    login_url = 'login'

    # 🌐 Menyaring data yang tampil di halaman utama web
    def get_queryset(self):
        user = self.request.user
        # Admin bisa melihat semua data (termasuk semua DRAFT)
        if getattr(user, 'is_admin', False) or user.is_staff:
            return Report.objects.all()
        # Citizen biasa hanya melihat data terverifikasi ATAU DRAFT miliknya sendiri
        return Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))


# CREATE (Menggunakan CitizenRequiredMixin agar hanya warga yang bisa membuat laporan)
class ReportCreateView(LoginRequiredMixin, CitizenRequiredMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Otomatis ikat data siapa warga yang sedang login sebagai pembuat laporan (reporter)
        form.instance.reporter = self.request.user 
        messages.success(self.request, "Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# UPDATE (Menggunakan OwnerRequiredMixin agar hanya pembuat laporan yang bisa mengedit)
class ReportUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)


# DELETE (Menggunakan OwnerRequiredMixin agar hanya pembuat laporan yang bisa menghapus)
class ReportDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# DETAIL - SUDAH DIPROTEKSI PRIVASI
class ReportDetailView(LoginRequiredMixin, DetailView):
    template_name = 'main_app/detail.html'
    context_object_name = 'report'
    login_url = 'login'

    # Mencegah user nakal nembak URL ID draft milik orang lain secara langsung
    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_admin', False) or user.is_staff:
            return Report.objects.all()
        return Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))


# =====================================================================
# 🔐 FUNCTION-BASED DECORATORS & VIEWS (AKSI KHUSUS ADMIN)
# =====================================================================

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not getattr(request.user, 'is_admin', False):
            messages.error(request, "Akses ditolak! Hanya admin yang boleh melakukan aksi ini.")
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return wrapper


# UPDATE STATUS (DITAMBAHKAN DECORATOR)
@admin_required
def update_status(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get('status')

        if new_status in ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']:
            report.status = new_status
            report.save()

            messages.success(request, f"Status berhasil diubah ke {new_status}!")

    return redirect('/')


# OPTIONAL
@admin_required
def verify_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'VERIFIED'
    report.save()
    messages.success(request, "Status diubah ke VERIFIED!")
    return redirect('home')


@admin_required
def process_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'IN_PROGRESS'
    report.save()
    messages.success(request, "Status diubah ke IN PROGRESS!")
    return redirect('home')


@admin_required
def resolve_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'RESOLVED'
    report.save()
    messages.success(request, "Status diubah ke RESOLVED!")
    return redirect('home')


# =====================================================================
# 🔍 LIVE SEARCH API - SUDAH DIPROTEKSI PRIVASI
# =====================================================================

@require_GET
def search_reports(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    user = request.user

    # Filter data pencarian berdasarkan hak privasi user yang sedang login
    if getattr(user, 'is_admin', False) or user.is_staff:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))

    if query:
        reports = reports.filter(title__icontains=query)

    paginator = Paginator(reports, 10)  # 10 data per halaman
    page_obj = paginator.get_page(page)

    data = []
    for r in page_obj:
        data.append({
            'id': r.id,
            'title': r.title,
            'location': r.location,
            'status': r.status,
        })

    return JsonResponse({
        'results': data,
        'has_next': page_obj.has_next(),
        'has_prev': page_obj.has_previous(),
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    })


# =====================================================================
# 🌐 DETAIL API - SUDAH DIPROTEKSI PRIVASI
# =====================================================================

@require_GET
def report_detail_api(request, pk):
    user = request.user
    
    # Validasi object agar endpoint API detail tidak bocor ke user lain
    if getattr(user, 'is_admin', False) or user.is_staff:
        report = get_object_or_404(Report, pk=pk)
    else:
        report = get_object_or_404(Report, Q(reporter=user) | ~Q(status='DRAFT'), pk=pk)

    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    }

    return JsonResponse(data)


# =====================================================================
# 🌟 FITUR BARU LAB 12: DRF API OPTIMIZATION (FIGURE 1)
# =====================================================================

class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Beritahu database siapa pembuat laporannya!
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
        

    def get_queryset(self):
        user = self.request.user
        
        # mekanisme sorting berdasarkan tanggal pembaruan terkini
        queryset = Report.objects.all().order_by('-updated_at')
        
        # mekanisme filtering berdasarkan jenis tab
        tab = self.request.query_params.get('tab', None)
        
        if tab == 'my_reports':
            queryset = queryset.filter(reporter=user)
        elif tab == 'feed':
            queryset = queryset.filter(~Q(reporter=user) & ~Q(status='DRAFT'))
        else:
            queryset = queryset.filter(~Q(status='DRAFT') | Q(status='DRAFT', reporter=user))
            
        return queryset