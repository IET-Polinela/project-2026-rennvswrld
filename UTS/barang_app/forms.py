from django import forms
from .models import Barang

class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = ['nama', 'kategori', 'harga_beli', 'stok']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori': forms.TextInput(attrs={'class': 'form-control'}),
            'harga_beli': forms.NumberInput(attrs={'class': 'form-control'}),
            'stok': forms.NumberInput(attrs={'class': 'form-control'}),
        }