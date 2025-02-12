import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class DatabaseRouter:
    """数据库配置路由类"""
    
    @staticmethod
    def get_database_config():
        # 获取环境变量中的数据库类型，默认使用sqlite
        db_type = os.getenv('DB_TYPE', 'sqlite')
        
        if db_type == 'sqlite':
            return {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
        
        elif db_type == 'mysql':
            return {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': os.getenv('DB_NAME', 'asset_management'),
                    'USER': os.getenv('DB_USER', 'asset_user'),
                    'PASSWORD': os.getenv('DB_PASSWORD', 'your_password'),
                    'HOST': os.getenv('DB_HOST', 'localhost'),
                    'PORT': os.getenv('DB_PORT', '3306'),
                }
            }
        
        else:
            raise ValueError(f'Unsupported database type: {db_type}') 