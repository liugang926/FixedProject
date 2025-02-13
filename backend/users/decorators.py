from functools import wraps
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

def data_scope(model_class):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            # 超级管理员可以查看所有数据
            if request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)

            # 获取用户角色的数据权限
            user_roles = request.user.userrole_set.all()
            data_scopes = []
            for user_role in user_roles:
                try:
                    data_scopes.append(user_role.role.datascope)
                except:
                    continue

            # 如果没有数据权限配置，默认只能查看个人数据
            if not data_scopes:
                self.queryset = model_class.objects.filter(user=request.user)
                return view_func(self, request, *args, **kwargs)

            # 获取最大权限范围
            max_scope = max([ds.scope for ds in data_scopes], key=lambda x: {
                'all': 4,
                'department_and_below': 3,
                'department': 2,
                'custom': 1,
                'personal': 0
            }.get(x, 0))

            # 根据权限范围过滤数据
            if max_scope == 'all':
                pass  # 不需要过滤
            elif max_scope == 'department_and_below':
                departments = request.user.department.get_descendants(include_self=True)
                self.queryset = model_class.objects.filter(department__in=departments)
            elif max_scope == 'department':
                self.queryset = model_class.objects.filter(department=request.user.department)
            elif max_scope == 'custom':
                custom_departments = set()
                for ds in data_scopes:
                    if ds.scope == 'custom':
                        custom_departments.update(ds.departments.all())
                self.queryset = model_class.objects.filter(department__in=custom_departments)
            else:  # personal
                self.queryset = model_class.objects.filter(user=request.user)

            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator 