from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from .models import User, LoginLog, Role, Permission, UserRole, OperationLog, DataScope
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            RegexValidator(
                r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$',
                '用户名只能包含字母、数字、下划线，必须以字母开头，长度在4-20位之间'
            )
        ]
    )
    password = serializers.CharField(write_only=True, required=False)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'first_name', 'last_name', 'display_name', 'full_name',
            'role', 'role_display', 'department', 'position',
            'phone', 'entry_date', 'is_active', 'date_joined', 'roles'
        ]
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'email': {'required': True},
            'role': {'required': True}
        }

    def validate_password(self, value):
        if value:
            validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password('123456')  # 设置默认密码
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def get_roles(self, obj):
        user_roles = UserRole.objects.filter(user=obj)
        return [{'id': ur.role.id, 'name': ur.role.name, 'code': ur.role.code}
                for ur in user_roles]

class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class OperationLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = OperationLog
        fields = '__all__'

class DataScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataScope
        fields = ['scope', 'departments'] 