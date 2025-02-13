from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model, logout, authenticate, update_session_auth_hash
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import logging
import random
import string
from .models import User, LoginLog, VerificationCode, Role, Permission, UserRole, OperationLog
from .serializers import (
    UserSerializer, LoginLogSerializer, RoleSerializer, PermissionSerializer,
    UserRoleSerializer, LoginSerializer, ChangePasswordSerializer, OperationLogSerializer
)
from .utils import send_email, send_sms
from django.db.models import Q, Count
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAdmin
from .decorators import data_scope
from rest_framework.authentication import TokenAuthentication

User = get_user_model()
logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
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
        'department': user.department,
        'position': user.position,
        'role': user.role,
        'is_active': user.is_active,
        'is_locked': user.is_locked,
        'avatar': user.avatar.url if user.avatar else None,
        'permissions': list(user.get_all_permissions()),
        'roles': [
            {
                'id': ur.role.id,
                'name': ur.role.name,
                'code': ur.role.code
            } for ur in user.userrole_set.all()
        ]
    })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.user.is_authenticated:
        # 删除用户的token
        Token.objects.filter(user=request.user).delete()
        
        # 记录登出日志
        LoginLog.objects.create(
            user=request.user,
            username=request.user.username,
            ip_address=request.META.get('REMOTE_ADDR'),
            result='success',
            detail='用户登出'
        )
        
    return Response({'message': '成功登出'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @data_scope(User)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @data_scope(User)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'lock', 'unlock']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search', '')
        role = self.request.query_params.get('role', '')
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(department__icontains=search)
            )
        if role:
            queryset = queryset.filter(role=role)
            
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            # 设置密码
            password = request.data.get('password', '123456')  # 默认密码
            user.set_password(password)
            user.save()
            
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 如果提供了新密码，则更新密码
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def developers(self, request):
        developers = User.objects.filter(role='developer')
        serializer = self.get_serializer(developers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def managers(self, request):
        managers = User.objects.filter(role='manager')
        serializer = self.get_serializer(managers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        user = self.get_object()
        reason = request.data.get('reason', '')
        user.is_locked = True
        user.lock_reason = reason
        user.save()
        return Response({'message': '账户已锁定'})

    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        user = self.get_object()
        user.is_locked = False
        user.failed_login_attempts = 0
        user.save()
        return Response({'message': '账户已解锁'})

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'detail': '原密码错误'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user)
            return Response({'detail': '密码修改成功'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

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

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        logger.info(f"Login attempt for user: {request.data.get('username')}")
        
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            if not username or not password:
                logger.warning("Missing username or password")
                return Response(
                    {'error': '用户名和密码不能为空'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 使用 Django 的 authenticate 函数
            user = authenticate(
                request,
                username=username,
                password=password
            )
            logger.debug(f"Authentication result for {username}: {user}")

            if not user:
                logger.warning(f"Authentication failed for user: {username}")
                return Response(
                    {'error': '用户名或密码错误'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not user.is_active:
                logger.warning(f"Inactive user attempt to login: {username}")
                return Response(
                    {'error': '账户已被禁用'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 创建或获取 token
            token, _ = Token.objects.get_or_create(user=user)
            
            # 记录登录成功
            LoginLog.objects.create(
                user=user,
                username=username,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                result='success',
                detail='登录成功'
            )
            
            logger.info(f"Login successful for user: {username}")
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'name': user.get_full_name() or user.username,
                    'role': user.role,
                    'permissions': list(user.get_all_permissions())
                }
            })

        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response(
                {'error': '登录失败，请稍后重试'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Role.objects.all()
        if not self.request.user.is_superuser:
            # 非超级管理员只能看到自己的角色
            queryset = queryset.filter(users=self.request.user)
        return queryset.prefetch_related('permissions')

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Permission.objects.all().order_by('code')

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return UserRole.objects.filter(user=self.request.user)
        return UserRole.objects.all()

class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filterset_fields = ['user', 'action', 'module', 'status']
    search_fields = ['description', 'url', 'ip']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # 时间范围过滤
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        return queryset 