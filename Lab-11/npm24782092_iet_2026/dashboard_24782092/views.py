from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'


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