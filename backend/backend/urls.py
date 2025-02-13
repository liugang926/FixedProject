from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomAuthToken, UserViewSet
from django.conf import settings
from django.conf.urls.static import static

# 创建路由器
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
        path('', include(router.urls)),
        path('users/', include('users.urls')),
    ])),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 