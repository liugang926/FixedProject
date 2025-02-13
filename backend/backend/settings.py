INSTALLED_APPS = [
    # ...
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'users',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 必须在其他中间件之前
    'django.middleware.common.CommonMiddleware',
    # ... 其他中间件
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'UNAUTHENTICATED_USER': None
}

# CORS 设置
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['*']
CORS_ALLOW_HEADERS = ['*']

# 或者指定允许的源
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
# ]

# Debug 设置
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# 确保这些设置存在
ALLOWED_HOSTS = ['*']

# 添加 APPEND_SLASH 设置
APPEND_SLASH = False

# 在 INSTALLED_APPS 中添加 debug_toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1'] 