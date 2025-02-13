from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.views import UserViewSet, LoginLogViewSet, CustomAuthToken
from assets.views import AssetViewSet
from django.conf import settings
from django.conf.urls.static import static

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
router.register(r'users', UserViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'login-logs', LoginLogViewSet)

urlpatterns = [
    path('api/debug/', debug_urls, name='debug-urls'),  # 添加调试路由
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/login/', CustomAuthToken.as_view(), name='login'),  # 修改登录路径
        path('users/', include('users.urls')),
        path('assets/', include('assets.urls')),
    ])),
]

# 调试工具栏
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
    # 添加媒体文件服务
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 