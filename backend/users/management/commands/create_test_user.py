from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Role, UserRole

User = get_user_model()

class Command(BaseCommand):
    help = '创建测试用户'

    def handle(self, *args, **options):
        # 确保角色存在
        admin_role, _ = Role.objects.get_or_create(
            code='admin',
            defaults={
                'name': '管理员',
                'description': '系统管理员'
            }
        )
        
        user_role, _ = Role.objects.get_or_create(
            code='user',
            defaults={
                'name': '普通用户',
                'description': '普通用户'
            }
        )

        # 创建超级管理员
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin'
            )
            UserRole.objects.create(user=admin, role=admin_role)
            self.stdout.write(self.style.SUCCESS('成功创建超级管理员用户'))

        # 创建测试用户
        if not User.objects.filter(username='test').exists():
            user = User.objects.create_user(
                username='test',
                email='test@example.com',
                password='test123',
                role='user'
            )
            UserRole.objects.create(user=user, role=user_role)
            self.stdout.write(self.style.SUCCESS('成功创建测试用户')) 