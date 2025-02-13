from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Role, Permission, UserRole

User = get_user_model()

class Command(BaseCommand):
    help = '重置测试用户'

    def handle(self, *args, **options):
        try:
            # 清理现有数据
            self.stdout.write('清理现有数据...')
            UserRole.objects.all().delete()
            User.objects.all().delete()
            Role.objects.all().delete()
            Permission.objects.all().delete()

            # 创建角色
            self.stdout.write('创建角色...')
            admin_role = Role.objects.create(
                name='管理员',
                code='admin',
                description='系统管理员'
            )

            dev_role = Role.objects.create(
                name='开发人员',
                code='developer',
                description='开发人员'
            )

            # 创建基本权限
            self.stdout.write('创建权限...')
            permissions = [
                Permission.objects.create(
                    name='用户管理',
                    code='user:manage',
                    description='用户管理权限'
                ),
                Permission.objects.create(
                    name='角色管理',
                    code='role:manage',
                    description='角色管理权限'
                ),
                Permission.objects.create(
                    name='资产管理',
                    code='asset:manage',
                    description='资产管理权限'
                )
            ]

            # 分配权限给角色
            admin_role.permissions.add(*permissions)
            dev_role.permissions.add(permissions[2])  # 只给开发者资产管理权限

            # 创建超级管理员
            self.stdout.write('创建管理员用户...')
            admin = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                is_staff=True,
                is_superuser=True,
                role='admin'
            )
            UserRole.objects.create(user=admin, role=admin_role)
            self.stdout.write(self.style.SUCCESS(f'成功创建管理员用户: {admin.username}'))

            # 验证密码是否正确设置
            self.stdout.write('验证用户密码...')
            if admin.check_password('admin123'):
                self.stdout.write(self.style.SUCCESS('密码设置正确'))
            else:
                self.stdout.write(self.style.ERROR('密码设置失败'))

            # 创建测试用户
            self.stdout.write('创建测试用户...')
            test_user = User.objects.create_user(
                username='test',
                email='test@example.com',
                password='test123',
                role='developer'
            )
            UserRole.objects.create(user=test_user, role=dev_role)
            self.stdout.write(self.style.SUCCESS(f'成功创建测试用户: {test_user.username}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'发生错误: {str(e)}'))
            raise 