from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class User(AbstractUser):
    phone = models.CharField(
        '手机号',
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入有效的手机号')],
        null=True,
        blank=True
    )
    email = models.EmailField('邮箱', unique=True)
    is_locked = models.BooleanField('是否锁定', default=False)
    lock_reason = models.CharField('锁定原因', max_length=200, blank=True)
    failed_login_attempts = models.IntegerField('登录失败次数', default=0)
    last_failed_login = models.DateTimeField('最后一次登录失败时间', null=True, blank=True)
    last_login_ip = models.GenericIPAddressField('最后登录IP', null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

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