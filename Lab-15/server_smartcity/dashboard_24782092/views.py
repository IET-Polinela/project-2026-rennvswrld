from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main_app.models import Report
from django.db.models import Count


# 🔒 Hanya admin/staff yang boleh mengakses dashboard
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (getattr(user, 'is_admin', False) or user.is_staff)

    def handle_no_permission(self):
        messages.error(self.request, "Akses ditolak! Hanya admin yang boleh mengakses dashboard.")
        return redirect('home')


class DashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    login_url = 'login'


def report_stats(request):
    # =========================
    # DATA GRAFIK
    # =========================
    category_data = (
        Report.objects.values('category')
        .annotate(total=Count('id'))
    )

    status_data = (
        Report.objects.values('status')
        .annotate(total=Count('id'))
    )

    # =========================
    # 🔥 DATA TERBARU 
    # =========================
    latest_reported = Report.objects.filter(status='REPORTED').order_by('-id')[:5]
    latest_resolved = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]

    # Convert ke format JSON-friendly
    reported_list = list(
        latest_reported.values('title', 'category', 'location')
    )

    resolved_list = list(
        latest_resolved.values('title', 'category', 'location')
    )

    return JsonResponse({
        'category_data': list(category_data),
        'status_data': list(status_data),
        'latest_reported': reported_list,   # 🔥 tambahan
        'latest_resolved': resolved_list,   # 🔥 tambahan
    })


def dashboard_view(request):
    return render(request, 'dashboard/index.html')