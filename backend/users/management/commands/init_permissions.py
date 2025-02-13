from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

class Command(BaseCommand):
    help = '初始化权限和角色数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化权限数据...')
        
        try:
            with transaction.atomic():
                # 先加载权限数据
                call_command('loaddata', 'initial_permissions.json')
                self.stdout.write(self.style.SUCCESS('权限数据初始化成功'))
                
                # 再加载角色数据
                call_command('loaddata', 'initial_roles.json')
                self.stdout.write(self.style.SUCCESS('角色数据初始化成功'))
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'初始化失败: {str(e)}')
            )
            # 打印更详细的错误信息
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc())) 