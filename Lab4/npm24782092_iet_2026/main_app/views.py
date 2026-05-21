from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Report

# READ
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

# CREATE
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

# UPDATE
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

# DELETE
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('home')

# DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/detail.html'

from django.views import View
from django.shortcuts import get_object_or_404, redirect

class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('home')
    
    from django.shortcuts import get_object_or_404

def verify_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'VERIFIED'
    report.save()
    return redirect('home')


def process_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'PROCESS'
    report.save()
    return redirect('home')


def resolve_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.status = 'RESOLVED'
    report.save()
    return redirect('home')