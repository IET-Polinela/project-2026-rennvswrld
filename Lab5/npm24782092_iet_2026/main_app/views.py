from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Report


# =========================
# READ (LIST)
# =========================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'


# =========================
# CREATE
# =========================
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# =========================
# UPDATE
# =========================
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)


# =========================
# DELETE
# =========================
class ReportDeleteView(DeleteView):
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
# UPDATE STATUS (VERSI UTAMA)
# =========================
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
# OPTIONAL (TIDAK WAJIB, BOLEH DIHAPUS)
# =========================
def verify_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'VERIFIED'
    report.save()
    messages.success(request, "Status diubah ke VERIFIED!")
    return redirect('home')


def process_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'IN_PROGRESS'
    report.save()
    messages.success(request, "Status diubah ke IN PROGRESS!")
    return redirect('home')


def resolve_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'RESOLVED'
    report.save()
    messages.success(request, "Status diubah ke RESOLVED!")
    return redirect('home')