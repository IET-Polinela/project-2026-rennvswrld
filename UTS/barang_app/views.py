from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Barang
from .forms import BarangForm
# Pastikan titik (.) di depan models ada, artinya mengambil dari file models.py di folder yang sama
from .models import Barang
# Mixin khusus untuk membatasi akses hanya untuk Owner
class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_owner

class BarangListView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = 'barang_list.html'
    context_object_name = 'semua_barang'

class BarangCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = Barang
    form_class = BarangForm
    template_name = 'barang_form.html'
    success_url = reverse_lazy('barang_list')

class BarangDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Barang
    template_name = 'barang_confirm_delete.html'
    success_url = reverse_lazy('barang_list')