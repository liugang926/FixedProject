from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        required_permission = getattr(view, 'required_permission', None)
        if not required_permission:
            return True
            
        user_roles = request.user.userrole_set.all()
        for user_role in user_roles:
            if user_role.role.permissions.filter(code=required_permission).exists():
                return True
        return False 