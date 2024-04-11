from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
        # Check permissions for write request
          return bool(request.user and request.user.is_staff)        #if its admin it will return true

class ReviewUserOrReadOnly(permissions.BasePermission):             #Only Review writer can edit his permission

    def has_object_permission(self, request, view, obj):            #Here obj is id.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
        # Check permissions for write request
          return obj.review_user == request.user or request.user.is_staff