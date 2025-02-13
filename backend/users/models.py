from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('developer', '开发人员'),
        ('manager', '项目经理'),
    ]

    # 已有的 first_name 和 last_name 字段来自 AbstractUser
    # 添加显示名称字段
    display_name = models.CharField('显示名称', max_length=50, blank=True)
    role = models.CharField(
        '角色',
        max_length=20,
        choices=ROLE_CHOICES,
        default='developer',
        db_index=True  # 添加索引
    )
    department = models.CharField(
        '部门',
        max_length=50,
        blank=True,
        db_index=True  # 添加索引
    )
    position = models.CharField(
        '职位',
        max_length=50,
        blank=True
    )
    phone = models.CharField(
        '手机号',
        max_length=11,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入有效的手机号')],
        blank=True,
        null=True,
        unique=True
    )
    email = models.EmailField('邮箱', unique=True)
    is_locked = models.BooleanField('是否锁定', default=False)
    lock_reason = models.CharField('锁定原因', max_length=200, blank=True)
    failed_login_attempts = models.IntegerField('登录失败次数', default=0)
    last_failed_login = models.DateTimeField('最后一次登录失败时间', null=True, blank=True)
    last_login_ip = models.GenericIPAddressField('最后登录IP', null=True, blank=True)
    entry_date = models.DateField(
        '入职日期',
        null=True,
        blank=True
    )
    avatar = models.ImageField(_('头像'), upload_to='avatars/', null=True, blank=True)

    # 添加多对多关系
    roles = models.ManyToManyField(
        'Role',
        through='UserRole',
        verbose_name=_('角色'),
        related_name='users'
    )

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
        db_table = 'users'

    def __str__(self):
        return f'{self.display_name or self.username} ({self.get_role_display()})'

    def get_full_name(self):
        """
        返回用户全名，优先使用显示名称
        """
        if self.display_name:
            return self.display_name
        full_name = super().get_full_name()
        return full_name if full_name else self.username

    def save(self, *args, **kwargs):
        """
        重写 save 方法，确保密码正确加密
        """
        # 不在这里处理密码加密，使用 create_user 和 create_superuser 方法
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """
        使用父类的 check_password 方法
        """
        return super().check_password(raw_password)

    def get_all_permissions(self):
        """获取用户所有权限"""
        if not hasattr(self, '_permission_cache'):
            perms = set()
            for role in self.roles.all():
                perms.update(perm.code for perm in role.permissions.all())
            self._permission_cache = perms
        return self._permission_cache

class LoginLog(models.Model):
    RESULT_CHOICES = [
        ('success', '成功'),
        ('password_error', '密码错误'),
        ('user_not_exist', '用户不存在'),
        ('user_locked', '账户锁定'),
        ('ip_restricted', 'IP受限'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='用户'
    )
    username = models.CharField('用户名', max_length=150)
    ip_address = models.GenericIPAddressField('IP地址')
    login_time = models.DateTimeField('登录时间', auto_now_add=True)
    result = models.CharField('登录结果', max_length=20, choices=RESULT_CHOICES)
    detail = models.CharField('详细信息', max_length=200, blank=True)

    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name
        ordering = ['-login_time']

class VerificationCode(models.Model):
    TYPE_CHOICES = [
        ('email', '邮箱验证'),
        ('phone', '手机验证'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    code = models.CharField('验证码', max_length=6)
    type = models.CharField('验证类型', max_length=10, choices=TYPE_CHOICES)
    target = models.CharField('验证目标', max_length=100)  # 邮箱或手机号
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    expires_at = models.DateTimeField('过期时间')
    is_used = models.BooleanField('是否已使用', default=False)
    attempts = models.IntegerField('尝试次数', default=0)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

class Role(models.Model):
    """角色模型"""
    name = models.CharField(_('角色名称'), max_length=50, unique=True)
    code = models.CharField(_('角色代码'), max_length=50, unique=True)
    description = models.TextField(_('描述'), blank=True)
    permissions = models.ManyToManyField(
        'Permission',
        verbose_name=_('权限'),
        blank=True
    )
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('角色')
        verbose_name_plural = _('角色')

    def __str__(self):
        return self.name

class Permission(models.Model):
    """权限模型"""
    name = models.CharField(_('权限名称'), max_length=50)
    code = models.CharField(_('权限代码'), max_length=50, unique=True)
    description = models.TextField(_('描述'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('权限')
        verbose_name_plural = _('权限')

    def __str__(self):
        return self.name

class UserRole(models.Model):
    """用户角色关联表"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('用户')
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name=_('角色')
    )
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('用户角色')
        verbose_name_plural = _('用户角色')
        unique_together = ['user', 'role']

class DataScope(models.Model):
    """数据权限范围"""
    SCOPE_CHOICES = [
        ('all', '所有数据'),
        ('department', '本部门数据'),
        ('department_and_below', '本部门及以下数据'),
        ('personal', '个人数据'),
        ('custom', '自定义数据')
    ]

    role = models.OneToOneField(
        Role,
        on_delete=models.CASCADE,
        verbose_name='角色'
    )
    scope = models.CharField(
        '数据范围',
        max_length=20,
        choices=SCOPE_CHOICES,
        default='personal'
    )
    departments = models.ManyToManyField(
        'Department',
        verbose_name='自定义部门',
        blank=True
    )

    class Meta:
        verbose_name = '数据权限'
        verbose_name_plural = verbose_name

class OperationLog(models.Model):
    """操作日志"""
    ACTION_CHOICES = [
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
        ('export', '导出'),
        ('import', '导入'),
        ('other', '其他')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='操作人'
    )
    action = models.CharField(
        '操作类型',
        max_length=20,
        choices=ACTION_CHOICES
    )
    module = models.CharField('功能模块', max_length=50)
    description = models.CharField('操作描述', max_length=200)
    url = models.CharField('请求地址', max_length=200)
    method = models.CharField('请求方法', max_length=20)
    params = models.JSONField('请求参数', null=True)
    ip = models.GenericIPAddressField('IP地址')
    browser = models.CharField('浏览器', max_length=200)
    os = models.CharField('操作系统', max_length=200)
    status = models.BooleanField('执行状态', default=True)
    error_msg = models.TextField('错误信息', blank=True)
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

class Department(models.Model):
    """部门模型"""
    name = models.CharField(_('部门名称'), max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('上级部门')
    )
    order = models.IntegerField(_('排序'), default=0)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('部门')
        verbose_name_plural = _('部门')
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_descendants(self, include_self=False):
        """获取所有下级部门"""
        descendants = []
        if include_self:
            descendants.append(self)
        for child in Department.objects.filter(parent=self):
            descendants.extend(child.get_descendants(True))
        return descendants 