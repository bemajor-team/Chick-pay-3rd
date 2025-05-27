import os
from pathlib import Path
from dotenv import load_dotenv

# 기본 경로
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# 보안 설정
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')
DEBUG = False
ALLOWED_HOSTS = ['*']

# 앱 설정
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "account_app",  # ✅ 너의 앱
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "account_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "account_service.wsgi.application"

# DB 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ.get('DB_USER'),
        'NAME': os.environ.get('DB_NAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'ATOMIC_REQUESTS': True,
    }
}

# 사용자 모델 (외부 인증 서비스에서 관리 중이면 없어도 됨)
# AUTH_USER_MODEL = 'account_app.CustomUser'  # ❌ 계좌만 담당할 경우 생략 가능

# 국제화
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# 정적 파일 설정 (Docker용)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF 설정
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Swagger 문서화
SPECTACULAR_SETTINGS = {
    'TITLE': 'Account Service API',
    'DESCRIPTION': '계좌 잔액 조회 전용 마이크로서비스',
    'VERSION': '1.0.0',
}

