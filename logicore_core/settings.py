from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-)*^mwfsj5l7)n*bk&)0eg%16^vc%3lj9$0#cu$3pe=i-2_!k(n'

DEBUG = True

ALLOWED_HOSTS = ['logicore-wms.onrender.com', '.onrender.com', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'inventario',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'logicore_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'inventario' / 'templates'],
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

WSGI_APPLICATION = 'logicore_core.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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
LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

# CORREGIDO: Apunta correctamente a la carpeta static dentro de la app 'inventario'
STATICFILES_DIRS = [
    BASE_DIR / 'inventario' / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Email
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# Jazzmin Visual & Enterprise Customization
JAZZMIN_SETTINGS = {
    "site_title": "LogiCore UPEC WMS",
    "site_header": "LogiCore UPEC",
    "site_brand": "LogiCore UPEC",
    "welcome_sign": "Bienvenido al Sistema de Gestión de Almacenes - UPEC",
    "copyright": "LogiCore UPEC - Ecuador",
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "inventario.proveedor": "fas fa-truck",
        "inventario.categoria": "fas fa-tags",
        "inventario.unidad": "fas fa-ruler-combined",
        "inventario.producto": "fas fa-boxes",
        "inventario.almacen": "fas fa-warehouse",
        "inventario.zona": "fas fa-th-large",
        "inventario.ubicacion": "fas fa-map-marker-alt",
    },
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "custom_css": "css/custom_admin.css",
    "custom_links": {
        "inventario": [{
            "name": "Añadir Producto",
            "url": "/admin/inventario/producto/add/",
            "icon": "fas fa-plus-circle",
            "permissions": ["inventario.add_producto"]
        }]
    },
}