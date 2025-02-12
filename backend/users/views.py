from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model, logout
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import logging
import random
import string
from .models import User, LoginLog, VerificationCode
from .serializers import UserSerializer, LoginLogSerializer
from .utils import send_email, send_sms

User = get_user_model()
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    logger.debug(f"Received request: {request.method} {request.path}")
    logger.debug(f"Headers: {request.headers}")
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'name': user.get_full_name() or user.username,
        'email': user.email,
        'phone': user.phone,
        'is_active': user.is_active,
        'is_locked': user.is_locked,
        'roles': ['admin'] if user.is_superuser else ['user'],
        'avatar': '',  # 可以添加用户头像URL
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.user.is_authenticated:
        # 删除用户的token
        Token.objects.filter(user=request.user).delete()
        logout(request)
    return Response({'message': '成功登出'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        user = self.get_object()
        reason = request.data.get('reason', '')
        
        user.is_locked = True
        user.lock_reason = reason
        user.save()

        # 发送通知
        if user.email:
            send_email(
                user.email,
                '账户锁定通知',
                f'您的账户已被锁定，原因：{reason}'
            )
        if user.phone:
            send_sms(
                user.phone,
                f'您的账户已被锁定，原因：{reason}'
            )

        return Response({'message': '账户已锁定'})

    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        user = self.get_object()
        reason = request.data.get('reason', '')
        
        user.is_locked = False
        user.failed_login_attempts = 0
        user.save()

        # 发送通知
        if user.email:
            send_email(
                user.email,
                '账户解锁通知',
                f'您的账户已解锁，原因：{reason}'
            )

        return Response({'message': '账户已解锁'})

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        verification_code = request.data.get('code')
        new_password = request.data.get('new_password')

        # 验证验证码
        try:
            code_obj = VerificationCode.objects.get(
                user=user,
                code=verification_code,
                is_used=False,
                expires_at__gt=timezone.now()
            )
        except VerificationCode.DoesNotExist:
            return Response(
                {'error': '验证码无效或已过期'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证新密码
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 更新密码
        user.set_password(new_password)
        user.save()
        code_obj.is_used = True
        code_obj.save()

        return Response({'message': '密码重置成功'})

class LoginLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # 获取时间范围
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        # 统计登录失败原因
        failure_stats = LoginLog.objects.filter(
            login_time__gte=start_date,
            result__in=['password_error', 'user_not_exist', 'user_locked', 'ip_restricted']
        ).values('result').annotate(count=Count('id'))

        return Response(failure_stats) 