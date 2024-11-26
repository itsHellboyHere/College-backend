from rest_framework import permissions

class IsStudentPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsFacultyPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_faculty
