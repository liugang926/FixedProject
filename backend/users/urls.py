from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, LoginLogViewSet, RoleViewSet,
    PermissionViewSet, UserRoleViewSet, OperationLogViewSet,
    get_user_info, user_logout
)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'user-roles', UserRoleViewSet, basename='user-role')
router.register(r'login-logs', LoginLogViewSet, basename='login-log')
router.register(r'operation-logs', OperationLogViewSet, basename='operation-log')

# 自定义路由
urlpatterns = [
    path('me/', get_user_info, name='user-info'),
    path('logout/', user_logout, name='logout'),
]

# 添加 router 的 URL
urlpatterns += router.urls 