from rest_framework import permissions


class IsOwnerAndAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # let permmission just for create user
        if request.method == 'POST' :
            return True
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user == obj
