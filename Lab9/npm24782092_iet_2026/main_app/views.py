from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Report
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator

# =========================
# 🔐 ADMIN MIXIN (DITAMBAHKAN)
# =========================
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    def handle_no_permission(self):
        messages.error(self.request, "Akses ditolak! Hanya admin yang boleh melakukan aksi ini.")
        return redirect('home')


# =========================
# READ (LIST)
# =========================
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    login_url = 'login'


# =========================
# CREATE (DITAMBAHKAN PROTEKSI)
# =========================
class ReportCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# =========================
# UPDATE (DITAMBAHKAN PROTEKSI)
# =========================
class ReportUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)


# =========================
# DELETE (DITAMBAHKAN PROTEKSI)
# =========================
class ReportDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# =========================
# DETAIL
# =========================
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/detail.html'


# =========================
# 🔐 DECORATOR (SUDAH ADA, TETAP DIPAKAI)
# =========================
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_admin:
            messages.error(request, "Akses ditolak! Hanya admin yang boleh melakukan aksi ini.")
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return wrapper


# =========================
# UPDATE STATUS (DITAMBAHKAN DECORATOR)
# =========================
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


# =========================
# OPTIONAL
# =========================
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

# =========================
# LIVE SEARCH API
# =========================
@require_GET
def search_reports(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    reports = Report.objects.all()

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


# =========================
# DETAIL API
# =========================
@require_GET
def report_detail_api(request, pk):
    report = get_object_or_404(Report, pk=pk)

    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    }

    return JsonResponse(data)