from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from assets.views import AssetViewSet
from users.views import UserViewSet, LoginLogViewSet

@api_view(['GET'])
def debug_urls(request):
    """列出所有可用的 URL"""
    return Response({
        'available_urls': [
            {'path': '/api/auth-token/', 'methods': ['POST']},
            {'path': '/api/users/me/', 'methods': ['GET']},
            {'path': '/api/assets/', 'methods': ['GET', 'POST']},
        ]
    })

router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'users', UserViewSet)
router.register(r'login-logs', LoginLogViewSet)

urlpatterns = [
    path('api/debug/', debug_urls, name='debug-urls'),  # 添加调试路由
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth-token/', views.obtain_auth_token),  # 登录获取token
    path('api/users/', include('users.urls')),  # 用户相关API
] 