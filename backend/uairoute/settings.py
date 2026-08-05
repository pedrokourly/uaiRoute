import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def env_list(name, default):
    """Lê uma variável de ambiente separada por vírgulas como lista."""
    return [item.strip() for item in os.environ.get(name, default).split(',') if item.strip()]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

CHAVE_DE_DESENVOLVIMENTO = 'django-insecure-uy*m606ry@h-akvtkvahs7bh-dz@rai6q59_1zk2j3+@*zq0q+'


def exigir_secret_key(debug, valor):
    """Em produção, subir sem SECRET_KEY é pior do que não subir.

    O fallback está versionado; assinar sessões com ele em produção equivale
    a não assinar nada.
    """
    if valor:
        return valor
    if debug:
        return CHAVE_DE_DESENVOLVIMENTO
    raise ImproperlyConfigured(
        'SECRET_KEY é obrigatória quando DEBUG=False. '
        'Gere uma com: python -c "import secrets; print(secrets.token_urlsafe(50))"'
    )


DEBUG = os.environ.get('DEBUG', 'True').strip().lower() in ('true', '1', 'yes', 'on')

SECRET_KEY = exigir_secret_key(DEBUG, os.environ.get('SECRET_KEY'))

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', 'localhost,127.0.0.1')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',  # Para o Django REST Framework
    'corsheaders',  # Para permitir requisições do frontend
    'api.obras',  # Para o app de Obras
    'api.funcionarios',  # Para o app de Funcionários
    'api.veiculos',  # Para o app de Veículos
    'api.registros',
    'api.alojamento',
    'api.ordens_servico',  # Para o app de Ordens de Serviço
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Deve ser o primeiro
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Logo após o de segurança
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uairoute.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uairoute.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASE_PATH permite apontar o SQLite para o volume persistente do Docker
# (/app/data/db.sqlite3). Sem a variável, cai no caminho padrão do dev local.
DATABASE_PATH = os.environ.get('DATABASE_PATH') or BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
# collectstatic precisa de destino, e sob gunicorn ninguém serve os
# estáticos do Django admin -- o whitenoise faz esse papel.
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Responde apenas com JSON
    ],
}


# CORS configuration
CORS_ALLOWED_ORIGINS = env_list(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5000,http://127.0.0.1:5000',
)

# Liberar todas as origens só faz sentido em desenvolvimento.
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True

# CSRF exemption for API
CSRF_TRUSTED_ORIGINS = env_list(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:5000,http://127.0.0.1:5000',
)
