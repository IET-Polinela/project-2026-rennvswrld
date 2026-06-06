from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Fitur Anonimitas
    reporter = serializers.SerializerMethodField()
    
    # 🔑 Fitur Baru Lab 12: Kustomisasi Is Owner (Figure 2)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 'is_owner', 
            'created_at', 'updated_at'
        ]

    def get_reporter(self, obj):
        return "Warga Anonim"

    # 🔑 tambahkan SerializerMethodField() untuk memeriksa
    # jika request.user merupakan pelapor
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user
        return False