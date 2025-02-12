from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': '欢迎访问固定资产管理系统API',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'auth': '/api/auth/',
        }
    }) 