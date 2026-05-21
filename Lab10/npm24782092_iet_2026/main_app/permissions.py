from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Mengizinkan metode akses data aman seperti GET, HEAD, atau OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Memastikan pengubah adalah pemilik laporan DAN status laporan masih DRAFT
        return obj.reporter == request.user and obj.status == 'DRAFT'