from django.apps import AppConfig
from django.db.models.signals import post_migrate

def init_permissions(sender, **kwargs):
    from django.core.management import call_command
    call_command('init_permissions')

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = '用户管理'

    def ready(self):
        post_migrate.connect(init_permissions, sender=self) 