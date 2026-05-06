from django.db import models

# Create your models here.
from django.db import models

class Barang(models.Model):
    # Field sesuai spesifikasi UTS
    nama = models.CharField(max_length=100)
    kategori = models.CharField(max_length=50)
    harga_beli = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField()

    def __str__(self):
        return self.nama