import json
from django.utils.deprecation import MiddlewareMixin
from .models import OperationLog

class OperationLogMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.IGNORE_PATHS = ['/api/login/', '/api/logout/']
        self.IGNORE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    def process_request(self, request):
        if request.path in self.IGNORE_PATHS or request.method in self.IGNORE_METHODS:
            return None

        try:
            # 获取请求参数
            if request.method == 'GET':
                params = request.GET.dict()
            else:
                params = json.loads(request.body.decode('utf-8')) if request.body else {}

            # 创建操作日志
            OperationLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=self._get_action(request.method, request.path),
                module=self._get_module(request.path),
                description=self._get_description(request.method, request.path),
                url=request.path,
                method=request.method,
                params=params,
                ip=self._get_client_ip(request),
                browser=f"{request.user_agent.browser.family} {request.user_agent.browser.version_string}",
                os=f"{request.user_agent.os.family} {request.user_agent.os.version_string}"
            )
        except Exception as e:
            print(f"记录操作日志失败: {str(e)}")

        return None

    def _get_action(self, method, path):
        if method == 'POST':
            return 'create'
        elif method in ['PUT', 'PATCH']:
            return 'update'
        elif method == 'DELETE':
            return 'delete'
        return 'other'

    def _get_module(self, path):
        parts = path.strip('/').split('/')
        return parts[1] if len(parts) > 1 else 'unknown'

    def _get_description(self, method, path):
        module = self._get_module(path)
        action = self._get_action(method, path)
        return f"{action} {module}"

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR') 