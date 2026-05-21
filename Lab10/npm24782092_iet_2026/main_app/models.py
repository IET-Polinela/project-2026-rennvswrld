from django.db import models
from django.conf import settings # Diperlukan untuk mengakses AUTH_USER_MODEL [cite: 37]

# 2.a Menambahkan nilai "DRAFT" ke dalam pilihan status 
STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

class Report(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # 2.b Tambahkan field reporter sebagai ForeignKey ke CustomUser 
    # null=True dan blank=True agar data lama yang tidak punya reporter tidak error [cite: 55, 56]
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # [cite: 32]
        related_name='reports',
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
    
    # 2.c Tambahkan field created_at dan updated_at untuk merekam jejak waktu 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title