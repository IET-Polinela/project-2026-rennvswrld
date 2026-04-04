from .models import Report
from .forms import ReportForm
from django.shortcuts import render, redirect

def home(request):
    reports = Report.objects.all()
    return render(request, 'main_app/home.html', {'reports': reports})

def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()

    return render(request, 'main_app/add_report.html', {'form': form})

def delete_report(request, id):
    report = Report.objects.get(id=id)
    report.delete()
    return redirect('home')

def edit_report(request, id):
    report = Report.objects.get(id=id)

    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm(instance=report)

    # ✅ INI WAJIB ADA (DI LUAR IF ELSE)
    return render(request, 'main_app/add_report.html', {'form': form})

# from django.shortcuts import render

# def home(request):
#     return render(request, 'main_app/home.html')