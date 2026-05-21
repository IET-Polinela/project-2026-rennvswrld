from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

# Menggunakan DefaultRouter sesuai instruksi lab [cite: 98, 103]
router = DefaultRouter()

# Registrasi ViewSet dengan awalan rute 'report' [cite: 104]
router.register(r'report', ReportViewSet, basename='report')

# Menetapkan daftar URL ke urlpatterns [cite: 105]
urlpatterns = router.urls